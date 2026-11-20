#!/usr/bin/env python3
"""Hệ thống Xếp hạng Elo (Elo Rating System) Chuẩn và Solo Trực Tiếp Máy vs Máy.

Tính toán chỉ số Elo chuẩn mực quốc tế (Bradley-Terry Maximum Likelihood & Logistic FIDE Elo),
hỗ trợ lưu trữ bền vững (persistent database) tại results/elo_ratings.json, và chế độ
Solo trực tiếp giữa 2 AI với hiển thị bàn cờ và cập nhật điểm Elo thời gian thực.

Sử dụng:
    python scripts/compute_elo.py                                        # Bảng xếp hạng Elo hiện tại
    python scripts/compute_elo.py --timed                                # Bảng Elo giải đấu 100ms
    python scripts/compute_elo.py --solo alphabeta mixed_mcts            # Solo 2 ván đổi bên
    python scripts/compute_elo.py --solo alphabeta mixed_mcts --games 4  # Solo 4 ván
    python scripts/compute_elo.py --solo alphabeta mixed_mcts --watch    # Hiển thị bàn cờ chi tiết
    python scripts/compute_elo.py --reset-elo                            # Khôi phục Elo gốc ban đầu
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from c4.agents import Budget, make_agent
from c4.game import COLS, PLAYER1, PLAYER2, ROWS, Connect4


AGENTS_ORDER = ["random", "heuristic", "nn", "mcts", "alphabeta", "mixed_mcts"]
AGENT_DISPLAY = {
    "random": "Level 1: Random Baseline",
    "heuristic": "Level 2: Priority Heuristic",
    "alphabeta": "Level 3: Alpha-Beta Pruning",
    "mcts": "Level 4: MCTS-UCT (1.000 sims)",
    "nn": "Level 5: Policy-Value ResNet",
    "mixed_mcts": "Level 6: Mixed-MCTS (PUCT)",
}

DATABASE_FILE = ROOT_DIR / "results" / "elo_ratings.json"
DEFAULT_CSV = ROOT_DIR / "results" / "tables" / "round_robin_default_summary.csv"
TIMED_CSV = ROOT_DIR / "results" / "tables" / "round_robin_levels_timed_summary.csv"


def compute_bradley_terry_elo(csv_path: Path, anchor_agent: str = "random", anchor_elo: float = 1000.0) -> dict[str, dict]:
    """Tính toán Elo chuẩn xác bằng phương pháp Bradley-Terry Maximum Likelihood Estimation (Hunter, 2004)."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Không tìm thấy tệp kết quả giải đấu: {csv_path}")

    rows: list[dict[str, str]] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    present_agents = set()
    for r in rows:
        present_agents.add(r["Agent_A"])
        present_agents.add(r["Agent_B"])

    agents = [a for a in AGENTS_ORDER if a in present_agents]
    n = len(agents)
    a2i = {a: i for i, a in enumerate(agents)}

    W = [[0.0] * n for _ in range(n)]
    N = [[0.0] * n for _ in range(n)]

    for r in rows:
        a = r["Agent_A"]
        b = r["Agent_B"]
        if a not in a2i or b not in a2i:
            continue
        i = a2i[a]
        j = a2i[b]
        w_a = float(r["A_Wins"])
        d = float(r["Draws"])
        w_b = float(r["B_Wins"])

        W[i][j] += w_a + 0.5 * d
        W[j][i] += w_b + 0.5 * d
        N[i][j] += w_a + d + w_b
        N[j][i] += w_a + d + w_b

    # Thuật toán lặp Bradley-Terry (Hunter 2004) bằng pure Python tiêu chuẩn
    gamma = [1.0] * n
    for _ in range(2000):
        gamma_old = list(gamma)
        for i in range(n):
            num = sum(W[i][j] for j in range(n))
            den = sum(N[i][j] / (gamma_old[i] + gamma_old[j]) for j in range(n) if (gamma_old[i] + gamma_old[j]) > 0)
            gamma[i] = num / den if den > 0 else 1.0
        log_mean = sum(math.log(max(g, 1e-12)) for g in gamma) / n
        geo_mean = math.exp(log_mean)
        gamma = [g / max(geo_mean, 1e-12) for g in gamma]

    # Đổi sang thang điểm Elo chuẩn: R = 400 * log10(gamma)
    elo = [400.0 * math.log10(max(g, 1e-12)) for g in gamma]

    # Cố định mốc anchor (Random = 1000.0)
    if anchor_agent in a2i:
        shift = anchor_elo - elo[a2i[anchor_agent]]
        elo = [e + shift for e in elo]

    out = {}
    for i, a in enumerate(agents):
        total_games = int(sum(N[i][j] for j in range(n)))
        total_score_pts = float(sum(W[i][j] for j in range(n)))
        win_rate = (total_score_pts / max(total_games, 1)) * 100.0
        wins = sum(int(r["A_Wins"]) for r in rows if r["Agent_A"] == a) + sum(int(r["B_Wins"]) for r in rows if r["Agent_B"] == a)
        draws = sum(int(r["Draws"]) for r in rows if r["Agent_A"] == a or r["Agent_B"] == a)
        losses = sum(int(r["B_Wins"]) for r in rows if r["Agent_A"] == a) + sum(int(r["A_Wins"]) for r in rows if r["Agent_B"] == a)
        out[a] = {
            "name": a,
            "display": AGENT_DISPLAY.get(a, a),
            "elo": round(float(elo[i]), 1),
            "score_pct": round(win_rate, 2),
            "total_games": total_games,
            "wins": wins,
            "draws": draws,
            "losses": losses,
        }
    return out


