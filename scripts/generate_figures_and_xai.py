#!/usr/bin/env python3
"""Script tổng hợp số liệu thực nghiệm và sinh toàn bộ biểu đồ chuẩn báo cáo khoa học + Saliency Map XAI."""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "c4_mpl_cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.game import COLS, PLAYER1, ROWS, Connect4
from c4.models import Connect4PolicyValueNet, compute_saliency_map

ROOT_DIR = Path(os.environ.get("C4_OUT_ROOT", str(Path(__file__).resolve().parent.parent)))
TABLES_DIR = ROOT_DIR / "results/tables"
FIGURES_DIR = ROOT_DIR / "results/figures"
CKPT_FILE = ROOT_DIR / "checkpoints/policy_net_best.pt"

AGENT_LABELS = {
    "random": "Random\n(Cấp 1)",
    "heuristic": "Heuristic\n(Cấp 2)",
    "nn": "Policy-Value NN\n(Cấp 5)",
    "mcts": "MCTS-UCT\n(Cấp 4)",
    "mixed_mcts": "Mixed-MCTS PUCT\n(Mở rộng)",
    "alphabeta": "Alpha-Beta\n(Cấp 3)",
}


def plot_round_robin_matrix() -> None:
    csv_path = TABLES_DIR / "round_robin_default_summary.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    order = ["random", "heuristic", "nn", "mcts", "mixed_mcts", "alphabeta"]
    present = [a for a in order if a in set(df["Agent_A"]).union(set(df["Agent_B"]))]
    n = len(present)
    mat = np.full((n, n), np.nan, dtype=float)
    wins_tot = {a: 0 for a in present}
    draws_tot = {a: 0 for a in present}
    games_tot = {a: 0 for a in present}

    idx = {a: i for i, a in enumerate(present)}
    for _, r in df.iterrows():
        a, b = r["Agent_A"], r["Agent_B"]
        if a in idx and b in idx:
            sa = float(r["A_Score"])
            mat[idx[a], idx[b]] = sa
            mat[idx[b], idx[a]] = 1.0 - sa

            g = int(r["Games"])
            aw, d, bw = int(r["A_Wins"]), int(r["Draws"]), int(r["B_Wins"])
            wins_tot[a] += aw
            draws_tot[a] += d
            games_tot[a] += g
            wins_tot[b] += bw
            draws_tot[b] += d
            games_tot[b] += g

    overall_scores = [
        (wins_tot[a] + 0.5 * draws_tot[a]) / max(games_tot[a], 1) for a in present
    ]
    ranked = sorted(zip(present, overall_scores), key=lambda x: x[1], reverse=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.8), gridspec_kw={"width_ratios": [1.25, 1.0]})

    masked = np.ma.masked_invalid(mat)
    cmap = plt.cm.RdYlGn
    cmap.set_bad(color="#E2E8F0")
    im = ax1.imshow(masked, cmap=cmap, vmin=0.0, vmax=1.0)
    short_names = [AGENT_LABELS.get(a, a).replace("\n", " ") for a in present]
    ax1.set_xticks(range(n))
    ax1.set_yticks(range(n))
    ax1.set_xticklabels(short_names, rotation=30, ha="right", fontsize=9)
    ax1.set_yticklabels(short_names, fontsize=9)
    ax1.set_title("Ma trận Điểm đối đầu Hàng vs Cột (200 ván/cặp)", fontsize=11, fontweight="bold")

    for i in range(n):
        for j in range(n):
            if i == j:
                ax1.text(j, i, "—", ha="center", va="center", color="#475569", fontweight="bold")
            elif not np.isnan(mat[i, j]):
                val = mat[i, j]
                txt_col = "white" if (val < 0.22 or val > 0.82) else "#0F172A"
                ax1.text(j, i, f"{val:.2f}", ha="center", va="center", color=txt_col, fontsize=9, fontweight="bold")
    fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04, label="Score = (W + 0.5·D) / N")

    r_agents = [AGENT_LABELS.get(a, a).replace("\n", " ") for a, _ in ranked][::-1]
    r_vals = [v * 100.0 for _, v in ranked][::-1]
    colors = ["#94A3B8", "#F59E0B", "#8B5CF6", "#10B981", "#0EA5E9", "#2563EB"][: len(r_vals)]
    bars = ax2.barh(r_agents, r_vals, color=colors, edgecolor="#1E293B", height=0.6)
    ax2.set_xlim(0, 108)
    ax2.set_xlabel("Điểm tổng hợp toàn giải (%)")
    ax2.set_title("Bảng xếp hạng Sức mạnh Tổng thể (Round-Robin)", fontsize=11, fontweight="bold")
    ax2.grid(axis="x", linestyle="--", alpha=0.5)
    for bar, v in zip(bars, r_vals):
        ax2.text(v + 1.5, bar.get_y() + bar.get_height() / 2, f"{v:.1f}%", va="center", fontsize=9.5, fontweight="bold")

    plt.tight_layout()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURES_DIR / "round_robin_heatmap.png", dpi=300)
    plt.close(fig)
    print("[+] Đã xuất: round_robin_heatmap.png")


