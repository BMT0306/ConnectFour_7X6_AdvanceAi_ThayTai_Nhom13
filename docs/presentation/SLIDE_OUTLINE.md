# DÀN Ý SLIDE BÁO CÁO BẢO VỆ ĐỒ ÁN CUỐI KỲ
## Đề tài: Xây Dựng và Đánh Giá Game AI Đa Cấp Độ (Connect Four 7×6)
**Nhóm 13 - Môn Trí Tuệ Nhân Tạo Nâng Cao - GVHD: Thầy Đỗ Như Tài**

---

### Slide 1: Trang bìa (Title Slide)
- **Tên đề tài**: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ TRÊN CONNECT FOUR (7×6)
- **Môn học**: Trí tuệ nhân tạo nâng cao (Advanced Artificial Intelligence)
- **Giảng viên hướng dẫn**: Thầy Đỗ Như Tài
- **Nhóm thực hiện (Nhóm 13)**:
  + Bùi Minh Trung (3124720074) - Nhóm trưởng
  + Trần Lê Minh Tâm (3124720064)
  + Chương Gia Thịnh (3124720067)
  + Nguyễn Thành Tài (3124720062)

### Slide 2: Đặt vấn đề và Mục tiêu nghiên cứu
- Bối cảnh: Đối kháng có thông tin hoàn hảo (AI kinh điển vs AI hiện đại).
- Trò chơi Connect Four 7×6: luật chơi, độ phức tạp không gian trạng thái ($4.5 \times 10^{12}$).
- Hai câu hỏi nghiên cứu trọng tâm:
  1. **RQ1**: Với cùng ngân sách thời gian, MCTS có vượt qua Minimax/Alpha-Beta không? Điểm giao thoa nằm ở đâu?
  2. **RQ2**: Mạng policy học có giám sát từ Alpha-Beta thể hiện sức mạnh ra sao so với tác tử chuyên gia dạy nó?

### Slide 3: Kiến trúc hệ thống tổng thể
- Sơ đồ phân tầng hệ thống:
  + **Tầng Core Game**: Bitboard Engine 49-bit (siêu tốc, $O(1)$ win-check bằng bitwise operations) + Reference Engine (đối chiếu kiểm thử chéo).
  + **Tầng Agent AI**: Random (Cấp 1) → Heuristic (Cấp 2) → Alpha-Beta (Cấp 3) → MCTS-UCT (Cấp 4) → CNN Policy (Cấp 5) → Mixed MCTS.
  + **Tầng Đánh giá**: Tournament Runner (200 ván/cặp, luân phiên đổi bên, opening seeds) + Wilson & Bootstrap CI.
  + **Tầng Giao diện**: Terminal CLI + Pygame GUI tương tác trực quan.

### Slide 4: Thiết kế Engine Bitboard 49-bit
- Biểu diễn 7 cột $\times$ 7 bit (6 ô quân + 1 bit đệm chống tràn).
- So sánh hiệu năng: Bitboard nhanh hơn $\approx 30\times$ so với quét mảng thông thường.
- Kết quả kiểm thử chéo: 10.000 ván ngẫu nhiên khớp hoàn toàn 100% giữa Bitboard và Engine mảng 2D.

### Slide 5: Tác tử Cấp 1, 2, 3 (Luật & Tìm kiếm)
- **Random**: Chọn ngẫu nhiên trong legal actions.
- **Heuristic**: Thứ tự 4 luật nghiêm ngặt (Thắng ngay → Chặn → Tránh tạo thế đối thủ → Cột trung tâm).
- **Alpha-Beta**:
  + Thuật toán Negamax với $\alpha$-$\beta$ Pruning.
  + Sắp xếp nước đi Center-First: $(3, 2, 4, 1, 5, 0, 6)$.
  + Iterative Deepening theo ngân sách thời gian thực `time.perf_counter()`.
  + Hàm đánh giá dựa trên 69 cửa sổ 4 ô.

