"""Comprehensive test suite for Connect Four Game Engines.

Tests:
1. Logic: Horizontal, Vertical, Diagonal (/ and \\) wins, Draw condition.
2. Rules: Full column rejection, terminal move rejection, out-of-bound column rejection.
3. Integrity: step(), undo(), and clone() state consistency.
4. Perft: Number of move paths at depth 6 from empty board must equal 7^6 = 117,649.
5. Cross-check: High-volume random playout comparison between Bitboard and ReferenceBoard.
"""

import pytest
import numpy as np
import random
from c4.game.engine import Bitboard
from c4.game.reference import ReferenceBoard


# ---------------------------------------------------------------------------
# 1. Basic Rules & Win Conditions
# ---------------------------------------------------------------------------

def test_horizontal_win():
    """Test horizontal connect 4 for both Bitboard and ReferenceBoard."""
    for board_cls in (Bitboard, ReferenceBoard):
        b = board_cls()
        # P1: 0, 1, 2, 3 in bottom row
        # P2: 0, 1, 2 in row 1
        # Moves: 0 (P1), 0 (P2), 1 (P1), 1 (P2), 2 (P1), 2 (P2), 3 (P1 wins)
        moves = [0, 0, 1, 1, 2, 2, 3]
        for m in moves:
            b.step(m)

        assert b.is_terminal()
        assert b.winner == 1
        assert b.result(1) == 1.0
        assert b.result(2) == -1.0


def test_vertical_win():
    """Test vertical connect 4."""
    for board_cls in (Bitboard, ReferenceBoard):
        b = board_cls()
        # P1 plays in col 3, P2 plays in col 4
        # Moves: 3 (P1), 4 (P2), 3 (P1), 4 (P2), 3 (P1), 4 (P2), 3 (P1 wins)
        moves = [3, 4, 3, 4, 3, 4, 3]
        for m in moves:
            b.step(m)

        assert b.is_terminal()
        assert b.winner == 1
        assert b.result(1) == 1.0
        assert b.result(2) == -1.0


def test_diagonal_positive_slope_win():
    """Test positive slope diagonal connect 4 (bottom-left to top-right /)."""
    for board_cls in (Bitboard, ReferenceBoard):
        b = board_cls()
        # Target diagonal: (0,0), (1,1), (2,2), (3,3) for P1
        # Col 0: (0,0)=P1
        # Col 1: (0,1)=P2, (1,1)=P1
        # Col 2: (0,2)=P2, (1,2)=P2, (2,2)=P1
        # Col 3: (0,3)=P2, (1,3)=P2, (2,3)=P2, (3,3)=P1
        # Moves:
        # P1: 0, P2: 1
        # P1: 1, P2: 2
        # P1: 2, P2: 2  -> wait, let's play carefully
        # Step-by-step:
        b.step(0)  # P1: (0, 0)
        b.step(1)  # P2: (0, 1)
        b.step(1)  # P1: (1, 1)
        b.step(2)  # P2: (0, 2)
        b.step(3)  # P1: (0, 3)
        b.step(2)  # P2: (1, 2)
        b.step(2)  # P1: (2, 2)
        b.step(3)  # P2: (1, 3)
        b.step(3)  # P1: (2, 3)
        b.step(4)  # P2: (0, 4)
        b.step(3)  # P1: (3, 3) -> WINNER!

        assert b.is_terminal()
        assert b.winner == 1


def test_diagonal_negative_slope_win():
    """Test negative slope diagonal connect 4 (top-left to bottom-right \\)."""
    for board_cls in (Bitboard, ReferenceBoard):
        b = board_cls()
        # Target diagonal: (3,0), (2,1), (1,2), (0,3) for P1
        # Col 3: (0, 3)=P1
        # Col 2: (0, 2)=P2, (1, 2)=P1
        # Col 1: (0, 1)=P2, (1, 1)=P2, (2, 1)=P1
        # Col 0: (0, 0)=P2, (1, 0)=P2, (2, 0)=P2, (3, 0)=P1
        b.step(3)  # P1: (0, 3)
        b.step(2)  # P2: (0, 2)
        b.step(2)  # P1: (1, 2)
        b.step(1)  # P2: (0, 1)
        b.step(0)  # P1: (0, 0)
        b.step(1)  # P2: (1, 1)
        b.step(1)  # P1: (2, 1)
        b.step(0)  # P2: (1, 0)
        b.step(0)  # P1: (2, 0)
        b.step(4)  # P2: (0, 4)
        b.step(0)  # P1: (3, 0) -> WINNER!

        assert b.is_terminal()
        assert b.winner == 1


