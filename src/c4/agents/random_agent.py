"""Cấp 1 - Random: chọn đều trong các nước đi hợp lệ (baseline)."""
from __future__ import annotations

from c4.agents.base import Agent, Budget
from c4.game.base import Connect4Base


class RandomAgent(Agent):
    name = "random"

    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        timed_out = bool(budget and budget.time_s is not None and budget.time_s <= 0)
        self.last_stats = {"timed_out": timed_out, "fallback_random": False}
        return self.rng.choice(game.legal_actions())
