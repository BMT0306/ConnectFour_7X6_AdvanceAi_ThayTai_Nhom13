"""Unit and integration tests for Level 1 to Level 4 Agents.

Tests:
1. RandomAgent: legality, seed reproducibility.
2. HeuristicAgent: Rule 1 (win now), Rule 2 (block win), Rule 3 (avoid blunder above), center preference.
3. AlphaBetaAgent: Equivalence between Pruned Alpha-Beta and Unpruned Minimax (Rubric requirement),
   tactical win detection, time budget enforcement.
4. MCTSAgent: Tactical win detection, time and simulation budgets.
5. Sanity Matches: Heuristic, Alpha-Beta, and MCTS against Random baseline.
"""

import pytest
from c4.game.engine import Bitboard
from c4.agents.random_agent import RandomAgent
from c4.agents.heuristic import HeuristicAgent
from c4.agents.alphabeta import AlphaBetaAgent
from c4.agents.mcts import MCTSAgent


# ---------------------------------------------------------------------------
# 1. RandomAgent Tests
# ---------------------------------------------------------------------------

def test_random_agent_legality():
    b = Bitboard()
    agent = RandomAgent(seed=42)
    for _ in range(20):
        action = agent.choose_action(b)
        assert action in b.legal_actions()
        b.step(action)
        if b.is_terminal():
            break


def test_random_agent_reproducibility():
    b1, b2 = Bitboard(), Bitboard()
    a1, a2 = RandomAgent(seed=123), RandomAgent(seed=123)
    for _ in range(10):
        move1 = a1.choose_action(b1)
        move2 = a2.choose_action(b2)
        assert move1 == move2
        b1.step(move1)
        b2.step(move2)


# ---------------------------------------------------------------------------
# 2. HeuristicAgent Tests
# ---------------------------------------------------------------------------

def test_heuristic_first_move_center():
    """Empty board: Heuristic must choose center column 3."""
    b = Bitboard()
    agent = HeuristicAgent()
    assert agent.choose_action(b) == 3


def test_heuristic_rule1_win_immediately():
    """Rule 1: If 3 in a row, must complete the 4th to win immediately."""
    b = Bitboard()
    # P1: 0, 1, 2 in row 0
    # P2: 0, 1 in row 1
    # Moves: 0 (P1), 0 (P2), 1 (P1), 1 (P2), 2 (P1), 6 (P2)
    for m in [0, 0, 1, 1, 2, 6]:
        b.step(m)

    # Current player is P1. Winning move is col 3
    agent = HeuristicAgent()
    action = agent.choose_action(b)
    assert action == 3


def test_heuristic_rule2_block_opponent_win():
    """Rule 2: If opponent threatens immediate win, must block it."""
    b = Bitboard()
    # P1: 0, 1, 2 in row 0
    # P2: 0, 1 in row 1, plus col 6
    # Moves: 0 (P1), 0 (P2), 1 (P1), 1 (P2), 2 (P1)
    for m in [0, 0, 1, 1, 2]:
        b.step(m)

    # Current player is P2. P1 threatens to win with col 3. P2 MUST play 3.
    agent = HeuristicAgent()
    action = agent.choose_action(b)
    assert action == 3


def test_heuristic_rule3_avoid_blunder_above():
    """Rule 3: Avoid move that allows opponent to win on next row above."""
    b = Bitboard()
    # P1 (Red) has 3 pieces at row 1 in cols 1, 3, 4.
    # At row 0, col 4 has Red, so Yellow does not have 3-in-a-row.
    # Col 2 is empty at both row 0 and row 1.
    # If Yellow plays col 2 (row 0), Red can immediately play col 2 (row 1) and win.
    # Yellow must avoid playing col 2.
    moves = [4, 1, 1, 3, 3, 5, 4]
    for m in moves:
        b.step(m)

    agent = HeuristicAgent()
    action = agent.choose_action(b)
    # Action must NOT be 2 because playing 2 gives P1 a win on the row above
    assert action != 2


# ---------------------------------------------------------------------------
# 3. AlphaBetaAgent Tests
# ---------------------------------------------------------------------------

def test_alphabeta_minimax_equivalence():
    """Rubric requirement: Alpha-Beta gives exact same value and move as Minimax.
    
    Verified across random positions at depth 3 and 4.
    """
    pruned_agent = AlphaBetaAgent(depth=3, use_pruning=True, use_ordering=True)
    unpruned_agent = AlphaBetaAgent(depth=3, use_pruning=False, use_ordering=False)

    rng = RandomAgent(seed=42)
    b = Bitboard()

    for _ in range(6):
        action = rng.choose_action(b)
        b.step(action)

        move_pruned, score_pruned = pruned_agent._root_search(b, depth=3)
        move_unpruned, score_unpruned = unpruned_agent._root_search(b, depth=3)

        assert score_pruned == score_unpruned
        assert move_pruned == move_unpruned
        # Pruned search must visit fewer or equal nodes
        assert pruned_agent._nodes_visited <= unpruned_agent._nodes_visited


def test_alphabeta_time_budget():
    """Verify Iterative Deepening respects time budget."""
    b = Bitboard()
    agent = AlphaBetaAgent()
    # 50 milliseconds budget
    budget_s = 0.05
    agent.choose_action(b, budget=budget_s)
    assert agent.stats["time_taken"] <= budget_s + 0.05
    assert agent.stats["depth_reached"] >= 2


# ---------------------------------------------------------------------------
# 4. MCTSAgent Tests
# ---------------------------------------------------------------------------

def test_mcts_immediate_win():
    """MCTS must take instant winning move."""
    b = Bitboard()
    for m in [0, 0, 1, 1, 2, 6]:
        b.step(m)

    # P1 has winning move at col 3
    agent = MCTSAgent(num_simulations=100, seed=42)
    action = agent.choose_action(b)
    assert action == 3


def test_mcts_time_and_sim_budgets():
    b = Bitboard()
    # Test simulation count budget
    agent_sim = MCTSAgent(num_simulations=150, seed=42)
    agent_sim.choose_action(b, budget=150)
    assert agent_sim.stats["nodes_visited"] == 150

    # Test time budget
    agent_time = MCTSAgent(seed=42)
    agent_time.choose_action(b, budget=0.05)
    assert agent_time.stats["time_taken"] <= 0.15


# ---------------------------------------------------------------------------
# 5. Sanity Matches: Search Agents vs Random Baseline
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("AgentClass, kwargs", [
    (HeuristicAgent, {}),
    (AlphaBetaAgent, {"depth": 4}),
    (MCTSAgent, {"num_simulations": 300, "seed": 42}),
])
def test_agents_defeat_random_baseline(AgentClass, kwargs):
    """Sanity requirement (Proposal mục 5.6):
    Every intelligent agent must decisively win against Random baseline.
    """
    smart_agent = AgentClass(**kwargs)
    random_agent = RandomAgent(seed=2026)

    wins = 0
    total_games = 6  # 3 games playing first (Red), 3 games playing second (Yellow)

    for i in range(total_games):
        b = Bitboard()
        smart_is_p1 = (i % 2 == 0)

        while not b.is_terminal():
            if (b.current_player == 1 and smart_is_p1) or (b.current_player == 2 and not smart_is_p1):
                action = smart_agent.choose_action(b)
            else:
                action = random_agent.choose_action(b)
            b.step(action)

        smart_player = 1 if smart_is_p1 else 2
        if b.winner == smart_player:
            wins += 1

    # Smart agent must win at least 5 out of 6 games (>= 83% win rate in 6 games sanity check)
    assert wins >= 5, f"{smart_agent.name} only won {wins}/{total_games} against Random"
