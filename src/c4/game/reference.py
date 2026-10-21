"""Reference implementation of Connect Four (7x6) using 2D NumPy array.

This implementation prioritizes readability, correctness, and transparency.
It serves as the ground-truth reference to verify the high-performance bitboard engine.
"""

from __future__ import annotations
from typing import List, Optional, Tuple
import numpy as np


class ReferenceBoard:
    """Connect Four Reference Board (6 rows x 7 columns).
    
    Coordinate convention:
      - row 0: bottom row
      - row 5: top row
      - col 0: leftmost column
      - col 6: rightmost column
      
    Player convention:
      - Player 1: Red (goes first, value +1)
      - Player 2: Yellow (goes second, value -1)
      - Empty: 0
    """

    ROWS: int = 6
    COLS: int = 7
    CONNECT: int = 4

    def __init__(self) -> None:
        self.grid = np.zeros((self.ROWS, self.COLS), dtype=np.int8)
        self.heights = [0] * self.COLS  # next available row in each column
        self.current_player: int = 1     # 1 or 2
        self.move_count: int = 0
        self.history: List[Tuple[int, int]] = []  # list of (col, row)
        self.winner: Optional[int] = None         # 1, 2, 0 (draw), or None

    def reset(self) -> ReferenceBoard:
        """Resets the board to the initial empty state."""
        self.grid.fill(0)
        self.heights = [0] * self.COLS
        self.current_player = 1
        self.move_count = 0
        self.history.clear()
        self.winner = None
        return self

    def clone(self) -> ReferenceBoard:
        """Returns a deep copy of the board."""
        new_board = ReferenceBoard()
        new_board.grid = np.copy(self.grid)
        new_board.heights = list(self.heights)
        new_board.current_player = self.current_player
        new_board.move_count = self.move_count
        new_board.history = list(self.history)
        new_board.winner = self.winner
        return new_board

    def legal_actions(self) -> List[int]:
        """Returns list of valid column indices [0..6] that are not full."""
        if self.is_terminal():
            return []
        return [c for c in range(self.COLS) if self.heights[c] < self.ROWS]

    def is_legal(self, action: int) -> bool:
        """Checks if a column action is legal."""
        return 0 <= action < self.COLS and self.heights[action] < self.ROWS and not self.is_terminal()

    def step(self, action: int) -> ReferenceBoard:
        """Drops a piece of the current player into column `action`.
        
        Raises ValueError if the move is illegal or game is over.
        """
        if not self.is_legal(action):
            raise ValueError(f"Illegal action: {action}. Legal actions: {self.legal_actions()}")

        row = self.heights[action]
        piece = 1 if self.current_player == 1 else -1

        self.grid[row, action] = piece
        self.heights[action] += 1
        self.history.append((action, row))
        self.move_count += 1

        # Check for victory from the placed piece
        if self._check_win_at(row, action, piece):
            self.winner = self.current_player
        elif self.move_count == self.ROWS * self.COLS:
            self.winner = 0  # Draw
        else:
            self.current_player = 2 if self.current_player == 1 else 1

        return self

    def undo(self) -> ReferenceBoard:
        """Reverts the last move made."""
        if not self.history:
            raise ValueError("No moves to undo.")

        action, row = self.history.pop()
        self.grid[row, action] = 0
        self.heights[action] -= 1
        self.move_count -= 1

        if self.winner is not None:
            # Last player was the one who made the move
            self.winner = None
            # current_player stays as the one who just moved
        else:
            # Switch current_player back
            self.current_player = 2 if self.current_player == 1 else 1

        return self

    def is_terminal(self) -> bool:
        """Returns True if the game has ended in a win or draw."""
        return self.winner is not None

    def result(self, player: Optional[int] = None) -> float:
        """Returns reward from the perspective of `player` (1 or 2).
        
        +1.0: win
         0.0: draw or ongoing
        -1.0: loss
        If player is None, uses `current_player`.
        """
        if self.winner is None or self.winner == 0:
            return 0.0

        p = player if player is not None else self.current_player
        return 1.0 if self.winner == p else -1.0

    def _check_win_at(self, r: int, c: int, piece: int) -> bool:
        """Checks if placing piece at (r, c) creates 4 in a row."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            # Forward direction
            nr, nc = r + dr, c + dc
            while 0 <= nr < self.ROWS and 0 <= nc < self.COLS and self.grid[nr, nc] == piece:
                count += 1
                nr += dr
                nc += dc
            # Backward direction
            nr, nc = r - dr, c - dc
            while 0 <= nr < self.ROWS and 0 <= nc < self.COLS and self.grid[nr, nc] == piece:
                count += 1
                nr -= dr
                nc -= dc
            if count >= self.CONNECT:
                return True
        return False

    def to_numpy(self) -> np.ndarray:
        """Returns a 6x7 numpy array copy of the board."""
        return np.copy(self.grid)

    def to_tensor(self) -> np.ndarray:
        """Returns 2x6x7 numpy array representing state for neural network.
        
        Channel 0: current player's pieces (1s and 0s)
        Channel 1: opponent player's pieces (1s and 0s)
        """
        cur_piece = 1 if self.current_player == 1 else -1
        opp_piece = -cur_piece
        ch0 = (self.grid == cur_piece).astype(np.float32)
        ch1 = (self.grid == opp_piece).astype(np.float32)
        return np.stack([ch0, ch1], axis=0)

    def render(self) -> str:
        """Renders the board as an ASCII string."""
        symbols = {0: ".", 1: "X", -1: "O"}
        lines = []
        lines.append("  " + " ".join(str(c) for c in range(self.COLS)))
        lines.append(" +" + "--" * self.COLS + "+")
        for r in reversed(range(self.ROWS)):
            row_str = " ".join(symbols[self.grid[r, c]] for c in range(self.COLS))
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
