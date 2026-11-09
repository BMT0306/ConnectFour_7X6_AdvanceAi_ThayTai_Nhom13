#!/usr/bin/env python3
"""Script chạy đầy đủ 4 thực nghiệm Phân tích Thành phần (Ablation Studies A1 - A4):
- A1: Bật/tắt cắt tỉa Alpha-Beta và thứ tự ưu tiên cột giữa ở các độ sâu 4, 5, 6
- A2: MCTS tăng dần số lượng mô phỏng (100, 500, 1000, 2000, 5000) đối đầu Alpha-Beta depth 4 (RQ1)
- A3: Đóng góp của Policy Prior & Value Head vs Random Rollout (NN Policy-only vs MCTS-UCT vs PUCT-Rollout vs PUCT-ValueHead) (RQ2 & RQ3)
- A4: Phân tích Lợi thế Người đi trước (First-player Bias: Đỏ đi trước vs Vàng đi sau) từ log giải đấu Round-Robin
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
import os
import sys
import time
from pathlib import Path

import pandas as pd
import torch

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.agents import Budget, MixedMCTSAgent, NNAgent, make_agent
from c4.agents.alphabeta import AlphaBetaAgent
from c4.eval.match import generate_openings, run_match, save_records_csv
from c4.eval.metrics import percentile, summarize, wilson_interval
from c4.game import Connect4

ROOT_DIR = Path(os.environ.get("C4_OUT_ROOT", str(Path(__file__).resolve().parent.parent)))


def run_ablation_a1(depths=(4, 5, 6)) -> Path:
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
        baseline_nodes = None
        temp_rows = []
        for cfg_name, pruning, ordering in configs:
            agent = AlphaBetaAgent(pruning=pruning, ordering=ordering, default_depth=d)
            g = Connect4()
            g.step(3)
            g.step(3)

            t0 = time.perf_counter()
            best_move = agent.choose_action(g, Budget(depth=d))
            elapsed = time.perf_counter() - t0
            nodes = agent.last_stats.get("nodes", 0)
            val = agent.last_stats.get("value")
            if not pruning and not ordering:
                baseline_nodes = nodes

            print(f"Depth {d} | {cfg_name:25s} | Nodes: {nodes:6d} | Time: {elapsed*1000:7.2f} ms | Move: {best_move+1}")
            temp_rows.append({
                "Depth": d,
                "Config": cfg_name,
                "Pruning": pruning,
                "Ordering": ordering,
                "Nodes": nodes,
                "Time_ms": round(elapsed * 1000, 3),
                "Best_Move": best_move + 1,
                "Score_Value": val,
            })

        for row in temp_rows:
            red_pct = (1.0 - row["Nodes"] / max(baseline_nodes or 1, 1)) * 100.0
            row["Node_Reduction_Pct"] = round(red_pct, 2)
            records.append(row)

    out_file = ROOT_DIR / "results/tables/ablation_a1_results.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"[+] Đã lưu kết quả Ablation A1 vào: {out_file}")
    return out_file


def run_ablation_a2(simulations=(100, 500, 1000, 2000, 5000), openings_count=50, seed=2026) -> Path:
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
    return out_file


def _run_a3_job(job: dict) -> dict:
    torch.set_num_threads(1)
    if job.get("ckpt_env"):
        os.environ["C4_CHECKPOINT_PATH"] = job["ckpt_env"]

    var_name = job["var_name"]
    opp_name = job["opp_name"]
    sims = job["sims"]
    seed = job["seed"]
    openings = job["openings"]
    root_dir = Path(job["root_dir"])

    if var_name == "NN_Policy_Only":
        agent_a, var_budget = NNAgent(seed=seed), Budget()
    elif var_name == "MCTS_UCT_Rollout":
        agent_a, var_budget = make_agent("mcts", seed=seed), Budget(simulations=sims)
    elif var_name == "PUCT_Prior_Rollout":
        agent_a, var_budget = MixedMCTSAgent(seed=seed, default_simulations=sims, use_value_head=False), Budget(simulations=sims)
    else:
        agent_a, var_budget = MixedMCTSAgent(seed=seed, default_simulations=sims, use_value_head=True), Budget(simulations=sims)

    if opp_name == "mcts_500":
        agent_b, opp_budget = make_agent("mcts", seed=seed + 99), Budget(simulations=500)
    else:
        agent_b, opp_budget = make_agent("alphabeta", seed=seed + 99), Budget(depth=4)

    pair_id = f"{var_name}_vs_{opp_name}"
    recs = run_match(agent_a, agent_b, openings, var_budget, opp_budget, pair=pair_id)
    save_path = root_dir / f"results/logs/ablation_a3_{pair_id}.csv"
    save_records_csv(recs, str(save_path))

    s = summarize([r.a_result for r in recs], seed=seed)
    times = [t for r in recs for t in r.a_times]
    mean_ms = 1000.0 * sum(times) / max(len(times), 1)
    sims_per_sec = (sims / (mean_ms / 1000.0)) if ("NN_Policy" not in var_name and mean_ms > 0) else 0.0

    return {
        "Variant": var_name,
        "Simulations_Budget": 0 if "NN_Policy" in var_name else sims,
        "Opponent": opp_name,
        "Games": s["n"],
        "Wins": s["wins"],
        "Draws": s["draws"],
        "Losses": s["losses"],
        "Score": round(s["score"], 4),
        "Score_CI_Low": round(s["score_boot_low"], 4),
        "Score_CI_High": round(s["score_boot_high"], 4),
        "WinRate": round(s["win_rate"], 4),
        "Win_Wilson_Low": round(s["win_rate_wilson_low"], 4),
        "Win_Wilson_High": round(s["win_rate_wilson_high"], 4),
        "Mean_Time_ms": round(mean_ms, 3),
        "p95_Time_ms": round(1000.0 * percentile(times, 95), 3),
        "Simulations_Per_Sec": round(sims_per_sec, 1),
    }


def run_ablation_a3(sims: int = 200, openings_count: int = 50, seed: int = 2026, workers: int = 4) -> Path:
    """Ablation A3 (RQ2 & RQ3): So sánh Policy-only NN, MCTS-UCT thuần, PUCT+Rollout và PUCT+ValueHead."""
    torch.set_num_threads(1)
    print("\n=====================================================================")
    print(" CHẠY ABLATION A3: ĐÓNG GÓP POLICY PRIOR & VALUE HEAD TRONG PUCT-MCTS")
    print("=====================================================================")
    openings = generate_openings(openings_count, plies=4, seed=seed)
    ckpt_env = os.environ.get("C4_CHECKPOINT_PATH")

    variants = ["NN_Policy_Only", "MCTS_UCT_Rollout", "PUCT_Prior_Rollout", "PUCT_Prior_ValueHead"]
    opponents = ["mcts_500", "alphabeta_d4"]

    jobs = [
        {
            "var_name": v,
            "opp_name": o,
            "sims": sims,
            "seed": seed,
            "openings": openings,
            "root_dir": str(ROOT_DIR),
            "ckpt_env": ckpt_env,
        }
        for v in variants
        for o in opponents
    ]

    records = []
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for row in ex.map(_run_a3_job, jobs):
                print(
                    f"    [+] {row['Variant']:20s} vs {row['Opponent']:12s} | "
                    f"Score: {row['Score']:.3f} [{row['Score_CI_Low']:.3f}, {row['Score_CI_High']:.3f}] | "
                    f"W/D/L: {row['Wins']}/{row['Draws']}/{row['Losses']} | Mean: {row['Mean_Time_ms']:.2f} ms"
                )
                records.append(row)
    else:
        for j in jobs:
            row = _run_a3_job(j)
            print(
                f"    [+] {row['Variant']:20s} vs {row['Opponent']:12s} | "
                f"Score: {row['Score']:.3f} [{row['Score_CI_Low']:.3f}, {row['Score_CI_High']:.3f}] | "
                f"W/D/L: {row['Wins']}/{row['Draws']}/{row['Losses']} | Mean: {row['Mean_Time_ms']:.2f} ms"
            )
            records.append(row)

    out_file = ROOT_DIR / "results/tables/ablation_a3_results.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"\n[+] Đã lưu kết quả Ablation A3 vào: {out_file}")
    return out_file


def run_ablation_a4() -> Path:
    """Ablation A4/A5: Phân tích lợi thế người đi trước (Quân Đỏ P1 vs Quân Vàng P2) từ toàn bộ log giải đấu chính."""
    print("\n=====================================================================")
    print(" CHẠY ABLATION A4: PHÂN TÍCH LỢI THẾ NGƯỜI ĐI TRƯỚC (FIRST-PLAYER BIAS)")
    print("=====================================================================")
    logs_dir = ROOT_DIR / "results/logs"
    log_files = sorted(logs_dir.glob("round_robin_default_*.csv"))
    if not log_files:
        raise FileNotFoundError("Chưa có log round_robin_default_*.csv trong results/logs/. Hãy chạy run_tournament.py trước!")

    rows = []
    total_games = 0
    total_p1_wins = 0
    total_p2_wins = 0
    total_draws = 0

    for lf in log_files:
        with open(lf, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        if not reader:
            continue

        pair = reader[0]["pair"]
        n = len(reader)
        p1_wins = 0
        p2_wins = 0
        draws = 0

        for r in reader:
            a_first = r["a_first"].strip().lower() in ("1", "true")
            a_res = int(r["a_result"])
            if a_res == 0:
                draws += 1
            elif (a_first and a_res == 1) or ((not a_first) and a_res == -1):
                p1_wins += 1
            else:
                p2_wins += 1

        total_games += n
        total_p1_wins += p1_wins
        total_p2_wins += p2_wins
        total_draws += draws

        p1_wr = p1_wins / n
        p2_wr = p2_wins / n
        w_lo, w_hi = wilson_interval(p1_wins, n)
        rows.append({
            "Pair": pair,
            "Games": n,
            "Red_P1_Wins": p1_wins,
            "Draws": draws,
            "Yellow_P2_Wins": p2_wins,
            "Red_P1_WinRate": round(p1_wr, 4),
            "Yellow_P2_WinRate": round(p2_wr, 4),
            "Delta_WinRate_Red_Minus_Yellow": round(p1_wr - p2_wr, 4),
            "Red_P1_Wilson95_Low": round(w_lo, 4),
            "Red_P1_Wilson95_High": round(w_hi, 4),
        })

    if total_games > 0:
        overall_p1_wr = total_p1_wins / total_games
        overall_p2_wr = total_p2_wins / total_games
        w_lo, w_hi = wilson_interval(total_p1_wins, total_games)
        rows.append({
            "Pair": "OVERALL_ALL_PAIRS",
            "Games": total_games,
            "Red_P1_Wins": total_p1_wins,
            "Draws": total_draws,
            "Yellow_P2_Wins": total_p2_wins,
            "Red_P1_WinRate": round(overall_p1_wr, 4),
            "Yellow_P2_WinRate": round(overall_p2_wr, 4),
            "Delta_WinRate_Red_Minus_Yellow": round(overall_p1_wr - overall_p2_wr, 4),
            "Red_P1_Wilson95_Low": round(w_lo, 4),
            "Red_P1_Wilson95_High": round(w_hi, 4),
        })
        print(
            f"[*] Tổng hợp {total_games} ván: Đỏ (đi trước) thắng {total_p1_wins} ({overall_p1_wr*100:.2f}%) | "
            f"Vàng (đi sau) thắng {total_p2_wins} ({overall_p2_wr*100:.2f}%) | Hòa {total_draws} | "
            f"Delta W = {(overall_p1_wr - overall_p2_wr)*100:+.2f}%"
        )

    out_file = ROOT_DIR / "results/tables/ablation_a4_first_player_bias.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"[+] Đã lưu kết quả Ablation A4 vào: {out_file}")
    return out_file


def main() -> None:
    global ROOT_DIR
    p = argparse.ArgumentParser(description="Chạy các thí nghiệm Ablation A1 - A4")
    p.add_argument("--a1", action="store_true", help="Chạy Ablation A1 (Pruning & Ordering)")
    p.add_argument("--a2", action="store_true", help="Chạy Ablation A2 (MCTS Simulations Scaling)")
    p.add_argument("--a3", action="store_true", help="Chạy Ablation A3 (Policy Prior & Value Head vs Rollout)")
    p.add_argument("--a4", action="store_true", help="Chạy Ablation A4 (First-player Bias từ log giải đấu)")
    p.add_argument("--all", action="store_true", help="Chạy toàn bộ A1, A2, A3, A4")
    p.add_argument("--out-root", default=None, help="Thư mục gốc lưu kết quả")
    p.add_argument("--workers", type=int, default=4, help="Số tiến trình song song cho A3")
    args = p.parse_args()

    if args.out_root:
        ROOT_DIR = Path(args.out_root)
    alt_ckpt = ROOT_DIR / "checkpoints/policy_net_best.pt"
    if alt_ckpt.exists():
        os.environ.setdefault("C4_CHECKPOINT_PATH", str(alt_ckpt))

    selected = args.a1 or args.a2 or args.a3 or args.a4 or args.all
    if args.a1 or args.all or not selected:
        run_ablation_a1()
    if args.a2 or args.all:
        run_ablation_a2()
    if args.a3 or args.all:
        run_ablation_a3(workers=args.workers)
    if args.a4 or args.all:
        run_ablation_a4()


if __name__ == "__main__":
    main()
