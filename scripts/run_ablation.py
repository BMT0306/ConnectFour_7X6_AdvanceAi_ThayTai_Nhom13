#!/usr/bin/env python3
"""Script chạy thực nghiệm Ablation A1 và A2 theo đề tài:
- A1: Bật/tắt cắt tỉa Alpha-Beta và thứ tự nước đi ở các độ sâu 4, 5, 6
- A2: MCTS tăng dần số lượng mô phỏng (100, 500, 1000, 2000, 5000) đối đầu Alpha-Beta depth 4
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
import pandas as pd

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.agents import Budget, make_agent
from c4.agents.alphabeta import AlphaBetaAgent
from c4.eval.match import generate_openings, run_match, save_records_csv
from c4.eval.metrics import percentile, summarize
from c4.game import Connect4

ROOT_DIR = Path(__file__).resolve().parent.parent


def run_ablation_a1(depths=(4, 5, 6)) -> None:
    print("\n=======================================================")
    print(" CHẠY ABLATION A1: CẮT TỈA ALPHA-BETA VÀ THỨ TỰ NƯỚC ĐI")
    print("=======================================================")
    records = []
    configs = [
        ("Pruning_ON_Ordering_ON", True, True),
        ("Pruning_ON_Ordering_OFF", True, False),
        ("Pruning_OFF_Ordering_ON", False, True),
        ("Pruning_OFF_Ordering_OFF", False, False),
    ]

    for d in depths:
        for cfg_name, pruning, ordering in configs:
            agent = AlphaBetaAgent(pruning=pruning, ordering=ordering, default_depth=d)
            g = Connect4()
            # Đi 2 nước mở đầu mẫu để bàn cờ có trạng thái
            g.step(3)
            g.step(3)

            t0 = time.perf_counter()
            best_move = agent.choose_action(g, Budget(depth=d))
            elapsed = time.perf_counter() - t0
            nodes = agent.last_stats.get("nodes", 0)
            val = agent.last_stats.get("value")

            print(f"Depth {d} | {cfg_name:25s} | Nodes: {nodes:6d} | Time: {elapsed*1000:7.2f} ms | Move: {best_move+1}")
            records.append({
                "Depth": d,
                "Config": cfg_name,
                "Pruning": pruning,
                "Ordering": ordering,
                "Nodes": nodes,
                "Time_ms": round(elapsed * 1000, 3),
                "Best_Move": best_move + 1,
                "Score_Value": val,
            })

    out_file = ROOT_DIR / "results/tables/ablation_a1_results.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"[+] Đã lưu kết quả Ablation A1 vào: {out_file}")


def run_ablation_a2(simulations=(100, 500, 1000, 2000), openings_count=20, seed=42) -> None:
    print("\n=======================================================")
    print(" CHẠY ABLATION A2: MCTS THEO SỐ LƯỢNG MÔ PHỎNG (RQ1)")
    print("=======================================================")
    openings = generate_openings(openings_count, plies=4, seed=seed)
    opp = make_agent("alphabeta", seed=seed)
    opp_budget = Budget(depth=4)

    records = []
    for sims in simulations:
        print(f"\n[*] Đang chạy MCTS ({sims} sims) vs Alpha-Beta (depth 4)...")
        mcts = make_agent("mcts", seed=seed)
        mcts_budget = Budget(simulations=sims)

        recs = run_match(mcts, opp, openings, mcts_budget, opp_budget, pair=f"mcts_{sims}_vs_ab4")
        save_path = ROOT_DIR / f"results/logs/ablation_a2_mcts_{sims}_vs_ab4.csv"
        save_records_csv(recs, str(save_path))

        s = summarize([r.a_result for r in recs], seed=seed)
        times = [t for r in recs for t in r.a_times]

        print(f"    Sims: {sims} | Score: {s['score']:.3f} (CI: {s['score_boot_low']:.3f}-{s['score_boot_high']:.3f}) | WinRate: {s['win_rate']:.3f}")
        records.append({
            "MCTS_Simulations": sims,
            "Opponent": "alphabeta_depth4",
            "Games": s["n"],
            "MCTS_Wins": s["wins"],
            "Draws": s["draws"],
            "AlphaBeta_Wins": s["losses"],
            "Score": round(s["score"], 4),
            "Score_CI_Low": round(s["score_boot_low"], 4),
            "Score_CI_High": round(s["score_boot_high"], 4),
            "WinRate": round(s["win_rate"], 4),
            "Mean_Time_ms": round(1000 * sum(times) / max(len(times), 1), 3),
            "p95_Time_ms": round(1000 * percentile(times, 95), 3),
        })

    out_file = ROOT_DIR / "results/tables/ablation_a2_results.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"\n[+] Đã lưu kết quả Ablation A2 vào: {out_file}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--a1", action="store_true", help="Chạy ablation A1")
    p.add_argument("--a2", action="store_true", help="Chạy ablation A2")
    p.add_argument("--all", action="store_true", help="Chạy cả A1 và A2")
    args = p.parse_args()

    if args.a1 or args.all or not (args.a1 or args.a2):
        run_ablation_a1()
    if args.a2 or args.all:
        run_ablation_a2()


if __name__ == "__main__":
    main()
