"""Chạy ván đấu và trận đấu (nhiều ván, có khai cuộc ngẫu nhiên + đổi bên).

Thiết kế công bằng:
  * Mỗi khai cuộc (vài nước đầu ngẫu nhiên theo seed) được chơi ở CẢ HAI chiều đổi bên.
  * Nước đi trong khai cuộc là bắt buộc, KHÔNG tính thời gian và không do agent chọn.
  * Thời gian mỗi nước đo bằng time.perf_counter, không tính chi phí clone().
"""
from __future__ import annotations

import csv
import json
import random
import time
from dataclasses import dataclass, field
from typing import Callable

from c4.agents.base import Agent, Budget
from c4.game.base import PLAYER1, Connect4Base
from c4.game.engine import Connect4


@dataclass
class GameRecord:
    opening: tuple[int, ...]
    moves: list[int]  # toàn bộ chuỗi cột, gồm cả khai cuộc
    winner: int  # +1 bên đi trước thắng, -1 bên đi sau thắng, 0 hòa
    times_first: list[float] = field(default_factory=list)  # giây/nước của bên đi trước
    times_second: list[float] = field(default_factory=list)
    stats_first: list[dict] = field(default_factory=list)
    stats_second: list[dict] = field(default_factory=list)


def generate_openings(n: int, plies: int = 4, seed: int = 0) -> list[tuple[int, ...]]:
    """n khai cuộc KHÁC NHAU, mỗi cái `plies` nước ngẫu nhiên hợp lệ, chưa kết thúc game."""
    rng = random.Random(seed)
    seen: set[tuple[int, ...]] = set()
    out: list[tuple[int, ...]] = []
    attempts = 0
    while len(out) < n:
        attempts += 1
        if attempts > 200 * n + 1000:
            raise ValueError(f"Không đủ {n} khai cuộc khác nhau với plies={plies}")
        g = Connect4()
        seq: list[int] = []
        for _ in range(plies):
            c = rng.choice(g.legal_actions())
            g.step(c)
            seq.append(c)
        if g.is_terminal():
            continue
        t = tuple(seq)
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def play_game(
    first: Agent,
    second: Agent,
    opening: tuple[int, ...] = (),
    budget_first: Budget | None = None,
    budget_second: Budget | None = None,
    game_factory: Callable[[], Connect4Base] = Connect4,
    timeout_policy: str = "best_or_random",
    fallback_seed: int = 0,
) -> GameRecord:
    """Một ván: `first` cầm PLAYER1 (đi trước), `second` cầm PLAYER2.

    `timeout_policy`:
      * "none"           : không can thiệp khi vượt giờ (agent đi sai vẫn ném IllegalMoveError).
      * "best_or_random" : ưu tiên nước tạm tốt nhất trước deadline do agent tự trả về; nếu hết giờ
                           mà agent chưa kịp chọn hoặc vượt quá ngưỡng cứng thì fallback random hợp lệ.
      * "strict_random"  : hễ vượt `budget.time_s` là hủy nước đi và ép chọn random hợp lệ.
    """
    if timeout_policy not in ("none", "best_or_random", "strict_random"):
        raise ValueError(f"timeout_policy không hợp lệ: {timeout_policy}")
    fallback_rng = random.Random(fallback_seed)
    g = game_factory()
    for m in opening:
        g.step(m)
    first.reset()
    second.reset()
    rec = GameRecord(opening=tuple(opening), moves=list(opening), winner=0)
    while not g.is_terminal():
        if g.current_player == PLAYER1:
            agent, budget, times, stats = first, budget_first, rec.times_first, rec.stats_first
        else:
            agent, budget, times, stats = second, budget_second, rec.times_second, rec.stats_second
        view = g.clone()
        t0 = time.perf_counter()
        action = agent.choose_action(view, budget)
        elapsed = time.perf_counter() - t0
        move_stats = dict(agent.last_stats)

        if timeout_policy != "none" and budget is not None and budget.time_s is not None:
            legal = g.legal_actions()
            limit_s = budget.time_s
            hard_limit_s = limit_s + max(0.05, limit_s * 0.5)
            over_soft = elapsed > limit_s
            over_hard = elapsed > hard_limit_s

            if timeout_policy == "strict_random" and over_soft:
                action = fallback_rng.choice(legal)
                move_stats["timed_out"] = True
                move_stats["fallback_random"] = True
                move_stats["hard_timeout_override"] = True
            elif timeout_policy == "best_or_random":
                if over_hard and not move_stats.get("timed_out", False):
                    action = fallback_rng.choice(legal)
                    move_stats["timed_out"] = True
                    move_stats["fallback_random"] = True
                    move_stats["hard_timeout_override"] = True
                elif over_soft:
                    move_stats["timed_out"] = True
                    move_stats.setdefault("fallback_random", False)
                else:
                    move_stats.setdefault("timed_out", False)
                    move_stats.setdefault("fallback_random", False)

        times.append(elapsed)
        stats.append(move_stats)
        g.step(action)  # IllegalMoveError nếu agent chọn sai -> lỗi rõ ràng, không im lặng
        rec.moves.append(action)
    rec.winner = g.winner
    return rec


