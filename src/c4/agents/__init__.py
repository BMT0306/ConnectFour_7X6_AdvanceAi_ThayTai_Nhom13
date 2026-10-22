"""Registry tác tử: tạo agent theo tên (dùng trong CLI và giải đấu).

Khi thêm agent mới: viết lớp kế thừa Agent, rồi đăng ký vào AGENTS bên dưới.
"""
from __future__ import annotations

from typing import Callable

from c4.agents.base import Agent, Budget
from c4.agents.alphabeta import AlphaBetaAgent
from c4.agents.heuristic import HeuristicAgent
from c4.agents.mcts import MCTSAgent
from c4.agents.random_agent import RandomAgent

AGENTS: dict[str, Callable[..., Agent]] = {
    "random": RandomAgent,
    "heuristic": HeuristicAgent,  # cấp 2
    "alphabeta": AlphaBetaAgent,  # cấp 3
    "mcts": MCTSAgent,  # cấp 4
    # "nn": NNAgent,    # cấp 5  (TODO)
}


def make_agent(name: str, **kwargs) -> Agent:
    try:
        factory = AGENTS[name]
    except KeyError:
        raise KeyError(f"Agent '{name}' chưa đăng ký. Có sẵn: {sorted(AGENTS)}") from None
    return factory(**kwargs)


__all__ = ["Agent", "Budget", "RandomAgent", "HeuristicAgent", "AlphaBetaAgent", "MCTSAgent", "AGENTS", "make_agent"]
