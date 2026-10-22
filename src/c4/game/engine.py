"""Engine Connect Four bằng BITBOARD (nhanh, dùng cho Alpha-Beta / MCTS).

Biểu diễn: mỗi cột dùng 7 bit (6 ô + 1 bit đệm ở trên cùng), tổng 49 bit.
Bit của ô (cột c, hàng r) là  c*7 + r  (hàng 0 = dưới cùng).

  _pos  : các quân của bên ĐANG ĐẾN LƯỢT
  _mask : tất cả các quân đã thả
=> quân của đối thủ = _pos ^ _mask.

Kỹ thuật theo ý tưởng của Pascal Pons (đã tự cài đặt lại). Bản chậm, dễ đọc dùng để
đối chiếu nằm ở reference.py; hai bản được kiểm thử chéo trong tests/test_crosscheck.py.
"""
from __future__ import annotations

import operator

import numpy as np

from c4.game.base import COLS, ROWS, PLAYER1, PLAYER2, Connect4Base, IllegalMoveError

_H = ROWS + 1  # 7 bit mỗi cột (có 1 bit đệm để tránh nhảy cột khi dịch bit)
_BOTTOM = tuple(1 << (c * _H) for c in range(COLS))  # bit hàng 0 của từng cột
_COLMASK = tuple(((1 << ROWS) - 1) << (c * _H) for c in range(COLS))  # 6 bit hợp lệ của cột
_TOP = tuple(1 << (c * _H + ROWS - 1) for c in range(COLS))  # bit hàng 5 (trên cùng)
_FULL = ROWS * COLS


def _has_four(b: int) -> bool:
    """Có 4 quân liên tiếp trong bitboard b? (ngang, 2 đường chéo, dọc)."""
    m = b & (b >> _H)  # ngang
    if m & (m >> (2 * _H)):
        return True
    m = b & (b >> (_H - 1))  # chéo \
    if m & (m >> (2 * (_H - 1))):
        return True
    m = b & (b >> (_H + 1))  # chéo /
    if m & (m >> (2 * (_H + 1))):
        return True
    m = b & (b >> 1)  # dọc
    if m & (m >> 2):
        return True
    return False


class Connect4(Connect4Base):
    __slots__ = ("_pos", "_mask", "_moves", "_winner", "_history")

    def __init__(self) -> None:
        self.reset()

    # ---- trạng thái ----
    def reset(self) -> None:
        self._pos = 0
        self._mask = 0
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

    # ---- hành động ----
    def legal_actions(self) -> list[int]:
        if self._winner or self._moves == _FULL:
            return []
        mask = self._mask
        return [c for c in range(COLS) if not mask & _TOP[c]]

    def step(self, action: int) -> None:
        if self._winner or self._moves == _FULL:
            raise IllegalMoveError("Game đã kết thúc, không thể đi tiếp")
        try:
            col = operator.index(action)  # nhận cả numpy int, từ chối float/str
        except TypeError:
            raise IllegalMoveError(f"Nước đi phải là số nguyên, nhận được {action!r}") from None
        if not 0 <= col < COLS:
            raise IllegalMoveError(f"Cột {col} ngoài phạm vi 0..{COLS - 1}")
        if self._mask & _TOP[col]:
            raise IllegalMoveError(f"Cột {col} đã đầy")

        new = (self._mask + _BOTTOM[col]) & _COLMASK[col]  # bit ô trống thấp nhất của cột
        if _has_four(self._pos | new):
            self._winner = self.current_player  # tính TRƯỚC khi đổi lượt
        self._pos ^= self._mask  # đổi vai: _pos giờ là quân của bên đến lượt kế tiếp
        self._mask |= new
        self._moves += 1
        self._history.append(col)

    def undo(self) -> int:
        if not self._history:
            raise IllegalMoveError("Không có nước đi nào để hoàn tác")
        col = self._history.pop()
        top = 1 << ((self._mask & _COLMASK[col]).bit_length() - 1)  # quân trên cùng của cột
        self._mask ^= top
        self._pos ^= self._mask
        self._moves -= 1
        self._winner = 0
        return col

    def clone(self) -> "Connect4":
        g = Connect4.__new__(Connect4)
        g._pos = self._pos
        g._mask = self._mask
        g._moves = self._moves
        g._winner = self._winner
        g._history = self._history.copy()
        return g

    # ---- truy vấn chiến thuật ----
    def winning_moves(self, player: int | None = None) -> list[int]:
        if self.is_terminal():
            return []
        if player is None:
            player = self.current_player
        stones = self._pos if player == self.current_player else self._pos ^ self._mask
        res = []
        for c in range(COLS):
            if self._mask & _TOP[c]:
                continue
            new = (self._mask + _BOTTOM[c]) & _COLMASK[c]
            if _has_four(stones | new):
                res.append(c)
        return res

    # ---- biểu diễn ----
    def to_array(self, relative: bool = False) -> np.ndarray:
        cur, opp = self._pos, self._pos ^ self._mask
        p1, p2 = (cur, opp) if self._moves % 2 == 0 else (opp, cur)
        arr = np.zeros((ROWS, COLS), dtype=np.int8)
        for c in range(COLS):
            for r in range(ROWS):
                bit = 1 << (c * _H + r)
                if p1 & bit:
                    arr[r, c] = 1
                elif p2 & bit:
                    arr[r, c] = -1
        if relative and self.current_player == PLAYER2:
            arr = -arr
        return arr

    def key(self) -> int:
        """Duy nhất cho mỗi vị trí: (quân bên đến lượt, tất cả quân) gói vào một số nguyên."""
        return (self._pos << 49) | self._mask

    def bitboards(self) -> tuple[int, int]:
        """(quân bên đang đến lượt, quân đối thủ) dưới dạng bitboard - dành cho hàm lượng giá nhanh.

        CHỈ có ở engine bitboard (không thuộc API chung). Bit của ô (cột c, hàng r) là c*7 + r.
        """
        return self._pos, self._pos ^ self._mask

    @property
    def history(self) -> tuple[int, ...]:
        """Chuỗi cột đã đi (chỉ đọc) - tiện cho log và debug."""
        return tuple(self._history)
