"""High-performance Bitboard implementation of Connect Four (7x6).

Each column has 6 board rows and 1 guard row (7 bits total).
The whole 7x6 board is represented using 49 bits across two integers
(one for Player 1 / Red, one for Player 2 / Yellow).

Bit index for (row, col) is `col * 7 + row`:
  - row 0: bottom row
  - row 5: top playable row
  - row 6: guard bit (always 0, prevents wrapping across columns)

Win detection is performed in 4 directions using single-cycle bitwise shifts:
  - Vertical: shift 1
  - Horizontal: shift 7
  - Diagonal \\: shift 6 (r-1, c+1)
  - Diagonal /: shift 8 (r+1, c+1)
"""

from __future__ import annotations
from typing import List, Optional, Tuple
import numpy as np


def check_win(bb: int) -> bool:
    """Checks if bitboard `bb` contains 4 connected pieces in any direction.
    
    Single-instruction bitwise tests:
      1. Horizontal: shift 7
      2. Diagonal \\: shift 6
      3. Diagonal /: shift 8
      4. Vertical:   shift 1
    """
    # Horizontal
    m = bb & (bb >> 7)
    if m & (m >> 14):
        return True
    # Diagonal \
    m = bb & (bb >> 6)
    if m & (m >> 12):
        return True
    # Diagonal /
    m = bb & (bb >> 8)
    if m & (m >> 16):
        return True
    # Vertical
    m = bb & (bb >> 1)
    if m & (m >> 2):
        return True
    return False


