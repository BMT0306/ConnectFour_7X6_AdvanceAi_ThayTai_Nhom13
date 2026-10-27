#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
echo "========================================================"
echo "  DANG KHOI DONG CONNECT FOUR GAME AI (NHOM 13)"
echo "========================================================"
if [ -f ".venv/Scripts/python.exe" ]; then
    ./.venv/Scripts/python.exe scripts/run_gui.py
elif [ -f ".venv/bin/python" ]; then
    ./.venv/bin/python scripts/run_gui.py
else
    python scripts/run_gui.py
fi
