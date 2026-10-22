# TRƯỜNG ĐẠI HỌC SÀI GÒN - KHOA CÔNG NGHỆ THÔNG TIN
# ĐỒ ÁN CUỐI KỲ: TRÍ TUỆ NHÂN TẠO NÂNG CAO
## ĐỀ TÀI: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ
### Trường hợp nghiên cứu: Connect Four (7×6)

* **GV Hướng dẫn**: Thầy Đỗ Như Tài
* **Nhóm**: 13 - Connect Four (7×6)
* **Thành viên tham gia**:
  1. Bùi Minh Trung - MSSV: 3124720074 (Nhóm Trưởng, 35%)
  2. Trần Lê Minh Tâm - MSSV: 3124720064 (Thành viên, 35%)
  3. Chương Gia Thịnh - MSSV: 3124720067 (Thành viên, 15%)
  4. Nguyễn Thành Tài - MSSV: 3124720062 (Thành viên, 15%)

---

## TÓM TẮT ĐỒ ÁN (ABSTRACT)
Đồ án này nghiên cứu và xây dựng hệ thống trí tuệ nhân tạo (AI) đa cấp độ cho trò chơi Connect Four kích thước chuẩn 7 cột × 6 hàng. Nhóm triển khai một chuỗi 5 tác tử tăng dần về độ phức tạp: Cấp 1 (Random baseline), Cấp 2 (Heuristic dựa trên luật ưu tiên), Cấp 3 (Minimax / Alpha-Beta Pruning với Negamax và Iterative Deepening), Cấp 4 (Monte Carlo Tree Search - MCTS với thuật toán chọn nút UCT), và Cấp 5 (Supervised Deep Convolutional Neural Network học từ chuyên gia). 

Toàn bộ hệ thống được xây dựng trên lõi Engine Bitboard 49-bit tốc độ cao, được kiểm thử chéo nghiêm ngặt qua 10.000 ván ngẫu nhiên với bản engine mảng tham chiếu. Hiệu năng thi đấu được đánh giá thông qua giải đấu round-robin đối kháng công bằng (200 ván/cặp, luân phiên đi trước/đi sau, tập khai cuộc cố định theo seed) với khoảng tin cậy Wilson 95% và Bootstrap 95%, phân tích độ trễ p95 và các nghiên cứu phân rã (ablation studies).

---

## CHƯƠNG 1. GIỚI THIỆU
### 1.1. Bối cảnh đề tài
- Lịch sử AI trong trò chơi đối kháng thông tin hoàn hảo (từ Deep Blue 1997 đến AlphaGo 2016, AlphaZero 2017).
- Ý nghĩa của việc so sánh tri thức do con người lập trình (luật, heuristic, tìm kiếm đối kháng) và tri thức máy tự học được (mạng nơ-ron sâu).

### 1.2. Trò chơi Connect Four (7×6)
- Luật chơi và cơ chế trọng lực: 7 cột, 6 hàng, 42 ô; 2 người chơi thả quân luân phiên (Đỏ đi trước, Vàng đi sau); điều kiện thắng là tạo chuỗi 4 quân cùng màu (ngang, dọc, chéo).
- Đặc điểm lý thuyết trò chơi: Quan sát đầy đủ (perfect information), xác định (deterministic), luân phiên (turn-based), tổng bằng không (zero-sum).
- Không gian trạng thái: Khoảng $4.5 \times 10^{12}$ trạng thái hợp lệ. Trò chơi đã được giải toán học (Allis, 1988), người đi trước thắng nếu chơi tối ưu.