def load_or_init_database(force_reset: bool = False) -> dict[str, dict]:
    """Tải cơ sở dữ liệu Elo bền vững từ file JSON; nếu chưa có thì khởi tạo từ 3.000 ván thực nghiệm."""
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if DATABASE_FILE.exists() and not force_reset:
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "ratings" in data:
                    return data["ratings"]
        except Exception:
            pass

    # Khởi tạo từ benchmark 3.000 ván
    ratings = compute_bradley_terry_elo(DEFAULT_CSV)
    save_database(ratings)
    return ratings


def save_database(ratings: dict[str, dict]) -> None:
    """Ghi dữ liệu Elo cập nhật vào tệp JSON."""
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "formula": "FIDE Standard Logistic Elo: E = 1 / (1 + 10^((R_b - R_a)/400)), delta = K * (S - E)",
        "ratings": ratings,
    }
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def render_board_pretty(game: Connect4) -> str:
    """Hiển thị bàn cờ với biểu tượng trực quan."""
    arr = game.to_array()
    lines = []
    lines.append("   ┌───┬───┬───┬───┬───┬───┬───┐")
    for r in range(ROWS - 1, -1, -1):
        row_str = f" {r+1} │"
        for c in range(COLS):
            val = arr[r, c]
            if val == PLAYER1:
                piece = " X "
            elif val == PLAYER2:
                piece = " O "
            else:
                piece = " · "
            row_str += piece + "│"
        lines.append(row_str)
        if r > 0:
            lines.append("   ├───┼───┼───┼───┼───┼───┼───┤")
    lines.append("   └───┴───┴───┴───┴───┴───┴───┘")
    lines.append("     1   2   3   4   5   6   7   (Cột)")
    return "\n".join(lines)


def get_tier(elo: float) -> str:
    if elo >= 2100:
        return "👑 [Grandmaster]"
    if elo >= 2000:
        return "⭐ [Master]"
    if elo >= 1900:
        return "🔷 [Expert]"
    if elo >= 1800:
        return "🟢 [Club]"
    return "⚪ [Novice]"