def plot_ablation_a1() -> None:
    csv_path = TABLES_DIR / "ablation_a1_results.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    depths = sorted(df["Depth"].unique())
    configs = [
        ("Pruning_OFF_Ordering_OFF", "Minimax thuần (Tắt cắt tỉa)", "#EF4444"),
        ("Pruning_ON_Ordering_OFF", "Alpha-Beta (Không sắp xếp)", "#F59E0B"),
        ("Pruning_ON_Ordering_ON", "Alpha-Beta + Center-First", "#10B981"),
    ]

    x = np.arange(len(depths))
    width = 0.26
    fig, ax = plt.subplots(figsize=(9.5, 5.0))

    for idx, (cfg_key, label, col) in enumerate(configs):
        sub = df[df["Config"] == cfg_key].sort_values("Depth")
        vals = sub["Nodes"].values
        rects = ax.bar(x + (idx - 1) * width, vals, width, label=label, color=col, edgecolor="#1E293B")
        for r, v in zip(rects, vals):
            ax.text(r.get_x() + r.get_width() / 2, v * 1.08, f"{int(v):,}", ha="center", va="bottom", fontsize=8.5)

    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Depth {d}" for d in depths], fontsize=10, fontweight="bold")
    ax.set_ylabel("Số nút duyệt (Log scale)")
    ax.set_title("Ablation A1: Hiệu quả Cắt tỉa Alpha-Beta & Thứ tự Center-First", fontsize=11.5, fontweight="bold")
    ax.set_ylim(40, df["Nodes"].max() * 2.2)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "ablation_a1_nodes.png", dpi=300)
    plt.close(fig)
    print("[+] Đã xuất: ablation_a1_nodes.png")


def plot_ablation_a2() -> None:
    csv_path = TABLES_DIR / "ablation_a2_results.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path).sort_values("MCTS_Simulations")
    sims = df["MCTS_Simulations"].values
    scores = df["Score"].values
    ci_lo = df["Score_CI_Low"].values
    ci_hi = df["Score_CI_High"].values
    p95 = df["p95_Time_ms"].values

    fig, ax1 = plt.subplots(figsize=(9.5, 5.0))
    ax1.plot(sims, scores, marker="o", linewidth=2.4, color="#2563EB", label="MCTS Score vs Alpha-Beta (d=4)")
    ax1.fill_between(sims, ci_lo, ci_hi, color="#2563EB", alpha=0.18, label="Bootstrap 95% CI")
    ax1.axhline(0.5, linestyle="--", color="#DC2626", linewidth=1.5, label="Ngưỡng cân bằng (Score = 0.50)")
    ax1.set_xscale("log")
    ax1.set_xticks(sims)
    ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.set_ylim(0.0, 0.85)
    ax1.set_xlabel("Ngân sách số mô phỏng MCTS (Log scale)")
    ax1.set_ylabel("Điểm đối đầu Score", color="#1D4ED8")

    ax2 = ax1.twinx()
    ax2.plot(sims, p95, marker="s", linestyle="-.", linewidth=1.8, color="#D97706", label="Độ trễ p95 (ms)")
    ax2.set_ylabel("Độ trễ p95 mỗi nước (ms)", color="#B45309")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.set_title("Ablation A2: Quy mô Mô phỏng MCTS đối đầu Alpha-Beta Depth 4", fontsize=11.5, fontweight="bold")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "ablation_a2_scaling.png", dpi=300)
    plt.close(fig)
    print("[+] Đã xuất: ablation_a2_scaling.png")


