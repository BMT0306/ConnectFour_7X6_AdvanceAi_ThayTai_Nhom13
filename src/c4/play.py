"""Chơi thử trong terminal: Người vs Máy.

    python -m c4.play --opponent random
    python -m c4.play --opponent random --human-second

Nhập số cột 1..7; gõ q để thoát.
"""
from __future__ import annotations

import argparse
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.agents import Budget, make_agent
from c4.game import PLAYER1, Connect4


def main(argv=None) -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--opponent", default="random")
    p.add_argument("--human-second", action="store_true", help="người chơi đi sau")
    p.add_argument("--seed", type=int)
    p.add_argument("--time", type=float, help="giây/nước cho máy")
    p.add_argument("--sims", type=int)
    p.add_argument("--depth", type=int)
    args = p.parse_args(argv)

    agent = make_agent(args.opponent, seed=args.seed)
    budget = Budget(time_s=args.time, simulations=args.sims, depth=args.depth)
    human = -1 if args.human_second else PLAYER1
    g = Connect4()
    while not g.is_terminal():
        print("\n" + g.render() + "\n")
        if g.current_player == human:
            raw = input("Cột của bạn (1-7, q để thoát): ").strip().lower()
            if raw == "q":
                return
            if not raw.isdigit() or not (int(raw) - 1) in g.legal_actions():
                print("Nước đi không hợp lệ, thử lại.")
                continue
            g.step(int(raw) - 1)
        else:
            a = agent.choose_action(g.clone(), budget)
            print(f"Máy ({agent.name}) chọn cột {a + 1}  {agent.last_stats or ''}")
            g.step(a)
    print("\n" + g.render() + "\n")
    if g.winner == 0:
        print("Hòa!")
    else:
        print("Bạn thắng!" if g.winner == human else "Máy thắng!")


if __name__ == "__main__":
    main()