def print_elo_table(elo_dict: dict[str, dict], title: str) -> None:
    """In bảng xếp hạng Elo ra màn hình console."""
    sorted_agents = sorted(elo_dict.values(), key=lambda x: x["elo"], reverse=True)

    print("\n" + "=" * 82)
    print(f" {title.upper()}")
    print("=" * 82)
    print(f"{'Hạng':<6}{'Tác tử AI':<32}{'Điểm Elo':<14}{'Tỉ lệ Score':<14}{'Tổng ván':<10}{'Thành tích':<12}")
    print("-" * 82)

    for rank, item in enumerate(sorted_agents, 1):
        tier = get_tier(item["elo"])
        w_d_l = f"{item.get('wins', 0)}T-{item.get('draws', 0)}H-{item.get('losses', 0)}B"
        print(
            f"#{rank:<5}{item['display']:<32}{item['elo']:>7.1f} Elo    "
            f"{item.get('score_pct', 0.0):>6.2f}%       {item.get('total_games', 0):<8} {w_d_l:<12} {tier}"
        )
    print("=" * 82)


def run_live_solo(
    agent_a_name: str,
    agent_b_name: str,
    games_count: int = 2,
    time_limit_s: float = 0.1,
    watch: bool = False,
    k_factor: float = 32.0,
    seed: int = 42,
) -> None:
    """Chạy trận solo trực tiếp từng ván: hiển thị nước đi, bàn cờ và cập nhật Elo THẬT sau mỗi ván."""
    ratings = load_or_init_database()

    if agent_a_name not in ratings:
        ratings[agent_a_name] = {
            "name": agent_a_name,
            "display": AGENT_DISPLAY.get(agent_a_name, agent_a_name),
            "elo": 1500.0,
            "total_games": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "score_pct": 50.0,
        }
    if agent_b_name not in ratings:
        ratings[agent_b_name] = {
            "name": agent_b_name,
            "display": AGENT_DISPLAY.get(agent_b_name, agent_b_name),
            "elo": 1500.0,
            "total_games": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "score_pct": 50.0,
        }

    initial_elo_a = ratings[agent_a_name]["elo"]
    initial_elo_b = ratings[agent_b_name]["elo"]

    print("\n" + "=" * 82)
    print(f" ⚔️  TRẬN ĐẤU SOLO TRỰC TIẾP: {agent_a_name.upper()} vs {agent_b_name.upper()} ⚔️")
    print(f" Tổng số ván đấu: {games_count} ván (đổi lượt đi trước/sau để đảm bảo công bằng)")
    print(f" Giới hạn thời gian suy nghĩ: {time_limit_s * 1000:.0f} ms/nước")
    print(f" Elo hiện tại: {agent_a_name} ({initial_elo_a:.1f}) | {agent_b_name} ({initial_elo_b:.1f})")
    print(f" Công thức Elo: FIDE Logistic Rating (Hệ số K={k_factor})")
    print("=" * 82)

    wins_a = 0
    draws = 0
    wins_b = 0

    for g_idx in range(1, games_count + 1):
        # Đổi bên mỗi ván: ván lẻ A đi trước, ván chẵn B đi trước
        if g_idx % 2 == 1:
            p1_name, p2_name = agent_a_name, agent_b_name
        else:
            p1_name, p2_name = agent_b_name, agent_a_name

        agent_p1 = make_agent(p1_name, seed=seed + g_idx * 17)
        agent_p2 = make_agent(p2_name, seed=seed + g_idx * 31)
        budget = Budget(time_s=time_limit_s)

        game = Connect4()
        agent_p1.reset()
        agent_p2.reset()

        print(f"\n▶ [VÁN {g_idx}/{games_count}] BẮT ĐẦU: [ĐỎ (X) Đi Trước] {p1_name}  vs  [VÀNG (O) Đi Sau] {p2_name}")

        moves_history = []
        turn = 1
        t_start = time.perf_counter()

        while not game.is_terminal():
            active_player = game.current_player
            active_agent = agent_p1 if active_player == PLAYER1 else agent_p2
            active_name = p1_name if active_player == PLAYER1 else p2_name
            active_symbol = "X (Đỏ)" if active_player == PLAYER1 else "O (Vàng)"

            t0 = time.perf_counter()
            action = active_agent.choose_action(game.clone(), budget)
            dt_ms = (time.perf_counter() - t0) * 1000.0

            game.step(action)
            moves_history.append((active_name, action + 1, dt_ms))

            if watch:
                print(f"   Lượt {turn:02d}: {active_name} [{active_symbol}] thả vào Cột {action + 1} ({dt_ms:.1f}ms)")
            turn += 1

        total_game_time = time.perf_counter() - t_start
        winner_code = game.winner  # +1 là P1, -1 là P2, 0 là Hòa

        if winner_code == PLAYER1:
            winner_name = p1_name
            score_p1, score_p2 = 1.0, 0.0
            result_str = f"🏆 {p1_name} THẮNG (Đỏ)!"
        elif winner_code == PLAYER2:
            winner_name = p2_name
            score_p1, score_p2 = 0.0, 1.0
            result_str = f"🏆 {p2_name} THẮNG (Vàng)!"
        else:
            winner_name = "Hòa"
            score_p1, score_p2 = 0.5, 0.5
            result_str = "🤝 HÒA CỜ (Bàn cờ đầy 42 ô)!"

        if winner_name == agent_a_name:
            wins_a += 1
        elif winner_name == agent_b_name:
            wins_b += 1
        else:
            draws += 1

        # Hiển thị bàn cờ kết thúc
        print(render_board_pretty(game))
        print(f"   Kết quả: {result_str} | Tổng số nước: {game.move_count} | Thời gian: {total_game_time:.2f}s")

        # CẬP NHẬT ELO THẬT THEO CÔNG THỨC FIDE
        if p1_name == p2_name:
            print(f"   📈 SELF-PLAY ({p1_name}): Điểm Elo giữ nguyên ({ratings[p1_name]['elo']:.1f} Elo)")
            continue

        elo_p1_before = ratings[p1_name]["elo"]
        elo_p2_before = ratings[p2_name]["elo"]

        expected_p1 = 1.0 / (1.0 + 10.0 ** ((elo_p2_before - elo_p1_before) / 400.0))
        expected_p2 = 1.0 - expected_p1

        delta_p1 = k_factor * (score_p1 - expected_p1)
        delta_p2 = -delta_p1

        elo_p1_after = round(elo_p1_before + delta_p1, 1)
        elo_p2_after = round(elo_p2_before + delta_p2, 1)

        # Cập nhật vào cơ sở dữ liệu
        ratings[p1_name]["elo"] = elo_p1_after
        ratings[p2_name]["elo"] = elo_p2_after
        ratings[p1_name]["total_games"] = ratings[p1_name].get("total_games", 0) + 1
        ratings[p2_name]["total_games"] = ratings[p2_name].get("total_games", 0) + 1

        if score_p1 == 1.0:
            ratings[p1_name]["wins"] = ratings[p1_name].get("wins", 0) + 1
            ratings[p2_name]["losses"] = ratings[p2_name].get("losses", 0) + 1
        elif score_p2 == 1.0:
            ratings[p2_name]["wins"] = ratings[p2_name].get("wins", 0) + 1
            ratings[p1_name]["losses"] = ratings[p1_name].get("losses", 0) + 1
        else:
            ratings[p1_name]["draws"] = ratings[p1_name].get("draws", 0) + 1
            ratings[p2_name]["draws"] = ratings[p2_name].get("draws", 0) + 1

        # Cập nhật tỉ lệ Score
        for p in (p1_name, p2_name):
            tg = ratings[p]["total_games"]
            pts = ratings[p].get("wins", 0) + 0.5 * ratings[p].get("draws", 0)
            ratings[p]["score_pct"] = round((pts / max(tg, 1)) * 100.0, 2)

        # Lưu ngay vào file JSON trên ổ cứng
        save_database(ratings)

        print(f"   📈 BIẾN ĐỘNG ELO THỰC TẾ:")
        print(f"      * {p1_name:<12}: {elo_p1_before:.1f} ➔ {elo_p1_after:.1f} ({delta_p1:+.1f} Elo)")
        print(f"      * {p2_name:<12}: {elo_p2_before:.1f} ➔ {elo_p2_after:.1f} ({delta_p2:+.1f} Elo)")

    final_elo_a = ratings[agent_a_name]["elo"]
    final_elo_b = ratings[agent_b_name]["elo"]
    total_delta_a = final_elo_a - initial_elo_a
    total_delta_b = final_elo_b - initial_elo_b

    print("\n" + "=" * 82)
    print(" 🏁 TỔNG KẾT TRẬN ĐẤU SOLO")
    print("=" * 82)
    print(f" Tỷ số chung cuộc: {agent_a_name} [{wins_a} Thắng] - [{draws} Hòa] - [{wins_b} Thắng] {agent_b_name}")
    print(f" Tổng biến động Elo:")
    print(f"   • {agent_a_name:<12}: {initial_elo_a:.1f} ➔ {final_elo_a:.1f} ({total_delta_a:+.1f} Elo) {get_tier(final_elo_a)}")
    print(f"   • {agent_b_name:<12}: {initial_elo_b:.1f} ➔ {final_elo_b:.1f} ({total_delta_b:+.1f} Elo) {get_tier(final_elo_b)}")
    print(f" [*] Đã lưu và cập nhật vĩnh viễn vào: results/elo_ratings.json")
    print("=" * 82)

    # Hiển thị lại bảng xếp hạng mới
    print_elo_table(ratings, "BẢNG XẾP HẠNG ELO SAU TRẬN ĐẤU")


