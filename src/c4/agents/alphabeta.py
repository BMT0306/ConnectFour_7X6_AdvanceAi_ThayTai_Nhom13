"""Level 3 Agent: Minimax with Alpha-Beta Pruning.

Features:
- Negamax formulation with depth-adjusted terminal scores (prefers faster wins).
- Ultra-fast Bitboard heuristic evaluator precomputing all 69 winning 4-cell windows.
- Center-outwards move ordering [3, 2, 4, 1, 5, 0, 6] to maximize cutoffs.
- Iterative Deepening with strict wall-clock time budget enforcement.
- Configurable ablation flags:
  * `use_pruning` (toggle Alpha-Beta cutoff on/off for Ablation A1)
  * `use_ordering` (toggle center move ordering)
  * `use_heuristic` (toggle heuristic evaluation vs 0-leaf payoff for Ablation A3)
"""

from __future__ import annotations
import time
from typing import Optional, Any, List, Tuple
from c4.agents.base import BaseAgent
from c4.game.engine import Bitboard, check_win

WIN_SCORE = 100_000


def _generate_windows_49bit() -> List[int]:
    """Generates 49-bit masks for all 69 possible 4-in-a-row windows."""
    windows = []
    # 1. Horizontal (24 windows: 6 rows x 4 col offsets)
    for r in range(6):
        for c in range(4):
            mask = 0
            for dc in range(4):
                mask |= 1 << ((c + dc) * 7 + r)
            windows.append(mask)

    # 2. Vertical (21 windows: 7 cols x 3 row offsets)
    for c in range(7):
        for r in range(3):
            mask = 0
            for dr in range(4):
                mask |= 1 << (c * 7 + (r + dr))
            windows.append(mask)

    # 3. Diagonal positive slope / (12 windows)
    for r in range(3):
        for c in range(4):
            mask = 0
            for d in range(4):
                mask |= 1 << ((c + d) * 7 + (r + d))
            windows.append(mask)

    # 4. Diagonal negative slope \ (12 windows)
    for r in range(3, 6):
        for c in range(4):
            mask = 0
            for d in range(4):
                mask |= 1 << ((c + d) * 7 + (r - d))
            windows.append(mask)

    assert len(windows) == 69, f"Expected 69 windows, got {len(windows)}"
    return windows


# Precomputed static windows & center mask
ALL_WINDOWS = _generate_windows_49bit()
CENTER_COL_MASK = sum(1 << (3 * 7 + r) for r in range(6))


def evaluate_bitboard(my_bb: int, opp_bb: int) -> int:
    """Evaluates position for player with `my_bb` relative to `opp_bb`."""
    score = 0

    # Center column control bonus
    center_my = (my_bb & CENTER_COL_MASK).bit_count()
    center_opp = (opp_bb & CENTER_COL_MASK).bit_count()
    score += (center_my - center_opp) * 6

    # 69 winning window evaluation
    for w in ALL_WINDOWS:
        my_cnt = (my_bb & w).bit_count()
        opp_cnt = (opp_bb & w).bit_count()

        if my_cnt > 0 and opp_cnt == 0:
            if my_cnt == 3:
                score += 50
            elif my_cnt == 2:
                score += 10
            elif my_cnt == 1:
                score += 1
        elif opp_cnt > 0 and my_cnt == 0:
            if opp_cnt == 3:
                score -= 50
            elif opp_cnt == 2:
                score -= 10
            elif opp_cnt == 1:
                score -= 1

    return score


