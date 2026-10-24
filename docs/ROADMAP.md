# Danh sách việc (sao chép thành GitHub Issues)

Ký hiệu: **[L]** = cần lập trình, **[D]** = tài liệu/chạy lệnh, không cần code. Gán người theo thực tế nhóm.

## Tuần 1
- [x] S0-S2: khung repo, engine bitboard + bản tham chiếu, unit test, kiểm thử chéo *(đã xong ở v0.1)*
- [x] Random agent, khung giải đấu, Wilson/bootstrap *(đã xong ở v0.1)*
- [x] **[L] Heuristic** *(xong ở v0.2)* (`agents/heuristic.py`): thắng ngay → chặn → tránh nước tạo thế cho đối thủ → trung tâm. Dùng `game.winning_moves()`. Xong khi: test tình huống dựng sẵn đúng, thắng Random >= 95%.
- [x] **[L] MCTS-UCT** *(xong ở v0.2)* (`agents/mcts.py`): cây nhiều tầng (N, W mỗi nút), 4 bước, ngân sách `Budget.simulations` hoặc `time_s`, chọn nước có số thăm lớn nhất. Xong khi: thắng Random >= 95% ở 500 mô phỏng.
- [ ] **[D] Bổ sung `tests/data/positions.csv`** lên >= 30 vị trí đa dạng (xem `tests/data/README.md`).
- [ ] **[D] Báo cáo Chương 1-2** (đọc sách Ch. 1-8), điền `THIRD_PARTY.md`.

## Tuần 2 (mốc chấm tiến độ)
- [x] **[L] Alpha-Beta** *(xong ở v0.2)* (`agents/alphabeta.py`): negamax, thứ tự `CENTER_FIRST`, iterative deepening theo `time_s`, cờ bật/tắt cắt tỉa, cờ bật/tắt hàm lượng giá, đếm nút (`last_stats["nodes"]`). Xong khi: cùng giá trị với minimax thuần ở độ sâu <= 4 (viết test).
- [ ] **[L] Script sinh dữ liệu NN** (`train/gen_data.py`): Alpha-Beta độ sâu 4 tự chơi, khai cuộc ngẫu nhiên, nhãn không nhiễu; lưu theo ván.
- [ ] **[L] Giao diện tối thiểu / pygame** (`ui/`).
- [ ] **[D] Pilot giải đấu**: chạy 20-50 ván/cặp, ghi cấu hình máy và thời gian/nước để chốt mức ngân sách (100/300 ms).
- [ ] **[D] Slide tiến độ + diễn tập demo.**

## Tuần 3
- [ ] **[L] Tuning** trên tập seed riêng (trọng số hàm lượng giá, hằng số C của UCT) -> lưu vào `configs/`, tag `v0.5-frozen`.
- [ ] **[L] Huấn luyện NN** (`train/train_policy.py`, `agents/nn_agent.py`): chia 70/15/15 THEO VÁN, loại trùng, lật ngang chỉ cho train, 3 seed, lưu checkpoint.
- [ ] **[D] Giải đấu chính** 2 chế độ ngân sách, 200 ván/cặp; **[L]** ablation A1 (cắt tỉa), A2 (MCTS 100-5000 mô phỏng), A5 (đi trước/sau).

## Tuần 4
- [ ] Notebook dựng bảng/hình từ log thô; phân tích ván (chọn theo quy tắc cố định); Chương 3-5; slide; poster; video; kiểm tra README chạy lại trên máy sạch; đóng gói ZIP; in ấn.
