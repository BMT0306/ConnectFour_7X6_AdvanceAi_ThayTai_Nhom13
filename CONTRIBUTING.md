# Quy trình Cộng tác & Chuẩn Đóng góp Repository — Nhóm 13

* **Repository chính thức**: https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13
* **Kho lưu trữ Thực nghiệm (Google Drive)**: https://drive.google.com/drive/folders/1k-q-cuTi3Rb_eYnrmfmrr_6-C35j7M6K?usp=sharing

---

## 1. Hệ sinh thái 5 Công cụ Quản lý Dự án

| Mảng công việc | Nền tảng sử dụng | File / Liên kết chuẩn trong Repo |
|---|---|---|
| **Mã nguồn (Code & CI)** | **GitHub** (`Actions pytest`) | `src/`, `tests/`, `configs/`, `scripts/`, `.github/workflows/tests.yml` |
| **Kết quả thí nghiệm & Video** | **Google Drive** | `results/logs/`, `results/tables/`, `results/figures/` + Link Drive chung |
| **Nhật ký thí nghiệm** | **Google Sheets / Excel** | `docs/NHAT_KY_THI_NGHIEM.xlsx` & `docs/NHAT_KY_THI_NGHIEM.csv` |
| **Vẽ sơ đồ & Slide** | **Google Slides / PowerPoint** | `docs/SLIDE_THUYET_TRINH_CONNECT_FOUR_NHOM13.pptx` |
| **Kế hoạch & Viết báo cáo** | **Google Docs / Word** | `docs/BAO_CAO_DO_AN_CUOI_KY.docx` & `docs/BAO_CAO_DO_AN_CUOI_KY.md` |

---

## 2. Phân công Trục Dọc × Trục Ngang (`45% – 35% – 10% – 10%`)

1. **Bùi Minh Trung (`45%` — Nhóm trưởng)**: Trục Code & Hạ tầng AI (Bitboard 49-bit, `AlphaBetaAgent`, khung giải đấu/timeout `best_or_random`, thống kê `Wilson`/`Bootstrap`/`p95`, Web UI, Saliency XAI, quản lý GitHub & tổng hợp Google Docs).
2. **Trần Lê Minh Tâm (`35%`)**: Trục Học sâu & Demo (`MCTSAgent`, `Connect4PolicyValueNet`, Data Pipeline, `MixedMCTSAgent` PUCT, Pygame GUI, hỗ trợ test game thực tế, quay Video Demo & đề xuất idea fix lỗi).
3. **Nguyễn Thành Tài (`10%`)**: Chỉnh sửa Báo cáo (Google Docs Chương 4–5 & bảng số liệu), chỉnh sửa Slide PPTX và đồng bộ Nhật ký thí nghiệm Google Sheets/Drive.
4. **Chương Gia Thịnh (`10%`)**: Chỉnh sửa Báo cáo (Google Docs Chương 1–3 & văn phong), chỉnh sửa Slide PPTX, chuẩn hóa Tài liệu tham khảo & Kịch bản trình bày (`docs/KICH_BAN_TRINH_BAY.md`).

Chi tiết ma trận Trục dọc × Trục ngang, Nhật ký tuần và **Khung đánh giá dựa vào người yếu nhất** xem tại [docs/QUAN_LY_CONG_TAC_VA_NHAT_KY.md](docs/QUAN_LY_CONG_TAC_VA_NHAT_KY.md).

---

## 3. Quy ước Nhánh Git & Kiểm thử trước khi Push

- Không push trực tiếp code chưa chạy `pytest` vào nhánh `main`; dùng nhánh cá nhân (`tv1/*`, `feature/*`, `tv3/*`, `fix/*`) rồi tạo Pull Request kèm `.github/pull_request_template.md`.
- Lệnh kiểm tra bắt buộc trước khi commit:
  ```bash
  pytest -q
  ```
- Đóng gói sản phẩm nộp cuối kỳ (không commit file `.zip` lên GitHub vì đã cấu hình trong `.gitignore`):
  ```bash
  python scripts/package_submission.py
  ```
