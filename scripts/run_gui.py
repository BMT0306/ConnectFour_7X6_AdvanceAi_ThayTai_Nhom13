#!/usr/bin/env python3
"""Script khởi chạy nhanh giao diện đồ họa Pygame của trò chơi Connect Four."""
from __future__ import annotations

import os
import sys

if sys.platform == "win32":
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.ui.gui import main

if __name__ == "__main__":
    main()
