"""Level 2 Agent: Rule-Based / Heuristic Agent.

Strict priority rules:
1. Win immediately: If any legal move connects 4, play it.
2. Block opponent: If opponent can win next turn in any column, block it.
3. Avoid blunder: Exclude moves that allow the opponent to win immediately above.
4. Center control: Among remaining candidate moves, prioritize columns [3, 2, 4, 1, 5, 0, 6].
5. Conflict resolution: If all moves give the opponent a win above, pick the least-bad move by center order.
"""

from __future__ import annotations
import time
from typing import Optional, Any, List
from c4.agents.base import BaseAgent
from c4.game.engine import Bitboard, check_win


class HeuristicAgent(BaseAgent):
    """Rule-based priority agent with tactical look-ahead."""

    # 0-indexed center-outwards preference: col 3 (center), then 2, 4, 1, 5, 0, 6
    CENTER_PREFERENCE: List[int] = [3, 2, 4, 1, 5, 0, 6]

    def __init__(self, name: str = "Heuristic") -> None:
        super().__init__(name=name)

    def choose_action(self, game: Bitboard, budget: Optional[Any] = None) -> int:
        start_time = time.perf_counter()
        legal = game.legal_actions()
        if not legal:
            raise ValueError("No legal actions available.")

        nodes = 0

        # Rule 1: Win immediately
        for action in legal:
            nodes += 1
            if game.is_winning_move(action):
                self._record_stats(start_time, nodes)
                return action

        # Rule 2: Block immediate opponent win
        for action in legal:
            nodes += 1
            if game.is_opponent_winning_move(action):
                self._record_stats(start_time, nodes)
                return action

        # Rule 3: Filter out suicidal moves (moves that hand opponent a win right above)
        safe_actions = []
        opp_idx = 1 if game.current_player == 1 else 0
        opp_bb = game.bitboards[opp_idx]

        for action in legal:
            nodes += 1
            # Next cell in this column if we play here
            next_height = game.heights[action] + 1
            guard_bit = game.GUARD_BITS[action]
            if next_height < guard_bit:
                cell_above_bit = 1 << next_height
                # If opponent placing a piece at cell_above_bit would win:
                if check_win(opp_bb | cell_above_bit):
                    # Dangerous move: skip
                    continue
            safe_actions.append(action)

        # Rule 4: Pick center-most action from safe candidates
        candidates = safe_actions if safe_actions else legal
        for col in self.CENTER_PREFERENCE:
            if col in candidates:
                self._record_stats(start_time, nodes)
                return col

        # Fallback (should never be reached)
        action = candidates[0]
        self._record_stats(start_time, nodes)
        return action

    def _record_stats(self, start_time: float, nodes: int) -> None:
        self.stats["time_taken"] = time.perf_counter() - start_time
        self.stats["nodes_visited"] = nodes
