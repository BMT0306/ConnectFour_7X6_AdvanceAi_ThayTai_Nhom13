"""Engine THAM CHIẾU: chậm nhưng cực kỳ dễ đọc (mảng 2 chiều + kiểm tra thắng bằng vòng lặp).

Chỉ dùng để (1) kiểm thử chéo engine bitboard, (2) để cả nhóm đọc hiểu luật.
Tuyệt đối không dùng cho Alpha-Beta/MCTS vì chậm.
"""
from __future__ import annotations

import operator

import numpy as np

from c4.game.base import COLS, ROWS, PLAYER1, PLAYER2, Connect4Base, IllegalMoveError

_DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))  # ngang, dọc, chéo /, chéo \  (dr, dc)


class ReferenceConnect4(Connect4Base):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._grid = [[0] * COLS for _ in range(ROWS)]  # _grid[hàng][cột], hàng 0 = dưới cùng
        self._heights = [0] * COLS
        self._moves = 0
        self._winner = 0
        self._history: list[int] = []

    @property
    def current_player(self) -> int:
        return PLAYER1 if self._moves % 2 == 0 else PLAYER2

    @property
    def winner(self) -> int:
        return self._winner

    @property
    def move_count(self) -> int:
        return self._moves

    def _is_over(self) -> bool:
        return self._winner != 0 or self._moves == ROWS * COLS

    def legal_actions(self) -> list[int]:
        if self._is_over():
            return []
        return [c for c in range(COLS) if self._heights[c] < ROWS]

    def _makes_four(self, r: int, c: int, player: int) -> bool:
        """Nếu `player` có quân ở (r, c), có đường 4 đi qua ô đó không?"""
        for dr, dc in _DIRECTIONS:
            count = 1
            for sign in (1, -1):
                rr, cc = r + sign * dr, c + sign * dc
                while 0 <= rr < ROWS and 0 <= cc < COLS and self._grid[rr][cc] == player:
                    count += 1
                    rr += sign * dr
                    cc += sign * dc
            if count >= 4:
                return True
        return False

    def step(self, action: int) -> None:
        if self._is_over():
            raise IllegalMoveError("Game đã kết thúc, không thể đi tiếp")
        try:
            col = operator.index(action)
        except TypeError:
            raise IllegalMoveError(f"Nước đi phải là số nguyên, nhận được {action!r}") from None
        if not 0 <= col < COLS:
            raise IllegalMoveError(f"Cột {col} ngoài phạm vi 0..{COLS - 1}")
        if self._heights[col] >= ROWS:
            raise IllegalMoveError(f"Cột {col} đã đầy")
        player = self.current_player
        row = self._heights[col]
        self._grid[row][col] = player
        self._heights[col] += 1
        self._moves += 1
        self._history.append(col)
        if self._makes_four(row, col, player):
            self._winner = player

    def undo(self) -> int:
        if not self._history:
            raise IllegalMoveError("Không có nước đi nào để hoàn tác")
        col = self._history.pop()
        self._heights[col] -= 1
        self._grid[self._heights[col]][col] = 0
        self._moves -= 1
        self._winner = 0
        return col

    def clone(self) -> "ReferenceConnect4":
        g = ReferenceConnect4.__new__(ReferenceConnect4)
        g._grid = [row.copy() for row in self._grid]
        g._heights = self._heights.copy()
        g._moves = self._moves
        g._winner = self._winner
        g._history = self._history.copy()
        return g

    def winning_moves(self, player: int | None = None) -> list[int]:
        if self._is_over():
            return []
        if player is None:
            player = self.current_player
        res = []
        for c in range(COLS):
            if self._heights[c] >= ROWS:
                continue
            r = self._heights[c]
            self._grid[r][c] = player  # đặt thử
            if self._makes_four(r, c, player):
                res.append(c)
            self._grid[r][c] = 0  # gỡ ra
        return res

    def to_array(self, relative: bool = False) -> np.ndarray:
        arr = np.array(self._grid, dtype=np.int8)
        if relative and self.current_player == PLAYER2:
            arr = -arr
        return arr

    def key(self):
        return tuple(v for row in self._grid for v in row)
