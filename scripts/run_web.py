#!/usr/bin/env python3
"""Script khởi chạy nhanh giao diện Web của Connect Four AI."""
from __future__ import annotations

import argparse
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.ui.web_server import run_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chạy Web Server Connect Four AI")
    parser.add_argument("--host", default="0.0.0.0", help="Địa chỉ IP host")
    parser.add_argument("--port", type=int, default=5000, help="Cổng port (mặc định 5000)")
    parser.add_argument("--no-browser", action="store_true", help="Không tự mở trình duyệt")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port, open_browser=not args.no_browser)