@dataclass
class MatchRecord:
    pair: str
    opening_id: int
    opening: tuple[int, ...]
    a_first: bool
    winner: int  # theo màu: +1 bên đi trước, -1 bên đi sau, 0 hòa
    a_result: int  # +1 A thắng, 0 hòa, -1 A thua
    plies: int
    a_times: list[float]
    b_times: list[float]
    a_stats: list[dict]
    b_stats: list[dict]


def run_match(
    a: Agent,
    b: Agent,
    openings: list[tuple[int, ...]],
    budget_a: Budget | None = None,
    budget_b: Budget | None = None,
    pair: str | None = None,
    timeout_policy: str = "best_or_random",
) -> list[MatchRecord]:
    """Mỗi khai cuộc chơi 2 ván (A đi trước, rồi B đi trước) => 2 x len(openings) ván."""
    pair = pair or f"{a.name}_vs_{b.name}"
    out: list[MatchRecord] = []
    for i, op in enumerate(openings):
        for a_first in (True, False):
            fb_seed = i * 2 + (0 if a_first else 1)
            if a_first:
                rec = play_game(a, b, op, budget_a, budget_b, timeout_policy=timeout_policy, fallback_seed=fb_seed)
                a_times, b_times = rec.times_first, rec.times_second
                a_stats, b_stats = rec.stats_first, rec.stats_second
                a_result = rec.winner
            else:
                rec = play_game(b, a, op, budget_b, budget_a, timeout_policy=timeout_policy, fallback_seed=fb_seed)
                a_times, b_times = rec.times_second, rec.times_first
                a_stats, b_stats = rec.stats_second, rec.stats_first
                a_result = -rec.winner
            out.append(
                MatchRecord(pair, i, op, a_first, rec.winner, a_result, len(rec.moves),
                            a_times, b_times, a_stats, b_stats)
            )
    return out


CSV_FIELDS = ["pair", "opening_id", "opening", "a_first", "winner", "a_result", "plies",
              "a_times_s", "b_times_s", "a_stats", "b_stats"]


def save_records_csv(records: list[MatchRecord], path: str) -> None:
    """Lưu LOG THÔ mức ván (kèm thời gian/stats từng nước dạng JSON) để dựng bảng/hình sau này."""
    import os

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in records:
            w.writerow({
                "pair": r.pair, "opening_id": r.opening_id,
                "opening": " ".join(map(str, r.opening)), "a_first": int(r.a_first),
                "winner": r.winner, "a_result": r.a_result, "plies": r.plies,
                "a_times_s": json.dumps([round(t, 6) for t in r.a_times]),
                "b_times_s": json.dumps([round(t, 6) for t in r.b_times]),
                "a_stats": json.dumps(r.a_stats), "b_stats": json.dumps(r.b_stats),
            })
