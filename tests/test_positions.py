"""Kiểm tra engine/tác tử trên bộ vị trí do con người ghi tay (tests/data/positions.csv)."""
import csv
import os

from c4.game import Connect4, ReferenceConnect4

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "positions.csv")


def _cols(text):
    text = text.strip()
    return [] if text in ("", "-") else [int(t) - 1 for t in text.split()]  # 1..7 -> 0..6


def _rows():
    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_positions_csv_is_valid_and_matches_engines():
    rows = _rows()
    assert len(rows) >= 1
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "id bị trùng"
    for r in rows:
        for E in (Connect4, ReferenceConnect4):
            g = E()
            for c in _cols(r["moves"]):
                g.step(c)
            who = "X" if g.move_count % 2 == 0 else "O"
            assert who == r["side_to_move"].strip(), f"{r['id']}: side_to_move phải là {who}"
            assert g.winning_moves() == sorted(_cols(r["winning_moves"])), f"{r['id']}: winning_moves sai ({E.__name__})"
            assert g.winning_moves(-g.current_player) == sorted(_cols(r["blocking_moves"])), \
                f"{r['id']}: blocking_moves sai ({E.__name__})"
