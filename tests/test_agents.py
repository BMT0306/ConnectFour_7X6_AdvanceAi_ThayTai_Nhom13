import random

from c4.agents import AGENTS, Budget, make_agent
from c4.game import Connect4


def test_random_agent_returns_legal_moves_and_is_seeded():
    for name in AGENTS:  # kiểm tra mọi agent đã đăng ký: luôn trả về nước hợp lệ
        agent = make_agent(name, seed=3)
        rng = random.Random(0)
        for _ in range(10):
            g = Connect4()
            while not g.is_terminal():
                a = agent.choose_action(g.clone(), Budget(depth=2, simulations=50))
                assert a in g.legal_actions()
                g.step(rng.choice(g.legal_actions()))


def test_same_seed_same_choices():
    g = Connect4()
    a1, a2 = make_agent("random", seed=5), make_agent("random", seed=5)
    assert [a1.choose_action(g) for _ in range(20)] == [a2.choose_action(g) for _ in range(20)]


def test_unknown_agent_message():
    try:
        make_agent("khong-ton-tai")
    except KeyError as e:
        assert "random" in str(e)
    else:
        raise AssertionError("phải ném KeyError")
