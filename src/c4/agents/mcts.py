"""Level 4 Agent: Monte Carlo Tree Search (MCTS) with UCT.

Four canonical phases:
1. Selection: Traverse down the tree using UCB1:
     UCB = W / N + C * sqrt(ln(N_parent) / N_child)
2. Expansion: When reaching a leaf with unvisited legal moves, expand a child node.
3. Simulation (Rollout): Play out the game to a terminal state using random moves.
4. Backpropagation: Update visit count N and cumulative reward W along the path.

Final decision selects the most-visited child (Robust Child).
Supports budget as either:
  - Integer: number of simulations (e.g. 1000)
  - Float: time budget in seconds (e.g. 0.3s)
"""

from __future__ import annotations
import math
import random
import time
from typing import Optional, Any, List, Dict
from c4.agents.base import BaseAgent
from c4.game.engine import Bitboard


class MCTSNode:
    """A node in the Monte Carlo search tree."""

    __slots__ = (
        "parent",
        "action",
        "player_who_moved",
        "visits",
        "total_reward",
        "children",
        "unexplored_actions",
    )

    def __init__(
        self,
        parent: Optional[MCTSNode] = None,
        action: Optional[int] = None,
        player_who_moved: Optional[int] = None,
        legal_actions: Optional[List[int]] = None,
    ) -> None:
        self.parent = parent
        self.action = action
        self.player_who_moved = player_who_moved
        self.visits: int = 0
        self.total_reward: float = 0.0
        self.children: Dict[int, MCTSNode] = {}
        self.unexplored_actions: List[int] = list(legal_actions) if legal_actions is not None else []

    def is_fully_expanded(self) -> bool:
        return len(self.unexplored_actions) == 0

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def best_child(self, c_param: float) -> MCTSNode:
        """Selects child with maximum UCB value."""
        log_parent = math.log(self.visits)
        best_score = -float("inf")
        best_node = None

        for child in self.children.values():
            if child.visits == 0:
                return child
            # Q is win-rate for player_who_moved into this child
            q = child.total_reward / child.visits
            u = c_param * math.sqrt(log_parent / child.visits)
            score = q + u
            if score > best_score:
                best_score = score
                best_node = child

        return best_node  # type: ignore


class MCTSAgent(BaseAgent):
    """Monte Carlo Tree Search agent using Upper Confidence Bounds for Trees (UCT)."""

    def __init__(
        self,
        name: str = "MCTS",
        num_simulations: int = 1000,
        c_param: float = 1.414,
        seed: Optional[int] = None,
    ) -> None:
        super().__init__(name=name)
        self.default_simulations = num_simulations
        self.c_param = c_param
        self.rng = random.Random(seed)

    def choose_action(self, game: Bitboard, budget: Optional[Any] = None) -> int:
        start_time = time.perf_counter()
        legal = game.legal_actions()
        if not legal:
            raise ValueError("No legal actions available.")
        if len(legal) == 1:
            self._record_stats(start_time, 1)
            return legal[0]

        # Instant winning move check (tactical short-circuit)
        for a in legal:
            if game.is_winning_move(a):
                self._record_stats(start_time, 1)
                return a

        # Determine budget mode
        is_time_budget = budget is not None and isinstance(budget, (int, float)) and budget < 20.0
        max_simulations = budget if (isinstance(budget, int) and budget >= 20) else self.default_simulations
        deadline = (start_time + budget) if is_time_budget else float("inf")

        root = MCTSNode(legal_actions=legal)
        sim_count = 0

        # We use a clone for tree search simulations
        sim_game = game.clone()

        while True:
            if is_time_budget:
                if sim_count & 63 == 0 and time.perf_counter() >= deadline:
                    break
            else:
                if sim_count >= max_simulations:
                    break

            self._run_simulation_round(sim_game, root)
            sim_count += 1

        # Select most visited child (Robust Child)
        best_action = max(root.children.items(), key=lambda item: item[1].visits)[0]
        self._record_stats(start_time, sim_count)
        return best_action

    def _run_simulation_round(self, game: Bitboard, root: MCTSNode) -> None:
        node = root
        moves_made: List[int] = []

        # 1. Selection
        while not node.is_leaf() and node.is_fully_expanded() and not game.is_terminal():
            node = node.best_child(self.c_param)
            game.step(node.action)
            moves_made.append(node.action)

        # 2. Expansion
        if not game.is_terminal() and not node.is_fully_expanded():
            action = node.unexplored_actions.pop()
            player_who_moved = game.current_player
            game.step(action)
            moves_made.append(action)

            child_node = MCTSNode(
                parent=node,
                action=action,
                player_who_moved=player_who_moved,
                legal_actions=game.legal_actions(),
            )
            node.children[action] = child_node
            node = child_node

        # 3. Simulation (Rollout)
        winner = self._rollout(game, moves_made)

        # 4. Backpropagation
        while node is not None:
            node.visits += 1
            if node.player_who_moved is not None:
                if winner == node.player_who_moved:
                    node.total_reward += 1.0
                elif winner == 0:
                    node.total_reward += 0.0
                else:
                    node.total_reward -= 1.0
            node = node.parent

        # Revert board back to root state via undo()
        for _ in range(len(moves_made)):
            game.undo()

    def _rollout(self, game: Bitboard, moves_made: List[int]) -> int:
        """Fast rollout to terminal state."""
        rollout_steps = 0
        while not game.is_terminal():
            legal = game.legal_actions()
            action = self.rng.choice(legal)
            game.step(action)
            moves_made.append(action)
            rollout_steps += 1

        return game.winner  # type: ignore

    def _record_stats(self, start_time: float, simulations: int) -> None:
        self.stats["time_taken"] = time.perf_counter() - start_time
        self.stats["nodes_visited"] = simulations
