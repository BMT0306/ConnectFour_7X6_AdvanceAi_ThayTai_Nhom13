"""Level 1 Agent: Random Baseline.

Picks uniformly from available legal actions.
Can be seeded for deterministic reproducibility.
"""

from __future__ import annotations
import random
import time
from typing import Optional, Any
from c4.agents.base import BaseAgent
from c4.game.engine import Bitboard


class RandomAgent(BaseAgent):
    """Uniform random baseline agent."""

    def __init__(self, name: str = "Random", seed: Optional[int] = None) -> None:
        super().__init__(name=name)
        self.rng = random.Random(seed)

    def choose_action(self, game: Bitboard, budget: Optional[Any] = None) -> int:
        start_time = time.perf_counter()
        legal = game.legal_actions()
        if not legal:
            raise ValueError("No legal actions available.")

        action = self.rng.choice(legal)
        self.stats["time_taken"] = time.perf_counter() - start_time
        self.stats["nodes_visited"] = 1
        return action
