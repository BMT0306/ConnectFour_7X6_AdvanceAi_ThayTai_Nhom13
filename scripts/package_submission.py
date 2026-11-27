#!/usr/bin/env python3
"""Script đóng gói đồ án nộp cuối kỳ theo đúng quy định của môn học:
Tên file: Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip

Kiểm tra tự động các thành phần bắt buộc theo yêu cầu NỘP ĐỀ TÀI CUỐI KỲ:
1. Báo cáo (.docx & .md), Slide thuyết trình (.pptx) và Poster giới thiệu đề tài (.pdf & .pptx)
2. Mã nguồn (src/, tests/, scripts/), file cấu hình (configs/*.yaml) và hướng dẫn cài đặt (README.md, RUN_FAST.bat)
3. Dataset (data/*.npz, dataset_summary.json) & Mô hình huấn luyện (checkpoints/policy_net_best.pt)
4. Tài nguyên liên quan: Notebook (.ipynb), kết quả thực nghiệm (results/), hình ảnh, video demo (DEMO.mp4), tài liệu tham khảo & nhật ký (.xlsx/.csv)
"""
from __future__ import annotations

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

REQUIRED_ITEMS = [
    ("Báo cáo Word (.docx)", "docs/BAO_CAO_DO_AN_CUOI_KY.docx"),
    ("Báo cáo Markdown (.md)", "docs/BAO_CAO_DO_AN_CUOI_KY.md"),
    ("Slide thuyết trình (.pptx)", "docs/SLIDE_THUYET_TRINH_CONNECT_FOUR_NHOM13.pptx"),
    ("Poster in ấn (.pdf)", "docs/POSTER_CONNECT_FOUR_NHOM13.pdf"),
    ("Poster chỉnh sửa (.pptx)", "docs/POSTER_CONNECT_FOUR_NHOM13.pptx"),
    ("Kịch bản trình bày (.md)", "docs/KICH_BAN_TRINH_BAY.md"),
    ("Nhật ký thí nghiệm Excel (.xlsx)", "docs/NHAT_KY_THI_NGHIEM.xlsx"),
    ("Quản lý cộng tác & Nhật ký (.md)", "docs/QUAN_LY_CONG_TAC_VA_NHAT_KY.md"),
    ("Tài liệu nguồn kế thừa (.md)", "docs/THIRD_PARTY.md"),
    ("Hướng dẫn cài đặt & Danh sách nhóm", "README.md"),
    ("Launcher khởi chạy nhanh", "RUN_FAST.bat"),
    ("Mô hình huấn luyện (.pt)", "checkpoints/policy_net_best.pt"),
    ("Dữ liệu huấn luyện (.npz)", "data/train.npz"),
    ("Dữ liệu kiểm tra (.npz)", "data/test.npz"),
    ("Notebook phân tích thực nghiệm", "notebooks/01_tournament_analysis.ipynb"),
    ("Cơ sở dữ liệu xếp hạng Elo", "results/elo_ratings.json"),
    ("Báo cáo kiểm thử tự động", "results/TEST_AND_EVALUATION_REPORT.md"),
]

EXCLUDE_DIRS = {
    ".git",
    ".github",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "c4.egg-info",
    ".vscode",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".zip",
}


def should_exclude(path: Path) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
        if part.endswith(".egg-info"):
            return True
    if path.suffix in EXCLUDE_EXTS:
        return True
    if path.name.startswith("~$") or path.name.endswith(".tmp"):
        return True
    if path.name == ZIP_NAME:
        return True
    return False


def verify_required_deliverables() -> None:
    print("[*] Kiểm tra danh mục sản phẩm bắt buộc trước khi đóng gói:")
    missing = []
    for label, rel in REQUIRED_ITEMS:
        p = ROOT_DIR / rel
        if p.exists():
            sz_kb = p.stat().st_size / 1024
            print(f"    [OK] {label:<36} -> {rel} ({sz_kb:,.1f} KB)")
        else:
            print(f"    [MISSING] {label:<31} -> {rel}")
            missing.append(rel)
    demo_p = ROOT_DIR / "DEMO.mp4"
    if demo_p.exists():
        print(f"    [OK] {'Video Demo thực tế (.mp4)':<36} -> DEMO.mp4 ({demo_p.stat().st_size / (1024*1024):,.2f} MB)")
    else:
        print("    [INFO] Không tìm thấy DEMO.mp4 cục bộ (tham chiếu qua link Google Drive trong README.md)")
    if missing:
        raise FileNotFoundError(f"Thiếu các tệp bắt buộc: {missing}")


def create_submission_zip(output_path: Path | None = None) -> Path:
    if output_path is None:
        output_path = ROOT_DIR / ZIP_NAME

    verify_required_deliverables()
    print(f"\n[*] Bắt đầu đóng gói đề tài vào: {output_path.name}")
    count = 0
    total_bytes = 0

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(ROOT_DIR.rglob("*")):
            if file_path.is_file() and not should_exclude(file_path):
                rel_path = file_path.relative_to(ROOT_DIR)
                archive_name = Path("connect4-ai") / rel_path
                # Không nén lại file video .mp4 đã nén sẵn H.264 để tăng tốc độ đóng gói gấp 10x
                comp_type = zipfile.ZIP_STORED if file_path.suffix.lower() == ".mp4" else zipfile.ZIP_DEFLATED
                zf.write(file_path, str(archive_name), compress_type=comp_type)
                count += 1
                total_bytes += file_path.stat().st_size

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"[+] Hoàn thành! Đã đóng gói {count} tệp tin ({total_bytes / (1024 * 1024):.2f} MB gốc).")
    print(f"[+] Kích thước tệp ZIP cuối cùng: {size_mb:.2f} MB")
    print(f"[+] Đường dẫn tệp nộp bài: {output_path}")
    return output_path


if __name__ == "__main__":
    create_submission_zip()