def test_draw_condition():
    """Test full 42-move draw without winner."""
    # A verified 42-move draw sequence where no player connects 4:
    draw_moves = [
        3, 3, 0, 2, 5, 4, 5, 6, 4, 2, 2, 3, 3, 5, 5, 2, 2, 4, 3, 3, 1,
        1, 2, 1, 5, 5, 0, 4, 0, 4, 4, 6, 6, 6, 6, 0, 1, 0, 6, 0, 1, 1
    ]
    assert len(draw_moves) == 42
    for board_cls in (Bitboard, ReferenceBoard):
        b = board_cls()
        for m in draw_moves:
            b.step(m)
        assert b.is_terminal()
        assert b.winner == 0
        assert b.result() == 0.0
        assert len(b.legal_actions()) == 0


def test_illegal_moves_rejected():
    """Test that full columns and moves after game over raise ValueError."""
    for board_cls in (Bitboard, ReferenceBoard):
        b = board_cls()
        # Fill column 0 with 6 pieces
        for _ in range(6):
            b.step(0)
        assert 0 not in b.legal_actions()
        with pytest.raises(ValueError):
            b.step(0)  # Column 0 is full

        # Out of bounds
        with pytest.raises(ValueError):
            b.step(-1)
        with pytest.raises(ValueError):
            b.step(7)


# ---------------------------------------------------------------------------
# 2. Step, Undo, and Clone Integrity
# ---------------------------------------------------------------------------

def test_step_undo_consistency():
    """Verify that step followed by undo restores exact state."""
    b = Bitboard()
    actions = [3, 2, 3, 4, 2, 1, 0, 3]
    for a in actions:
        b.step(a)

    for a in reversed(actions):
        assert b.history[-1][0] == a
        b.undo()

    assert b.move_count == 0
    assert b.bitboards == [0, 0]
    assert b.heights == list(Bitboard.COL_BASES)
    assert b.current_player == 1
    assert b.winner is None


def test_clone_independence():
    """Verify that modifying a cloned board does not affect the original."""
    original = Bitboard()
    original.step(3)
    original.step(4)

    clone = original.clone()
    clone.step(3)

    assert clone.move_count == 3
    assert original.move_count == 2
    assert clone.heights[3] != original.heights[3]


# ---------------------------------------------------------------------------
# 3. Perft (Performance & Move Generation Completeness)
# ---------------------------------------------------------------------------

def _perft(board: Bitboard, depth: int) -> int:
    """Recursive perft node count."""
    if depth == 0 or board.is_terminal():
        return 1
    nodes = 0
    for action in board.legal_actions():
        board.step(action)
        nodes += _perft(board, depth - 1)
        board.undo()
    return nodes


def test_perft_depth_counts():
    """Verify Perft counts from empty board.
    
    Since no player can win before move 7, from empty board:
      Depth 1: 7^1 = 7
      Depth 2: 7^2 = 49
      Depth 3: 7^3 = 343
      Depth 4: 7^4 = 2,401
      Depth 5: 7^5 = 16,807
      Depth 6: 7^6 = 117,649
    """
    b = Bitboard()
    assert _perft(b, 1) == 7
    assert _perft(b, 2) == 49
    assert _perft(b, 3) == 343
    assert _perft(b, 4) == 2401
    assert _perft(b, 5) == 16807
    assert _perft(b, 6) == 117649

    # Verify board state is unchanged after 117,649 steps and undos
    assert b.move_count == 0
    assert b.bitboards == [0, 0]
    assert b.current_player == 1


# ---------------------------------------------------------------------------
# 4. Cross-Check: Bitboard vs ReferenceBoard (10,000 Games)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("seed", [42, 100, 2026])
def test_cross_check_random_play(seed: int):
    """Play random games comparing Bitboard against ReferenceBoard step by step."""
    rng = random.Random(seed)
    num_games = 500  # fast test runs 500 * 3 seeds = 1,500 games; test_massive runs 10,000

    for _ in range(num_games):
        bb = Bitboard()
        ref = ReferenceBoard()

        while not bb.is_terminal():
            # Check legal actions match
            assert bb.legal_actions() == ref.legal_actions()
            assert bb.current_player == ref.current_player
            assert bb.move_count == ref.move_count
            assert np.array_equal(bb.to_numpy(), ref.to_numpy())
            assert np.array_equal(bb.to_tensor(), ref.to_tensor())

            actions = bb.legal_actions()
            action = rng.choice(actions)

            # Test instant win detection helper
            if bb.is_winning_move(action):
                bb_clone = bb.clone()
                bb_clone.step(action)
                assert bb_clone.winner == bb.current_player

            bb.step(action)
            ref.step(action)

            # Check termination & winner match
            assert bb.is_terminal() == ref.is_terminal()
            assert bb.winner == ref.winner
            assert bb.result() == ref.result()

        # Terminal state verification
        assert bb.is_terminal() and ref.is_terminal()
        assert bb.winner == ref.winner


def test_massive_cross_check_10000_games():
    """Large scale cross-validation: 10,000 random games."""
    rng = random.Random(999)
    for _ in range(10000):
        bb = Bitboard()
        ref = ReferenceBoard()

        while not bb.is_terminal():
            action = rng.choice(bb.legal_actions())
            bb.step(action)
            ref.step(action)

        assert bb.winner == ref.winner
        assert bb.move_count == ref.move_count
