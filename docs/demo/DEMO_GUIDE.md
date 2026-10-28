# HƯỚNG DẪN KỊCH BẢN QUAY VIDEO DEMO ĐỒ ÁN
## Đề tài: Connect Four Game AI (Nhóm 13)

### 1. Yêu cầu video demo
- **Thời lượng khuyến nghị**: 3 - 5 phút.
- **Độ phân giải**: Full HD (1080p).
- **Phụ trách**: Chương Gia Thịnh (TV3) và Nguyễn Thành Tài (TV4).
- **Mục tiêu**: Minh chứng chương trình chạy thực tế, không có lỗi runtime, thể hiện được các cấp độ AI và tính năng nổi bật.

---

### 2. Kịch bản từng phân cảnh (Storyline)

#### Phân cảnh 1: Giới thiệu đề tài (30 giây)
- Hiện slide bìa: Tên đề tài, Nhóm 13, GVHD Thầy Đỗ Như Tài, 4 thành viên.
- Giới thiệu ngắn gọn mục tiêu: Xây dựng và so sánh 5 cấp độ AI trên Connect Four 7x6.

#### Phân cảnh 2: Chạy kiểm thử tự động (Unit Tests) (30 giây)
- Mở terminal trong môi trường `.venv`:
  ```bash
  pytest -v
  ```
- Thuyết minh: Toàn bộ 48+ unit test đều pass 100%, bao gồm kiểm thử logic engine, kiểm thử chéo 10.000 ván ngẫu nhiên giữa Bitboard và Reference engine, và kiểm tra tính đúng đắn của Heuristic, Alpha-Beta, MCTS.

#### Phân cảnh 3: Chơi Người vs Máy qua Terminal CLI (45 giây)
- Lệnh chạy:
  ```bash
  python -m c4.play --opponent heuristic
  ```
- Người chơi thả quân vào các cột 1-7.
- Thể hiện: Máy biết thắng ngay, biết chặn nước đi của người chơi.
- Thoát trận đấu bằng phím `q`.

#### Phân cảnh 4: Chơi trên Giao diện Đồ họa Pygame (1.5 phút)
- Lệnh chạy:
  ```bash
  python scripts/run_gui.py
  ```
- Thao tác:
  + Giới thiệu bàn cờ 7x6 màu sắc rõ nét, trực quan.
  + Thử nghiệm chế độ Người vs Máy (AI: Alpha-Beta / MCTS): Thả quân bằng click chuột, hiển thị quân rơi theo trọng lực.
  + Xem máy suy nghĩ và đưa ra nước đi chiến thuật (chặn, bẫy, tạo thế).
  + Thử nghiệm chế độ Máy vs Máy: Alpha-Beta đấu với MCTS, hiển thị thời gian suy nghĩ từng nước đi.
  + Nút "Ván mới" (Reset) hoạt động mượt mà.

#### Phân cảnh 5: Chạy giải đấu đối kháng tự động (Tournament) (1 phút)
- Lệnh chạy:
  ```bash
  python -m c4.eval.cli --a alphabeta --b mcts --openings 20 --depth-a 4 --sims-b 500 --out results/logs/demo_match.csv
  ```
- Thể hiện: Hệ thống tự động chơi 40 ván (20 khai cuộc x 2 lượt đổi bên), đo thời gian bằng `time.perf_counter()`, xuất log thô CSV và tính toán Score, Wilson 95% CI, Bootstrap 95% CI và p95 latency trực tiếp trên màn hình.

#### Phân cảnh 6: Đóng gói sản phẩm nộp bài (30 giây)
- Lệnh chạy:
  ```bash
  python scripts/package_submission.py
  ```
- Hiển thị file ZIP `Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip` được tạo thành công với cấu trúc thư mục sạch sẽ, sẵn sàng nộp lên hệ thống.
