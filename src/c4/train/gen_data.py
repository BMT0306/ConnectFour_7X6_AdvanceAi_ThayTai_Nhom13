"""Script tự động sinh dữ liệu huấn luyện cho mạng nơ-ron từ Alpha-Beta tự chơi (Self-play).

Quy trình:
1. Mỗi ván bắt đầu bằng 4 nước khai cuộc ngẫu nhiên (opening plies) để tạo trạng thái đa dạng.
2. Hai bên do Alpha-Beta (depth 4) điều khiển, có xác suất nhiễu epsilon=0.1 để khám phá.
3. Ghi nhận (state (2,6,7), legal_mask (7,), action (0..6), value (-1/0/+1)) tại mỗi nước đi.
4. Tách ván thành Train (70%), Val (15%), Test (15%) THEO VÁN để loại bỏ hoàn toàn rò rỉ dữ liệu.
5. Hỗ trợ Data Augmentation: Lật gương ngang bàn cờ (horizontal flip).
"""
from __future__ import annotations

import argparse
import os
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
    epsilon: float = 0.1,
    rng: random.Random | None = None,
) -> list[dict]:
    """Chơi 1 ván tự chơi và trả về danh sách các mẫu (samples)."""
    if rng is None:
        rng = random.Random()

    game = Connect4()
    agent = AlphaBetaAgent(seed=rng.randint(0, 1000000), depth=depth)
    budget = Budget(depth=depth)

    # 1. Khai cuộc ngẫu nhiên
    for _ in range(opening_plies):
        if game.is_terminal():
            break
        legal = game.legal_actions()
        game.step(rng.choice(legal))

    samples = []

    # 2. Chơi tiếp bằng Alpha-Beta kết hợp epsilon
    while not game.is_terminal():
        legal = game.legal_actions()
        state = game.encode()  # shape (2, 6, 7)
        legal_mask = np.zeros(7, dtype=bool)
        for a in legal:
            legal_mask[a] = True

        current_player = game.current_player

        if rng.random() < epsilon:
            action = rng.choice(legal)
        else:
            action = agent.choose_action(game, budget)

        samples.append({
            "game_id": game_id,
            "state": state,
            "legal_mask": legal_mask,
            "action": action,
            "player": current_player,
        })
        game.step(action)

    # 3. Gán nhãn giá trị kết quả cuối cùng (Value target)
    winner = game.winner  # +1, -1, hoặc 0
    for s in samples:
        s["value"] = float(winner * s["player"])  # +1 nếu thắng, -1 nếu thua, 0 nếu hòa

    return samples


def augment_horizontal_flip(states: np.ndarray, actions: np.ndarray, legal_masks: np.ndarray, values: np.ndarray):
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


def generate_dataset(
    num_games: int = 500,
    depth: int = 4,
    opening_plies: int = 4,
    epsilon: float = 0.1,
    seed: int = 42,
    out_dir: str | Path = "data",
    augment_train: bool = True,
) -> dict[str, int]:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)

    print(f"[*] Bắt đầu sinh {num_games} ván tự đấu (Alpha-Beta depth={depth}, epsilon={epsilon})...")
    start_time = time.perf_counter()

    all_games_samples: list[list[dict]] = []
    total_samples = 0

    for gid in range(num_games):
        samples = generate_game(gid, depth=depth, opening_plies=opening_plies, epsilon=epsilon, rng=rng)
        if samples:
            all_games_samples.append(samples)
            total_samples += len(samples)

        if (gid + 1) % 50 == 0 or (gid + 1) == num_games:
            elapsed = time.perf_counter() - start_time
            print(f"    -> Đã sinh {gid + 1}/{num_games} ván ({total_samples} nước đi, {elapsed:.1f}s)")

    # Xáo trộn danh sách ván đấu để chia 70% / 15% / 15%
    rng.shuffle(all_games_samples)
    n_total = len(all_games_samples)
    n_train = int(n_total * 0.70)
    n_val = int(n_total * 0.15)

    train_games = all_games_samples[:n_train]
    val_games = all_games_samples[n_train : n_train + n_val]
    test_games = all_games_samples[n_train + n_val :]

    def pack_subset(games_list):
        items = [s for g in games_list for s in g]
        if not items:
            return (
                np.empty((0, 2, 6, 7), dtype=np.float32),
                np.empty((0,), dtype=np.int64),
                np.empty((0, 7), dtype=bool),
                np.empty((0,), dtype=np.float32),
            )
        states = np.stack([x["state"] for x in items]).astype(np.float32)
        actions = np.array([x["action"] for x in items], dtype=np.int64)
        masks = np.stack([x["legal_mask"] for x in items]).astype(bool)
        values = np.array([x["value"] for x in items], dtype=np.float32)
        return states, actions, masks, values

    tr_s, tr_a, tr_m, tr_v = pack_subset(train_games)
    val_s, val_a, val_m, val_v = pack_subset(val_games)
    te_s, te_a, te_m, te_v = pack_subset(test_games)

    if augment_train and len(tr_s) > 0:
        before_count = len(tr_s)
        tr_s, tr_a, tr_m, tr_v = augment_horizontal_flip(tr_s, tr_a, tr_m, tr_v)
        print(f"[*] Đã tăng cường lật ngang tập Train: {before_count} -> {len(tr_s)} mẫu.")

    np.savez_compressed(out_path / "train.npz", states=tr_s, actions=tr_a, legal_masks=tr_m, values=tr_v)
    np.savez_compressed(out_path / "val.npz", states=val_s, actions=val_a, legal_masks=val_m, values=val_v)
    np.savez_compressed(out_path / "test.npz", states=te_s, actions=te_a, legal_masks=te_m, values=te_v)

    print(f"\n[+] Đã lưu dữ liệu hoàn tất vào thư mục: {out_path}")
    print(f"    Train: {len(tr_s)} mẫu ({len(train_games)} ván)")
    print(f"    Val:   {len(val_s)} mẫu ({len(val_games)} ván)")
    print(f"    Test:  {len(te_s)} mẫu ({len(test_games)} ván)")

    return {
        "train_samples": len(tr_s),
        "val_samples": len(val_s),
        "test_samples": len(te_s),
    }


def main():
    p = argparse.ArgumentParser(description="Sinh dữ liệu ván đấu Connect Four cho mạng nơ-ron")
    p.add_argument("--games", type=int, default=300, help="Số ván tự chơi cần sinh")
    p.add_argument("--depth", type=int, default=4, help="Độ sâu Alpha-Beta chuyên gia")
    p.add_argument("--openings", type=int, default=4, help="Số nước khai cuộc ngẫu nhiên đầu ván")
    p.add_argument("--epsilon", type=float, default=0.1, help="Tỷ lệ khám phá ngẫu nhiên")
    p.add_argument("--seed", type=int, default=42, help="Seed ngẫu nhiên")
    p.add_argument("--out-dir", default="data", help="Thư mục xuất dữ liệu")
    args = p.parse_args()

    generate_dataset(
        num_games=args.games,
        depth=args.depth,
        opening_plies=args.openings,
        epsilon=args.epsilon,
        seed=args.seed,
        out_dir=args.out_dir,
    )


if __name__ == "__main__":
    main()
