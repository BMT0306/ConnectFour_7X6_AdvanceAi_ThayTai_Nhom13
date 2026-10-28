"""Web server backend cho Connect Four AI (Nhóm 13).

Cung cấp API RESTful và giao diện web hiện đại, chạy mượt mà trên trình duyệt
và hỗ trợ chạy trong Docker container.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict

from c4.agents import AGENTS, Budget, make_agent
from c4.game import COLS, PLAYER1, PLAYER2, ROWS, Connect4

STATIC_DIR = Path(__file__).resolve().parent / "web_static"


class GameSession:
    """Quản lý trạng thái ván cờ trên web."""

    def __init__(self):
        self.game = Connect4()
        self.history = []

    def reset(self):
        self.game.reset()
        self.history.clear()

    def step(self, col: int) -> bool:
        if col not in self.game.legal_actions():
            return False
        # Lưu lại state để undo
        self.history.append(self.game.clone())
        self.game.step(col)
        return True

    def undo(self) -> bool:
        if not self.history:
            return False
        self.game = self.history.pop()
        return True

    def find_winning_quad(self) -> list[tuple[int, int]]:
        if self.game.winner == 0:
            return []
        arr = self.game.to_array()
        w = self.game.winner
        # Ngang
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(arr[r, c + i] == w for i in range(4)):
                    return [(r, c + i) for i in range(4)]
        # Dọc
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(arr[r + i, c] == w for i in range(4)):
                    return [(r + i, c) for i in range(4)]
        # Chéo chính
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(arr[r + i, c + i] == w for i in range(4)):
                    return [(r + i, c + i) for i in range(4)]
        # Chéo phụ
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(arr[r - i, c + i] == w for i in range(4)):
                    return [(r - i, c + i) for i in range(4)]
        return []

    def to_dict(self) -> Dict[str, Any]:
        arr = self.game.to_array()
        board_list = [[int(arr[r, c]) for c in range(COLS)] for r in range(ROWS)]
        return {
            "board": board_list,
            "current_player": int(self.game.current_player),
            "move_count": int(self.game.move_count),
            "is_terminal": bool(self.game.is_terminal()),
            "winner": int(self.game.winner),
            "legal_actions": self.game.legal_actions(),
            "winning_quad": self.find_winning_quad(),
        }


# Global game session (single-player focus)
SESSION = GameSession()
AGENT_CACHE: Dict[str, Any] = {}


def get_agent(name: str):
    if name not in AGENT_CACHE:
        AGENT_CACHE[name] = make_agent(name)
    return AGENT_CACHE[name]


class Connect4HTTPHandler(BaseHTTPRequestHandler):
    """Xử lý request HTTP cho web app."""

    def _set_headers(self, content_type: str = "application/json", status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status=HTTPStatus.NO_CONTENT)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            index_path = STATIC_DIR / "index.html"
            if index_path.exists():
                with open(index_path, "rb") as f:
                    content = f.read()
                self._set_headers("text/html; charset=utf-8")
                self.wfile.write(content)
                return
            else:
                self._set_headers("text/plain", 404)
                self.wfile.write(b"Static index.html not found.")
                return

        if self.path == "/api/state":
            self._set_headers()
            self.wfile.write(json.dumps(SESSION.to_dict()).encode("utf-8"))
            return

        if self.path == "/api/agents":
            agents_info = [
                {"id": "random", "name": "Random Baseline", "desc": "Nước đi ngẫu nhiên, đối chứng cơ bản", "level": 1},
                {"id": "heuristic", "name": "Rule-Based Heuristic", "desc": "4 tầng luật: Thắng ngay -> Chặn -> Tránh bẫy -> Cột giữa", "level": 2},
                {"id": "alphabeta", "name": "Alpha-Beta Pruning", "desc": "Minimax cắt tỉa 69 cửa sổ + Transposition Table", "level": 3},
                {"id": "mcts", "name": "MCTS-UCT", "desc": "Monte Carlo Tree Search mô phỏng ngẫu nhiên UCB1", "level": 4},
                {"id": "mixed_mcts", "name": "Mixed MCTS / AlphaZero", "desc": "PUCT MCTS + Value Head + Dirichlet Noise", "level": 5},
                {"id": "nn", "name": "Deep CNN Policy", "desc": "Mạng tích chập đánh giá bàn cờ trực tiếp", "level": 5},
            ]
            self._set_headers()
            self.wfile.write(json.dumps({"agents": agents_info}).encode("utf-8"))
            return

        # Phục vụ static file
        rel_path = self.path.lstrip("/")
        file_path = STATIC_DIR / rel_path
        if file_path.exists() and file_path.is_file():
            ext = file_path.suffix.lower()
            mime = "text/plain"
            if ext == ".css":
                mime = "text/css"
            elif ext == ".js":
                mime = "application/javascript"
            elif ext in (".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg"):
                mime = f"image/{ext.lstrip('.')}"
            with open(file_path, "rb") as f:
                content = f.read()
            self._set_headers(mime)
            self.wfile.write(content)
            return

        self._set_headers("text/plain", 404)
        self.wfile.write(b"Not Found")

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            data = json.loads(post_body)
        except Exception:
            data = {}

        if self.path == "/api/reset":
            SESSION.reset()
            self._set_headers()
            self.wfile.write(json.dumps(SESSION.to_dict()).encode("utf-8"))
            return

        if self.path == "/api/undo":
            # Undo 2 lượt nếu đánh với máy (lượt máy + lượt người)
            steps = data.get("steps", 1)
            for _ in range(steps):
                SESSION.undo()
            self._set_headers()
            self.wfile.write(json.dumps(SESSION.to_dict()).encode("utf-8"))
            return

        if self.path == "/api/move":
            col = data.get("col")
            if col is None or not (0 <= col < COLS):
                self._set_headers("application/json", 400)
                self.wfile.write(json.dumps({"error": "Cột không hợp lệ"}).encode("utf-8"))
                return

            ok = SESSION.step(col)
            if not ok:
                self._set_headers("application/json", 400)
                self.wfile.write(json.dumps({"error": "Cột đã đầy"}).encode("utf-8"))
                return

            self._set_headers()
            self.wfile.write(json.dumps(SESSION.to_dict()).encode("utf-8"))
            return

        if self.path == "/api/ai_move":
            if SESSION.game.is_terminal():
                self._set_headers()
                self.wfile.write(json.dumps(SESSION.to_dict()).encode("utf-8"))
                return

            agent_name = data.get("agent", "alphabeta")
            depth = data.get("depth", 5)
            sims = data.get("simulations", 1000)
            time_limit = data.get("time_s", 0.2)

            agent = get_agent(agent_name)
            budget = Budget(depth=depth, simulations=sims, time_s=time_limit)

            t0 = time.perf_counter()
            chosen_col = agent.choose_action(SESSION.game.clone(), budget)
            elapsed_ms = (time.perf_counter() - t0) * 1000

            SESSION.step(chosen_col)

            res = SESSION.to_dict()
            res["ai_col"] = chosen_col
            res["elapsed_ms"] = round(elapsed_ms, 2)
            res["stats"] = getattr(agent, "last_stats", None) or f"{elapsed_ms:.1f} ms"

            self._set_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        self._set_headers("text/plain", 404)
        self.wfile.write(b"Not Found")


def run_server(host: str = "0.0.0.0", port: int = 5000, open_browser: bool = True):
    server = ThreadingHTTPServer((host, port), Connect4HTTPHandler)
    url = f"http://localhost:{port}"
    print("=" * 60)
    print(f"  CONNECT FOUR AI WEB SERVER (NHOM 13)")
    print(f"  Server listening at: {url}")
    print("=" * 60)
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Stopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", help="Host binding")
    parser.add_argument("--port", type=int, default=5000, help="Port binding")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser")
    args = parser.parse_args()

    run_server(args.host, args.port, open_browser=not args.no_browser)
