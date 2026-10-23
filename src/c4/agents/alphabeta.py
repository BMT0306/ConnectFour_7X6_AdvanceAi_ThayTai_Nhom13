"""Cấp 3 - Minimax / Alpha-Beta (negamax).

Quy ước điểm (theo góc nhìn bên ĐANG ĐẾN LƯỢT tại nút đang xét):
  * thắng ở độ sâu `ply` tính từ gốc: WIN - ply   (thắng càng sớm điểm càng cao, thua càng muộn càng tốt)
  * hòa (đầy bàn): 0
  * hết độ sâu: hàm lượng giá `evaluate` (nếu use_eval=False thì coi là 0, giống cách làm đơn giản ở sách Ch. 5)
`depth` = số nước (ply) nhìn trước, tính cả nước đi ở gốc.

Các cờ phục vụ ablation / so sánh:
  pruning  : bật/tắt cắt tỉa alpha-beta (tắt = minimax thuần, cùng giá trị và cùng nước đi, chỉ tốn nhiều nút hơn)
  ordering : sắp xếp nước đi từ giữa ra (tăng hiệu quả cắt tỉa)
  use_eval : bật/tắt hàm lượng giá khi hết độ sâu

Ngân sách (Budget):
  * depth       -> tìm kiếm cố định độ sâu đó
  * time_s      -> iterative deepening: tăng dần độ sâu, dừng khi hết giờ và dùng kết quả của độ sâu cuối cùng
                   HOÀN THÀNH (tối đa `Budget.depth` nếu có, mặc định 42)
  * không có gì -> độ sâu mặc định `default_depth`
Chỉ chạy trên engine bitboard (cần `bitboards()` cho hàm lượng giá).
"""
from __future__ import annotations

import time

from c4.agents.base import Agent, Budget
from c4.game.base import CENTER_FIRST, COLS, ROWS, Connect4Base

WIN = 1_000_000
_H = ROWS + 1
_RANK = {c: i for i, c in enumerate(CENTER_FIRST)}


def _build_windows() -> list[int]:
    """69 cửa sổ 4 ô liên tiếp (mỗi cửa sổ là một bitmask)."""
    wins = []
    bit = lambda c, r: 1 << (c * _H + r)
    for c in range(COLS):
        for r in range(ROWS):
            for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
                cells = [(c + k * dc, r + k * dr) for k in range(4)]
                if all(0 <= cc < COLS and 0 <= rr < ROWS for cc, rr in cells):
                    wins.append(sum(bit(cc, rr) for cc, rr in cells))
    return wins


_WINDOWS = _build_windows()
assert len(_WINDOWS) == 69
_CENTER_MASK = sum(1 << (3 * _H + r) for r in range(ROWS))


class _Timeout(Exception):
    pass


