import os
import tempfile

from c4.agents import Agent, make_agent
from c4.eval.match import generate_openings, play_game, run_match, save_records_csv
from c4.game import Connect4, IllegalMoveError


def test_openings_distinct_nonterminal_and_reproducible():
    ops = generate_openings(100, plies=4, seed=0)
    assert len(ops) == len(set(ops)) == 100
    assert all(len(o) == 4 for o in ops)
    assert ops == generate_openings(100, plies=4, seed=0)
    assert ops != generate_openings(100, plies=4, seed=1)


def test_match_plays_each_opening_with_both_colours():
    ops = generate_openings(10, seed=3)
    recs = run_match(make_agent("random", seed=1), make_agent("random", seed=2), ops)
    assert len(recs) == 20
    for i in range(10):
        pair = [r for r in recs if r.opening_id == i]
        assert sorted(r.a_first for r in pair) == [False, True]
    for r in recs:
        assert r.a_result == (r.winner if r.a_first else -r.winner)
        # số nước đo thời gian = số nước do agent chọn (không tính khai cuộc)
        assert len(r.a_times) + len(r.b_times) == r.plies - len(r.opening)


def test_match_is_reproducible_with_same_seeds():
    ops = generate_openings(8, seed=9)
    run = lambda: [(r.winner, r.plies) for r in
                   run_match(make_agent("random", seed=1), make_agent("random", seed=2), ops)]
    assert run() == run()


def test_illegal_agent_move_raises():
    class Bad(Agent):
        name = "bad"

        def choose_action(self, game, budget=None):
            return 99

    try:
        play_game(Bad(), make_agent("random", seed=0))
    except IllegalMoveError:
        pass
    else:
        raise AssertionError("agent đi sai phải làm ván đấu báo lỗi")


def test_csv_log_written():
    tmp_path_str = os.path.join(tempfile.mkdtemp(), "log.csv")
    ops = generate_openings(3, seed=1)
    recs = run_match(make_agent("random", seed=1), make_agent("random", seed=2), ops)
    save_records_csv(recs, tmp_path_str)
    with open(tmp_path_str, encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    assert len(lines) == 1 + len(recs)
    assert lines[0].startswith("pair,opening_id")


def test_timeout_zero_budget_falls_back_safely_without_crashing():
    from c4.agents import Budget

    g = Connect4()
    g.step(3)
    for name in ("random", "heuristic", "alphabeta", "mcts", "nn", "mixed_mcts"):
        ag = make_agent(name, seed=123)
        mv = ag.choose_action(g.clone(), Budget(time_s=0.0))
        assert mv in g.legal_actions(), name
        assert ag.last_stats.get("timed_out") is True, (name, ag.last_stats)


def test_play_game_timeout_policies():
    import time as _t
    from c4.agents import Budget

    class SlowIgnoreAgent(Agent):
        name = "slow_ignore"

        def choose_action(self, game, budget=None):
            _t.sleep(0.08)
            return game.legal_actions()[0]

    rec_strict = play_game(
        SlowIgnoreAgent(seed=1),
        make_agent("random", seed=2),
        budget_first=Budget(time_s=0.01),
        timeout_policy="strict_random",
        fallback_seed=7,
    )
    assert rec_strict.stats_first[0]["timed_out"] is True
    assert rec_strict.stats_first[0]["fallback_random"] is True
    assert rec_strict.stats_first[0]["hard_timeout_override"] is True

    rec_best = play_game(
        make_agent("alphabeta", seed=1),
        make_agent("mcts", seed=2),
        budget_first=Budget(time_s=0.02),
        budget_second=Budget(time_s=0.02),
        timeout_policy="best_or_random",
        fallback_seed=7,
    )
    assert rec_best.winner in (-1, 0, 1)
    assert all(isinstance(s.get("timed_out"), bool) for s in rec_best.stats_first)
    assert all(isinstance(s.get("timed_out"), bool) for s in rec_best.stats_second)