### 1.3. Mục tiêu và câu hỏi nghiên cứu (Research Questions)
- **Mục tiêu chung**: Xây dựng hệ thống Connect Four hoàn chỉnh với engine bitboard, 5 cấp độ tác tử AI, giao diện đồ họa và khung giải đấu khoa học.
- **RQ1**: Với cùng ngân sách thời gian mỗi nước đi, MCTS có thắng được Alpha-Beta hay không, và điểm giao nhau (cross-over point) nằm ở mức ngân sách nào?
- **RQ2**: Mô hình Policy Network học có giám sát (Supervised Learning) từ nước đi của Alpha-Beta đạt sức mạnh thi đấu đến mức nào so với chính tác tử dạy nó và so với MCTS?
- **RQ3 (Mở rộng)**: Việc tích hợp xác suất tiên nghiệm (prior probability) từ policy network vào MCTS (Mixed MCTS) có cải thiện hiệu năng so với MCTS thuần hay không?

### 1.4. Phạm vi đề tài
- Trong phạm vi: Engine bitboard, 5 cấp tác tử (Random -> Heuristic -> Alpha-Beta -> MCTS -> Neural Network), GUI pygame và CLI, giải đấu round-robin, phân tích thống kê Wilson/Bootstrap, ablation A1, A2, A5.
- Ngoài phạm vi: Huấn luyện mạng siêu sâu trên cụm GPU lớn, chứng minh tối ưu toán học hoàn toàn, thuật toán AlphaZero-inspired lặp self-play phức tạp.

### 1.5. Bộ sản phẩm bàn giao
- Mã nguồn Python chuẩn PEP8, cấu hình YAML, requirements.txt, bộ test tự động pass 100%.
- Báo cáo khoa học 5 chương, slide thuyết trình, poster A0, video demo ứng dụng.
- Log thực nghiệm thô CSV, biểu đồ ma trận đối đầu, script đóng gói tự động ZIP.

---

## CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG TRÌNH LIÊN QUAN
### 2.1. Tác tử thông minh và phân loại môi trường
- Khái niệm Agent, Perception, Action, Performance Measure.
- Môi trường hoàn toàn quan sát được, xác định, rời rạc, đối kháng.

### 2.2. Tìm kiếm đối kháng (Adversarial Search)
- Thuật toán Minimax và biến thể gọn gàng Negamax.
- Cắt tỉa Alpha-Beta ($\alpha$-$\beta$ pruning): nguyên lý, điều kiện cắt, ảnh hưởng của thứ tự duyệt nước đi (Move Ordering: Center-First).
- Kỹ thuật Iterative Deepening theo ngân sách thời gian.
- Hàm lượng giá trạng thái tĩnh (Heuristic Evaluation Function) dựa trên 69 cửa sổ 4 ô và kiểm soát cột trung tâm.

### 2.3. Tìm kiếm cây Monte Carlo (MCTS)
- Thuật toán UCT (Upper Confidence Bounds applied to Trees):
  $$UCB1 = \frac{W_i}{N_i} + C \sqrt{\frac{\ln N_{parent}}{N_i}}$$
- 4 giai đoạn cốt lõi: Selection -> Expansion -> Simulation (Rollout) -> Backpropagation.
- Cân bằng giữa khai thác (Exploitation) và khám phá (Exploration).

### 2.4. Học sâu và Mạng nơ-ron trong trò chơi
- Kiến trúc Convolutional Neural Network (CNN) 2D xử lý bàn cờ dạng spatial tensor $2 \times 6 \times 7$.
- Mô hình Policy Network dự đoán phân phối xác suất trên 7 cột với mặt nạ nước đi hợp lệ (legal move mask).
- Học có giám sát (Supervised Learning) từ tập dữ liệu ván đấu chuyên gia.

### 2.5. Các hướng tiếp cận tiên tiến (AlphaGo và AlphaZero)
- Phân biệt kiến trúc học tăng cường (RL) tự chơi (Self-play) và học có giám sát.
- Cơ chế kết hợp Policy-Value Network với MCTS (PUCT).

---

