"""Cấp 4 - MCTS với UCT: Selection - Expansion - Simulation - Backpropagation (cây nhiều tầng).

Mỗi nút lưu:
  N      : số lần thăm
  W      : tổng giá trị theo góc nhìn của bên VỪA ĐI vào nút này (thắng = 1, hòa = 0.5, thua = 0)
  untried: các nước chưa mở rộng
Chọn con theo UCB = W/N + C * sqrt(ln(N_cha) / N_con)  (C mặc định 1.4, xấp xỉ sqrt(2)).
Nước đi thật là con có SỐ LẦN THĂM lớn nhất.

rollout:
  "random" : mô phỏng bằng nước ngẫu nhiên đều (UCT chuẩn)
  "greedy" : mô phỏng có luật nhẹ - thắng ngay nếu có, nếu không thì ngẫu nhiên (dùng cho ablation)

Ngân sách: Budget.simulations (mặc định 1000) và/hoặc Budget.time_s (dừng khi hết giờ).
"""
from __future__ import annotations

import math
import time

from c4.agents.base import Agent, Budget
from c4.game.base import Connect4Base


class _Node:
    __slots__ = ("move", "parent", "mover", "children", "untried", "N", "W")

    def __init__(self, move, parent, mover, untried):
        self.move = move  # nước đi dẫn tới nút này (None ở gốc)
        self.parent = parent
        self.mover = mover  # bên vừa đi nước dẫn tới nút này
        self.children: list[_Node] = []
        self.untried = untried
        self.N = 0
        self.W = 0.0


class MCTSAgent(Agent):
    name = "mcts"

    def __init__(self, seed: int | None = None, default_simulations: int = 1000,
                 c: float = 1.4, rollout: str = "random") -> None:
        super().__init__(seed)
        if rollout not in ("random", "greedy"):
            raise ValueError("rollout phải là 'random' hoặc 'greedy'")
        self.default_simulations = default_simulations
        self.c = c
        self.rollout = rollout

    def _select_child(self, node: _Node) -> _Node:
        log_n = math.log(node.N)
        c = self.c
        best, best_u = None, -1.0
        for ch in node.children:
            u = ch.W / ch.N + c * math.sqrt(log_n / ch.N)
            if u > best_u:
                best, best_u = ch, u
        return best

    def _playout(self, g) -> None:
        rng = self.rng
        if self.rollout == "random":
            while not g.is_terminal():
                g.step(rng.choice(g.legal_actions()))
        else:
            while not g.is_terminal():
                wins = g.winning_moves()
                g.step(rng.choice(wins) if wins else rng.choice(g.legal_actions()))

    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        legal = game.legal_actions()
        if len(legal) == 1:
            self.last_stats = {"simulations": 0}
            return legal[0]
        max_sims = budget.simulations if budget and budget.simulations else None
        time_s = budget.time_s if budget else None
        if max_sims is None and time_s is None:
            max_sims = self.default_simulations
        deadline = time.perf_counter() + time_s if time_s is not None else None

        root = _Node(None, None, -game.current_player, list(legal))
        sims = 0
        while (max_sims is None or sims < max_sims):
            if deadline is not None and sims > 0 and (sims & 7) == 0 and time.perf_counter() > deadline:
                break
            g = game.clone()
            node = root
            # 1. Selection: đi xuống khi nút đã mở rộng hết các con
            while not node.untried and node.children:
                node = self._select_child(node)
                g.step(node.move)
            # 2. Expansion
            if node.untried and not g.is_terminal():
                idx = self.rng.randrange(len(node.untried))
                mv = node.untried.pop(idx)
                mover = g.current_player
                g.step(mv)
                child = _Node(mv, node, mover, [] if g.is_terminal() else g.legal_actions())
                node.children.append(child)
                node = child
            # 3. Simulation
            self._playout(g)
            w = g.winner
            # 4. Backpropagation
            while node is not None:
                node.N += 1
                node.W += 1.0 if node.mover == w else (0.5 if w == 0 else 0.0)
                node = node.parent
            sims += 1

        best = max(root.children, key=lambda ch: (ch.N, ch.W / ch.N))
        self.last_stats = {"simulations": sims, "best_visits": best.N, "best_value": best.W / best.N}
        return best.move
