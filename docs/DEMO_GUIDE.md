# HƯỚNG DẪN KỊCH BẢN QUAY VIDEO DEMO ĐỒ ÁN
## Đề tài: Connect Four Game AI (Nhóm 13)

### 1. Yêu cầu video demo
- **Thời lượng khuyến nghị**: 3 - 5 phút.
- **Độ phân giải**: Full HD (1080p).
- **Phụ trách**: **Trần Lê Minh Tâm** (35% — trực tiếp test game thực tế, quay Video Demo và đề xuất ý tưởng fix code); **Bùi Minh Trung** (45% — hỗ trợ kỹ thuật Web UI & giải đấu); **Nguyễn Thành Tài & Chương Gia Thịnh** (mỗi bạn 10% — hoàn thiện Google Docs & slide PPT).
- **Mục tiêu**: Minh chứng chương trình chạy thực tế trên cả Pygame Desktop (60 FPS) và Web UI (`http.server`), kiểm tra cơ chế `best_or_random` khi giới hạn thời gian và thể hiện đầy đủ 6 cấp độ AI.

---

### 2. Kịch bản từng phân cảnh (Storyline)

#### Phân cảnh 1: Giới thiệu đề tài (30 giây)
- Hiện slide bìa: Tên đề tài, Nhóm 13, GVHD Thầy Đỗ Như Tài, bảng phân công 4 thành viên (`45% – 35% – 10% – 10%`).
- Giới thiệu ngắn gọn mục tiêu: Xây dựng và đánh giá 6 cấp độ AI trên Connect Four 7×6.

#### Phân cảnh 2: Chạy kiểm thử tự động (Unit Tests) (30 giây)
- Mở terminal trong môi trường `.venv`:
  ```
  pytest -v
  ```
- Thuyết minh: Toàn bộ **59/59 unit test** (trên 11 tệp kiểm thử) đều pass 100%, bao gồm kiểm thử logic Bitboard 49-bit, kiểm thử chéo 10.000 ván ngẫu nhiên giữa Bitboard và Reference engine, kiểm thử timeout `best_or_random` và kiểm tra tính đúng đắn của Heuristic, Alpha-Beta, MCTS, Neural Net và PUCT.

#### Phân cảnh 3: Chơi Người vs Máy qua Terminal CLI (45 giây)
- Lệnh chạy:
  ```
  python -m c4.play --opponent heuristic
  ```
- Người chơi thả quân vào các cột 1-7.
- Thể hiện: Máy biết thắng ngay, biết chặn nước đi của người chơi.
- Thoát trận đấu bằng phím `q`.

#### Phân cảnh 4: Chơi trên Giao diện Đồ họa Pygame & Giao diện Web (1.5 phút)
- Cách nhanh nhất trên Windows: nhấp đúp tệp duy nhất **`RUN_FAST.bat`** để chọn mở Web App hoặc Desktop Pygame.
- Hoặc lệnh chạy Pygame Desktop GUI:
  ```
  python -m c4.ui.gui
  ```
- (Tùy chọn) Lệnh chạy Giao diện Web hiện đại (`http.server`):
  ```
  python -m c4.ui.web_server --port 5000
  ```
- Thao tác:
  + Giới thiệu bàn cờ 7×6 màu sắc rõ nét, hiệu ứng rơi trọng lực 60 FPS.
  + Thử nghiệm chế độ Người vs Máy (chọn cả Đi trước cầm Đỏ hoặc bấm phím `S` / chọn Đi sau cầm Vàng; thử AI Alpha-Beta, Neural Net và Mixed-MCTS PUCT).
  + Quan sát bảng thông số độ trễ suy luận (ms), số nút duyệt / mô phỏng và trạng thái nạp checkpoint thực tế.
  + Thử nghiệm chế độ Máy vs Máy: Alpha-Beta đấu với Mixed-MCTS / MCTS.
  + Nút "Đi lại" (Undo) và "Ván mới" (Reset) hoạt động mượt mà.

#### Phân cảnh 5: Chạy giải đấu đối kháng tự động (Tournament) (1 phút)
- Lệnh chạy:
  ```
  python -m c4.eval.cli --a alphabeta --b mcts --openings 20 --depth-a 4 --sims-b 500 --out results/logs/demo_match.csv
  ```
- Hoặc chạy giải đấu 6 cấp độ giới hạn `100 ms/nước`:
  ```
  python scripts/run_tournament.py --config configs/tournament_levels_timed.yaml --resume
  ```
- Thể hiện: Hệ thống tự động đổi bên Đỏ/Vàng đối xứng, đo thời gian bằng `time.perf_counter()`, áp dụng `best_or_random` khi chạm ngưỡng thời gian, xuất log thô CSV và tính toán Score, Wilson 95% CI, Bootstrap 95% CI và p95 latency trực tiếp trên màn hình.

#### Phân cảnh 6: Đóng gói sản phẩm nộp bài (30 giây)
- Lệnh chạy:
  ```
  python scripts/package_submission.py
  ```
- Hiển thị file ZIP `Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip` được tạo thành công với cấu trúc thư mục sạch sẽ, sẵn sàng nộp lên hệ thống và đồng bộ Google Drive.
