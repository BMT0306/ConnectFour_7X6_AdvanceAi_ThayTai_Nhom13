"""Giao diện đồ họa (GUI) Connect Four bằng Pygame.

Các tính năng nổi bật:
- Đồ họa hiện đại (Dark theme cao cấp, hiệu ứng 3D đổ bóng và highlight cho quân cờ).
- Animation thả quân vật lý chân thực (gia tốc trọng lực và độ nảy khi tiếp đất).
- Đánh dấu 4 quân chiến thắng bằng vệt sáng laser và vòng hào quang.
- Hỗ trợ 3 chế độ chơi: Người vs Máy, Máy vs Máy, Người vs Người.
- Cho phép chọn mọi cấp độ AI:
  + Cấp 1: Random Baseline
  + Cấp 2: Heuristic Rule-Based
  + Cấp 3: Alpha-Beta Pruning (Negamax)
  + Cấp 4: Monte Carlo Tree Search (UCT)
  + Cấp 5: Deep Convolutional Neural Network (CNN)
  + Cấp mở rộng: Mixed MCTS (PUCT)
- Bảng điều khiển trực quan: hiển thị độ trễ, số nút/mô phỏng duyệt, nút Hoàn tác (Undo) và Ván mới.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Optional

DATABASE_FILE = Path(__file__).resolve().parents[3] / "results" / "elo_ratings.json"


def get_elo_dict() -> dict[str, float]:
    """Lấy điểm Elo hiện tại từ database kết quả thi đấu."""
    if DATABASE_FILE.exists():
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                return {k: float(v.get("elo", 1500.0)) for k, v in d.get("ratings", {}).items()}
        except Exception:
            pass
    return {
        "random": 1000.0,
        "heuristic": 1822.2,
        "nn": 1922.3,
        "mcts": 2004.3,
        "alphabeta": 2113.1,
        "mixed_mcts": 2114.8,
    }

if sys.platform == "win32":
    os.environ.setdefault("SDL_VIDEO_CENTERED", "1")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pygame

from c4.agents import Budget, make_agent
from c4.game import COLS, PLAYER1, PLAYER2, ROWS, Connect4

# ----------------- CẤU HÌNH BẢNG MÀU VÀ KÍCH THƯỚC -----------------
WINDOW_WIDTH = 1040
WINDOW_HEIGHT = 720
FPS = 60

# Palette màu sắc hiện đại
COLOR_BG = (15, 23, 42)          # Slate tối (#0F172A)
COLOR_PANEL = (30, 41, 59)       # Slate nhạt (#1E293B)
COLOR_PANEL_BORDER = (51, 65, 85)
COLOR_BOARD = (30, 58, 138)      # Blue đậm (#1E3A8A)
COLOR_BOARD_SHADOW = (15, 23, 42)
COLOR_SLOT_EMPTY = (15, 23, 42)
COLOR_RED = (239, 68, 68)        # Đỏ Ruby (#EF4444)
COLOR_RED_HIGHLIGHT = (252, 165, 165)
COLOR_YELLOW = (245, 158, 11)    # Vàng Hổ Phách (#F59E0B)
COLOR_YELLOW_HIGHLIGHT = (253, 230, 138)
COLOR_WHITE = (248, 250, 252)
COLOR_MUTED = (148, 163, 184)
COLOR_ACCENT = (14, 165, 233)    # Cyan (#0EA5E9)
COLOR_ACCENT_HOVER = (56, 189, 248)
COLOR_WIN_GLOW = (52, 211, 153)  # Emerald (#34D399)

# Kích thước bàn cờ
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 130
SLOT_SIZE = 82
RADIUS = 35


class FallingPiece:
    """Quân cờ đang rơi với mô phỏng vật lý (trọng lực + nảy)."""

    def __init__(self, col: int, target_row: int, player: int):
        self.col = col
        self.target_row = target_row
        self.player = player
        self.x = BOARD_OFFSET_X + col * SLOT_SIZE + SLOT_SIZE // 2
        self.target_y = BOARD_OFFSET_Y + (ROWS - 1 - target_row) * SLOT_SIZE + SLOT_SIZE // 2
        self.y = BOARD_OFFSET_Y - 40.0
        self.vy = 0.0
        self.gravity = 1400.0  # px / s^2
        self.bounce_factor = -0.32
        self.bounces = 0
        self.is_done = False

    def update(self, dt: float) -> None:
        if self.is_done:
            return
        self.vy += self.gravity * dt
        self.y += self.vy * dt
        if self.y >= self.target_y:
            self.y = self.target_y
            if abs(self.vy) > 80.0 and self.bounces < 2:
                self.vy *= self.bounce_factor
                self.bounces += 1
            else:
                self.vy = 0.0
                self.is_done = True


class Connect4GUI:
    """Ứng dụng Pygame Connect Four hoàn chỉnh."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Connect Four AI (7x6 Bitboard)")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_title = pygame.font.SysFont("segoeui,arial", 28, bold=True)
        self.font_header = pygame.font.SysFont("segoeui,arial", 20, bold=True)
        self.font_main = pygame.font.SysFont("segoeui,arial", 16)
        self.font_bold = pygame.font.SysFont("segoeui,arial", 16, bold=True)
        self.font_small = pygame.font.SysFont("segoeui,arial", 13)

        # Trạng thái game
        self.game = Connect4()
        self.mode = "H_VS_AI"  # "H_VS_AI", "AI_VS_AI", "H_VS_H"
        self.human_player = PLAYER1  # PLAYER1 (+1: Đỏ đi trước) hoặc PLAYER2 (-1: Vàng đi sau)
        self.ai_agent_name = "alphabeta"  # Máy 1 (Đỏ) hoặc Máy đối thủ khi H_VS_AI
        self.ai_agent_name_p2 = "mixed_mcts"  # Máy 2 (Vàng) khi AI_VS_AI
        self.active_ai_picker = 1  # 1 cho Máy 1 (Đỏ), 2 cho Máy 2 (Vàng)
        self.ai_budget = Budget(depth=5, simulations=1000, time_s=0.2)
        self.agent = make_agent(self.ai_agent_name)
        self.agent_p2 = make_agent(self.ai_agent_name_p2)

        self.falling_piece: Optional[FallingPiece] = None
        self.winning_coords: list[tuple[int, int]] = []
        self.hover_col = 3
        self.last_ai_time_ms = 0.0
        self.last_ai_stats = ""
        self.is_thinking = False
        self.paused = False
        self.battle_started = False
        self.elo_processed = False
        self.last_elo_msg = ""
        self.random_opening_mode = True  # Mặc định bật thế cờ ngẫu nhiên cho Solo để ván cờ không bị lặp lại
        self.elo_dict = get_elo_dict()

    def reset_game(self, force_empty: bool = False) -> None:
        self.game.reset()
        self.falling_piece = None
        self.winning_coords.clear()
        self.last_ai_time_ms = 0.0
        self.last_ai_stats = ""
        self.is_thinking = False
        self.paused = False
        self.battle_started = False
        self.elo_processed = False
        self.last_elo_msg = ""
        self.elo_dict = get_elo_dict()
        if self.random_opening_mode and not force_empty and self.mode == "AI_VS_AI":
            import random
            rng = random.Random()
            for _ in range(4):
                if not self.game.is_terminal():
                    legal = self.game.legal_actions()
                    if legal:
                        self.game.step(rng.choice(legal))

    def apply_random_opening(self, plies: int = 4) -> None:
        """Tạo thế cờ khai cuộc ngẫu nhiên gồm `plies` nước để mỗi ván đấu là một kịch bản hoàn toàn mới."""
        self.reset_game(force_empty=True)
        import random
        rng = random.Random()
        for _ in range(plies):
            if not self.game.is_terminal():
                legal = self.game.legal_actions()
                if legal:
                    self.game.step(rng.choice(legal))
        self.battle_started = False

    def change_agent(self, name: str, slot: int = 1) -> None:
        if slot == 1:
            self.ai_agent_name = name
            self.agent = make_agent(name)
        else:
            self.ai_agent_name_p2 = name
            self.agent_p2 = make_agent(name)
        self.reset_game()

    def update_elo_on_game_end(self) -> str:
        """Cập nhật biến động Elo thật vào database khi trận solo AI vs AI kết thúc."""
        if not DATABASE_FILE.exists():
            return ""
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            ratings = data.get("ratings", {})
            p1_name = self.ai_agent_name
            p2_name = self.ai_agent_name_p2
            if p1_name not in ratings or p2_name not in ratings:
                return ""
            if p1_name == p2_name:
                return f"Self-play ({p1_name}): Elo không đổi"
            r1 = ratings[p1_name]["elo"]
            r2 = ratings[p2_name]["elo"]
            e1 = 1.0 / (1.0 + 10.0 ** ((r2 - r1) / 400.0))
            w = self.game.winner
            s1 = 1.0 if w == PLAYER1 else (0.5 if w == 0 else 0.0)
            delta = round(32.0 * (s1 - e1), 1)
            ratings[p1_name]["elo"] = round(r1 + delta, 1)
            ratings[p2_name]["elo"] = round(r2 - delta, 1)
            ratings[p1_name]["total_games"] = ratings[p1_name].get("total_games", 0) + 1
            ratings[p2_name]["total_games"] = ratings[p2_name].get("total_games", 0) + 1
            if s1 == 1.0:
                ratings[p1_name]["wins"] = ratings[p1_name].get("wins", 0) + 1
                ratings[p2_name]["losses"] = ratings[p2_name].get("losses", 0) + 1
            elif s1 == 0.0:
                ratings[p2_name]["wins"] = ratings[p2_name].get("wins", 0) + 1
                ratings[p1_name]["losses"] = ratings[p1_name].get("losses", 0) + 1
            else:
                ratings[p1_name]["draws"] = ratings[p1_name].get("draws", 0) + 1
                ratings[p2_name]["draws"] = ratings[p2_name].get("draws", 0) + 1
            for p in (p1_name, p2_name):
                tg = ratings[p]["total_games"]
                pts = ratings[p].get("wins", 0) + 0.5 * ratings[p].get("draws", 0)
                ratings[p]["score_pct"] = round((pts / max(tg, 1)) * 100.0, 2)
            data["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(DATABASE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.elo_dict = {k: float(v.get("elo", 1500.0)) for k, v in ratings.items()}
            sign = "+" if delta >= 0 else ""
            return f"Elo: {p1_name} ({sign}{delta}) | {p2_name} ({-delta:+.1f})"
        except Exception:
            return ""

    def find_winning_quad(self) -> list[tuple[int, int]]:
        """Tìm 4 ô liên tiếp tạo thành chiến thắng để highlight."""
        if self.game.winner == 0:
            return []
        arr = self.game.to_array()
        w = self.game.winner
        # Kiểm tra ngang
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(arr[r, c + i] == w for i in range(4)):
                    return [(r, c + i) for i in range(4)]
        # Kiểm tra dọc
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(arr[r + i, c] == w for i in range(4)):
                    return [(r + i, c) for i in range(4)]
        # Kiểm tra chéo lên
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(arr[r + i, c + i] == w for i in range(4)):
                    return [(r + i, c + i) for i in range(4)]
        # Kiểm tra chéo xuống
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(arr[r - i, c + i] == w for i in range(4)):
                    return [(r - i, c + i) for i in range(4)]
        return []

    def handle_ai_turn(self) -> None:
        """Thực thi nước đi của máy."""
        if self.game.is_terminal() or self.falling_piece is not None:
            return

        current = self.game.current_player
        is_ai = False
        active_agent = self.agent

        if self.mode == "H_VS_AI" and current == -self.human_player:
            is_ai = True
            active_agent = self.agent
        elif self.mode == "AI_VS_AI":
            if not self.battle_started:
                return
            is_ai = True
            active_agent = self.agent if current == PLAYER1 else self.agent_p2

        if is_ai and not self.paused:
            self.is_thinking = True
            self.draw()
            pygame.display.flip()

            if active_agent.name == "alphabeta":
                budget = Budget(depth=5)
            elif active_agent.name == "mixed_mcts":
                budget = Budget(simulations=200)
            elif active_agent.name == "mcts":
                budget = Budget(simulations=1000)
            else:
                budget = Budget()

            t0 = time.perf_counter()
            col = active_agent.choose_action(self.game.clone(), budget)
            dt = (time.perf_counter() - t0) * 1000.0

            self.last_ai_time_ms = dt
            self.last_ai_stats = str(active_agent.last_stats)
            self.is_thinking = False

            # Tìm hàng rơi
            arr = self.game.to_array()
            target_row = 0
            for r in range(ROWS):
                if arr[r, col] == 0:
                    target_row = r
                    break

            self.falling_piece = FallingPiece(col, target_row, current)

    def draw_disc(self, surface: pygame.Surface, x: int, y: int, radius: int, player: int, alpha: int = 255) -> None:
        """Vẽ quân cờ bóng bẩy với hiệu ứng 3D gradient và specular highlight."""
        if player == 0:
            return
        base_color = COLOR_RED if player == PLAYER1 else COLOR_YELLOW
        highlight_color = COLOR_RED_HIGHLIGHT if player == PLAYER1 else COLOR_YELLOW_HIGHLIGHT

        if alpha < 255:
            # Ghost preview
            s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*base_color, alpha), (radius, radius), radius)
            surface.blit(s, (x - radius, y - radius))
            return

        # Viền bóng đổ
        pygame.draw.circle(surface, (10, 10, 20), (x, y + 3), radius)
        # Thân quân cờ
        pygame.draw.circle(surface, base_color, (x, y), radius)
        # Vòng viền bên trong
        pygame.draw.circle(surface, (0, 0, 0, 40), (x, y), radius, 2)
        # Ánh sáng phản xạ (specular 3D highlight)
        hl_pos = (x - radius // 3, y - radius // 3)
        pygame.draw.circle(surface, highlight_color, hl_pos, radius // 3)

    def draw_board(self) -> None:
        """Vẽ khung bàn cờ 7x6 và các quân cờ tĩnh."""
        board_w = COLS * SLOT_SIZE
        board_h = ROWS * SLOT_SIZE
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, board_w, board_h)

        # Đổ bóng bàn cờ
        shadow_rect = pygame.Rect(BOARD_OFFSET_X + 6, BOARD_OFFSET_Y + 8, board_w, board_h)
        pygame.draw.rect(self.screen, COLOR_BOARD_SHADOW, shadow_rect, border_radius=18)

        # Mặt phẳng bàn cờ
        pygame.draw.rect(self.screen, COLOR_BOARD, board_rect, border_radius=18)
        pygame.draw.rect(self.screen, (59, 130, 246), board_rect, width=3, border_radius=18)

        arr = self.game.to_array()
        anim_col = self.falling_piece.col if self.falling_piece else -1
        anim_row = self.falling_piece.target_row if self.falling_piece else -1

        for c in range(COLS):
            for r in range(ROWS):
                cx = BOARD_OFFSET_X + c * SLOT_SIZE + SLOT_SIZE // 2
                cy = BOARD_OFFSET_Y + (ROWS - 1 - r) * SLOT_SIZE + SLOT_SIZE // 2

                # Vẽ lỗ cờ rỗng
                pygame.draw.circle(self.screen, COLOR_SLOT_EMPTY, (cx, cy), RADIUS)
                pygame.draw.circle(self.screen, (15, 23, 42), (cx, cy), RADIUS, 2)

                # Vẽ quân cờ tĩnh đã hạ cánh
                p = arr[r, c]
                if p != 0 and not (c == anim_col and r == anim_row and self.falling_piece):
                    self.draw_disc(self.screen, cx, cy, RADIUS - 2, p)

        # Vẽ quân cờ đang rơi (animation)
        if self.falling_piece:
            self.draw_disc(self.screen, int(self.falling_piece.x), int(self.falling_piece.y), RADIUS - 2, self.falling_piece.player)

        # Vẽ preview quân cờ hover ở trên bàn cờ
        if not self.game.is_terminal() and not self.falling_piece and self.mode != "AI_VS_AI":
            if (self.mode == "H_VS_AI" and self.game.current_player == self.human_player) or self.mode == "H_VS_H":
                if self.hover_col in self.game.legal_actions():
                    hx = BOARD_OFFSET_X + self.hover_col * SLOT_SIZE + SLOT_SIZE // 2
                    hy = BOARD_OFFSET_Y - 45
                    self.draw_disc(self.screen, hx, hy, RADIUS - 4, self.game.current_player, alpha=180)

        # Highlight 4 quân thắng
        if self.winning_coords:
            glow_time = time.perf_counter() * 6.0
            pulse = int(180 + 75 * math.sin(glow_time))
            for r, c in self.winning_coords:
                cx = BOARD_OFFSET_X + c * SLOT_SIZE + SLOT_SIZE // 2
                cy = BOARD_OFFSET_Y + (ROWS - 1 - r) * SLOT_SIZE + SLOT_SIZE // 2
                pygame.draw.circle(self.screen, (*COLOR_WIN_GLOW, pulse), (cx, cy), RADIUS + 4, width=4)

    def draw_sidebar(self) -> None:
        """Vẽ thanh điều khiển và thống kê bên phải."""
        panel_x = 650
        panel_y = 25
        panel_w = 350
        panel_h = 665

        # Card nền Sidebar
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect, border_radius=16)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, panel_rect, width=2, border_radius=16)

        # 1. Header
        title = self.font_title.render("CONNECT FOUR AI", True, COLOR_WHITE)
        self.screen.blit(title, (panel_x + 20, panel_y + 14))
        pygame.draw.line(self.screen, COLOR_PANEL_BORDER, (panel_x + 20, panel_y + 46), (panel_x + panel_w - 20, panel_y + 46))

        # 2. Game Status (Section 1)
        status_y = 78
        lbl_status = self.font_header.render("Trạng Thái Trận Đấu", True, COLOR_ACCENT)
        self.screen.blit(lbl_status, (panel_x + 20, status_y))

        if self.game.is_terminal():
            if self.game.winner == 0:
                msg = "KẾT QUẢ: HÒA CỜ!"
                col = COLOR_MUTED
            else:
                winner_name = "ĐỎ (MÁY 1 / P1)" if self.game.winner == PLAYER1 else "VÀNG (MÁY 2 / P2)"
                msg = f"CHIẾN THẮNG: {winner_name}"
                col = COLOR_RED if self.game.winner == PLAYER1 else COLOR_YELLOW
        else:
            curr_str = "Đỏ đi (P1)" if self.game.current_player == PLAYER1 else "Vàng đi (P2)"
            msg = f"Lượt chơi: {curr_str}"
            col = COLOR_RED if self.game.current_player == PLAYER1 else COLOR_YELLOW
            if self.is_thinking:
                msg += " (Đang suy nghĩ...)"

        txt_msg = self.font_bold.render(msg, True, col)
        self.screen.blit(txt_msg, (panel_x + 20, status_y + 24))

        # Move count & Turn badge
        info_str = f"Tổng số nước: {self.game.move_count} / 42"
        if self.mode == "H_VS_AI":
            side_txt = "Phe bạn: Đỏ [S đổi bên]" if self.human_player == PLAYER1 else "Phe bạn: Vàng [S đổi bên]"
            info_str += f"  •  {side_txt}"
        elif self.mode == "AI_VS_AI" and self.last_elo_msg:
            info_str += f"  •  {self.last_elo_msg}"
        self.screen.blit(self.font_small.render(info_str, True, COLOR_MUTED), (panel_x + 20, status_y + 46))

        # 3. Mode selector (Section 2)
        mode_y = 154
        self.screen.blit(self.font_header.render("Chế Độ Chơi", True, COLOR_ACCENT), (panel_x + 20, mode_y))

        modes = [("H_VS_AI", "Người vs Máy"), ("AI_VS_AI", "Máy vs Máy"), ("H_VS_H", "Người vs Người")]
        for i, (m_code, m_label) in enumerate(modes):
            btn_rect = pygame.Rect(panel_x + 20 + i * 106, mode_y + 28, 98, 32)
            is_active = self.mode == m_code
            bg_col = (14, 165, 233) if is_active else (51, 65, 85)
            pygame.draw.rect(self.screen, bg_col, btn_rect, border_radius=6)
            txt = self.font_small.render(m_label, True, COLOR_WHITE)
            self.screen.blit(txt, (btn_rect.centerx - txt.get_width() // 2, btn_rect.centery - txt.get_height() // 2))

        # 4. AI Level Picker (Section 3)
        ai_y = 236
        elo_dict = self.elo_dict

        ai_levels = [
            ("random", "Cấp 1: Random"),
            ("heuristic", "Cấp 2: Heuristic"),
            ("alphabeta", "Cấp 3: Alpha-Beta"),
            ("mcts", "Cấp 4: MCTS"),
            ("nn", "Cấp 5: ResNet"),
            ("mixed_mcts", "Cấp 6: Mixed-MCTS"),
        ]

        if self.mode == "AI_VS_AI":
            self.screen.blit(self.font_header.render("Chọn Cấp Độ Solo (Máy vs Máy)", True, COLOR_ACCENT), (panel_x + 20, ai_y))

            # 2 Tabs lớn để chọn cấu hình cho Máy 1 (Đỏ) hoặc Máy 2 (Vàng)
            tab1_rect = pygame.Rect(panel_x + 20, ai_y + 28, 150, 32)
            tab2_rect = pygame.Rect(panel_x + 180, ai_y + 28, 150, 32)

            t1_active = self.active_ai_picker == 1
            t1_bg = (185, 28, 28) if t1_active else (51, 65, 85)
            pygame.draw.rect(self.screen, t1_bg, tab1_rect, border_radius=6)
            if t1_active:
                pygame.draw.rect(self.screen, COLOR_RED, tab1_rect, width=2, border_radius=6)
            # Vẽ hình tròn vector đỏ thay vì emoji để tránh lỗi ô chữ nhật
            pygame.draw.circle(self.screen, COLOR_RED, (tab1_rect.x + 16, tab1_rect.centery), 6)
            pygame.draw.circle(self.screen, COLOR_WHITE, (tab1_rect.x + 16, tab1_rect.centery), 6, width=1)
            t1_txt = self.font_small.render(f"Máy 1: {self.ai_agent_name[:8]}", True, COLOR_WHITE)
            self.screen.blit(t1_txt, (tab1_rect.x + 28, tab1_rect.centery - t1_txt.get_height() // 2))

            t2_active = self.active_ai_picker == 2
            t2_bg = (180, 83, 9) if t2_active else (51, 65, 85)
            pygame.draw.rect(self.screen, t2_bg, tab2_rect, border_radius=6)
            if t2_active:
                pygame.draw.rect(self.screen, COLOR_YELLOW, tab2_rect, width=2, border_radius=6)
            # Vẽ hình tròn vector vàng thay vì emoji
            pygame.draw.circle(self.screen, COLOR_YELLOW, (tab2_rect.x + 16, tab2_rect.centery), 6)
            pygame.draw.circle(self.screen, COLOR_WHITE, (tab2_rect.x + 16, tab2_rect.centery), 6, width=1)
            t2_txt = self.font_small.render(f"Máy 2: {self.ai_agent_name_p2[:8]}", True, COLOR_WHITE)
            self.screen.blit(t2_txt, (tab2_rect.x + 28, tab2_rect.centery - t2_txt.get_height() // 2))

            # Nhãn chỉ dẫn đang chọn slot nào
            slot_name = "MÁY 1 (Quân ĐỎ - Đi trước)" if self.active_ai_picker == 1 else "MÁY 2 (Quân VÀNG - Đi sau)"
            slot_col = COLOR_RED if self.active_ai_picker == 1 else COLOR_YELLOW
            self.screen.blit(self.font_small.render(f"Đang chọn cho: {slot_name}", True, slot_col), (panel_x + 20, ai_y + 66))

            btn_start_y = ai_y + 88
            current_choice = self.ai_agent_name if self.active_ai_picker == 1 else self.ai_agent_name_p2

            for i, (a_code, a_label) in enumerate(ai_levels):
                col_idx = i % 2
                row_idx = i // 2
                btn_rect = pygame.Rect(panel_x + 20 + col_idx * 160, btn_start_y + row_idx * 29, 150, 26)
                is_active = current_choice == a_code
                if is_active:
                    bg_col = (220, 38, 38) if self.active_ai_picker == 1 else (217, 119, 6)
                else:
                    bg_col = (51, 65, 85)
                pygame.draw.rect(self.screen, bg_col, btn_rect, border_radius=6)
                elo_val = elo_dict.get(a_code, 1500.0)
                txt = self.font_small.render(f"{a_label} ({elo_val:.0f})", True, COLOR_WHITE)
                self.screen.blit(txt, (btn_rect.centerx - txt.get_width() // 2, btn_rect.centery - txt.get_height() // 2))

            # Nút chọn chế độ Khai cuộc nằm gọn gàng bên dưới 6 cấp độ
            btn_open_rect = pygame.Rect(panel_x + 20, btn_start_y + 3 * 29 + 6, panel_w - 40, 28)
            if self.random_opening_mode:
                pygame.draw.rect(self.screen, (16, 185, 129), btn_open_rect, border_radius=6)
                lbl_open = self.font_small.render("Khai cuộc: 4 NƯỚC NGẪU NHIÊN (Phím O)", True, COLOR_WHITE)
            else:
                pygame.draw.rect(self.screen, (71, 85, 105), btn_open_rect, border_radius=6)
                lbl_open = self.font_small.render("Khai cuộc: BÀN CỜ TRỐNG (Phím O)", True, COLOR_WHITE)
            self.screen.blit(lbl_open, (btn_open_rect.centerx - lbl_open.get_width() // 2, btn_open_rect.centery - lbl_open.get_height() // 2))

        elif self.mode == "H_VS_AI":
            self.screen.blit(self.font_header.render("Cấp Độ Tác Tử AI (Đối Thủ)", True, COLOR_ACCENT), (panel_x + 20, ai_y))
            btn_start_y = ai_y + 32
            for i, (a_code, a_label) in enumerate(ai_levels):
                col_idx = i % 2
                row_idx = i // 2
                btn_rect = pygame.Rect(panel_x + 20 + col_idx * 160, btn_start_y + row_idx * 42, 150, 36)
                is_active = self.ai_agent_name == a_code
                bg_col = (16, 185, 129) if is_active else (51, 65, 85)
                pygame.draw.rect(self.screen, bg_col, btn_rect, border_radius=6)
                elo_val = elo_dict.get(a_code, 1500.0)
                txt = self.font_small.render(f"{a_label} ({elo_val:.0f})", True, COLOR_WHITE)
                self.screen.blit(txt, (btn_rect.centerx - txt.get_width() // 2, btn_rect.centery - txt.get_height() // 2))
        else:
            self.screen.blit(self.font_header.render("Chế Độ 2 Người Chơi", True, COLOR_ACCENT), (panel_x + 20, ai_y))
            info_hvh = self.font_main.render("Hai người chơi luân phiên thả quân trực tiếp.", True, COLOR_MUTED)
            self.screen.blit(info_hvh, (panel_x + 20, ai_y + 36))

        # 5. AI Analytics / Stats Box (Section 4)
        stats_y = 478
        self.screen.blit(self.font_header.render("Hiệu Năng & Elo", True, COLOR_ACCENT), (panel_x + 20, stats_y))
        box_rect = pygame.Rect(panel_x + 20, stats_y + 26, panel_w - 40, 84)
        pygame.draw.rect(self.screen, (15, 23, 42), box_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, box_rect, width=1, border_radius=8)

        if self.mode == "AI_VS_AI":
            elo1 = elo_dict.get(self.ai_agent_name, 1500.0)
            elo2 = elo_dict.get(self.ai_agent_name_p2, 1500.0)
            # Vẽ chấm tròn vector đỏ và vàng
            pygame.draw.circle(self.screen, COLOR_RED, (box_rect.x + 14, box_rect.y + 16), 5)
            p1_txt = f"Máy 1: {self.agent.name.upper()} ({elo1:.1f} Elo)"
            self.screen.blit(self.font_small.render(p1_txt, True, (252, 165, 165)), (box_rect.x + 26, box_rect.y + 8))

            pygame.draw.circle(self.screen, COLOR_YELLOW, (box_rect.x + 14, box_rect.y + 38), 5)
            p2_txt = f"Máy 2: {self.agent_p2.name.upper()} ({elo2:.1f} Elo)"
            self.screen.blit(self.font_small.render(p2_txt, True, (253, 230, 138)), (box_rect.x + 26, box_rect.y + 30))

            if not self.battle_started:
                status_txt = "CHỜ BẮT ĐẦU"
                status_col = (245, 158, 11)
            elif self.paused:
                status_txt = "TẠM DỪNG (P)"
                status_col = (252, 165, 165)
            else:
                status_txt = "ĐANG THI ĐẤU"
                status_col = (52, 211, 153)
            info_sub = f"Độ trễ: {self.last_ai_time_ms:.1f} ms  •  Trạng thái: {status_txt}"
            self.screen.blit(self.font_small.render(info_sub, True, status_col), (box_rect.x + 12, box_rect.y + 56))
        else:
            lat_txt = f"Thời gian tính nước trước: {self.last_ai_time_ms:.1f} ms"
            self.screen.blit(self.font_small.render(lat_txt, True, (52, 211, 153)), (box_rect.x + 12, box_rect.y + 12))
            elo = elo_dict.get(self.ai_agent_name, 1500.0)
            self.screen.blit(self.font_small.render(f"Tác tử: {self.agent.name.upper()} ({elo:.1f} Elo)", True, COLOR_WHITE), (box_rect.x + 12, box_rect.y + 34))
            stat_short = self.last_ai_stats[:38] + ("..." if len(self.last_ai_stats) > 38 else "")
            self.screen.blit(self.font_small.render(f"Chi tiết: {stat_short}", True, COLOR_MUTED), (box_rect.x + 12, box_rect.y + 56))

        # 6. Action Buttons (Section 5)
        btn_y = 608
        btn_new = pygame.Rect(panel_x + 20, btn_y, 150, 44)
        pygame.draw.rect(self.screen, (239, 68, 68), btn_new, border_radius=8)
        t_new = self.font_bold.render("VÁN MỚI (R)", True, COLOR_WHITE)
        self.screen.blit(t_new, (btn_new.centerx - t_new.get_width() // 2, btn_new.centery - t_new.get_height() // 2))

        btn_action2 = pygame.Rect(panel_x + 180, btn_y, 150, 44)
        if self.mode == "AI_VS_AI":
            if not self.battle_started:
                act_col = (16, 185, 129)  # Emerald green nổi bật
                t_label = "BẮT ĐẦU (Space)"
            elif self.paused:
                act_col = (16, 185, 129)  # Emerald green
                t_label = "TIẾP TỤC (P)"
            else:
                act_col = (217, 119, 6)   # Amber
                t_label = "TẠM DỪNG (P)"
            pygame.draw.rect(self.screen, act_col, btn_action2, border_radius=8)
            t_act = self.font_bold.render(t_label, True, COLOR_WHITE)
        else:
            pygame.draw.rect(self.screen, (100, 116, 139), btn_action2, border_radius=8)
            t_act = self.font_bold.render("ĐI LẠI (U)", True, COLOR_WHITE)
        self.screen.blit(t_act, (btn_action2.centerx - t_act.get_width() // 2, btn_action2.centery - t_act.get_height() // 2))

    def draw(self) -> None:
        self.screen.fill(COLOR_BG)
        # Tiêu đề góc trên bên trái
        header = self.font_title.render("CONNECT FOUR - AI ENGINE", True, COLOR_WHITE)
        self.screen.blit(header, (BOARD_OFFSET_X, 30))

        if self.mode == "AI_VS_AI":
            sub_txt = "Chế độ Solo 2 Máy | Bấm BẮT ĐẦU trên thanh điều khiển để theo dõi thi đấu"
            self.screen.blit(self.font_small.render(sub_txt, True, (56, 189, 248)), (BOARD_OFFSET_X, 68))
        else:
            sub = self.font_small.render("Nhấp chuột vào cột hoặc bấm phím số 1..7 để thả quân", True, COLOR_MUTED)
            self.screen.blit(sub, (BOARD_OFFSET_X, 68))

        self.draw_board()
        self.draw_sidebar()

    def handle_click(self, pos: tuple[int, int]) -> None:
        mx, my = pos

        # 1. Kiểm tra click trên bàn cờ
        if BOARD_OFFSET_X <= mx < BOARD_OFFSET_X + COLS * SLOT_SIZE:
            if not self.game.is_terminal() and self.falling_piece is None and not self.is_thinking:
                col = (mx - BOARD_OFFSET_X) // SLOT_SIZE
                if col in self.game.legal_actions():
                    is_human = False
                    if self.mode == "H_VS_H":
                        is_human = True
                    elif self.mode == "H_VS_AI" and self.game.current_player == self.human_player:
                        is_human = True

                    if is_human:
                        # Tìm target row
                        arr = self.game.to_array()
                        target_row = 0
                        for r in range(ROWS):
                            if arr[r, col] == 0:
                                target_row = r
                                break
                        self.falling_piece = FallingPiece(col, target_row, self.game.current_player)
                        return

        # 2. Click trên sidebar
        panel_x = 650
        panel_w = 350

        # Check Mode buttons
        mode_y = 154
        modes = ["H_VS_AI", "AI_VS_AI", "H_VS_H"]
        for i, m_code in enumerate(modes):
            r = pygame.Rect(panel_x + 20 + i * 106, mode_y + 28, 98, 32)
            if r.collidepoint(mx, my):
                self.mode = m_code
                self.reset_game()
                return

        # Check AI Level buttons & Tabs
        ai_y = 236
        ai_levels = ["random", "heuristic", "alphabeta", "mcts", "nn", "mixed_mcts"]

        if self.mode == "AI_VS_AI":
            tab1_rect = pygame.Rect(panel_x + 20, ai_y + 28, 150, 32)
            tab2_rect = pygame.Rect(panel_x + 180, ai_y + 28, 150, 32)
            if tab1_rect.collidepoint(mx, my):
                self.active_ai_picker = 1
                return
            if tab2_rect.collidepoint(mx, my):
                self.active_ai_picker = 2
                return

            btn_start_y = ai_y + 88
            for i, a_code in enumerate(ai_levels):
                col_idx = i % 2
                row_idx = i // 2
                r = pygame.Rect(panel_x + 20 + col_idx * 160, btn_start_y + row_idx * 29, 150, 26)
                if r.collidepoint(mx, my):
                    self.change_agent(a_code, slot=self.active_ai_picker)
                    return

            # Check nút Khai cuộc
            btn_open_rect = pygame.Rect(panel_x + 20, btn_start_y + 3 * 29 + 6, panel_w - 40, 28)
            if btn_open_rect.collidepoint(mx, my):
                self.random_opening_mode = not self.random_opening_mode
                if self.random_opening_mode:
                    self.apply_random_opening(4)
                else:
                    self.reset_game(force_empty=True)
                return

        elif self.mode == "H_VS_AI":
            btn_start_y = ai_y + 32
            for i, a_code in enumerate(ai_levels):
                col_idx = i % 2
                row_idx = i // 2
                r = pygame.Rect(panel_x + 20 + col_idx * 160, btn_start_y + row_idx * 42, 150, 36)
                if r.collidepoint(mx, my):
                    self.change_agent(a_code, slot=1)
                    return

        # Check Action Buttons
        btn_y = 608
        btn_new = pygame.Rect(panel_x + 20, btn_y, 150, 44)
        if btn_new.collidepoint(mx, my):
            self.reset_game()
            return

        btn_action2 = pygame.Rect(panel_x + 180, btn_y, 150, 44)
        if btn_action2.collidepoint(mx, my):
            if self.mode == "AI_VS_AI":
                if not self.battle_started:
                    self.battle_started = True
                    self.paused = False
                else:
                    self.paused = not self.paused
            else:
                self.undo_move()
            return

    def undo_move(self) -> None:
        """Hoàn tác nước đi (2 nước nếu đang đấu với AI)."""
        if self.falling_piece is not None:
            return
        if self.mode == "H_VS_AI":
            if self.game.move_count >= 2:
                self.game.undo()
                self.game.undo()
            elif self.game.move_count == 1:
                self.game.undo()
        else:
            if self.game.move_count >= 1:
                self.game.undo()
        self.winning_coords.clear()

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            # Cập nhật animation
            if self.falling_piece:
                self.falling_piece.update(dt)
                if self.falling_piece.is_done:
                    self.game.step(self.falling_piece.col)
                    self.falling_piece = None
                    if self.game.is_terminal():
                        self.winning_coords = self.find_winning_quad()
                        if not self.elo_processed and self.mode == "AI_VS_AI":
                            self.elo_processed = True
                            self.battle_started = False
                            self.last_elo_msg = self.update_elo_on_game_end()

            # Lấy vị trí chuột cho hover
            mx, my = pygame.mouse.get_pos()
            if BOARD_OFFSET_X <= mx < BOARD_OFFSET_X + COLS * SLOT_SIZE:
                self.hover_col = (mx - BOARD_OFFSET_X) // SLOT_SIZE

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_o and self.mode == "AI_VS_AI":
                        self.random_opening_mode = not self.random_opening_mode
                        if self.random_opening_mode:
                            self.apply_random_opening(4)
                        else:
                            self.reset_game(force_empty=True)
                    elif event.key in (pygame.K_p, pygame.K_SPACE) and self.mode == "AI_VS_AI":
                        if not self.battle_started:
                            self.battle_started = True
                            self.paused = False
                        else:
                            self.paused = not self.paused
                    elif event.key == pygame.K_s and self.mode == "H_VS_AI":
                        self.human_player = -self.human_player
                        self.reset_game()
                    elif event.key == pygame.K_u:
                        self.undo_move()
                    elif pygame.K_1 <= event.key <= pygame.K_7:
                        col = event.key - pygame.K_1
                        can_human_play = (
                            self.mode == "H_VS_H"
                            or (self.mode == "H_VS_AI" and self.game.current_player == self.human_player)
                        )
                        if (
                            can_human_play
                            and not self.game.is_terminal()
                            and col in self.game.legal_actions()
                            and not self.falling_piece
                            and not self.is_thinking
                        ):
                            arr = self.game.to_array()
                            target_row = 0
                            for r in range(ROWS):
                                if arr[r, col] == 0:
                                    target_row = r
                                    break
                            self.falling_piece = FallingPiece(col, target_row, self.game.current_player)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            # Máy tự động đi nếu tới lượt
            self.handle_ai_turn()

            # Vẽ màn hình
            self.draw()
            pygame.display.flip()

        pygame.quit()


def main():
    app = Connect4GUI()
    app.run()


if __name__ == "__main__":
    main()
