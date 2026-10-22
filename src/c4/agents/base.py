"""Giao diện chung cho MỌI tác tử (Random, Heuristic, Alpha-Beta, MCTS, NN...)."""
from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

from c4.game.base import Connect4Base


@dataclass(frozen=True)
class Budget:
    """Ngân sách tính toán cho MỘT nước đi. Trường nào là None nghĩa là 'không giới hạn theo trường đó'.

    * time_s      : thời gian tối đa (giây)  -> dùng cho giải đấu chế độ A (cùng thời gian/nước)
    * simulations : số mô phỏng tối đa (MCTS)
    * depth       : độ sâu tối đa (Alpha-Beta)
    Mỗi tác tử tự quyết định dùng trường nào; trường không dùng thì bỏ qua.
    """

    time_s: float | None = None
    simulations: int | None = None
    depth: int | None = None


class Agent(ABC):
    """Mọi tác tử kế thừa lớp này.

    Quy tắc:
      * choose_action() KHÔNG được sửa `game` gốc (giải đấu đã truyền bản clone, nhưng hãy tự giác).
      * Luôn trả về một cột nằm trong game.legal_actions().
      * Mọi ngẫu nhiên phải đi qua self.rng (khởi tạo bằng seed) để tái lập được.
      * Sau mỗi nước, đặt self.last_stats (ví dụ {"nodes": 1234} hoặc {"simulations": 500}).
    """

    name = "agent"

    def __init__(self, seed: int | None = None) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.last_stats: dict = {}

    def reset(self) -> None:
        """Gọi đầu mỗi ván (xóa cache/cây tìm kiếm cũ nếu có)."""

    @abstractmethod
    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        """Chọn một cột hợp lệ cho bên đang đến lượt."""
