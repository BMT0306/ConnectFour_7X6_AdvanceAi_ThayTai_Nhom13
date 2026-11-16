# Connect Four Game AI (7×6) — Nhóm 13

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Tests-59%2F59%20Passed-brightgreen.svg)](results/TEST_AND_EVALUATION_REPORT.md)
[![Agents](https://img.shields.io/badge/Game%20AI-6%20Levels-orange.svg)](#4-cấu-trúc-thư-mục-dự-án)

Đồ án cuối kỳ học phần **Trí tuệ nhân tạo nâng cao (Advanced Artificial Intelligence)** — Trường Đại học Sài Gòn (SGU): Xây dựng và đánh giá thực nghiệm hệ thống **Game AI đa cấp độ** trên trò chơi **Connect Four (7 cột × 6 hàng)**, từ tác tử phản xạ luật, duyệt cây đối kháng kinh điển, tìm kiếm Monte Carlo đến mạng nơ-ron phần dư hai đầu (**Policy-Value ResNet**) và tìm kiếm định hướng **PUCT-MCTS** (*AlphaGo-/AlphaZero-inspired*), kèm khung giải đấu đối xứng gương (mirror matching), cơ chế timeout an toàn (`best_or_random`), khoảng tin cậy thống kê và phân tích độ nhạy **Explainable AI (Saliency Heatmap)**.

> **Trạng thái**: **v1.1 Hoàn chỉnh** — Engine Bitboard 49-bit + 6 tác tử AI (`random`, `heuristic`, `alphabeta`, `mcts`, `nn`, `mixed_mcts`) + Chính sách timeout an toàn (`best_or_random`) + Checkpoint mạng đã huấn luyện (`checkpoints/policy_net_best.pt`) + 3 giao diện (CLI, Pygame GUI, Web UI) + Giải đấu 3.000 ván, 1.500 ván 6-Level 100ms & 4 Ablations (A1–A4) + 100% Unit Tests Passed (`59/59`).

* **Repository GitHub chính thức**: https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13
* **Kho lưu trữ Thực nghiệm & Video (Google Drive)**: https://drive.google.com/drive/folders/1k-q-cuTi3Rb_eYnrmfmrr_6-C35j7M6K?usp=sharing
* **Tài liệu Nộp & Quản lý Cộng tác Nhóm 13**:
  [Báo cáo Word (.docx)](docs/BAO_CAO_DO_AN_CUOI_KY.docx) ·
  [Báo cáo Markdown](docs/BAO_CAO_DO_AN_CUOI_KY.md) ·
  [Slide Thuyết trình 36 Slides (.pptx)](docs/SLIDE_THUYET_TRINH_CONNECT_FOUR_NHOM13.pptx) ·
  [Kịch bản Trình bày](docs/KICH_BAN_TRINH_BAY.md) ·
  [Nhật ký Thí nghiệm (.xlsx)](docs/NHAT_KY_THI_NGHIEM.xlsx) ·
  [Quản lý Trục Dọc/Ngang & Người Yếu Nhất](docs/QUAN_LY_CONG_TAC_VA_NHAT_KY.md) ·
  [Chuẩn Đóng góp (CONTRIBUTING)](CONTRIBUTING.md)

---

## 1. Hướng dẫn cài đặt (Python 3.10+)

```bash
git clone https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13.git
cd ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13
python -m venv .venv
# Kích hoạt môi trường ảo:
# - Windows (PowerShell/CMD): .venv\Scripts\activate
# - Linux / macOS:            source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Kiểm tra tính đúng đắn (Unit Tests & Lưu báo cáo kiểm thử)
```bash
pytest -v                                     # chạy nhanh toàn bộ 59 bài kiểm thử tự động
python scripts/run_test_suite_and_save.py     # chạy kiểm thử & xuất báo cáo vào results/test_results/
```

---

## 2. Chạy chương trình & Chơi thử (Khởi chạy nhanh 1 chạm)

Trên Windows, bạn chỉ cần nhấp đúp duy nhất tệp **`RUN_FAST.bat`** ở thư mục gốc để mở menu chọn nhanh mọi chế độ (Web App, Desktop Pygame, Terminal CLI hoặc chạy 59 Unit Tests).

Hoặc chạy trực tiếp bằng lệnh Python:

### A. Giao diện Web Hiện đại (Khuyên dùng)
```bash
python -m c4.ui.web_server --port 5000
```
* Mở trình duyệt tại `http://localhost:5000`: hỗ trợ chọn 6 cấp độ AI, chọn đi trước / đi sau, thanh trượt độ sâu và hiển thị độ trễ/nút duyệt trực tiếp.

### B. Giao diện Đồ họa Desktop Pygame (60 FPS)
```bash
python -m c4.ui.gui
```
* Hỗ trợ 3 chế độ: **Người vs Máy**, **Máy vs Máy**, **Người vs Người**.
* Phím tắt nhanh: `1..7` thả quân vào cột, `S` đổi bên Đi trước (Đỏ) / Đi sau (Vàng), `U` hoàn tác (Undo), `R` ván mới.

### C. Giao diện Dòng lệnh (Terminal CLI)
```bash
python -m c4.play --opponent alphabeta --depth 5
python -m c4.play --opponent mixed_mcts --sims 200 --human-second
```

---

## 3. Tái lập Quy trình Sinh dữ liệu, Huấn luyện & Thực nghiệm

Toàn bộ thí nghiệm cố định hạt giống ngẫu nhiên (`seed`), cấu hình lưu trong `configs/`, dữ liệu nằm tại `data/` và trọng số đã huấn luyện sẵn nằm tại `checkpoints/policy_net_best.pt`.

```bash
# Bước 1: Sinh dữ liệu chuyên gia sạch (tách 70/15/15 theo ván, loại trùng, chống rò rỉ đối xứng)
python -m c4.train.gen_data --games 2500 --depth 4 --epsilon 0.14 --seed 42 --out-dir data

# Bước 2: Huấn luyện mạng Policy-Value ResNet & đánh giá trên tập Test độc lập
python -m c4.train.train_policy --data-dir data --checkpoint-dir checkpoints --epochs 10 --batch-size 256 --lr 0.0015 --weight-decay 0.001 --label-smoothing 0.05 --seed 42

# Bước 3: Chạy Giải đấu Round-Robin 6 tác tử (15 cặp x 200 ván = 3.000 ván)
python scripts/run_tournament.py --config configs/tournament_default.yaml

# Bước 4a: Chạy Giải đấu cùng ngân sách thời gian 50ms / 100ms / 300ms (RQ1)
python scripts/run_tournament.py --config configs/tournament_timed.yaml

# Bước 4b: Chạy Giải đấu đầy đủ 6 Cấp độ giới hạn 100 ms/nước (1.500 ván, best_or_random)
python scripts/run_tournament.py --config configs/tournament_levels_timed.yaml --resume

# Bước 5: Chạy đầy đủ 4 nghiên cứu phân rã Ablation A1, A2, A3, A4
python scripts/run_ablation.py --all

# Bước 6: Sinh toàn bộ biểu đồ phân tích & bản đồ nhiệt Saliency XAI (300 DPI)
python scripts/generate_figures_and_xai.py
```

---

## 4. Cấu trúc Thư mục Dự án

```text
src/c4/
  game/          base.py (API chuẩn), engine.py (Bitboard 49-bit O(1)), reference.py (Mảng 2D đối chiếu)
  agents/        random_agent.py, heuristic.py, alphabeta.py, mcts.py, nn_agent.py, mixed_mcts.py (PUCT)
  models/        model.py (Connect4PolicyValueNet - 3 ResBlocks), explain.py (Gradient Saliency Map)
  train/         gen_data.py (sinh dữ liệu nhãn sạch & loại trùng), train_policy.py (huấn luyện đa mục tiêu)
  eval/          match.py (đấu cặp đổi bên + kiểm soát timeout fallback), metrics.py (Wilson 95%, Bootstrap 95%, p95), cli.py
  ui/            gui.py (Pygame 60 FPS), web_server.py + web_static/index.html (Web RESTful qua Python http.server)
configs/         Cấu hình YAML cho giải đấu (200 ván không giới hạn thời gian, 100 ván giới hạn 100ms, Ablation A1–A4)
checkpoints/     policy_net_best.pt (mô hình đã huấn luyện) & training_history.json
data/            Dữ liệu huấn luyện/kiểm định/kiểm tra (.npz) & dataset_summary.json
results/         logs/ (CSV từng ván), tables/ (bảng tổng hợp), figures/ (biểu đồ 300 DPI), test_results/
tests/           59 unit tests tự động + tests/data/positions.csv (33 thế cờ chiến thuật kiểm thử thủ công)
notebooks/       01_tournament_analysis.ipynb (phân tích thống kê & trực quan hóa kết quả)
docs/            BAO_CAO_DO_AN_CUOI_KY.docx/.md, SLIDE_THUYET_TRINH_CONNECT_FOUR_NHOM13.pptx, KICH_BAN_TRINH_BAY.md, QUAN_LY_CONG_TAC_VA_NHAT_KY.md, NHAT_KY_THI_NGHIEM.xlsx/.csv, DEMO_GUIDE.md, ConnectFour_Proposal_Nhom13.pdf, THIRD_PARTY.md
scripts/         Các script tự động hóa giải đấu, ablation, kiểm thử và đóng gói nộp bài
.github/         GitHub Actions CI (pytest tự động), Issue Template (Trục Dọc/Ngang) & Pull Request Checklist
CONTRIBUTING.md  Quy trình 5 nền tảng cộng tác (GitHub, Drive, Sheets, Slides/PPT, Docs) và quy tắc nhánh Git
```

---

## 5. Môi trường Phần cứng Tham chiếu & Đạo đức Học thuật

* **Cấu hình thực nghiệm**: Windows 11, CPU AMD 16 luồng xử lý, RAM 16 GB, Python 3.13, PyTorch CPU (`torch 2.x`).
* **Cam kết trung thực học thuật**: Nhóm **không sử dụng bất kỳ solver giải sẵn nào** của Connect Four; mọi kết quả thắng/hòa/thua và độ trễ đều được trích xuất tự động từ log thực nghiệm thô trong `results/logs/`. Chi tiết nguồn tham khảo và ý tưởng kế thừa được kê khai minh bạch tại [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md).

---

## 6. Quản lý Cộng tác, Phân công Trục Dọc/Ngang & Danh sách Thành viên (Nhóm 13)

* **Giảng viên hướng dẫn**: TS. Đỗ Như Tài
* **Quản lý mã nguồn (GitHub)**: https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13
* **Kho lưu trữ kết quả thí nghiệm (Google Drive)**: https://drive.google.com/drive/folders/1k-q-cuTi3Rb_eYnrmfmrr_6-C35j7M6K?usp=sharing
* **Hệ thống công cụ cộng tác**: GitHub (Code) · Google Drive + Google Sheets/Excel (Kết quả & Nhật ký thí nghiệm) · Google Slides/PowerPoint/Canva (Vẽ sơ đồ visual & Slide) · Google Docs (Kế hoạch & Soạn thảo báo cáo).
* **Nguyên tắc đánh giá**: Phân công theo ma trận **Trục dọc** (đầu mối nhóm việc) × **Trục ngang** (chia nhỏ task cho từng thành viên có nhật ký kiểm chứng), kết hợp đánh giá năng lực dựa trên **thành viên yếu nhất** qua số liệu quá trình học tập (chi tiết tại [docs/QUAN_LY_CONG_TAC_VA_NHAT_KY.md](docs/QUAN_LY_CONG_TAC_VA_NHAT_KY.md)).

| STT | Họ và tên | MSSV | Vai trò | Trục dọc phụ trách & Công việc thực hiện | Tỷ lệ đóng góp |
|:---:|---|:---:|:---:|---|:---:|
| 1 | **Bùi Minh Trung** | `3124720074` | Nhóm Trưởng (TV1) | **Trục Code, Hạ tầng & Kiến trúc hệ thống**: Thiết kế lõi `Bitboard` 49-bit + `ReferenceConnect4`, bộ unit test, `HeuristicAgent`, `AlphaBetaAgent`, khung giải đấu `match.py` (kèm cơ chế timeout/fallback), thống kê (`Wilson`, `Bootstrap`, `p95`), Web UI, Saliency XAI, cấu hình Ablation & quản lý GitHub/Google Docs tổng thể | **45%** |
| 2 | **Trần Lê Minh Tâm** | `3124720064` | Thành viên (TV2) | **Trục Mô hình AI, Test Game & Demo**: Cài đặt `RandomAgent`, `MCTSAgent`, mạng hai đầu `Connect4PolicyValueNet`, pipeline sinh dữ liệu/huấn luyện & `MixedMCTSAgent` (PUCT + Cache + Dirichlet); giao diện Pygame; **hỗ trợ test game thực tế, quay video demo và đề xuất ý tưởng/fix lỗi code** | **35%** |
| 3 | **Nguyễn Thành Tài** | `3124720062` | Thành viên (TV3) | **Trục Báo cáo, Slide & Nhật ký thí nghiệm**: Chỉnh sửa, chuẩn hóa nội dung báo cáo trên Google Docs và file PowerPoint thuyết trình; tham gia ghi nhận nhật ký thí nghiệm lên Google Sheets/Drive và rà soát số liệu đối chiếu | **10%** |
| 4 | **Chương Gia Thịnh** | `3124720067` | Thành viên (TV4) | **Trục Báo cáo, Slide & Tư liệu thuyết trình**: Chỉnh sửa, hoàn thiện bố cục báo cáo trên Google Docs và file PowerPoint thuyết trình; rà soát tài liệu tham khảo, kịch bản trình bày và chuẩn bị tài liệu bảo vệ | **10%** |
| | **TỔNG CỘNG** | | | | **100%** |

---

## 7. Đóng gói Sản phẩm Nộp Cuối Kỳ

```bash
python scripts/package_submission.py
```
Lệnh trên tự động kiểm tra đầy đủ thành phần và nén toàn bộ sản phẩm ra tệp chuẩn:
`Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip`
