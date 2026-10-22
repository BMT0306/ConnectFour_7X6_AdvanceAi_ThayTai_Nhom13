"""Chạy một trận đấu từ dòng lệnh, ví dụ:

    python -m c4.eval.cli --a random --b random --openings 100 --seed 0 --out results/logs/random_vs_random.csv
    python -m c4.eval.cli --a alphabeta --b mcts --time-a 0.1 --time-b 0.1 --openings 100
"""
from __future__ import annotations

import argparse

from c4.agents import Budget, make_agent
from c4.eval.match import generate_openings, run_match, save_records_csv
from c4.eval.metrics import percentile, summarize


def _budget(time_s, sims, depth):
    if time_s is None and sims is None and depth is None:
        return None
    return Budget(time_s=time_s, simulations=sims, depth=depth)


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description="Chạy trận đấu giữa hai tác tử")
    p.add_argument("--a", required=True, help="tên agent A (xem c4.agents.AGENTS)")
    p.add_argument("--b", required=True, help="tên agent B")
    p.add_argument("--openings", type=int, default=100, help="số khai cuộc (số ván = 2 x giá trị này)")
    p.add_argument("--opening-plies", type=int, default=4)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--time-a", type=float); p.add_argument("--time-b", type=float)
    p.add_argument("--sims-a", type=int); p.add_argument("--sims-b", type=int)
    p.add_argument("--depth-a", type=int); p.add_argument("--depth-b", type=int)
    p.add_argument("--out", help="đường dẫn CSV log thô")
    args = p.parse_args(argv)

    a = make_agent(args.a, seed=args.seed)
    b = make_agent(args.b, seed=args.seed + 1)
    openings = generate_openings(args.openings, plies=args.opening_plies, seed=args.seed)
    recs = run_match(a, b, openings,
                     _budget(args.time_a, args.sims_a, args.depth_a),
                     _budget(args.time_b, args.sims_b, args.depth_b))
    if args.out:
        save_records_csv(recs, args.out)
        print(f"Đã lưu log thô: {args.out}")

    s = summarize([r.a_result for r in recs], seed=args.seed)
    first = [r.a_result for r in recs if r.a_first]
    second = [r.a_result for r in recs if not r.a_first]
    print(f"{a.name} vs {b.name}: {s['n']} ván -> W/D/L = {s['wins']}/{s['draws']}/{s['losses']}")
    print(f"  score = {s['score']:.3f}  (bootstrap 95%: {s['score_boot_low']:.3f}-{s['score_boot_high']:.3f})")
    print(f"  tỷ lệ thắng = {s['win_rate']:.3f}  (Wilson 95%: {s['win_rate_wilson_low']:.3f}-{s['win_rate_wilson_high']:.3f})")
    print(f"  khi đi trước: score = {summarize(first)['score']:.3f}; khi đi sau: score = {summarize(second)['score']:.3f}")
    ta = [t for r in recs for t in r.a_times]
    print(f"  {a.name}: thời gian TB/nước = {1000 * sum(ta) / max(len(ta), 1):.3f} ms, p95 = {1000 * percentile(ta, 95):.3f} ms")


if __name__ == "__main__":
    main()
