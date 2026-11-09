#!/usr/bin/env python3
"""Script chạy giải đấu Round-Robin tự động từ file cấu hình YAML.
Lưu log thô mức ván vào results/logs/ và tạo bảng tổng kết vào results/tables/.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import csv
import itertools
import json
import os
import sys
from pathlib import Path
import pandas as pd
import torch
import yaml

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


def _run_pair_job(job: dict) -> dict:
    torch.set_num_threads(1)
    if job.get("ckpt_env"):
        os.environ["C4_CHECKPOINT_PATH"] = job["ckpt_env"]

    entry_a = job["entry_a"]
    entry_b = job["entry_b"]
    seed = job["seed"]
    time_limit_s = job["time_limit_s"]
    openings = job["openings"]
    t_name = job["t_name"]
    log_dir = Path(job["log_dir"])

    type_a, budget_a_cfg = entry_a["name"], entry_a.get("budget")
    type_b, budget_b_cfg = entry_b["name"], entry_b.get("budget")
    label_a = entry_a.get("label", type_a)
    label_b = entry_b.get("label", type_b)
    params_a = dict(entry_a.get("params") or {})
    params_b = dict(entry_b.get("params") or {})

    agent_a = make_agent(type_a, seed=seed, **params_a)
    agent_b = make_agent(type_b, seed=seed + 1, **params_b)

    if time_limit_s is not None:
        budget_a = Budget(time_s=time_limit_s)
        budget_b = Budget(time_s=time_limit_s)
    else:
        budget_a = parse_budget(budget_a_cfg)
        budget_b = parse_budget(budget_b_cfg)

    level_tag = f"_{int(round(time_limit_s * 1000))}ms" if time_limit_s is not None else ""
    pair_name = f"{label_a}_vs_{label_b}{level_tag}"
    log_file = log_dir / f"{t_name}_{pair_name}.csv"

    expected_games = 2 * len(openings)
    loaded_rows = None
    if job.get("resume") and log_file.exists():
        with open(log_file, "r", encoding="utf-8") as lf:
            rows_csv = list(csv.DictReader(lf))
        if len(rows_csv) == expected_games:
            loaded_rows = rows_csv

    if loaded_rows is not None:
        a_results = [int(r["a_result"]) for r in loaded_rows]
        stats_a = summarize(a_results, seed=seed)
        first_scores = [
            1.0 if int(r["a_result"]) == 1 else (0.5 if int(r["a_result"]) == 0 else 0.0)
            for r in loaded_rows
            if r["a_first"].strip().lower() in ("1", "true")
        ]
        second_scores = [
            1.0 if int(r["a_result"]) == 1 else (0.5 if int(r["a_result"]) == 0 else 0.0)
            for r in loaded_rows
            if r["a_first"].strip().lower() not in ("1", "true")
        ]
        times_a = [t for r in loaded_rows for t in json.loads(r["a_times_s"])]
        times_b = [t for r in loaded_rows for t in json.loads(r["b_times_s"])]
    else:
        recs = run_match(agent_a, agent_b, openings, budget_a, budget_b, pair=pair_name)
        save_records_csv(recs, str(log_file))

        stats_a = summarize([r.a_result for r in recs], seed=seed)
        first_scores = [1.0 if r.a_result == 1 else (0.5 if r.a_result == 0 else 0.0) for r in recs if r.a_first]
        second_scores = [1.0 if r.a_result == 1 else (0.5 if r.a_result == 0 else 0.0) for r in recs if not r.a_first]

        times_a = [t for r in recs for t in r.a_times]
        times_b = [t for r in recs for t in r.b_times]

    return {
        "Pair": pair_name,
        "Agent_A": label_a,
        "Agent_B": label_b,
        "Time_Limit_s": time_limit_s if time_limit_s is not None else "custom",
        "Games": stats_a["n"],
        "A_Wins": stats_a["wins"],
        "Draws": stats_a["draws"],
        "B_Wins": stats_a["losses"],
        "A_Score": round(stats_a["score"], 4),
        "A_Score_CI_Low": round(stats_a["score_boot_low"], 4),
        "A_Score_CI_High": round(stats_a["score_boot_high"], 4),
        "A_WinRate": round(stats_a["win_rate"], 4),
        "A_Win_Wilson_Low": round(stats_a["win_rate_wilson_low"], 4),
        "A_Win_Wilson_High": round(stats_a["win_rate_wilson_high"], 4),
        "A_Score_First": round(sum(first_scores) / max(len(first_scores), 1), 4),
        "A_Score_Second": round(sum(second_scores) / max(len(second_scores), 1), 4),
        "A_Mean_Time_ms": round(1000 * sum(times_a) / max(len(times_a), 1), 3),
        "A_p95_Time_ms": round(1000 * percentile(times_a, 95), 3),
        "B_Mean_Time_ms": round(1000 * sum(times_b) / max(len(times_b), 1), 3),
        "B_p95_Time_ms": round(1000 * percentile(times_b, 95), 3),
    }


def run_tournament(
    config_path: Path, out_root: Path | None = None, workers: int | None = None, resume: bool = False
) -> Path:
    torch.set_num_threads(1)
    base_out = out_root if out_root is not None else Path(os.environ.get("C4_OUT_ROOT", str(ROOT_DIR)))
    alt_ckpt = base_out / "checkpoints/policy_net_best.pt"
    ckpt_env = None
    if alt_ckpt.exists():
        ckpt_env = str(alt_ckpt)
        os.environ.setdefault("C4_CHECKPOINT_PATH", ckpt_env)

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    t_cfg = cfg.get("tournament", {})
    t_name = t_cfg.get("name", "tournament")
    n_openings = t_cfg.get("openings", 20)
    plies = t_cfg.get("opening_plies", 4)
    seed = t_cfg.get("seed", 42)

    log_dir = base_out / cfg.get("output", {}).get("log_dir", "results/logs")
    summary_dir = base_out / cfg.get("output", {}).get("summary_dir", "results/tables")
    log_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    agent_entries = cfg.get("agents", [])
    time_levels = cfg.get("time_levels")

    # Giải đấu giới hạn thời gian thực (time_levels) luôn chạy tuần tự 1 luồng để không nhiễu bộ đếm ms
    if time_levels:
        eff_workers = 1
    else:
        eff_workers = workers if workers is not None else min(8, os.cpu_count() or 1)

    print(f"[*] Bắt đầu giải đấu '{t_name}' (workers={eff_workers})")
    print(f"[*] Số tác tử tham gia: {len(agent_entries)} | Khai cuộc: {n_openings} ({2 * n_openings} ván/cặp)")

    openings = generate_openings(n_openings, plies=plies, seed=seed)
    pairs = list(itertools.combinations(range(len(agent_entries)), 2))
    levels = time_levels if time_levels else [None]

    jobs = []
    for tl in levels:
        time_limit_s = tl.get("time_s") if tl else None
        for idx_a, idx_b in pairs:
            jobs.append({
                "entry_a": agent_entries[idx_a],
                "entry_b": agent_entries[idx_b],
                "seed": seed,
                "time_limit_s": time_limit_s,
                "openings": openings,
                "t_name": t_name,
                "log_dir": str(log_dir),
                "ckpt_env": ckpt_env,
                "resume": resume,
            })

    summary_rows = []
    if eff_workers > 1 and len(jobs) > 1:
        with ProcessPoolExecutor(max_workers=eff_workers) as ex:
            for row in ex.map(_run_pair_job, jobs):
                print(
                    f"    [+] {row['Pair']:28s} | W={row['A_Wins']:3d} D={row['Draws']:2d} L={row['B_Wins']:3d} | "
                    f"Score={row['A_Score']:.3f} [{row['A_Score_CI_Low']:.3f}, {row['A_Score_CI_High']:.3f}]"
                )
                summary_rows.append(row)
    else:
        for j in jobs:
            row = _run_pair_job(j)
            print(
                f"    [+] {row['Pair']:28s} | W={row['A_Wins']:3d} D={row['Draws']:2d} L={row['B_Wins']:3d} | "
                f"Score={row['A_Score']:.3f} [{row['A_Score_CI_Low']:.3f}, {row['A_Score_CI_High']:.3f}]"
            )
            summary_rows.append(row)

    df = pd.DataFrame(summary_rows)
    table_file = summary_dir / f"{t_name}_summary.csv"
    df.to_csv(table_file, index=False, encoding="utf-8-sig")
    print(f"\n[+] Hoàn thành giải đấu! Bảng tổng kết lưu tại: {table_file}")
    return table_file


def main() -> None:
    p = argparse.ArgumentParser(description="Chạy giải đấu Connect Four AI từ file YAML")
    p.add_argument("--config", default=str(ROOT_DIR / "configs/tournament_default.yaml"))
    p.add_argument("--out-root", default=None, help="Thư mục gốc lưu kết quả (mặc định: thư mục repo)")
    p.add_argument("--workers", type=int, default=None, help="Số tiến trình song song cho giải đấu cố định cấu hình")
    p.add_argument("--resume", action="store_true", help="Tái sử dụng log CSV đủ số ván nếu đã tồn tại")
    args = p.parse_args()
    run_tournament(Path(args.config), Path(args.out_root) if args.out_root else None, args.workers, args.resume)


if __name__ == "__main__":
    main()
