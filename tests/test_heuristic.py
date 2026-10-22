import csv
import os
import random

from c4.agents import HeuristicAgent, make_agent
from c4.eval.match import generate_openings, run_match
from c4.eval.metrics import summarize
from c4.game import Connect4
from helpers import random_game_moves

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "positions.csv")


def _cols(text):
    text = text.strip()
    return [] if text in ("", "-") else [int(t) - 1 for t in text.split()]


def test_heuristic_follows_priority_on_handwritten_positions():
    agent = HeuristicAgent()
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        g = Connect4()
        for c in _cols(r["moves"]):
            g.step(c)
        wins, blocks = _cols(r["winning_moves"]), _cols(r["blocking_moves"])
        a = agent.choose_action(g.clone())
        if wins:
            assert a in wins, f"{r['id']}: phải thắng ngay"
            assert agent.last_stats["rule"] == "win"
        elif blocks:
            assert a in blocks, f"{r['id']}: phải chặn"
            assert agent.last_stats["rule"] == "block"


def test_heuristic_never_hands_over_an_immediate_win_when_it_can_avoid_it():
    agent = HeuristicAgent()
    rng = random.Random(11)
    checked = 0
    for _ in range(300):
        seq = random_game_moves(random.Random(rng.random()))
        g = Connect4()
        for c in seq[: rng.randint(0, max(len(seq) - 1, 0))]:
            g.step(c)
        if g.is_terminal() or g.winning_moves() or g.winning_moves(-g.current_player):
            continue  # chỉ xét vị trí mà luật 1 và 2 không áp dụng
        a = agent.choose_action(g.clone())
        assert a in g.legal_actions()
        g.step(a)
        gave_win = bool(g.winning_moves())
        g.undo()
        if gave_win:
            # chỉ được phép khi MỌI nước đều tạo thế cho đối thủ
            for c in g.legal_actions():
                g.step(c)
                assert g.winning_moves(), "có nước an toàn nhưng agent không chọn"
                g.undo()
        checked += 1
    assert checked > 50


def test_heuristic_does_not_modify_the_game_it_receives():
    g = Connect4()
    for c in [3, 3, 4]:
        g.step(c)
    before = (g.key(), g.move_count)
    HeuristicAgent().choose_action(g)
    assert (g.key(), g.move_count) == before


def test_heuristic_beats_random():
    ops = generate_openings(25, seed=4)
    recs = run_match(make_agent("heuristic"), make_agent("random", seed=1), ops)
    s = summarize([r.a_result for r in recs])
    assert s["score"] >= 0.9, s