class AlphaBetaAgent(BaseAgent):
    """Negamax Alpha-Beta search agent."""

    CENTER_ORDER: List[int] = [3, 2, 4, 1, 5, 0, 6]

    def __init__(
        self,
        name: str = "AlphaBeta",
        depth: int = 5,
        use_pruning: bool = True,
        use_ordering: bool = True,
        use_heuristic: bool = True,
    ) -> None:
        super().__init__(name=name)
        self.default_depth = depth
        self.use_pruning = use_pruning
        self.use_ordering = use_ordering
        self.use_heuristic = use_heuristic

        self._nodes_visited: int = 0
        self._deadline: float = float("inf")
        self._time_exceeded: bool = False

    def choose_action(self, game: Bitboard, budget: Optional[Any] = None) -> int:
        start_time = time.perf_counter()
        legal = game.legal_actions()
        if not legal:
            raise ValueError("No legal actions available.")
        if len(legal) == 1:
            self._record_stats(start_time, 1, 1)
            return legal[0]

        # Instant check for winning move
        for a in legal:
            if game.is_winning_move(a):
                self._record_stats(start_time, 1, 1)
                return a

        self._nodes_visited = 0
        self._time_exceeded = False

        if budget is not None and isinstance(budget, (int, float)) and budget < 20.0:
            # Budget treated as time limit in seconds (Iterative Deepening)
            self._deadline = start_time + budget
            best_action, max_depth_completed = self._iterative_deepening(game, legal)
            self._record_stats(start_time, self._nodes_visited, max_depth_completed)
            return best_action
        else:
            # Fixed depth budget
            target_depth = budget if isinstance(budget, int) and budget >= 1 else self.default_depth
            self._deadline = float("inf")
            best_action, _ = self._root_search(game, target_depth)
            self._record_stats(start_time, self._nodes_visited, target_depth)
            return best_action

    def _iterative_deepening(self, game: Bitboard, legal: List[int]) -> Tuple[int, int]:
        best_action = legal[0]
        completed_depth = 1

        for depth in range(1, 43):
            action, score = self._root_search(game, depth)
            if self._time_exceeded:
                break
            best_action = action
            completed_depth = depth
            # Stop if decisive forced win found
            if abs(score) >= WIN_SCORE - 100:
                break

        return best_action, completed_depth

    def _get_ordered_moves(self, legal: List[int]) -> List[int]:
        if not self.use_ordering:
            return legal
        return [c for c in self.CENTER_ORDER if c in legal]

    def _root_search(self, game: Bitboard, depth: int) -> Tuple[int, int]:
        ordered = self._get_ordered_moves(game.legal_actions())
        best_action = ordered[0]
        alpha = -float("inf")
        beta = float("inf")

        for action in ordered:
            game.step(action)
            # From next player's viewpoint, score is negated
            val = -self._negamax(game, depth - 1, -beta, -alpha, ply=1)
            game.undo()

            if self._time_exceeded:
                return best_action, alpha

            if val > alpha:
                alpha = val
                best_action = action

            if self.use_pruning and alpha >= beta:
                break

        return best_action, alpha

    def _negamax(self, game: Bitboard, depth: int, alpha: float, beta: float, ply: int) -> float:
        self._nodes_visited += 1

        if self._nodes_visited & 1023 == 0:
            if time.perf_counter() >= self._deadline:
                self._time_exceeded = True
                return alpha

        if game.is_terminal():
            # Check who won
            if game.winner == 0:
                return 0.0
            # Current player is facing a state where previous player won
            return -float(WIN_SCORE - ply)

        if depth <= 0:
            if not self.use_heuristic:
                return 0.0
            p_idx = 0 if game.current_player == 1 else 1
            opp_idx = 1 - p_idx
            return float(evaluate_bitboard(game.bitboards[p_idx], game.bitboards[opp_idx]))

        ordered = self._get_ordered_moves(game.legal_actions())
        max_val = -float("inf")

        for action in ordered:
            game.step(action)
            val = -self._negamax(game, depth - 1, -beta, -alpha, ply + 1)
            game.undo()

            if self._time_exceeded:
                return alpha

            if val > max_val:
                max_val = val
            if val > alpha:
                alpha = val

            if self.use_pruning and alpha >= beta:
                break  # Cutoff

        return max_val

    def _record_stats(self, start_time: float, nodes: int, depth: int) -> None:
        self.stats["time_taken"] = time.perf_counter() - start_time
        self.stats["nodes_visited"] = nodes
        self.stats["depth_reached"] = depth
