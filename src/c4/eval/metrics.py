"""Thống kê cho giải đấu: score, khoảng tin cậy Wilson / bootstrap, phân vị thời gian."""
from __future__ import annotations

from math import sqrt

import numpy as np


def score(wins: int, draws: int, losses: int) -> float:
    """score = (thắng + 0,5 x hòa) / tổng số ván."""
    n = wins + draws + losses
    return float("nan") if n == 0 else (wins + 0.5 * draws) / n


def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Khoảng tin cậy Wilson (mặc định 95%) cho một tỷ lệ nhị phân (vd tỷ lệ thắng)."""
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def bootstrap_score_ci(
    results: list[int], n_boot: int = 10000, alpha: float = 0.05, seed: int = 0
) -> tuple[float, float]:
    """Khoảng tin cậy bootstrap cho score. `results`: mỗi ván là +1 (thắng), 0 (hòa), -1 (thua)."""
    arr = (np.asarray(results, dtype=float) + 1) / 2  # +1 -> 1.0, 0 -> 0.5, -1 -> 0.0
    if arr.size == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, arr.size, size=(n_boot, arr.size))
    means = arr[idx].mean(axis=1)
    return (float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))


def summarize(results: list[int], seed: int = 0) -> dict:
    """Tóm tắt kết quả của MỘT tác tử: results là +1/0/-1 theo góc nhìn tác tử đó."""
    w = sum(1 for r in results if r > 0)
    d = sum(1 for r in results if r == 0)
    l = sum(1 for r in results if r < 0)
    n = len(results)
    wl, wh = wilson_interval(w, n)
    bl, bh = bootstrap_score_ci(results, seed=seed)
    return {
        "n": n, "wins": w, "draws": d, "losses": l,
        "win_rate": w / n if n else float("nan"),
        "win_rate_wilson_low": wl, "win_rate_wilson_high": wh,
        "score": score(w, d, l),
        "score_boot_low": bl, "score_boot_high": bh,
    }


def percentile(values: list[float], q: float) -> float:
    """Phân vị q (0..100) của danh sách; vd q=95 cho độ trễ p95."""
    return float("nan") if len(values) == 0 else float(np.percentile(values, q))
