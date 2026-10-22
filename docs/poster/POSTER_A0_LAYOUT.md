# THIẾT KẾ NỘI DUNG POSTER KHOA HỌC KHỔ A0
## ĐỀ TÀI: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ (CONNECT FOUR 7×6)
**Trường Đại học Sài Gòn - Khoa Công Nghệ Thông Tin**
**Học phần: Trí tuệ nhân tạo nâng cao - GVHD: Thầy Đỗ Như Tài**
**Nhóm 13**: Bùi Minh Trung (NT), Trần Lê Minh Tâm, Chương Gia Thịnh, Nguyễn Thành Tài

---

### [PANEL 1] TỔNG QUAN & BÀI TOÁN
- **Bối cảnh**: So sánh định lượng giữa các phương pháp tiếp cận AI trong trò chơi đối kháng thông tin hoàn hảo (Rule-based, Tree Search, Deep Learning).
- **Môi trường**: Trò chơi Connect Four kích thước chuẩn 7 cột × 6 hàng.
  + Không gian trạng thái: $\approx 4.5 \times 10^{12}$ trạng thái.
  + Số đường thắng: 69 đường (24 ngang, 21 dọc, 24 chéo).
- **Câu hỏi nghiên cứu**:
  1. *RQ1*: Với cùng ngân sách thời gian, MCTS có vượt qua Minimax/Alpha-Beta không?
  2. *RQ2*: Mô hình Supervised Policy Network mô phỏng Alpha-Beta đạt sức mạnh bao nhiêu % so với chuyên gia?

---

### [PANEL 2] KIẾN TRÚC HỆ THỐNG & ENGINE BITBOARD
- **Engine Bitboard 49-bit**:
  + Biểu diễn 7 cột $\times$ 7 bit với bit đệm chống tràn.
  + Tốc độ kiểm tra 4 quân liên tiếp bằng bitwise shift operations ($O(1)$).
  + Kiểm thử chéo với Reference Engine trên 10.000 ván ngẫu nhiên: Trùng khớp 100%.
- **Sơ đồ phân tầng**:
  + *Engine* -> *Agents (Cấp 1-5)* -> *Tournament Framework* -> *Pygame & CLI UI*.

---

### [PANEL 3] CÁC CẤP ĐỘ TÁC TỬ (AGENTS)
| Cấp độ | Thuật toán cốt lõi | Đặc điểm kỹ thuật & Tối ưu |
|:---:|:---|:---|
| **Cấp 1** | Random | Chọn ngẫu nhiên đều từ legal actions; làm baseline mốc dưới |
| **Cấp 2** | Rule-based Heuristic | 4 tầng luật ưu tiên: Thắng ngay $\to$ Chặn $\to$ Tránh tạo thế $\to$ Trung tâm |
| **Cấp 3** | Minimax / Alpha-Beta | Negamax, Alpha-Beta pruning, Center-First ordering, Iterative Deepening |
| **Cấp 4** | MCTS (UCT) | Selection (UCB1), Expansion, Playout, Backpropagation, cây đa tầng |
| **Cấp 5** | CNN Policy Network | Đầu vào tensor $2 \times 6 \times 7$, 2 lớp Conv2D, Dense, Masked Softmax 7 cột |
| **Mở rộng** | Mixed MCTS | Kết hợp Prior Probability từ Policy Network vào công thức chọn nút MCTS |

---

### [PANEL 4] THIẾT KẾ GIẢI ĐẤU & THỰC NGHIỆM
- **Quy chuẩn giải đấu công bằng**:
  + Thể thức Round-Robin giữa toàn bộ các cặp tác tử.
  + 200 ván/cặp: 100 khai cuộc ngẫu nhiên 4 nước $\times$ 2 lượt đổi bên người đi trước/đi sau để triệt tiêu hoàn toàn first-player bias.
- **Độ đo khoa học**:
  + Score: $(\text{Thắng} + 0.5 \times \text{Hòa}) / \text{Tổng số ván}$.
  + Khoảng tin cậy: Wilson CI 95% và Bootstrap CI 95%.
  + Độ trễ: Đo độc quyền bằng `time.perf_counter()`, báo cáo trung bình và p95 latency.

---

### [PANEL 5] KẾT QUẢ ĐỐI KHÁNG & ABLATION STUDIES
- **Ma trận đối đầu tổng quát** (Round-robin 5 tác tử):
  + Minh chứng sự phân hóa sức mạnh rõ rệt từ Cấp 1 đến Cấp 4.
  + Alpha-Beta và MCTS đạt tỷ lệ thắng áp đảo trước Random ($>98\%$).
- **Ablation A1 (Alpha-Beta Pruning)**:
  + Cắt tỉa Alpha-Beta giảm trên $85\%$ số nút duyệt so với Minimax thuần mà không làm suy giảm chất lượng nước đi.
- **Ablation A2 (MCTS Scaling)**:
  + MCTS tăng điểm số rõ rệt khi tăng số lượng mô phỏng từ 100 lên 5.000 simulations.
- **Ablation A5 (Lợi thế đi trước)**:
  + Bên đi trước (Đỏ) có ưu thế nhẹ trong các cặp đấu ngang sức.

---

### [PANEL 6] KẾT LUẬN & ĐÓNG GÓP
1. **Kết quả**: Giải quyết trọn vẹn các yêu cầu của môn học Trí tuệ nhân tạo nâng cao với chất lượng kỹ thuật cao.
2. **Khả năng tái lập**: Toàn bộ dữ liệu, hạt giống (seed) và mã nguồn tự động hóa 100%.
3. **Mã nguồn GitHub**: Đầy đủ commit history, phân công nhiệm vụ rõ ràng và đóng gói ZIP đúng quy định.
