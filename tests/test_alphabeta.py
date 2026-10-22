import csv
import os
import random
import time

from c4.agents import AlphaBetaAgent, Budget
from c4.agents.alphabeta import WIN
from c4.game import CENTER_FIRST, Connect4
from helpers import random_game_moves

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "positions.csv")


def _cols(text):
    text = text.strip()
    return [] if text in ("", "-") else [int(t) - 1 for t in text.split()]


def _random_positions(n, seed, min_plies=0, max_plies=16):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        seq = random_game_moves(random.Random(rng.random()))
        k = rng.randint(min_plies, min(max_plies, len(seq) - 1))
        g = Connect4()
        for c in seq[:k]:
            g.step(c)
        if not g.is_terminal():
            out.append(g)
    return out


def _minimax_value(g, depth, ply):
    """Minimax THUẦN viết độc lập (không cắt tỉa, không ordering, lá = 0) để đối chiếu."""
    best = -WIN - 1
    for c in g.legal_actions():
        g.step(c)
        if g.winner:
            v = WIN - ply
        elif g.move_count == 42:
            v = 0
        elif depth <= 1:
            v = 0
        else:
            v = -_minimax_value(g, depth - 1, ply + 1)
        g.undo()
        best = max(best, v)
    return best


def _minimax_root(g, depth):
    """(giá trị, nước đầu tiên theo thứ tự CENTER_FIRST đạt giá trị lớn nhất)."""
    g = g.clone()
    legal = set(g.legal_actions())
    best_v, best_c = -WIN - 1, None
    for c in [c for c in CENTER_FIRST if c in legal]:
        g.step(c)
        if g.winner:
            v = WIN
        elif g.move_count == 42:
            v = 0
        elif depth <= 1:
            v = 0
        else:
            v = -_minimax_value(g, depth - 1, 1)
        g.undo()
        if v > best_v:
            best_v, best_c = v, c
    return best_v, best_c


def test_matches_independent_plain_minimax():
    for g in _random_positions(25, seed=1):
        for depth in (2, 3, 4):
            expected = _minimax_root(g, depth)
            for pruning in (True, False):
                agent = AlphaBetaAgent(pruning=pruning, ordering=True, use_eval=False)
                assert agent.search_fixed_depth(g, depth) == expected, (pruning, depth, g.history)


def test_pruning_changes_node_count_not_the_result():
    pruned = AlphaBetaAgent(pruning=True)
    full = AlphaBetaAgent(pruning=False)
    n_pruned = n_full = 0
    for g in _random_positions(15, seed=2):
        pruned.nodes = full.nodes = 0
        assert pruned.search_fixed_depth(g, 4) == full.search_fixed_depth(g, 4)  # có hàm lượng giá
        n_pruned += pruned.nodes
        n_full += full.nodes
    assert n_pruned < n_full / 2, (n_pruned, n_full)


def test_move_ordering_reduces_nodes():
    ordered = AlphaBetaAgent(ordering=True)
    plain = AlphaBetaAgent(ordering=False)
    n_o = n_p = 0
    for g in _random_positions(15, seed=3):
        ordered.nodes = plain.nodes = 0
        ordered.search_fixed_depth(g, 5)
        plain.search_fixed_depth(g, 5)
        n_o += ordered.nodes
        n_p += plain.nodes
    assert n_o < n_p, (n_o, n_p)


def test_finds_forced_win_in_three_plies():
    g = Connect4()
    for c in [3, 0, 4, 0]:  # X có cột 3,4 ở hàng đáy; X đi 2 hoặc 5 tạo ba quân mở 2 đầu
        g.step(c)
    value, move = AlphaBetaAgent().search_fixed_depth(g, 3)
    assert move in (2, 5)
    assert value == WIN - 2  # thắng ở nước thứ 3 (ply 2 tính từ 0)


def test_takes_immediate_win_and_blocks_single_threat():
    agent = AlphaBetaAgent(default_depth=3)
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        g = Connect4()
        for c in _cols(r["moves"]):
            g.step(c)
        wins, blocks = _cols(r["winning_moves"]), _cols(r["blocking_moves"])
        a = agent.choose_action(g.clone())
        if wins:
            assert a in wins, r["id"]
        elif len(blocks) == 1:
            assert a == blocks[0], r["id"]


def test_evaluation_is_mirror_symmetric_and_zero_on_empty_board():
    agent = AlphaBetaAgent()
    assert agent.evaluate(Connect4()) == 0
    for g in _random_positions(40, seed=5, max_plies=30):
        mirrored = Connect4()
        for c in g.history:
            mirrored.step(6 - c)
        assert agent.evaluate(g) == agent.evaluate(mirrored)


def test_time_budget_is_respected_and_returns_legal_move():
    agent = AlphaBetaAgent()
    g = Connect4()
    for limit in (0.02, 0.1):
        t0 = time.perf_counter()
        a = agent.choose_action(g.clone(), Budget(time_s=limit))
        dt = time.perf_counter() - t0
        assert a in g.legal_actions()
        assert dt < limit + 0.05, dt
        assert agent.last_stats["depth"] >= 1


def test_depth_budget_overrides_default_and_reports_stats():
    agent = AlphaBetaAgent(default_depth=6)
    g = Connect4()
    agent.choose_action(g.clone(), Budget(depth=2))
    assert agent.last_stats["depth"] == 2 and agent.last_stats["nodes"] > 0