class Bitboard:
    """Connect Four 7x6 Game Engine using 49-bit Bitboards."""

    ROWS: int = 6
    COLS: int = 7
    CONNECT: int = 4
    TOTAL_CELLS: int = 42

    # Column base bit offsets: col * 7
    COL_BASES: Tuple[int, ...] = (0, 7, 14, 21, 28, 35, 42)
    # Column guard bit positions: col * 7 + 6
    GUARD_BITS: Tuple[int, ...] = (6, 13, 20, 27, 34, 41, 48)
    # Default exploration order: center outwards for better move ordering
    EXPLORATION_ORDER: Tuple[int, ...] = (3, 2, 4, 1, 5, 0, 6)

    def __init__(self) -> None:
        self.bitboards: List[int] = [0, 0]  # [0]: Player 1 (Red), [1]: Player 2 (Yellow)
        self.heights: List[int] = list(self.COL_BASES)  # Next available bit index per column
        self.current_player: int = 1         # 1 or 2
        self.move_count: int = 0
        self.history: List[Tuple[int, int, int]] = []  # (action, bit, prev_player)
        self.winner: Optional[int] = None              # 1, 2, 0 (draw), or None

    def reset(self) -> Bitboard:
        """Resets the board to an empty state."""
        self.bitboards[0] = 0
        self.bitboards[1] = 0
        self.heights = list(self.COL_BASES)
        self.current_player = 1
        self.move_count = 0
        self.history.clear()
        self.winner = None
        return self

    def clone(self) -> Bitboard:
        """Fast cloning without deepcopy overhead."""
        b = Bitboard.__new__(Bitboard)
        b.bitboards = [self.bitboards[0], self.bitboards[1]]
        b.heights = list(self.heights)
        b.current_player = self.current_player
        b.move_count = self.move_count
        b.history = list(self.history)
        b.winner = self.winner
        return b

    def legal_actions(self) -> List[int]:
        """Returns list of valid column indices [0..6] that are not full."""
        if self.winner is not None:
            return []
        return [c for c in range(self.COLS) if self.heights[c] < self.GUARD_BITS[c]]

    def is_legal(self, action: int) -> bool:
        """Checks if a column move is legal."""
        return (
            0 <= action < self.COLS
            and self.winner is None
            and self.heights[action] < self.GUARD_BITS[action]
        )

    def is_winning_move(self, action: int) -> bool:
        """Instantly checks if playing `action` wins the game for current player."""
        if not self.is_legal(action):
            return False
        bit = 1 << self.heights[action]
        p_idx = 0 if self.current_player == 1 else 1
        return check_win(self.bitboards[p_idx] | bit)

    def is_opponent_winning_move(self, action: int) -> bool:
        """Instantly checks if opponent playing `action` would win."""
        if not self.is_legal(action):
            return False
        bit = 1 << self.heights[action]
        opp_idx = 1 if self.current_player == 1 else 0
        return check_win(self.bitboards[opp_idx] | bit)

    def step(self, action: int) -> Bitboard:
        """Drops a piece into column `action` for the current player.
        
        Raises ValueError if the move is illegal or game is over.
        """
        if not self.is_legal(action):
            raise ValueError(f"Illegal action: {action}. Legal actions: {self.legal_actions()}")

        bit = 1 << self.heights[action]
        p_idx = 0 if self.current_player == 1 else 1

        self.history.append((action, bit, self.current_player))
        self.bitboards[p_idx] |= bit
        self.heights[action] += 1
        self.move_count += 1

        if check_win(self.bitboards[p_idx]):
            self.winner = self.current_player
        elif self.move_count == self.TOTAL_CELLS:
            self.winner = 0  # Draw
        else:
            self.current_player = 2 if self.current_player == 1 else 1

        return self

    def undo(self) -> Bitboard:
        """Reverts the last move made."""
        if not self.history:
            raise ValueError("No moves to undo.")

        action, bit, prev_player = self.history.pop()
        p_idx = 0 if prev_player == 1 else 1

        self.bitboards[p_idx] ^= bit
        self.heights[action] -= 1
        self.move_count -= 1
        self.current_player = prev_player
        self.winner = None

        return self

    def is_terminal(self) -> bool:
        """Returns True if the game is over (win or draw)."""
        return self.winner is not None

    def result(self, player: Optional[int] = None) -> float:
        """Returns outcome from the perspective of `player` (1 or 2).
        
        +1.0: win
         0.0: draw or ongoing
        -1.0: loss
        If player is None, uses `current_player`.
        """
        if self.winner is None or self.winner == 0:
            return 0.0

        p = player if player is not None else self.current_player
        return 1.0 if self.winner == p else -1.0

    def to_numpy(self) -> np.ndarray:
        """Converts bitboards to 6x7 numpy array (row 0 = bottom).
        
        Values: +1 for Player 1, -1 for Player 2, 0 for empty.
        """
        grid = np.zeros((self.ROWS, self.COLS), dtype=np.int8)
        bb1, bb2 = self.bitboards[0], self.bitboards[1]
        for c in range(self.COLS):
            base = self.COL_BASES[c]
            for r in range(self.ROWS):
                bit = 1 << (base + r)
                if bb1 & bit:
                    grid[r, c] = 1
                elif bb2 & bit:
                    grid[r, c] = -1
        return grid

    def to_tensor(self) -> np.ndarray:
        """Returns 2x6x7 numpy array representing state for neural network.
        
        Channel 0: current player's pieces (1.0 or 0.0)
        Channel 1: opponent's pieces (1.0 or 0.0)
        """
        cur_idx = 0 if self.current_player == 1 else 1
        opp_idx = 1 - cur_idx
        cur_bb, opp_bb = self.bitboards[cur_idx], self.bitboards[opp_idx]

        ch0 = np.zeros((self.ROWS, self.COLS), dtype=np.float32)
        ch1 = np.zeros((self.ROWS, self.COLS), dtype=np.float32)

        for c in range(self.COLS):
            base = self.COL_BASES[c]
            for r in range(self.ROWS):
                bit = 1 << (base + r)
                if cur_bb & bit:
                    ch0[r, c] = 1.0
                elif opp_bb & bit:
                    ch1[r, c] = 1.0

        return np.stack([ch0, ch1], axis=0)

    def render(self) -> str:
        """Renders the board as an ASCII string."""
        symbols = {0: ".", 1: "X", -1: "O"}
        grid = self.to_numpy()
        lines = []
        lines.append("  " + " ".join(str(c) for c in range(self.COLS)))
        lines.append(" +" + "--" * self.COLS + "+")
        for r in reversed(range(self.ROWS)):
            row_str = " ".join(symbols[grid[r, c]] for c in range(self.COLS))
            lines.append(f"{r}| {row_str} |")
        lines.append(" +" + "--" * self.COLS + "+")
        turn_str = "Red (X)" if self.current_player == 1 else "Yellow (O)"
        if self.winner == 1:
            status = "Winner: Red (X)"
        elif self.winner == 2:
            status = "Winner: Yellow (O)"
        elif self.winner == 0:
            status = "Result: Draw"
        else:
            status = f"Turn: {turn_str}"
        lines.append(f"Move: {self.move_count} | {status}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.render()