def plot_ablation_a3() -> None:
    csv_path = TABLES_DIR / "ablation_a3_results.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    variants_order = [
        ("NN_Policy_Only", "NN Policy-Only\n(0 search)"),
        ("MCTS_UCT_Rollout", "MCTS-UCT\n+ Rollout (200)"),
        ("PUCT_Prior_Rollout", "PUCT Prior\n+ Rollout (200)"),
        ("PUCT_Prior_ValueHead", "PUCT Prior\n+ Value Head (200)"),
    ]
    opps = [("mcts_500", "Đấu với MCTS (500 sims)", "#0EA5E9"), ("alphabeta_d4", "Đấu với Alpha-Beta (d=4)", "#8B5CF6")]

    x = np.arange(len(variants_order))
    width = 0.34
    fig, ax = plt.subplots(figsize=(10.2, 5.2))

    for idx, (opp_id, opp_lbl, col) in enumerate(opps):
        scores, err_lo, err_hi = [], [], []
        for v_id, _ in variants_order:
            row = df[(df["Variant"] == v_id) & (df["Opponent"] == opp_id)]
            if len(row) > 0:
                s = float(row["Score"].iloc[0])
                lo = float(row["Score_CI_Low"].iloc[0])
                hi = float(row["Score_CI_High"].iloc[0])
            else:
                s, lo, hi = 0.0, 0.0, 0.0
            scores.append(s)
            err_lo.append(max(0.0, s - lo))
            err_hi.append(max(0.0, hi - s))

        rects = ax.bar(
            x + (idx - 0.5) * width,
            scores,
            width,
            yerr=[err_lo, err_hi],
            capsize=4,
            label=opp_lbl,
            color=col,
            edgecolor="#1E293B",
        )
        for r, s in zip(rects, scores):
            ax.text(r.get_x() + r.get_width() / 2, min(s + 0.09, 0.98), f"{s:.2f}", ha="center", fontsize=8.5, fontweight="bold")

    ax.axhline(0.5, linestyle="--", color="#DC2626", linewidth=1.3, label="Ngưỡng cân bằng (0.50)")
    ax.set_xticks(x)
    ax.set_xticklabels([lbl for _, lbl in variants_order], fontsize=9.5, fontweight="bold")
    ax.set_ylim(0.0, 1.08)
    ax.set_ylabel("Điểm đối đầu Score (kèm 95% CI)")
    ax.set_title("Ablation A3 (RQ2 & RQ3): Đóng góp của Policy Prior & Value Head trong PUCT-MCTS", fontsize=11.5, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "ablation_a3_puct_value.png", dpi=300)
    plt.close(fig)
    print("[+] Đã xuất: ablation_a3_puct_value.png")


def plot_timed_rq1() -> None:
    csv_path = TABLES_DIR / "round_robin_timed_summary.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    df["Time_ms"] = (df["Time_Limit_s"].astype(float) * 1000).round().astype(int)
    df = df.sort_values("Time_ms")

    x = np.arange(len(df))
    ab_scores = df["A_Score"].values
    mcts_scores = 1.0 - ab_scores
    ab_lo = ab_scores - df["A_Score_CI_Low"].values
    ab_hi = df["A_Score_CI_High"].values - ab_scores

    width = 0.34
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    r1 = ax.bar(x - width / 2, ab_scores, width, yerr=[ab_lo, ab_hi], capsize=5, label="Alpha-Beta (Iterative Deepening)", color="#2563EB", edgecolor="#1E293B")
    r2 = ax.bar(x + width / 2, mcts_scores, width, yerr=[ab_hi, ab_lo], capsize=5, label="MCTS-UCT", color="#10B981", edgecolor="#1E293B")

    for r, v in zip(r1, ab_scores):
        ax.text(r.get_x() + r.get_width() / 2, min(v + 0.08, 0.98), f"{v:.2f}", ha="center", fontsize=9, fontweight="bold")
    for r, v in zip(r2, mcts_scores):
        ax.text(r.get_x() + r.get_width() / 2, min(v + 0.08, 0.98), f"{v:.2f}", ha="center", fontsize=9, fontweight="bold")

    ax.axhline(0.5, linestyle="--", color="#DC2626", linewidth=1.3)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{t} ms / nước\n({int(g)} ván)" for t, g in zip(df["Time_ms"], df["Games"])], fontweight="bold")
    ax.set_ylim(0.0, 1.08)
    ax.set_ylabel("Điểm đối đầu Score")
    ax.set_title("Chế độ A (RQ1): Alpha-Beta vs MCTS dưới cùng Ngân sách Thời gian", fontsize=11.5, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    ax.legend()

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "timed_crossover_rq1.png", dpi=300)
    plt.close(fig)
    print("[+] Đã xuất: timed_crossover_rq1.png")


