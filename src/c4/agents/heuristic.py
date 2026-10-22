"""Cấp 2 - Heuristic theo luật (có thứ tự ưu tiên rõ ràng).

Thứ tự ưu tiên (dừng ở luật đầu tiên áp dụng được):
  1. THẮNG NGAY      : nếu có nước tạo 4 quân liên tiếp thì đi.
  2. CHẶN            : nếu đối thủ có nước thắng ngay thì chặn (nếu đối thủ có 2 ô thắng - đòn kép -
                       không thể chặn cả hai, chọn cái ưu tiên theo trung tâm: đây là điểm yếu cố hữu).
  3. TRÁNH TẠO THẾ   : loại các nước khiến đối thủ có nước thắng ngay ở ô ngay phía trên.
  4. TRUNG TÂM       : trong các nước còn lại, ưu tiên cột theo thứ tự 3,2,4,1,5,0,6.

Xung đột luật: luật 2 luôn thắng luật 3 (chặn bắt buộc dù nước chặn có thể tạo thế cho đối thủ ngay phía
trên). Nếu MỌI nước đều bị luật 3 loại, chọn theo luật 4 trong toàn bộ nước hợp lệ.
`last_stats["rule"]` ghi lại luật đã dùng ("win" / "block" / "safe" / "forced") để phân tích sau này.
"""
from __future__ import annotations

from c4.agents.base import Agent, Budget
from c4.game.base import CENTER_FIRST, Connect4Base


def _center_order(cols) -> list[int]:
    s = set(cols)
    return [c for c in CENTER_FIRST if c in s]


class HeuristicAgent(Agent):
    name = "heuristic"

    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        legal = game.legal_actions()

        wins = game.winning_moves()
        if wins:
            self.last_stats = {"rule": "win"}
            return _center_order(wins)[0]

        blocks = game.winning_moves(-game.current_player)
        if blocks:
            self.last_stats = {"rule": "block", "double_threat": len(blocks) > 1}
            return _center_order(blocks)[0]

        safe = []
        for c in _center_order(legal):
            game.step(c)
            gives_win = bool(game.winning_moves())  # lúc này tới lượt đối thủ
            game.undo()
            if not gives_win:
                safe.append(c)
        if safe:
            self.last_stats = {"rule": "safe"}
            return safe[0]
        self.last_stats = {"rule": "forced"}
        return _center_order(legal)[0]
