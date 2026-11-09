#!/usr/bin/env python3
"""Script chạy toàn bộ bộ kiểm thử tự động (pytest), trích xuất kết quả chi tiết từng test case,
kiểm định các tiêu chí nghiệm thu của đề tài và xuất báo cáo đánh giá lưu vào `results/test_results/`.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import os
import platform
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_OUT_DIR = ROOT_DIR / "results/test_results"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out-root", default=None)
    args = p.parse_args()
    out_base = Path(args.out_root) if args.out_root else Path(os.environ.get("C4_OUT_ROOT", str(ROOT_DIR)))
    test_out_dir = out_base / "results/test_results"
    test_out_dir.mkdir(parents=True, exist_ok=True)
    junit_xml = test_out_dir / "pytest_junit.xml"
    console_txt = test_out_dir / "pytest_full_output.txt"
    cases_csv = test_out_dir / "unit_test_cases.csv"
    summary_json = test_out_dir / "test_evaluation_summary.json"

    ckpt_file = out_base / "checkpoints/policy_net_best.pt"
    if not ckpt_file.exists():
        ckpt_file = ROOT_DIR / "checkpoints/policy_net_best.pt"

    sub_env = os.environ.copy()
    if ckpt_file.exists():
        sub_env.setdefault("C4_CHECKPOINT_PATH", str(ckpt_file))

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-p",
        "no:cacheprovider",
        str(ROOT_DIR / "tests"),
        "-v",
        "--durations=10",
        f"--junitxml={junit_xml}",
    ]
    print(f"[*] Đang chạy toàn bộ bộ kiểm thử tự động: {' '.join(cmd)}")
    t0 = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT_DIR),
        env=sub_env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    elapsed_s = time.perf_counter() - t0

    full_log = proc.stdout + ("\n--- STDERR ---\n" + proc.stderr if proc.stderr.strip() else "")
    console_txt.write_text(full_log, encoding="utf-8")
    print(proc.stdout)

    # Phân tích file JUnit XML để lưu bảng CSV từng test case
    cases = []
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0

    if junit_xml.exists():
        tree = ET.parse(junit_xml)
        root = tree.getroot()
        suites = list(root.findall("testsuite")) if root.tag == "testsuites" else [root]
        for suite in suites:
            for tc in suite.findall("testcase"):
                total_tests += 1
                classname = tc.attrib.get("classname", "")
                name = tc.attrib.get("name", "")
                dur = float(tc.attrib.get("time", "0.0"))
                status = "PASSED"
                detail = ""
                if tc.find("failure") is not None:
                    status = "FAILED"
                    total_failures += 1
                    detail = (tc.find("failure").attrib.get("message") or "")[:200]
                elif tc.find("error") is not None:
                    status = "ERROR"
                    total_errors += 1
                    detail = (tc.find("error").attrib.get("message") or "")[:200]
                elif tc.find("skipped") is not None:
                    status = "SKIPPED"
                    total_skipped += 1
                    detail = (tc.find("skipped").attrib.get("message") or "")[:200]

                cases.append({
                    "Module": classname,
                    "Test_Name": name,
                    "Status": status,
                    "Duration_s": round(dur, 4),
                    "Detail": detail,
                })

    with open(cases_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Module", "Test_Name", "Status", "Duration_s", "Detail"])
        writer.writeheader()
        writer.writerows(cases)

    passed = total_tests - total_failures - total_errors - total_skipped
    pass_rate = (passed / total_tests * 100.0) if total_tests > 0 else 0.0

    # Kiểm tra nhanh trạng thái tài nguyên thực nghiệm đã huấn luyện
    ckpt_file = out_base / "checkpoints/policy_net_best.pt"
    if not ckpt_file.exists():
        ckpt_file = ROOT_DIR / "checkpoints/policy_net_best.pt"
    positions_file = ROOT_DIR / "tests/data/positions.csv"
    with open(positions_file, "r", encoding="utf-8") as pf:
        num_manual_positions = sum(1 for _ in csv.DictReader(pf))

    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "return_code": proc.returncode,
        "total_duration_s": round(elapsed_s, 3),
        "total_tests": total_tests,
        "passed": passed,
        "failed": total_failures,
        "errors": total_errors,
        "skipped": total_skipped,
        "pass_rate_pct": round(pass_rate, 2),
        "manual_positions_count": num_manual_positions,
        "trained_checkpoint_present": ckpt_file.exists(),
        "trained_checkpoint_size_kb": round(ckpt_file.stat().st_size / 1024.0, 2) if ckpt_file.exists() else 0.0,
    }
    summary_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[+] Đã lưu log kiểm thử chi tiết vào: {test_out_dir}")
    print(f"    - Tổng số test: {total_tests} | Pass: {passed} ({pass_rate:.1f}%) | Thời gian: {elapsed_s:.2f}s")
    print(f"    - Số vị trí kiểm thử thủ công (positions.csv): {num_manual_positions}")
    print(f"    - Checkpoint mạng nơ-ron: {'ĐÃ CÓ' if ckpt_file.exists() else 'CHƯA CÓ'}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
