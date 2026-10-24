"""Cấp 1 - Random: chọn đều trong các nước đi hợp lệ (baseline)."""
from __future__ import annotations

from c4.agents.base import Agent, Budget
from c4.game.base import Connect4Base


class RandomAgent(Agent):
    name = "random"

    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        self.last_stats = {}
        return self.rng.choice(game.legal_actions())