## CHƯƠNG 3. PHƯƠNG PHÁP VÀ THIẾT KẾ HỆ THỐNG
### 3.1. Mô hình hóa bài toán
- Trạng thái ($S$): Biểu diễn bàn cờ và lượt đi.
- Hành động ($A$): Các cột chưa đầy $\{0, \dots, 6\}$.
- Hàm chuyển trạng thái ($T$): Cơ chế thả quân trọng lực và đổi lượt.
- Phần thưởng ($R$): $+1$ thắng, $0$ hòa, $-1$ thua.

### 3.2. Thiết kế Engine Bitboard 49-bit
- Mỗi cột sử dụng 7 bit (6 ô hợp lệ + 1 bit đệm ngăn tràn khi dịch bit).
- Biểu diễn trạng thái bằng 2 số nguyên 64-bit: `_pos` (quân bên đến lượt) và `_mask` (tất cả các quân).
- Kiểm tra 4 quân liên tiếp bằng phép dịch bit siêu tốc (ngang, dọc, chéo chính, chéo phụ) chỉ trong vài chu kỳ CPU.
- Engine tham chiếu 2D array dùng để đối chiếu chéo (Cross-check) đảm bảo tính đúng đắn 100%.

### 3.3. Thiết kế và cài đặt các cấp tác tử
- **Cấp 1 - RandomAgent**: Chọn đều ngẫu nhiên từ legal actions, có seed để tái lập.
- **Cấp 2 - HeuristicAgent**: Thứ tự ưu tiên nghiêm ngặt (1. Thắng ngay -> 2. Chặn đối thủ -> 3. Tránh nước tạo thế phía trên -> 4. Ưu tiên cột giữa 3,2,4,1,5,0,6).
- **Cấp 3 - AlphaBetaAgent**: Negamax, Alpha-Beta pruning, Center-First ordering, Iterative Deepening theo thời gian thực `time.perf_counter()`, bộ đếm số nút duyệt.
- **Cấp 4 - MCTSAgent**: Cây nhiều tầng lưu trữ $N$ và $W$ ở mọi nút, chọn nút theo UCT, rollout ngẫu nhiên, dừng theo simulations hoặc time_s.
- **Cấp 5 - NNAgent**: Mạng CNN nhận đầu vào 2 kênh (quân mình, quân đối thủ), qua Conv layers + Batch Normalization + Dense layers -> Softmax 7 cột.
- **Cấp mở rộng - MixedMCTSAgent**: Bổ sung prior probability từ CNN vào công thức UCT của MCTS.

### 3.4. Dữ liệu và quy trình huấn luyện Policy Network
- Tự động sinh dữ liệu bằng cách cho Alpha-Beta (depth 4) tự đấu với chính nó với độ nhiễu $\epsilon=0.1$ và 4 nước khai cuộc ngẫu nhiên.
- Tách tập dữ liệu theo ván (Train 70% / Val 15% / Test 15%) để loại bỏ hoàn toàn rò rỉ dữ liệu (data leakage).
- Kỹ thuật Data Augmentation: Lật gương ngang bàn cờ (horizontal flip).
- Hàm mất mát: Categorical Cross-Entropy, Optimizer: Adam.

### 3.5. Thiết kế giải đấu công bằng (Fair Tournament Design)
- Thể thức Round-Robin giữa toàn bộ các cặp tác tử.
- Số lượng ván: 200 ván/cặp (100 khai cuộc ngẫu nhiên 4 nước $\times$ 2 lượt đổi bên).
- 2 chế độ đánh giá:
  + Chế độ A: Cố định ngân sách thời gian mỗi nước (vd: 100ms, 300ms).
  + Chế độ B: Cố định cấu hình mặc định (Alpha-Beta depth 5, MCTS 1000 sims).
- Đo lường độ trễ: Đo thời gian độc quyền từng nước đi bằng `time.perf_counter()`, ghi nhận p95 latency.

---