def plot_first_player_bias() -> None:
    csv_path = TABLES_DIR / "ablation_a4_first_player_bias.csv"
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    sub = df[df["Pair"] != "OVERALL_ALL_PAIRS"].copy()
    overall = df[df["Pair"] == "OVERALL_ALL_PAIRS"]

    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    y = np.arange(len(sub))
    red = sub["Red_P1_WinRate"].values * 100.0
    drw = (sub["Draws"].values / sub["Games"].values) * 100.0
    yel = sub["Yellow_P2_WinRate"].values * 100.0

    ax.barh(y, red, color="#EF4444", label="Đỏ (Đi trước - P1) thắng %")
    ax.barh(y, drw, left=red, color="#94A3B8", label="Hòa %")
    ax.barh(y, yel, left=red + drw, color="#F59E0B", label="Vàng (Đi sau - P2) thắng %")
    ax.axvline(50.0, linestyle="--", color="#0F172A", linewidth=1.4)

    ax.set_yticks(y)
    ax.set_yticklabels(sub["Pair"].values, fontsize=8.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Tỷ lệ kết quả theo màu quân (%)")
    title_extra = ""
    if len(overall) > 0:
        p1_all = float(overall["Red_P1_WinRate"].iloc[0]) * 100.0
        p2_all = float(overall["Yellow_P2_WinRate"].iloc[0]) * 100.0
        title_extra = f" — Tổng thể: Đỏ {p1_all:.1f}% vs Vàng {p2_all:.1f}% (Δ={p1_all - p2_all:+.1f}%)"
    ax.set_title(f"Ablation A4: Lợi thế Người đi trước trên toàn bộ các cặp đấu{title_extra}", fontsize=10.8, fontweight="bold")
    ax.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "first_player_advantage.png", dpi=300)
    plt.close(fig)
    print("[+] Đã xuất: first_player_advantage.png")


