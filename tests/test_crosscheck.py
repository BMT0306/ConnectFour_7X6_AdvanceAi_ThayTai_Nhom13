"""Đối chiếu chéo bitboard với bản tham chiếu trên nhiều ván ngẫu nhiên.

Mặc định 2.000 ván cho nhanh; để chạy 10.000 ván (theo proposal):  C4_CROSS_GAMES=10000 pytest
"""
import os
import random

import numpy as np

from c4.game import Connect4, ReferenceConnect4


def _same(a, b):
    assert a.legal_actions() == b.legal_actions()
    assert a.current_player == b.current_player
    assert a.winner == b.winner
    assert a.is_terminal() == b.is_terminal()
    assert a.move_count == b.move_count
    assert np.array_equal(a.to_array(), b.to_array())
    assert np.array_equal(a.to_array(relative=True), b.to_array(relative=True))
    for p in (1, -1):
        assert a.winning_moves(p) == b.winning_moves(p)


def test_bitboard_matches_reference_on_random_games():
    n_games = int(os.environ.get("C4_CROSS_GAMES", "2000"))
    rng = random.Random(2024)
    for _ in range(n_games):
        fast, slow = Connect4(), ReferenceConnect4()
        _same(fast, slow)
        seq = []
        while not fast.is_terminal():
            c = rng.choice(fast.legal_actions())
            fast.step(c)
            slow.step(c)
            seq.append(c)
            _same(fast, slow)
        for c in reversed(seq):
            assert fast.undo() == slow.undo() == c
            _same(fast, slow)
