"""API chung của game Connect Four (7 cột x 6 hàng).

Quy ước (CẢ NHÓM PHẢI THỐNG NHẤT, đừng tự đổi):
  * Cột đánh số từ 0..6 trong code (giao diện hiển thị 1..7).
  * Hàng 0 là hàng DƯỚI CÙNG của bàn cờ (quân rơi từ trên xuống nằm ở hàng thấp nhất còn trống).
  * PLAYER1 = +1 là bên đi TRƯỚC (Đỏ, ký hiệu 'X'); PLAYER2 = -1 là bên đi sau (Vàng, ký hiệu 'O').
  * result(player) trả về +1 thắng, 0 hòa, -1 thua THEO GÓC NHÌN của `player`.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

ROWS = 6
COLS = 7
PLAYER1 = 1
PLAYER2 = -1

# Thứ tự duyệt nước đi từ giữa ra (dùng cho move ordering, Heuristic).
CENTER_FIRST = (3, 2, 4, 1, 5, 0, 6)


class IllegalMoveError(ValueError):
    """Nước đi bất hợp lệ (cột đầy, ngoài phạm vi, game đã kết thúc...)."""


class Connect4Base(ABC):
    """Giao diện mà mọi engine (bitboard, bản tham chiếu) đều phải tuân theo."""

    # ---- trạng thái ----
    @abstractmethod
    def reset(self) -> None:
        """Đưa game về bàn cờ trống, PLAYER1 đi trước."""

    @property
    @abstractmethod
    def current_player(self) -> int:
        """PLAYER1 (+1) hoặc PLAYER2 (-1): bên đang đến lượt."""

    @property
    @abstractmethod
    def winner(self) -> int:
        """+1 / -1 nếu đã có người thắng, 0 nếu chưa có (hoặc hòa)."""

    @property
    @abstractmethod
    def move_count(self) -> int:
        """Số quân đã thả (0..42)."""

    # ---- hành động ----
    @abstractmethod
    def legal_actions(self) -> list[int]:
        """Danh sách cột hợp lệ (tăng dần). Rỗng nếu game đã kết thúc."""

    @abstractmethod
    def step(self, action: int) -> None:
        """Thả quân vào cột `action`. Ném IllegalMoveError nếu bất hợp lệ."""

    @abstractmethod
    def undo(self) -> int:
        """Hoàn tác nước đi gần nhất, trả về cột đã hoàn tác."""

    @abstractmethod
    def clone(self) -> "Connect4Base":
        """Bản sao độc lập (không dùng deepcopy)."""

    # ---- kết thúc ----
    def is_terminal(self) -> bool:
        return self.winner != 0 or self.move_count == ROWS * COLS

    def result(self, player: int = PLAYER1) -> int:
        """+1 thắng / 0 hòa / -1 thua theo góc nhìn của `player`. Chỉ gọi khi đã kết thúc."""
        if not self.is_terminal():
            raise ValueError("result() chỉ dùng được khi game đã kết thúc")
        return self.winner * player

    # ---- truy vấn chiến thuật ----
    @abstractmethod
    def winning_moves(self, player: int | None = None) -> list[int]:
        """Các cột mà `player` (mặc định: bên đang đến lượt) thả vào sẽ có ngay 4 quân liên tiếp.

        Dùng được cho CẢ bên không đến lượt (để phát hiện cần chặn). Không thay đổi trạng thái.
        """

    # ---- biểu diễn ----
    @abstractmethod
    def to_array(self, relative: bool = False) -> np.ndarray:
        """Mảng int8 shape (6, 7), hàng 0 = dưới cùng; +1 quân PLAYER1, -1 quân PLAYER2.

        relative=True: nhân dấu sao cho +1 luôn là quân của bên đang đến lượt.
        """

    @abstractmethod
    def key(self):
        """Khóa duy nhất của vị trí (hashable) - dùng để loại trùng, bảng chuyển vị."""

    def encode(self) -> np.ndarray:
        """Đầu vào cho mạng NN: float32 shape (2, 6, 7) = [quân của bên đến lượt, quân đối thủ]."""
        arr = self.to_array(relative=True)
        return np.stack([(arr == 1), (arr == -1)]).astype(np.float32)

    def render(self) -> str:
        """Bàn cờ dạng văn bản: X = PLAYER1, O = PLAYER2, '.' = trống; cột hiển thị 1..7."""
        arr = self.to_array()
        sym = {1: "X", -1: "O", 0: "."}
        lines = [" ".join(sym[int(v)] for v in arr[r]) for r in range(ROWS - 1, -1, -1)]
        lines.append(" ".join(str(c + 1) for c in range(COLS)))
        return "\n".join(lines)

    def __repr__(self) -> str:  # tiện khi debug
        return f"<{type(self).__name__} moves={self.move_count} to_move={self.current_player:+d}>\n{self.render()}"