## CHƯƠNG 4. THỰC NGHIỆM, KẾT QUẢ VÀ THẢO LUẬN
### 4.1. Môi trường thực nghiệm
- Cấu hình phần cứng máy chạy thử nghiệm (CPU, RAM, OS Windows).
- Phiên bản Python 3.13, PyTorch CPU, NumPy, Pytest.

### 4.2. Kiểm thử tính đúng đắn (Sanity Checks)
- Kết quả chạy unit test tự động (test_engine, test_crosscheck, test_agents, test_heuristic, test_alphabeta, test_mcts, test_positions): 100% Passed.
- Kiểm thử chéo bitboard vs reference engine trên 10.000 ván ngẫu nhiên không sai lệch.

### 4.3. Kết quả giải đấu đối kháng
- Ma trận đối đầu đầy đủ giữa các tác tử (Random, Heuristic, Alpha-Beta, MCTS, Neural Network).
- Bảng tỷ lệ thắng / hòa / thua và Score = (Wins + 0.5 * Draws) / Total.
- Khoảng tin cậy 95% Wilson CI cho tỷ lệ thắng và Bootstrap 95% CI cho Score.

### 4.4. Chi phí tính toán và độ trễ
- Thời gian trung bình mỗi nước đi và độ trễ p95.
- Số lượng nút duyệt của Alpha-Beta vs Số lượng mô phỏng của MCTS.

### 4.5. Các nghiên cứu phân rã (Ablation Studies)
- **Ablation A1**: Bật/tắt cắt tỉa Alpha-Beta và sắp xếp nước đi (so sánh số nút duyệt và thời gian thực thi ở các độ sâu 4, 5, 6).
- **Ablation A2**: MCTS với các mức ngân sách mô phỏng tăng dần (100, 500, 1000, 2000, 5000 sims) đối đầu Alpha-Beta depth 4 (trả lời RQ1).
- **Ablation A5**: Phân tích lợi thế người đi trước (First-player advantage) qua tỷ lệ score khi cầm Đỏ vs Vàng.

### 4.6. Phân tích các tình huống chiến thuật tiêu biểu
- Tình huống thắng ngay và phòng thủ bắt buộc.
- Phân tích đòn kép (double threat) mà Heuristic không thể giải quyết nhưng Alpha-Beta và MCTS phát hiện được.
- Phân tích sai lầm điển hình của từng tác tử.

---

## CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
### 5.1. Trả lời các câu hỏi nghiên cứu
- Tổng kết câu trả lời cho RQ1, RQ2 và RQ3 dựa trên số liệu thực nghiệm.

### 5.2. Đóng góp của đề tài
- Hệ thống engine bitboard mã nguồn mở tốc độ cao viết bằng Python.
- Bộ khung giải đấu khoa học, trung thực, có thể tái lập 100%.

### 5.3. Hạn chế
- Dung lượng dữ liệu huấn luyện và giới hạn phần cứng tính toán cá nhân (CPU).
- Chưa áp dụng mạng Value Network và quy trình Self-play nâng cao.

### 5.4. Hướng mở rộng
- Mở rộng sang thuật toán AlphaZero hoàn chỉnh (Policy-Value Network + PUCT).
- Áp dụng trên các trò chơi đối kháng kích thước lớn hơn (Gomoku, Othello).

---

## TÀI LIỆU THAM KHẢO
1. M. Liu, *AlphaGo Simplified: Rule-Based AI and Deep Learning in Everyday Games*, CRC Press, 2025.
2. S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2021.
3. R. S. Sutton and A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018.
4. L. Kocsis and C. Szepesvári, "Bandit based Monte-Carlo Planning," in *ECML*, 2006.
5. V. Allis, *A Knowledge-Based Approach of Connect-Four*, Master's thesis, Vrije Universiteit Amsterdam, 1988.
6. D. Silver et al., "Mastering the game of Go with deep neural networks and tree search," *Nature*, 2016.
7. D. Silver et al., "Mastering the game of Go without human knowledge," *Nature*, 2017.
