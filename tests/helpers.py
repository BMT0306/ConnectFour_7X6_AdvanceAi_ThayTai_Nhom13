"""Hàm dùng chung cho test."""
import random

from c4.game import Connect4, ReferenceConnect4

ENGINES = (Connect4, ReferenceConnect4)


def play(game, cols):
    for c in cols:
        game.step(c)
    return game


def random_game_moves(rng: random.Random, engine_cls=Connect4):
    """Chơi một ván ngẫu nhiên đến hết, trả về chuỗi cột."""
    g = engine_cls()
    seq = []
    while not g.is_terminal():
        c = rng.choice(g.legal_actions())
        g.step(c)
        seq.append(c)
    return seq
