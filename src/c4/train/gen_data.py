"""Script tự động sinh dữ liệu huấn luyện cho mạng nơ-ron từ Alpha-Beta tự chơi (Expert Self-play).

Quy trình chuẩn chống nhiễu nhãn & chống rò rỉ dữ liệu:
1. Mỗi ván bắt đầu bằng `opening_plies` nước khai cuộc ngẫu nhiên hợp lệ để đa dạng hóa trạng thái.
2. Tại mỗi lượt tiếp theo, chuyên gia Alpha-Beta luôn tính nước đi tối ưu `expert_action` làm nhãn Policy sạch
   (không bị nhiễm nước đi ngẫu nhiên). Với xác suất `epsilon` (ở giai đoạn đầu/trung cuộc), bàn cờ bước sang
   một nhánh khám phá ngẫu nhiên để mở rộng không gian trạng thái, sau đó đánh chuẩn Alpha-Beta đến hết ván.
3. Tách tập dữ liệu THEO VÁN (70% Train / 15% Val / 15% Test) trước mọi bước xử lý.
4. Loại trùng trạng thái (`deduplicate=True`) theo mã hóa bàn cờ tương đối (gộp giá trị kỳ vọng `value` trung bình)
   và loại bỏ hoàn toàn mọi trạng thái ở Val/Test trùng (kể cả trùng đối xứng gương ngang) với tập Train.
5. Tăng cường dữ liệu đối xứng trục dọc (Horizontal Flip: cột c <-> 6 - c) CHỈ áp dụng trên tập Train.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import json
import os
import platform
import random
import sys
import time
from pathlib import Path

import numpy as np

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.agents import AlphaBetaAgent, Budget
from c4.game import Connect4


def generate_game(
    game_id: int,
    depth: int = 4,
    opening_plies: int = 4,
    epsilon: float = 0.12,
    pure_after_ply: int = 18,
    rng: random.Random | None = None,
    agent: AlphaBetaAgent | None = None,
) -> list[dict]:
    """Chơi 1 ván tự chơi có hướng dẫn và trả về danh sách các mẫu sạch (clean-label samples)."""
    if rng is None:
        rng = random.Random()

    game = Connect4()
    if agent is None:
        agent = AlphaBetaAgent(seed=rng.randint(0, 1_000_000), depth=depth)
    budget = Budget(depth=depth)

    # 1. Khai cuộc ngẫu nhiên để phủ rộng không gian trạng thái
    for _ in range(opening_plies):
        if game.is_terminal():
            break
        legal = game.legal_actions()
        game.step(rng.choice(legal))

    samples: list[dict] = []

    # 2. Luôn gán nhãn bằng nước đi chuyên gia Alpha-Beta; chỉ dùng epsilon cho bước chuyển khám phá
    while not game.is_terminal():
        legal = game.legal_actions()
        state = game.encode()  # shape (2, 6, 7), góc nhìn bên đang đến lượt
        legal_mask = np.zeros(7, dtype=bool)
        for a in legal:
            legal_mask[a] = True

        current_player = game.current_player
        expert_action = agent.choose_action(game, budget)

        samples.append({
            "game_id": game_id,
            "ply": game.move_count,
            "state": state,
            "legal_mask": legal_mask,
            "action": expert_action,
            "player": current_player,
        })

        use_random_step = (game.move_count < pure_after_ply) and (rng.random() < epsilon)
        step_action = rng.choice(legal) if use_random_step else expert_action
        game.step(step_action)

    # 3. Gán nhãn giá trị kết quả cuối ván theo góc nhìn người chơi tại từng trạng thái
    winner = game.winner  # +1, -1, hoặc 0
    for s in samples:
        s["value"] = float(winner * s["player"])

    return samples


def augment_horizontal_flip(
    states: np.ndarray,
    actions: np.ndarray,
    legal_masks: np.ndarray,
    values: np.ndarray,
):
    """Tăng cường dữ liệu bằng phép lật ngang bàn cờ (cột c -> 6 - c)."""
    flipped_states = states[:, :, :, ::-1].copy()
    flipped_actions = 6 - actions
    flipped_masks = legal_masks[:, ::-1].copy()
    flipped_values = values.copy()

    aug_states = np.concatenate([states, flipped_states], axis=0)
    aug_actions = np.concatenate([actions, flipped_actions], axis=0)
    aug_masks = np.concatenate([legal_masks, flipped_masks], axis=0)
    aug_values = np.concatenate([values, flipped_values], axis=0)

    return aug_states, aug_actions, aug_masks, aug_values


def _state_bytes(state: np.ndarray) -> bytes:
    return np.ascontiguousarray(state, dtype=np.float32).tobytes()


def _mirror_state_bytes(state: np.ndarray) -> bytes:
    return np.ascontiguousarray(state[:, :, ::-1], dtype=np.float32).tobytes()


def _pack_and_deduplicate(
    games_list: list[list[dict]],
    deduplicate: bool = True,
    forbidden_keys: set[bytes] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, int], set[bytes]]:
    """Đóng gói danh sách ván thành mảng numpy, loại trùng trạng thái và lọc chống rò rỉ chéo."""
    raw_items = [s for g in games_list for s in g]
    raw_count = len(raw_items)
    if not raw_items:
        empty_stats = {"raw": 0, "cross_filtered": 0, "duplicates_merged": 0, "unique": 0}
        return (
            np.empty((0, 2, 6, 7), dtype=np.float32),
            np.empty((0,), dtype=np.int64),
            np.empty((0, 7), dtype=bool),
            np.empty((0,), dtype=np.float32),
            empty_stats,
            set(),
        )

    cross_filtered = 0
    filtered_items = []
    for item in raw_items:
        st = item["state"]
        k = _state_bytes(st)
        mk = _mirror_state_bytes(st)
        if forbidden_keys and (k in forbidden_keys or mk in forbidden_keys):
            cross_filtered += 1
            continue
        filtered_items.append((k, mk, item))

    seen_with_mirrors: set[bytes] = set()

    if not deduplicate:
        for k, mk, _ in filtered_items:
            seen_with_mirrors.add(k)
            seen_with_mirrors.add(mk)
        if not filtered_items:
            return (
                np.empty((0, 2, 6, 7), dtype=np.float32),
                np.empty((0,), dtype=np.int64),
                np.empty((0, 7), dtype=bool),
                np.empty((0,), dtype=np.float32),
                {"raw": raw_count, "cross_filtered": cross_filtered, "duplicates_merged": 0, "unique": 0},
                seen_with_mirrors,
            )
        states = np.stack([x[2]["state"] for x in filtered_items]).astype(np.float32)
        actions = np.array([x[2]["action"] for x in filtered_items], dtype=np.int64)
        masks = np.stack([x[2]["legal_mask"] for x in filtered_items]).astype(bool)
        values = np.array([x[2]["value"] for x in filtered_items], dtype=np.float32)
        return (
            states,
            actions,
            masks,
            values,
            {"raw": raw_count, "cross_filtered": cross_filtered, "duplicates_merged": 0, "unique": len(states)},
            seen_with_mirrors,
        )

    grouped: dict[bytes, dict] = {}
    for k, mk, item in filtered_items:
        seen_with_mirrors.add(k)
        seen_with_mirrors.add(mk)
        if k not in grouped:
            grouped[k] = {
                "state": item["state"],
                "legal_mask": item["legal_mask"],
                "actions": [int(item["action"])],
                "values": [float(item["value"])],
            }
        else:
            grouped[k]["actions"].append(int(item["action"]))
            grouped[k]["values"].append(float(item["value"]))

    if not grouped:
        return (
            np.empty((0, 2, 6, 7), dtype=np.float32),
            np.empty((0,), dtype=np.int64),
            np.empty((0, 7), dtype=bool),
            np.empty((0,), dtype=np.float32),
            {
                "raw": raw_count,
                "cross_filtered": cross_filtered,
                "duplicates_merged": len(filtered_items),
                "unique": 0,
            },
            seen_with_mirrors,
        )

    unique_states = []
    unique_actions = []
    unique_masks = []
    unique_values = []

    for entry in grouped.values():
        unique_states.append(entry["state"])
        unique_masks.append(entry["legal_mask"])
        best_act = Counter(entry["actions"]).most_common(1)[0][0]
        unique_actions.append(best_act)
        unique_values.append(float(np.mean(entry["values"])))

    states = np.stack(unique_states).astype(np.float32)
    actions = np.array(unique_actions, dtype=np.int64)
    masks = np.stack(unique_masks).astype(bool)
    values = np.array(unique_values, dtype=np.float32)
    stats = {
        "raw": raw_count,
        "cross_filtered": cross_filtered,
        "duplicates_merged": len(filtered_items) - len(states),
        "unique": len(states),
    }
    return states, actions, masks, values, stats, seen_with_mirrors


def _generate_game_worker(task: tuple[int, int, int, float, int]) -> list[dict]:
    """Hàm worker độc lập theo seed cố định cho từng ván (hỗ trợ chạy đa nhân tái lập 100%)."""
    gid, depth, base_openings, epsilon, base_seed = task
    rng_g = random.Random(base_seed * 1_000_003 + gid)
    plies = base_openings if (gid % 5 != 0) else rng_g.choice([0, 2, 6])
    teacher = AlphaBetaAgent(seed=base_seed + gid, depth=depth)
    return generate_game(
        gid,
        depth=depth,
        opening_plies=plies,
        epsilon=epsilon,
        rng=rng_g,
        agent=teacher,
    )


def generate_dataset(
    num_games: int = 2000,
    depth: int = 4,
    opening_plies: int = 4,
    epsilon: float = 0.12,
    seed: int = 42,
    out_dir: str | Path = "data",
    augment_train: bool = True,
    deduplicate: bool = True,
    workers: int = 1,
) -> dict[str, int]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    print(
        f"[*] Bắt đầu sinh {num_games} ván chuyên gia "
        f"(Alpha-Beta depth={depth}, opening_plies={opening_plies}, epsilon={epsilon}, seed={seed}, workers={workers})..."
    )
    start_time = time.perf_counter()

    tasks = [(gid, depth, opening_plies, epsilon, seed) for gid in range(num_games)]
    all_games_samples: list[list[dict]] = []
    total_raw_samples = 0

    if workers > 1 and num_games >= 40:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for idx, samples in enumerate(ex.map(_generate_game_worker, tasks, chunksize=25), start=1):
                if samples:
                    all_games_samples.append(samples)
                    total_raw_samples += len(samples)
                if idx % 500 == 0 or idx == num_games:
                    elapsed = time.perf_counter() - start_time
                    print(f"    -> Đã sinh {idx}/{num_games} ván ({total_raw_samples} nước đi thô, {elapsed:.1f}s)")
    else:
        for idx, t in enumerate(tasks, start=1):
            samples = _generate_game_worker(t)
            if samples:
                all_games_samples.append(samples)
                total_raw_samples += len(samples)
            if idx % 200 == 0 or idx == num_games:
                elapsed = time.perf_counter() - start_time
                print(f"    -> Đã sinh {idx}/{num_games} ván ({total_raw_samples} nước đi thô, {elapsed:.1f}s)")

    # Tách ván theo tỷ lệ 70% Train / 15% Val / 15% Test TRƯỚC khi loại trùng & augment
    rng.shuffle(all_games_samples)
    n_total = len(all_games_samples)
    n_train = int(n_total * 0.70)
    n_val = int(n_total * 0.15)

    train_games = all_games_samples[:n_train]
    val_games = all_games_samples[n_train : n_train + n_val]
    test_games = all_games_samples[n_train + n_val :]

    tr_s, tr_a, tr_m, tr_v, tr_stats, tr_keys = _pack_and_deduplicate(
        train_games, deduplicate=deduplicate, forbidden_keys=None
    )
    val_s, val_a, val_m, val_v, val_stats, val_keys = _pack_and_deduplicate(
        val_games, deduplicate=deduplicate, forbidden_keys=tr_keys if deduplicate else None
    )
    te_s, te_a, te_m, te_v, te_stats, _ = _pack_and_deduplicate(
        test_games, deduplicate=deduplicate, forbidden_keys=(tr_keys | val_keys) if deduplicate else None
    )

    tr_unique_before_aug = len(tr_s)
    if augment_train and len(tr_s) > 0:
        tr_s, tr_a, tr_m, tr_v = augment_horizontal_flip(tr_s, tr_a, tr_m, tr_v)
        print(f"[*] Tăng cường đối xứng ngang tập Train: {tr_unique_before_aug} -> {len(tr_s)} mẫu.")

    np.savez_compressed(out_path / "train.npz", states=tr_s, actions=tr_a, legal_masks=tr_m, values=tr_v)
    np.savez_compressed(out_path / "val.npz", states=val_s, actions=val_a, legal_masks=val_m, values=val_v)
    np.savez_compressed(out_path / "test.npz", states=te_s, actions=te_a, legal_masks=te_m, values=te_v)

    elapsed_total = time.perf_counter() - start_time
    summary = {
        "seed": seed,
        "teacher": f"AlphaBetaAgent(depth={depth})",
        "num_games_total": n_total,
        "split_games": {
            "train": len(train_games),
            "val": len(val_games),
            "test": len(test_games),
        },
        "opening_plies_default": opening_plies,
        "epsilon_exploration": epsilon,
        "clean_expert_labels": True,
        "deduplicated": deduplicate,
        "horizontal_flip_train_only": augment_train,
        "raw_samples_total": total_raw_samples,
        "split_details": {
            "train": {**tr_stats, "augmented_final": int(len(tr_s))},
            "val": val_stats,
            "test": te_stats,
        },
        "generation_time_s": round(elapsed_total, 2),
        "platform": platform.platform(),
    }
    with open(out_path / "dataset_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Đã lưu bộ dữ liệu sạch vào thư mục: {out_path}")
    print(f"    Train: {len(tr_s)} mẫu (từ {tr_unique_before_aug} thế cờ duy nhất / {len(train_games)} ván)")
    print(f"    Val:   {len(val_s)} mẫu duy nhất ({len(val_games)} ván, 0% trùng Train/Mirror)")
    print(f"    Test:  {len(te_s)} mẫu duy nhất ({len(test_games)} ván, 0% trùng Train/Val/Mirror)")

    return {
        "train_samples": int(len(tr_s)),
        "val_samples": int(len(val_s)),
        "test_samples": int(len(te_s)),
    }


def main():
    p = argparse.ArgumentParser(description="Sinh dữ liệu ván đấu Connect Four sạch cho mạng nơ-ron")
    p.add_argument("--games", type=int, default=2000, help="Số ván tự chơi cần sinh")
    p.add_argument("--depth", type=int, default=4, help="Độ sâu Alpha-Beta chuyên gia")
    p.add_argument("--openings", type=int, default=4, help="Số nước khai cuộc ngẫu nhiên đầu ván")
    p.add_argument("--epsilon", type=float, default=0.12, help="Tỷ lệ bước chuyển khám phá ngẫu nhiên")
    p.add_argument("--seed", type=int, default=42, help="Seed ngẫu nhiên")
    p.add_argument("--out-dir", default="data", help="Thư mục xuất dữ liệu")
    p.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1), help="Số tiến trình song song")
    args = p.parse_args()

    generate_dataset(
        num_games=args.games,
        depth=args.depth,
        opening_plies=args.openings,
        epsilon=args.epsilon,
        seed=args.seed,
        out_dir=args.out_dir,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
