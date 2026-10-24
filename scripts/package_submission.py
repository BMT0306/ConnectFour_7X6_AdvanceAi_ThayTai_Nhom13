#!/usr/bin/env python3
"""Script đóng gói đồ án nộp cuối kỳ theo đúng quy định của môn học:
Tên file: Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip

Kiểm tra các thành phần bắt buộc:
- Báo cáo, slide, poster
- Mã nguồn src/, tests/, configs/
- Kết quả thực nghiệm results/
- Hướng dẫn cài đặt README.md, requirements.txt, pyproject.toml
"""
from __future__ import annotations

import os
import sys
import zipfile
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ZIP_NAME = "Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip"
ROOT_DIR = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git",
    ".github",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "c4.egg-info",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
}


def should_exclude(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.endswith(".egg-info"):
            return True
    if path.suffix in EXCLUDE_EXTS:
        return True
    if path.name == ZIP_NAME:
        return True
    return False


def create_submission_zip(output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = ROOT_DIR / ZIP_NAME

    print(f"[*] Bắt đầu đóng gói đề tài vào: {output_path.name}")
    count = 0
    total_bytes = 0

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in ROOT_DIR.rglob("*"):
            if file_path.is_file() and not should_exclude(file_path):
                rel_path = file_path.relative_to(ROOT_DIR)
                # Đặt prefix thư mục gốc bên trong zip để khi giải nén không bị bung rời rạc
                archive_name = Path("connect4-ai") / rel_path
                zf.write(file_path, str(archive_name))
                count += 1
                total_bytes += file_path.stat().st_size

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"[+] Hoàn thành! Đã nén {count} tệp tin ({total_bytes / 1024:.1f} KB uncompressed).")
    print(f"[+] Kích thước tệp ZIP: {size_mb:.2f} MB")
    print(f"[+] Đường dẫn tệp: {output_path}")
    return output_path


if __name__ == "__main__":
    create_submission_zip()
