import time

import pytest

from c4.agents import Budget, MCTSAgent, make_agent
from c4.eval.match import generate_openings, run_match
from c4.eval.metrics import summarize
from c4.game import Connect4
from test_engine import LAST_MOVE_WIN_GAME


def test_same_seed_same_result_and_reports_simulations():
    g = Connect4()
    for c in [3, 3, 4]:
        g.step(c)
    a1, a2 = MCTSAgent(seed=7), MCTSAgent(seed=7)
    m1 = a1.choose_action(g.clone(), Budget(simulations=300))
    m2 = a2.choose_action(g.clone(), Budget(simulations=300))
    assert m1 == m2
    assert a1.last_stats["simulations"] == 300 and a1.last_stats == a2.last_stats


def test_finds_immediate_win():
    for seed in range(5):
        g = Connect4()
        for c in [0, 6, 1, 6, 3, 6]:  # X thắng ngay ở cột 2
            g.step(c)
        assert MCTSAgent(seed=seed).choose_action(g.clone(), Budget(simulations=600)) == 2


def test_single_legal_move_needs_no_search():
    g = Connect4()
    for c in LAST_MOVE_WIN_GAME[:-1]:
        g.step(c)
    assert len(g.legal_actions()) == 1
    agent = MCTSAgent(seed=0)
    assert agent.choose_action(g, Budget(simulations=500)) == g.legal_actions()[0]
    assert agent.last_stats["simulations"] == 0


def test_time_budget_is_respected():
    agent = MCTSAgent(seed=0)
    g = Connect4()
    t0 = time.perf_counter()
    a = agent.choose_action(g.clone(), Budget(time_s=0.05))
    dt = time.perf_counter() - t0
    assert a in g.legal_actions()
    assert agent.last_stats["simulations"] > 0
    assert dt < 0.05 + 0.05, dt


def test_does_not_modify_the_game_it_receives():
    g = Connect4()
    for c in [3, 3, 4]:
        g.step(c)
    before = (g.key(), g.move_count)
    MCTSAgent(seed=1).choose_action(g, Budget(simulations=100))
    assert (g.key(), g.move_count) == before


def test_invalid_rollout_rejected():
    with pytest.raises(ValueError):
        MCTSAgent(rollout="khac")


def test_greedy_rollout_returns_legal_moves():
    g = Connect4()
    a = MCTSAgent(seed=2, rollout="greedy").choose_action(g.clone(), Budget(simulations=100))
    assert a in g.legal_actions()


def test_beats_random():
    ops = generate_openings(12, seed=6)
    recs = run_match(MCTSAgent(seed=1), make_agent("random", seed=2), ops,
                     budget_a=Budget(simulations=200))
    s = summarize([r.a_result for r in recs])
    assert s["score"] >= 0.9, s
