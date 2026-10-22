#!/usr/bin/env python3
"""Script chạy giải đấu Round-Robin tự động từ file cấu hình YAML.
Lưu log thô mức ván vào results/logs/ và tạo bảng tổng kết vào results/tables/.
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path
import yaml
import pandas as pd

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.agents import Budget, make_agent
from c4.eval.match import generate_openings, run_match, save_records_csv
from c4.eval.metrics import percentile, summarize

ROOT_DIR = Path(__file__).resolve().parent.parent


def parse_budget(cfg_dict: dict | None) -> Budget | None:
    if not cfg_dict:
        return None
    return Budget(
        time_s=cfg_dict.get("time_s"),
        simulations=cfg_dict.get("simulations"),
        depth=cfg_dict.get("depth"),
    )


def run_tournament(config_path: Path) -> None:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    t_cfg = cfg.get("tournament", {})
    t_name = t_cfg.get("name", "tournament")
    n_openings = t_cfg.get("openings", 20)
    plies = t_cfg.get("opening_plies", 4)
    seed = t_cfg.get("seed", 42)

    log_dir = ROOT_DIR / cfg.get("output", {}).get("log_dir", "results/logs")
    summary_dir = ROOT_DIR / cfg.get("output", {}).get("summary_dir", "results/tables")
    log_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    agent_entries = cfg.get("agents", [])
    print(f"[*] Bắt đầu giải đấu '{t_name}'")
    print(f"[*] Số tác tử tham gia: {len(agent_entries)}")
    print(f"[*] Số khai cuộc: {n_openings} (2 x {n_openings} = {2 * n_openings} ván/cặp)")

    openings = generate_openings(n_openings, plies=plies, seed=seed)

    summary_rows = []

    # Cặp đấu vòng tròn (Round-Robin)
    pairs = list(itertools.combinations(range(len(agent_entries)), 2))
    for idx_a, idx_b in pairs:
        entry_a = agent_entries[idx_a]
        entry_b = agent_entries[idx_b]
        name_a, budget_a_cfg = entry_a["name"], entry_a.get("budget")
        name_b, budget_b_cfg = entry_b["name"], entry_b.get("budget")

        agent_a = make_agent(name_a, seed=seed)
        agent_b = make_agent(name_b, seed=seed + 1)
        budget_a = parse_budget(budget_a_cfg)
        budget_b = parse_budget(budget_b_cfg)

        pair_name = f"{name_a}_vs_{name_b}"
        print(f"\n--- Trận đấu: {pair_name} ---")

        recs = run_match(agent_a, agent_b, openings, budget_a, budget_b, pair=pair_name)
        log_file = log_dir / f"{t_name}_{pair_name}.csv"
        save_records_csv(recs, str(log_file))
        print(f"    Đã lưu {len(recs)} ván vào {log_file.name}")

        stats_a = summarize([r.a_result for r in recs], seed=seed)
        times_a = [t for r in recs for t in r.a_times]
        times_b = [t for r in recs for t in r.b_times]

        summary_rows.append({
            "Pair": pair_name,
            "Agent_A": name_a,
            "Agent_B": name_b,
            "Games": stats_a["n"],
            "A_Wins": stats_a["wins"],
            "Draws": stats_a["draws"],
            "B_Wins": stats_a["losses"],
            "A_Score": round(stats_a["score"], 4),
            "A_Score_CI_Low": round(stats_a["score_boot_low"], 4),
            "A_Score_CI_High": round(stats_a["score_boot_high"], 4),
            "A_WinRate": round(stats_a["win_rate"], 4),
            "A_Mean_Time_ms": round(1000 * sum(times_a) / max(len(times_a), 1), 3),
            "A_p95_Time_ms": round(1000 * percentile(times_a, 95), 3),
            "B_Mean_Time_ms": round(1000 * sum(times_b) / max(len(times_b), 1), 3),
            "B_p95_Time_ms": round(1000 * percentile(times_b, 95), 3),
        })

    df = pd.DataFrame(summary_rows)
    table_file = summary_dir / f"{t_name}_summary.csv"
    df.to_csv(table_file, index=False, encoding="utf-8-sig")
    print(f"\n[+] Hoàn thành giải đấu! Bảng tổng kết lưu tại: {table_file}")


def main() -> None:
    p = argparse.ArgumentParser(description="Chạy giải đấu Connect Four AI từ file YAML")
    p.add_argument("--config", default=str(ROOT_DIR / "configs/tournament_default.yaml"))
    args = p.parse_args()
    run_tournament(Path(args.config))


if __name__ == "__main__":
    main()