def main() -> None:
    parser = argparse.ArgumentParser(description="Hệ thống Xếp hạng Elo & Solo Đối kháng Connect Four")
    parser.add_argument("--timed", action="store_true", help="Tính Elo từ giải đấu giới hạn thời gian 100ms")
    parser.add_argument("--solo", nargs=2, metavar=("AGENT_A", "AGENT_B"), help="Cho 2 máy solo trực tiếp")
    parser.add_argument("--games", type=int, default=2, help="Số ván thi đấu (mặc định 2: 1 lượt đi trước, 1 lượt đi sau)")
    parser.add_argument("--time", type=float, default=0.1, help="Giới hạn thời gian mỗi nước (giây, mặc định 0.1s)")
    parser.add_argument("--watch", action="store_true", help="Hiển thị chi tiết từng nước cờ thả xuống")
    parser.add_argument("--k", type=float, default=32.0, help="Hệ số K factor của Elo (mặc định 32)")
    parser.add_argument("--reset-elo", action="store_true", help="Khôi phục điểm Elo về mốc chuẩn 3.000 ván")
    parser.add_argument("--seed", type=int, default=42, help="Seed ngẫu nhiên")
    args = parser.parse_args()

    if args.reset_elo:
        print("[*] Đang khôi phục bảng xếp hạng Elo về dữ liệu chuẩn gốc (3.000 ván)...")
        ratings = load_or_init_database(force_reset=True)
        print_elo_table(ratings, "BẢNG XẾP HẠNG ELO GỐC (CHUẨN 3.000 VÁN)")
        return

    if args.solo:
        a_name, b_name = args.solo
        run_live_solo(
            a_name.lower(),
            b_name.lower(),
            games_count=args.games,
            time_limit_s=args.time,
            watch=args.watch,
            k_factor=args.k,
            seed=args.seed,
        )
    else:
        if args.timed:
            elo_timed = compute_bradley_terry_elo(TIMED_CSV)
            print_elo_table(elo_timed, "BẢNG XẾP HẠNG ELO (GIẢI ĐẤU 100MS / 1.500 VÁN)")
        else:
            ratings = load_or_init_database()
            print_elo_table(ratings, "BẢNG XẾP HẠNG ELO HIỆN TẠI (PERSISTENT DATABASE)")
            print("\nGợi ý:")
            print("  - Cho 2 máy solo và xem trực tiếp bàn cờ: python scripts/compute_elo.py --solo alphabeta mixed_mcts --watch")
            print("  - Solo nhiều ván (ví dụ 6 ván):           python scripts/compute_elo.py --solo heuristic mcts --games 6")
            print("  - Khôi phục bảng Elo về ban đầu:          python scripts/compute_elo.py --reset-elo")


if __name__ == "__main__":
    main()
