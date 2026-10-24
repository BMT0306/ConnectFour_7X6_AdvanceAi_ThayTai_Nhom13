# Quy tắc làm việc nhóm

1. **Không push thẳng vào `main`.** Mỗi việc làm trên nhánh riêng: `tv2/mcts`, `tv3/positions-csv`, `tv4/report-ch2`...
2. Làm xong mở **Pull Request**, gắn `Closes #<số issue>`; nhóm trưởng (hoặc người còn lại) review rồi mới merge.
3. **Commit nhỏ, đều, thông điệp rõ** (vd `mcts: thêm bước backpropagation`, `docs: viết Chương 2 mục 2.1`). Không dồn code lên sát hạn nộp.
4. **Ai cũng commit phần của mình** (code, log, báo cáo, slide đều được); lịch sử GitHub là căn cứ tỷ lệ đóng góp.
5. Trước khi mở PR: `pytest` phải xanh.
6. **Không tự ý đổi API** ở `src/c4/game/base.py` và `src/c4/agents/base.py`. Cần đổi thì mở Issue thảo luận.
7. **Số liệu trong báo cáo phải do nhóm tự chạy** và có log thô trong `results/logs/`. Không dùng kết quả của sách như của nhóm.
8. Mọi tham số thí nghiệm lưu vào file cấu hình trong `configs/`, kèm seed.

## Quy ước kỹ thuật (đừng tự đổi)
* Cột trong code: **0..6** (giao diện hiển thị 1..7). Hàng 0 = dưới cùng.
* `PLAYER1 = +1` đi trước (X, Đỏ); `PLAYER2 = -1` đi sau (O, Vàng).
* `result(player)`: +1 thắng / 0 hòa / -1 thua theo góc nhìn của `player`.
* Thứ tự duyệt nước từ giữa ra: `CENTER_FIRST = (3, 2, 4, 1, 5, 0, 6)`.
* Mọi ngẫu nhiên đi qua `self.rng` (khởi tạo bằng seed) để tái lập.