def plot_xai_saliency() -> None:
    model = Connect4PolicyValueNet(num_res_blocks=3, num_filters=64)
    if CKPT_FILE.exists():
        data = torch.load(CKPT_FILE, map_location="cpu", weights_only=False)
        state_dict = data["model_state_dict"] if isinstance(data, dict) and "model_state_dict" in data else data
        model.load_state_dict(state_dict)
    model.eval()

    cases = [
        ("Tình huống 1: Phòng thủ sớm đòn kép hàng đáy (O chặn Cột 3 hoặc 6)", [3, 0, 4]),
        ("Tình huống 2: Nước thắng đường chéo khe giữa (X thắng ngay Cột 3)", [0, 1, 1, 2, 3, 2, 3, 3, 3, 6]),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.2), gridspec_kw={"width_ratios": [1.3, 1.0]})

    for row_idx, (title, moves) in enumerate(cases):
        g = Connect4()
        for m in moves:
            g.step(m)
        out = compute_saliency_map(model, g)
        sal = out["saliency"]  # (6, 7), row 0 is bottom
        probs = out["probs"]
        val = out["value"]
        chosen = out["chosen_col"]
        flat_top = np.argsort(sal.ravel())[::-1][:3]
        top_coords = [(int(idx // COLS) + 1, int(idx % COLS) + 1, round(float(sal.ravel()[idx]), 3)) for idx in flat_coords] if False else [
            (int(idx // COLS) + 1, int(idx % COLS) + 1, round(float(sal.ravel()[idx]), 3)) for idx in flat_top
        ]
        print(
            f"    [XAI Case {row_idx+1}] Chosen=Col {chosen+1} (P={probs[chosen]*100:.1f}%) | "
            f"Value={val:+.3f} | Top salient (row,col,w)={top_coords}"
        )
        arr = g.to_array()

        ax_b = axes[row_idx, 0]
        im = ax_b.imshow(sal, origin="lower", cmap="YlOrRd", vmin=0.0, vmax=1.0, aspect="equal")
        for r in range(ROWS):
            for c in range(COLS):
                p = arr[r, c]
                if p == PLAYER1:
                    ax_b.scatter(c, r, s=460, c="#DC2626", edgecolors="white", linewidths=2.0, zorder=3)
                    ax_b.text(c, r, "X", ha="center", va="center", color="white", fontweight="bold", fontsize=10, zorder=4)
                elif p == -PLAYER1:
                    ax_b.scatter(c, r, s=460, c="#FACC15", edgecolors="#1E293B", linewidths=2.0, zorder=3)
                    ax_b.text(c, r, "O", ha="center", va="center", color="#0F172A", fontweight="bold", fontsize=10, zorder=4)
                else:
                    ax_b.text(c, r, f"{sal[r, c]:.2f}", ha="center", va="center", color="#334155", fontsize=7.5, zorder=2)

        ax_b.set_xticks(range(COLS))
        ax_b.set_xticklabels([f"Cột {c+1}" for c in range(COLS)])
        ax_b.set_yticks(range(ROWS))
        ax_b.set_yticklabels([f"Hàng {r+1}" for r in range(ROWS)])
        ax_b.set_title(f"{title}\nSaliency Heatmap |d logit(Cột {chosen+1}) / dX|", fontsize=10, fontweight="bold")
        fig.colorbar(im, ax=ax_b, fraction=0.042, pad=0.03, label="Độ nhạy chuẩn hóa [0,1]")

        ax_p = axes[row_idx, 1]
        cols_x = np.arange(1, 8)
        bar_cols = ["#10B981" if (c - 1) == chosen else "#3B82F6" for c in cols_x]
        bars = ax_p.bar(cols_x, probs * 100.0, color=bar_cols, edgecolor="#1E293B")
        for b, pr in zip(bars, probs * 100.0):
            ax_p.text(b.get_x() + b.get_width() / 2, pr + 1.5, f"{pr:.1f}%", ha="center", fontsize=8.5, fontweight="bold")
        ax_p.set_xticks(cols_x)
        ax_p.set_xticklabels([f"Cột {c}" for c in cols_x])
        ax_p.set_ylim(0, 112)
        ax_p.set_ylabel("Xác suất Policy P(a|s) (%)")
        side = "X (Đỏ)" if g.current_player == PLAYER1 else "O (Vàng)"
        ax_p.set_title(
            f"Dự đoán của Mạng cho lượt {side}\nChọn Cột {chosen+1} | Value V(s) = {val:+.3f}",
            fontsize=10,
            fontweight="bold",
        )
        ax_p.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURES_DIR / "xai_saliency_double_threat.png", dpi=300)
    plt.close(fig)
    print("[+] Đã xuất: xai_saliency_double_threat.png")


def main() -> None:
    global ROOT_DIR, TABLES_DIR, FIGURES_DIR, CKPT_FILE
    p = argparse.ArgumentParser()
    p.add_argument("--out-root", default=None)
    args = p.parse_args()
    if args.out_root:
        ROOT_DIR = Path(args.out_root)
        TABLES_DIR = ROOT_DIR / "results/tables"
        FIGURES_DIR = ROOT_DIR / "results/figures"
        CKPT_FILE = ROOT_DIR / "checkpoints/policy_net_best.pt"
    plot_round_robin_matrix()
    plot_ablation_a1()
    plot_ablation_a2()
    plot_ablation_a3()
    plot_timed_rq1()
    plot_first_player_bias()
    plot_xai_saliency()


if __name__ == "__main__":
    main()