class AlphaBetaAgent(Agent):
    name = "alphabeta"

    def __init__(
        self,
        seed: int | None = None,
        default_depth: int = 5,
        pruning: bool = True,
        ordering: bool = True,
        use_eval: bool = True,
        eval_weights: tuple[int, int, int] = (2, 5, 3),  # (cửa sổ 2 quân, cửa sổ 3 quân, mỗi quân ở cột giữa)
        depth: int | None = None,
    ) -> None:
        super().__init__(seed)
        if depth is not None:
            default_depth = depth
        self.default_depth = default_depth
        self.pruning = pruning
        self.ordering = ordering
        self.use_eval = use_eval
        self.eval_weights = eval_weights
        self.nodes = 0
        self._deadline: float | None = None

    # ---------- hàm lượng giá (góc nhìn bên đang đến lượt) ----------
    def evaluate(self, game) -> int:
        w2, w3, wc = self.eval_weights
        me, opp = game.bitboards()
        score = wc * ((me & _CENTER_MASK).bit_count() - (opp & _CENTER_MASK).bit_count())
        for w in _WINDOWS:
            a = (me & w).bit_count()
            b = (opp & w).bit_count()
            if b == 0:
                if a == 3:
                    score += w3
                elif a == 2:
                    score += w2
            elif a == 0:
                if b == 3:
                    score -= w3
                elif b == 2:
                    score -= w2
        return score

    # ---------- tìm kiếm ----------
    def _ordered(self, game) -> list[int]:
        legal = game.legal_actions()
        return sorted(legal, key=_RANK.__getitem__) if self.ordering else legal

    def _negamax(self, g, depth: int, alpha: int, beta: int, ply: int) -> int:
        """Giá trị của vị trí g (chưa kết thúc) cho bên đang đến lượt, nhìn trước `depth` nước."""
        self.nodes += 1
        if self._deadline is not None and (self.nodes & 15) == 0 and time.perf_counter() > self._deadline:
            raise _Timeout
        best = -WIN - 1
        for c in self._ordered(g):
            g.step(c)
            if g.winner:
                v = WIN - ply
            elif g.move_count == ROWS * COLS:
                v = 0
            elif depth <= 1:
                v = -self.evaluate(g) if self.use_eval else 0
            else:
                v = -self._negamax(g, depth - 1, -beta, -alpha, ply + 1)
            g.undo()
            if v > best:
                best = v
                if self.pruning:
                    if best > alpha:
                        alpha = best
                    if alpha >= beta:
                        break
        return best

    def search_fixed_depth(self, game, depth: int, first: int | None = None) -> tuple[int, int]:
        """Tìm kiếm cố định độ sâu từ vị trí `game` (không bị sửa đổi). Trả về (giá trị, nước đi tốt nhất).

        `first`: nước thử trước ở gốc (kết quả độ sâu trước, giúp cắt tỉa tốt hơn). Dùng cho test/ablation.
        """
        g = game.clone()
        moves = self._ordered(g)
        if first in moves:
            moves.remove(first)
            moves.insert(0, first)
        alpha, beta = -WIN - 1, WIN + 1
        best_v, best_c = -WIN - 1, moves[0]
        for c in moves:
            g.step(c)
            if g.winner:
                v = WIN
            elif g.move_count == ROWS * COLS:
                v = 0
            elif depth <= 1:
                v = -self.evaluate(g) if self.use_eval else 0
            else:
                v = -self._negamax(g, depth - 1, -beta, -alpha, 1)
            g.undo()
            if v > best_v:  # chỉ thay khi LỚN HƠN hẳn => nước đầu tiên (theo thứ tự) đạt max được giữ
                best_v, best_c = v, c
                if self.pruning and best_v > alpha:
                    alpha = best_v
        return best_v, best_c

    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        legal = game.legal_actions()
        self.nodes = 0
        if len(legal) == 1:
            self.last_stats = {"nodes": 0, "depth": 0, "value": None}
            return legal[0]
        max_depth = (budget.depth if budget and budget.depth else None)
        time_s = budget.time_s if budget else None

        if time_s is None:
            depth = max_depth or self.default_depth
            value, move = self.search_fixed_depth(game, depth)
            self.last_stats = {"nodes": self.nodes, "depth": depth, "value": value}
            return move

        # iterative deepening theo thời gian
        start = time.perf_counter()
        self._deadline = start + time_s
        best_move = self._ordered(game)[0]
        best_value, done_depth = None, 0
        try:
            for d in range(1, (max_depth or ROWS * COLS) + 1):
                value, move = self.search_fixed_depth(game, d, first=best_move)
                best_move, best_value, done_depth = move, value, d
                if abs(value) >= WIN - ROWS * COLS:  # đã thấy thắng/thua cưỡng bức: không cần sâu thêm
                    break
                if time.perf_counter() > self._deadline:
                    break
        except _Timeout:
            pass
        finally:
            self._deadline = None
        self.last_stats = {"nodes": self.nodes, "depth": done_depth, "value": best_value}
        return best_move
