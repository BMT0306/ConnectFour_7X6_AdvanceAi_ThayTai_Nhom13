# Connect Four Game AI (7×6) — Nhóm 13

Đồ án cuối kỳ học phần **Trí tuệ nhân tạo nâng cao (Advanced Artificial Intelligence)** — Trường Đại học Sài Gòn (SGU): Xây dựng và đánh giá thực nghiệm hệ thống **Game AI đa cấp độ** trên trò chơi **Connect Four (7 cột × 6 hàng)**, từ tác tử phản xạ luật, duyệt cây đối kháng kinh điển, tìm kiếm Monte Carlo đến mạng nơ-ron phần dư hai đầu (**Policy-Value ResNet**) và tìm kiếm định hướng **PUCT-MCTS** (*AlphaGo-/AlphaZero-inspired*), kèm khung giải đấu đối xứng gương (mirror matching), khoảng tin cậy thống kê và phân tích độ nhạy **Explainable AI (Saliency Heatmap)**.

> **Trạng thái**: **v1.0 Hoàn chỉnh** — Engine Bitboard 49-bit + 6 tác tử AI (`random`, `heuristic`, `alphabeta`, `mcts`, `nn`, `mixed_mcts`) + Checkpoint mạng đã huấn luyện (`checkpoints/policy_net_best.pt`) + 3 giao diện (CLI, Pygame GUI, Web UI) + Giải đấu 3.000 ván & 4 Ablations (A1–A4) + 100% Unit Tests Passed (`57/57`).

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
pytest -v                                     # chạy nhanh toàn bộ 57 bài kiểm thử tự động
python scripts/run_test_suite_and_save.py     # chạy kiểm thử & xuất báo cáo vào results/test_results/
```

---

## 2. Chạy chương trình & Chơi thử (Khởi chạy nhanh 1 chạm)

Trên Windows, bạn chỉ cần nhấp đúp duy nhất tệp **`RUN_FAST.bat`** ở thư mục gốc để mở menu chọn nhanh mọi chế độ (Web App, Desktop Pygame, Terminal CLI hoặc chạy 57 Unit Tests).

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

# Bước 4: Chạy Giải đấu cùng ngân sách thời gian 50ms / 100ms / 300ms (RQ1)
python scripts/run_tournament.py --config configs/tournament_timed.yaml

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
  models/        net.py (Connect4PolicyValueNet - 3 ResBlocks), explain.py (Gradient Saliency Map)
  train/         gen_data.py (sinh dữ liệu nhãn sạch & loại trùng), train_policy.py (huấn luyện đa mục tiêu)
  eval/          match.py (đấu cặp đổi bên theo khai cuộc), metrics.py (Wilson 95%, Bootstrap 95%, p95), cli.py
  ui/            gui.py (Pygame 60 FPS), web_server.py + web_static/index.html (Web RESTful UI)
configs/         Cấu hình YAML cho giải đấu và các bài toán Ablation
checkpoints/     policy_net_best.pt (mô hình đã huấn luyện) & training_history.json
data/            Dữ liệu huấn luyện/kiểm định/kiểm tra (.npz) & dataset_summary.json
results/         logs/ (CSV từng ván), tables/ (bảng tổng hợp), figures/ (biểu đồ 300 DPI), test_results/
tests/           57 unit tests tự động + tests/data/positions.csv (33 thế cờ chiến thuật kiểm thử thủ công)
notebooks/       01_tournament_analysis.ipynb (phân tích thống kê & trực quan hóa kết quả)
docs/            BAO_CAO_DO_AN_CUOI_KY.md, SLIDE_OUTLINE.md, POSTER_A0_LAYOUT.md, DEMO_GUIDE.md, ConnectFour_Proposal_Nhom13.pdf, THIRD_PARTY.md
scripts/         Các script tự động hóa giải đấu, ablation, kiểm thử và đóng gói nộp bài
```

---

## 5. Môi trường Phần cứng Tham chiếu & Đạo đức Học thuật

* **Cấu hình thực nghiệm**: Windows 11, CPU AMD 16 luồng xử lý, RAM 16 GB, Python 3.13, PyTorch CPU (`torch 2.x`).
* **Cam kết trung thực học thuật**: Nhóm **không sử dụng bất kỳ solver giải sẵn nào** của Connect Four; mọi kết quả thắng/hòa/thua và độ trễ đều được trích xuất tự động từ log thực nghiệm thô trong `results/logs/`. Chi tiết nguồn tham khảo và ý tưởng kế thừa được kê khai minh bạch tại [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md).

---

## 6. Danh sách Thành viên & Tỷ lệ Đóng góp (Nhóm 13)

* **Giảng viên hướng dẫn**: Thầy Đỗ Như Tài
* **Repository chính thức**: https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13

| STT | Họ và tên | MSSV | Vai trò | Nhiệm vụ & Công việc thực hiện (khớp Đề cương & Git) | Tỷ lệ đóng góp |
|:---:|---|:---:|:---:|---|:---:|
| 1 | **Bùi Minh Trung** | `3124720074` | Nhóm Trưởng (TV1) | Engine (`bitboard` + `reference`), API & bộ unit test; `HeuristicAgent`; `AlphaBetaAgent` (cắt tỉa, sắp xếp nước đi, iterative deepening); khung giải đấu & thống kê (`Wilson`, `Bootstrap`, `p95`); Ablation A1 & A3; Web UI; quản lý GitHub, review PR & đóng gói nộp bài | **32%** |
| 2 | **Trần Lê Minh Tâm** | `3124720064` | Thành viên (TV2) | `RandomAgent`, `MCTSAgent` (UCT 4 bước); kiến trúc mạng hai đầu `Connect4PolicyValueNet`, pipeline huấn luyện & `MixedMCTSAgent` (PUCT + Transposition Cache + Dirichlet noise); giao diện Pygame GUI; Ablation A2 & A4 | **32%** |
| 3 | **Nguyễn Thành Tài** | `3124720062` | Thành viên (TV3) | Chạy thực nghiệm giải đấu & ablation, thu thập log CSV thô; xây dựng & chạy notebook phân tích (`01_tournament_analysis.ipynb`); bổ sung vị trí kiểm thử thủ công (`positions.csv`); phân tích ván đấu & viết Chương 4 | **18%** |
| 4 | **Chương Gia Thịnh** | `3124720067` | Thành viên (TV4) | Biên soạn Chương 1, 2, 3, 5 của báo cáo cuối kỳ; thiết kế Slide thuyết trình, Poster khổ A0, kịch bản/quay Video Demo; rà soát tài liệu tham khảo, `THIRD_PARTY.md`, `README.md` và chuẩn bị bản in | **18%** |
| | **TỔNG CỘNG** | | | | **100%** |

---

## 7. Đóng gói Sản phẩm Nộp Cuối Kỳ

```bash
python scripts/package_submission.py
```
Lệnh trên tự động kiểm tra đầy đủ thành phần và nén toàn bộ sản phẩm ra tệp chuẩn:
`Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip`
