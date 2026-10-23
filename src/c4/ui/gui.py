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

import math
import sys
import time
from typing import Optional

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
        pygame.display.set_caption("Connect Four AI - Nhóm 13 (7x6 Bitboard)")
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
        self.ai_agent_name = "alphabeta"  # random, heuristic, alphabeta, mcts, nn, mixed_mcts
        self.ai_budget = Budget(depth=5, simulations=1000, time_s=0.2)
        self.agent = make_agent(self.ai_agent_name)
        self.agent_p2 = make_agent("mcts")

        self.falling_piece: Optional[FallingPiece] = None
        self.winning_coords: list[tuple[int, int]] = []
        self.hover_col = 3
        self.last_ai_time_ms = 0.0
        self.last_ai_stats = ""
        self.is_thinking = False
        self.paused = False

    def reset_game(self) -> None:
        self.game.reset()
        self.falling_piece = None
        self.winning_coords.clear()
        self.last_ai_time_ms = 0.0
        self.last_ai_stats = ""
        self.is_thinking = False

    def change_agent(self, name: str) -> None:
        self.ai_agent_name = name
        self.agent = make_agent(name)

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

        if self.mode == "H_VS_AI" and current == PLAYER2:
            is_ai = True
            active_agent = self.agent
        elif self.mode == "AI_VS_AI":
            is_ai = True
            active_agent = self.agent if current == PLAYER1 else self.agent_p2

        if is_ai and not self.paused:
            self.is_thinking = True
            self.draw()
            pygame.display.flip()

            t0 = time.perf_counter()
            col = active_agent.choose_action(self.game.clone(), self.ai_budget)
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
            if (self.mode == "H_VS_AI" and self.game.current_player == PLAYER1) or self.mode == "H_VS_H":
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
        panel_y = 40
        panel_w = 350
        panel_h = 640

        # Card nền Sidebar
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect, border_radius=16)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, panel_rect, width=2, border_radius=16)

        # 1. Header
        title = self.font_title.render("CONNECT FOUR AI", True, COLOR_WHITE)
        self.screen.blit(title, (panel_x + 20, panel_y + 20))
        subtitle = self.font_small.render("Đồ án tốt nghiệp AI nâng cao - Nhóm 13", True, COLOR_MUTED)
        self.screen.blit(subtitle, (panel_x + 20, panel_y + 55))

        pygame.draw.line(self.screen, COLOR_PANEL_BORDER, (panel_x + 20, panel_y + 78), (panel_x + panel_w - 20, panel_y + 78))

        # 2. Game Status
        status_y = panel_y + 90
        lbl_status = self.font_header.render("Trạng Thái Trận Đấu", True, COLOR_ACCENT)
        self.screen.blit(lbl_status, (panel_x + 20, status_y))

        if self.game.is_terminal():
            if self.game.winner == 0:
                msg = "KẾT QUẢ: HÒA CỜ!"
                col = COLOR_MUTED
            else:
                winner_name = "ĐỎ (PLAYER 1)" if self.game.winner == PLAYER1 else "VÀNG (PLAYER 2)"
                msg = f"CHIẾN THẮNG: {winner_name}"
                col = COLOR_RED if self.game.winner == PLAYER1 else COLOR_YELLOW
        else:
            curr_str = "Đỏ đi (P1)" if self.game.current_player == PLAYER1 else "Vàng đi (P2)"
            msg = f"Lượt chơi: {curr_str}"
            col = COLOR_RED if self.game.current_player == PLAYER1 else COLOR_YELLOW
            if self.is_thinking:
                msg += " (Đang suy nghĩ...)"

        txt_msg = self.font_bold.render(msg, True, col)
        self.screen.blit(txt_msg, (panel_x + 20, status_y + 30))

        # Move count & Turn badge
        info_str = f"Tổng số nước: {self.game.move_count} / 42"
        self.screen.blit(self.font_main.render(info_str, True, COLOR_WHITE), (panel_x + 20, status_y + 55))

        # 3. Mode selector
        mode_y = panel_y + 195
        self.screen.blit(self.font_header.render("Chế Độ Chơi", True, COLOR_ACCENT), (panel_x + 20, mode_y))

        modes = [("H_VS_AI", "Người vs Máy"), ("AI_VS_AI", "Máy vs Máy"), ("H_VS_H", "Người vs Người")]
        for i, (m_code, m_label) in enumerate(modes):
            btn_rect = pygame.Rect(panel_x + 20 + i * 102, mode_y + 30, 96, 32)
            is_active = self.mode == m_code
            bg_col = (14, 165, 233) if is_active else (51, 65, 85)
            pygame.draw.rect(self.screen, bg_col, btn_rect, border_radius=6)
            txt = self.font_small.render(m_label, True, COLOR_WHITE)
            self.screen.blit(txt, (btn_rect.centerx - txt.get_width() // 2, btn_rect.centery - txt.get_height() // 2))

        # 4. AI Level Picker
        ai_y = panel_y + 275
        self.screen.blit(self.font_header.render("Cấp Độ Tác Tử AI (Máy)", True, COLOR_ACCENT), (panel_x + 20, ai_y))

        ai_levels = [
            ("random", "Cấp 1: Random"),
            ("heuristic", "Cấp 2: Heuristic"),
            ("alphabeta", "Cấp 3: Alpha-Beta"),
            ("mcts", "Cấp 4: MCTS (UCT)"),
            ("nn", "Cấp 5: Neural Net"),
            ("mixed_mcts", "Mở rộng: Mixed-MCTS"),
        ]

        for i, (a_code, a_label) in enumerate(ai_levels):
            col_idx = i % 2
            row_idx = i // 2
            btn_rect = pygame.Rect(panel_x + 20 + col_idx * 155, ai_y + 30 + row_idx * 38, 145, 30)
            is_active = self.ai_agent_name == a_code
            bg_col = (16, 185, 129) if is_active else (51, 65, 85)
            pygame.draw.rect(self.screen, bg_col, btn_rect, border_radius=6)
            txt = self.font_small.render(a_label, True, COLOR_WHITE)
            self.screen.blit(txt, (btn_rect.centerx - txt.get_width() // 2, btn_rect.centery - txt.get_height() // 2))

        # 5. AI Analytics / Stats Box
        stats_y = panel_y + 420
        self.screen.blit(self.font_header.render("Hiệu Năng & Độ Trễ", True, COLOR_ACCENT), (panel_x + 20, stats_y))
        box_rect = pygame.Rect(panel_x + 20, stats_y + 28, panel_w - 40, 80)
        pygame.draw.rect(self.screen, (15, 23, 42), box_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, box_rect, width=1, border_radius=8)

        lat_txt = f"Thời gian tính nước trước: {self.last_ai_time_ms:.1f} ms"
        self.screen.blit(self.font_small.render(lat_txt, True, (52, 211, 153)), (box_rect.x + 12, box_rect.y + 12))
        stat_short = self.last_ai_stats[:38] + ("..." if len(self.last_ai_stats) > 38 else "")
        self.screen.blit(self.font_small.render(f"Chi tiết: {stat_short}", True, COLOR_MUTED), (box_rect.x + 12, box_rect.y + 35))
        self.screen.blit(self.font_small.render(f"Tác tử: {self.agent.name.upper()}", True, COLOR_WHITE), (box_rect.x + 12, box_rect.y + 55))

        # 6. Action Buttons
        btn_y = panel_y + 545
        # Nút Ván Mới
        btn_new = pygame.Rect(panel_x + 20, btn_y, 145, 42)
        pygame.draw.rect(self.screen, (239, 68, 68), btn_new, border_radius=8)
        t_new = self.font_bold.render("VÁN MỚI (R)", True, COLOR_WHITE)
        self.screen.blit(t_new, (btn_new.centerx - t_new.get_width() // 2, btn_new.centery - t_new.get_height() // 2))

        # Nút Đi Lại (Undo)
        btn_undo = pygame.Rect(panel_x + 180, btn_y, 145, 42)
        pygame.draw.rect(self.screen, (100, 116, 139), btn_undo, border_radius=8)
        t_undo = self.font_bold.render("ĐI LẠI (U)", True, COLOR_WHITE)
        self.screen.blit(t_undo, (btn_undo.centerx - t_undo.get_width() // 2, btn_undo.centery - t_undo.get_height() // 2))

    def draw(self) -> None:
        self.screen.fill(COLOR_BG)
        # Tiêu đề góc trên bên trái
        header = self.font_title.render("CONNECT FOUR - AI TRẬN ĐẤU ĐA CẤP ĐỘ", True, COLOR_WHITE)
        self.screen.blit(header, (BOARD_OFFSET_X, 30))
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
                    elif self.mode == "H_VS_AI" and self.game.current_player == PLAYER1:
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
        panel_y = 40
        # Check Mode buttons
        mode_y = panel_y + 195
        modes = ["H_VS_AI", "AI_VS_AI", "H_VS_H"]
        for i, m_code in enumerate(modes):
            r = pygame.Rect(panel_x + 20 + i * 102, mode_y + 30, 96, 32)
            if r.collidepoint(mx, my):
                self.mode = m_code
                self.reset_game()
                return

        # Check AI Level buttons
        ai_y = panel_y + 275
        ai_levels = ["random", "heuristic", "alphabeta", "mcts", "nn", "mixed_mcts"]
        for i, a_code in enumerate(ai_levels):
            col_idx = i % 2
            row_idx = i // 2
            r = pygame.Rect(panel_x + 20 + col_idx * 155, ai_y + 30 + row_idx * 38, 145, 30)
            if r.collidepoint(mx, my):
                self.change_agent(a_code)
                return

        # Check Ván Mới
        btn_new = pygame.Rect(panel_x + 20, panel_y + 545, 145, 42)
        if btn_new.collidepoint(mx, my):
            self.reset_game()
            return

        # Check Đi Lại (Undo)
        btn_undo = pygame.Rect(panel_x + 180, panel_y + 545, 145, 42)
        if btn_undo.collidepoint(mx, my):
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
                    elif event.key == pygame.K_u:
                        self.undo_move()
                    elif pygame.K_1 <= event.key <= pygame.K_7:
                        col = event.key - pygame.K_1
                        if col in self.game.legal_actions() and not self.falling_piece and not self.is_thinking:
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