### Slide 6: Tác tử Cấp 4 & 5 (MCTS và Neural Network)
- **MCTS với UCT**:
  + 4 bước chuẩn mực: Selection ($UCB1 = \frac{W_i}{N_i} + C\sqrt{\frac{\ln N}{N_i}}$), Expansion, Simulation, Backpropagation.
  + Quản lý ngân sách theo Simulations và Time Budget.
- **CNN Policy Network (Cấp 5)**:
  + Dữ liệu: 10.000 ván tự sinh từ Alpha-Beta depth 4 với nhiễu $\epsilon=0.1$.
  + Tách 70% Train / 15% Val / 15% Test **theo ván** (ngăn chặn triệt để data leakage).
  + Kỹ thuật Data Augmentation: Lật đối xứng bàn cờ.
  + Mạng 2D-CNN $\rightarrow$ Flatten $\rightarrow$ Dense $\rightarrow$ Masked Softmax 7 cột.

### Slide 7: Thiết kế thực nghiệm và Độ đo khoa học
- **Thể thức thi đấu**: Round-robin toàn bộ các cặp tác tử.
- **Kiểm soát thiên lệch**: 200 ván/cặp (100 khai cuộc ngẫu nhiên 4 nước $\times$ 2 lượt đổi bên người đi trước/đi sau).
- **Độ đo thống kê**:
  + Score: $(\text{Thắng} + 0.5 \times \text{Hòa}) / \text{Tổng số ván}$.
  + Khoảng tin cậy: Wilson CI 95% cho tỷ lệ thắng, Bootstrap CI 95% cho Score.
  + Chi phí tính toán: Thời gian trung bình/nước, phân vị độ trễ p95.

### Slide 8: Kết quả thực nghiệm và Ma trận đối đầu
- Ma trận kết quả đối đầu giữa các tác tử (Score, Tỷ lệ thắng/thua/hòa).
- Phân tích tương quan sức mạnh: Random < Heuristic < Policy NN < MCTS < Alpha-Beta.
- Thảo luận trả lời **RQ1** và **RQ2** bằng số liệu thống kê thực tế.

### Slide 9: Các nghiên cứu phân rã (Ablations)
- **Ablation A1 (Alpha-Beta Pruning)**:
  + Đo số nút duyệt và thời gian khi BẬT vs TẮT cắt tỉa $\alpha$-$\beta$ ở depth 4, 5, 6 (tiết kiệm $>85\%$ số nút duyệt).
- **Ablation A2 (MCTS Scaling)**:
  + Đánh giá MCTS với 100, 500, 1000, 2000, 5000 simulations khi đấu với Alpha-Beta depth 4.
- **Ablation A5 (Lợi thế người đi trước)**:
  + Phân tích first-player advantage trên Connect Four.

### Slide 10: Phân tích chiến thuật & Ván đấu tiêu biểu
- Tình huống đòn kép (Double threat): Heuristic thất bại do chỉ chặn được 1 ô, trong khi Alpha-Beta nhìn trước và ngăn chặn từ sớm.
- Tình huống lỗi sai đặc trưng của từng tác tử.

### Slide 11: Demo Ứng Dụng
- Trình diễn giao diện Pygame trực quan.
- Chế độ Người vs Máy: Lựa chọn cấp độ AI tùy ý (Heuristic, Alpha-Beta, MCTS, NN).
- Chế độ Máy vs Máy: Trực quan hóa diễn biến ván cờ theo thời gian thực và thời gian suy nghĩ từng nước.

### Slide 12: Kết luận và Hướng phát triển
- Tóm tắt kết quả đạt được: Đạt trọn vẹn các mốc M1 - M8 trong đề cương.
- Khả năng tái lập: Toàn bộ code chạy lại được 100% với file cấu hình và hạt giống cố định.
- Hướng mở rộng: AlphaZero-inspired vòng lặp PUCT và tự chơi lặp (Self-play).
