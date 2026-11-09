# DÀN Ý SLIDE BÁO CÁO BẢO VỆ ĐỒ ÁN CUỐI KỲ (THEO KHUNG KHOA HỌC KLTN 5 CHƯƠNG)
## Đề tài: Xây Dựng và Đánh Giá Game AI Đa Cấp Độ trên Connect Four (7×6)
**Nhóm 13 — Học phần: Trí Tuệ Nhân Tạo Nâng Cao — GVHD: Thầy Đỗ Như Tài**

---

## PHẦN MỞ ĐẦU

### Slide 1: Trang bìa (Title Slide)
- **Tên đề tài**: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ — TRƯỜNG HỢP NGHIÊN CỨU: CONNECT FOUR (7×6)
- **Học phần**: Trí tuệ nhân tạo nâng cao (Advanced Artificial Intelligence)
- **Giảng viên hướng dẫn**: Thầy Đỗ Như Tài
- **Nhóm thực hiện (Nhóm 13)**:
  + Bùi Minh Trung (`3124720074`) — Nhóm trưởng (32%)
  + Trần Lê Minh Tâm (`3124720064`) — Thành viên (32%)
  + Nguyễn Thành Tài (`3124720062`) — Thành viên (18%)
  + Chương Gia Thịnh (`3124720067`) — Thành viên (18%)
- **Link GitHub**: `https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13`

---

## CHƯƠNG 1: GIỚI THIỆU VÀ KHẢO SÁT CHƯƠNG TRÌNH CONNECT FOUR

### Slide 2: Hình thức hóa toán học bài toán Connect Four $(S, A, T, R)$ (Mục 1.1)
- **Bản chất Lý thuyết Trò chơi**: Thông tin hoàn hảo, xác định, tuần tự hai người chơi, tổng bằng không (*Zero-sum*).
- **Bộ bốn toán học $(S, A, T, R)$**:
  + **Không gian trạng thái ($S$)**: $|S| \approx 4,53 \times 10^{12}$ trạng thái hợp lệ (Allis, 1988).
  + **Không gian hành động ($A(s)$)**: Chọn cột chưa đầy $c \in \{0..6\}$ với $h_s(c) < 6$; hệ số nhánh $b \le 7$, tối đa $42$ ply.
  + **Hàm chuyển tiếp ($T(s,a)$)**: Quân cờ rơi theo trọng lực xuống ô trống thấp nhất $(h_s(a), a)$.
  + **Hàm phần thưởng ($R(s) \in \{-1, 0, +1\}$)**: Kiểm tra trên **69 cửa sổ chiến thắng 4 ô** (24 ngang, 21 dọc, 12 chéo chính `\`, 12 chéo phụ `/`).

### Slide 3: Khảo sát Chương trình Sẵn có & Thiết lập Benchmark Baseline (Mục 1.2 & 1.3)
- **Bảng khảo sát 4 trường phái thuật toán Connect Four**:
  1. *Luật Phản xạ 1-ply* (`inventwithpython` / Rule-based) $\rightarrow$ Chuẩn hóa thành **`HeuristicAgent` (Level 2)**.
  2. *Duyệt cây Cổ điển + 69 Cửa sổ* (`KeithGalli` / Allis) $\rightarrow$ Nâng cấp thành **`AlphaBetaAgent` (Level 3 — Baseline Tất định / Tác tử Thầy)**.
  3. *Tìm kiếm Monte Carlo Thuần* (Kocsis & Szepesvári, 2006) $\rightarrow$ Chuẩn hóa thành **`MCTSAgent` (Level 4 — Baseline Ngẫu nhiên)**.
  4. *Học sâu Bắt chước & PUCT* (Silver et al., 2017; Liu, 2025) $\rightarrow$ Đề xuất **`NNAgent` (Level 5)** & **`MixedMCTSAgent` (AlphaZero-lite)**.
- **Ba câu hỏi nghiên cứu định lượng (RQ1 – RQ3)**:
  + **RQ1**: Dưới cùng ngân sách thời gian (`50ms`, `100ms`, `300ms`), MCTS thuần có vượt Alpha-Beta không? Điểm giao thoa mô phỏng ở đâu?
  + **RQ2**: Mạng `Connect4PolicyValueNet` đạt độ chính xác Top-1/Top-2 bao nhiêu trên tập `Test` và mạnh cỡ nào khi đánh `0-search`?
  + **RQ3**: Tích hợp Policy Prior $P(s,a)$ & Value Head $V(s)$ vào PUCT giúp giảm bao nhiêu lần số playout mà vẫn thắng cả `MCTS-1000` lẫn `Alpha-Beta`?

---

## CHƯƠNG 2: HẠ TẦNG KỸ THUẬT VÀ CẤU TRÚC DỮ LIỆU BITBOARD

### Slide 4: Thiết kế Bitboard 49-bit & Toán tử Bitwise $O(1)$ (Mục 2.1)
- **Sơ đồ ánh xạ 49-bit (7 cột × 7 bit)**:
  + Mỗi cột $c \in \{0..6\}$ gồm 6 bit dữ liệu $[7c .. 7c+5]$ + **1 bit đệm chống tràn (`sentinel bit = 0`) tại đỉnh $7c+6 \in \{6, 13, 20, 27, 34, 41, 48\}$**.
  + Lưu trạng thái bằng 2 thanh ghi 64-bit: `_pos` (quân người sắp đi) và `_mask` (tất cả quân).
  + **Khóa băm duy nhất 1-1 $O(1)$**: `key = _pos + _mask` phục vụ tra cứu tức thời *Transposition Cache*.
- **Toán tử thả quân & kiểm tra thắng `_has_won` độ phức tạp $O(1)$**:
  + Thả quân: `_mask |= _mask + (1 << (col * 7))` (tự động nhớ lên ô trống thấp nhất).
  + Kiểm tra 4 quân liên tiếp bằng 4 cặp phép dịch bit (`shift = 1` dọc, `7` ngang, `6` chéo phụ `/`, `8` chéo chính `\`) chỉ trong vài chu kỳ CPU.

### Slide 5: Kiểm chuẩn Cây Trò chơi Perft (Depth 1–6) & 57 Unit Tests (Mục 2.2)
- **Bảng kiểm chuẩn toán học Perft (`Connect4` Bitboard vs `ReferenceConnect4` Mảng 2D vs Lý thuyết OEIS A212693)**:
  + `Depth 1`: **7** nút | `Depth 2`: **49** nút | `Depth 3`: **238** nút
  + `Depth 4`: **1.120** nút | `Depth 5`: **4.263** nút | `Depth 6`: **16.422** nút $\rightarrow$ **Sai số = 0 (Khớp 100%)**.
- **Kiểm thử tự động quy mô lớn (`57/57` bài test đạt `100% PASSED`)**:
  + Đối chiếu chéo **10.000 ván ngẫu nhiên** (~210.000 trạng thái + `undo`) giữa 2 engine: `0` lỗi.
  + Kiểm thử chiến thuật trên **33 thế cờ thủ công (`tests/data/positions.csv`)**.

---

## CHƯƠNG 3: PHƯƠNG PHÁP TRIỂN KHAI CHUỖI TÁC TỬ AI (LEVEL 1 – LEVEL 5 & ALPHAZERO-LITE)

### Slide 6: Nhóm Tác tử Cổ điển & Monte Carlo (Level 1 – Level 4) (Mục 3.1 & 3.2)
- **Level 1 (`RandomAgent`)**: Chọn đều ngẫu nhiên có hạt giống tái lập.
- **Level 2 (`HeuristicAgent`)**: 4 tầng luật ưu tiên: (1) Thắng ngay 1-ply $\rightarrow$ (2) Chặn thua ngay 1-ply $\rightarrow$ (3) **Lọc chống tự sát (*Anti-blunder*)** $\rightarrow$ (4) Ưu tiên trung tâm `(3, 2, 4, 1, 5, 0, 6)`.
- **Level 3 (`AlphaBetaAgent`)**: Duyệt cây Negamax + cắt tỉa $\alpha$-$\beta$ + sắp xếp *Center-First* + *Iterative Deepening* + lượng giá 69 cửa sổ bitmask (`+50` chuỗi 3 mình, `-80` chuỗi 3 địch, `+3` cột giữa).
- **Level 4 (`MCTSAgent`)**: Duyệt cây 4 pha (*Selection, Expansion, Simulation, Backpropagation*) với công thức UCT ($c = 1,4 \approx \sqrt{2}$), chọn nhánh *Robust Child* ($\arg\max N$).

### Slide 7: Đề xuất Tác tử Học sâu AlphaZero-lite (`Connect4PolicyValueNet` + `PUCT Search`) (Mục 3.3)
- **Kiến trúc mạng hai đầu `Connect4PolicyValueNet` (`278.952` tham số)**:
  + Đầu vào Tensor chuẩn hóa góc nhìn $2 \times 6 \times 7 \rightarrow$ Stem Conv 64 kênh $\rightarrow$ **3 Residual Blocks** $\rightarrow$ tách làm 2 đầu:
  + **Policy Head**: Masked Softmax xuất phân phối xác suất 7 cột $P_\theta(s, a)$.
  + **Value Head**: Kích hoạt $\tanh$ xuất ước lượng thắng cuộc $V_\theta(s) \in [-1, +1]$.
- **Nâng cấp từ Biased MCTS (KLTN tham khảo) lên PUCT-MCTS (`MixedMCTSAgent`)**:
  + Bước *Selection* dẫn đường bằng công thức **PUCT**:
    $$a^* = \arg\max_{a} \left[ Q(s,a) + c_{\text{puct}} P_\theta(s,a) \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)} \right]$$
  + Bước *Leaf Evaluation*: Dùng trực tiếp **Value Head $V_\theta(s)$** hoặc **Fast Bitboard Rollout**, kết hợp **Bảng băm Hoán vị $O(1)$ (`Transposition Cache` theo khóa `pos + mask`)**.

---

## CHƯƠNG 4: QUY TRÌNH QUẢN TRỊ DỮ LIỆU VÀ MINH BẠCH HÓA AI (XAI)

### Slide 8: Sơ đồ Data Pipeline 5 Bước & Chống Rò rỉ Dữ liệu Gương (Mục 4.1)
- **Sơ đồ quy trình tự sinh dữ liệu chuyên gia sạch (`src/c4/train/gen_data.py`)**:
  1. **Tự đấu chuyên gia**: `2.500` ván `Alpha-Beta (depth=4)`, khai cuộc ngẫu nhiên 4–6 ply, khám phá $\epsilon = 0,14$ ở 18 nước đầu nhưng **luôn lưu nhãn chuyên gia sạch (`y_policy = expert_action`)**.
  2. **Chia tập theo ván (`Game-level Split 70/15/15`)**: `1.750` ván Train / `375` ván Val / `375` ván Test.
  3. **Khử trùng lặp & Lọc chéo gương ngang**: Loại bỏ mọi mẫu trong Val/Test trùng với trạng thái gốc hoặc ảnh gương của Train (**0% Data Leakage**).
  4. **Tăng cường đối xứng lật ngang (`c' = 6 - c`) trên Train**: Thu được tổng cộng **`87.725` mẫu sạch** (`75.036` Train, `6.396` Val, `6.293` Test).

### Slide 9: Kiểm định Toán học Quá trình Huấn luyện Joint Loss (Mục 4.2a — Trả lời RQ2)
- *Hình chèn trên Slide*: `results/figures/nn_learning_curves.png`
- **Hàm mất mát kết hợp đa mục tiêu (*Joint Loss*)**:
  $$\mathcal{L}(\theta) = -\sum_{a=0}^6 \tilde{\pi}_a \log P_\theta(a \mid s) + 0,5 (z - V_\theta(s))^2 + 10^{-3} \|\theta\|_2^2$$
- **Sự hội tụ ổn định giữa Train & Validation**:
  + `Val Loss` giảm mượt từ `1,3859` (Epoch 1) xuống cực tiểu **`1,1336` tại Epoch 6** (không bị overfitting).
- **Kết quả kiểm định trên tập `Test` độc lập (`6.293` mẫu)**:
  + **Test Top-1 Accuracy = `71,68%`** (cao gấp **5,02 lần** đoán ngẫu nhiên `14,29%`).
  + **Test Top-2 Accuracy = `89,07%`** (gần 9/10 thế cờ nước tối ưu nằm trong 2 cột đầu của mạng!).
  + Độ trễ suy luận đơn lẻ trên CPU: **`1,91 ms`** (`p95 = 2,48 ms`).

### Slide 10: Minh bạch hóa Hộp đen bằng Bản đồ Độ nhạy Saliency Map (XAI) (Mục 4.2b)
- *Hình chèn trên Slide*: `results/figures/xai_saliency_double_threat.png`
- **Công thức độ nhạy đạo hàm bậc nhất**: $S_{r,c} = \sum_{k \in \{0,1\}} |\partial z_{a^*}(X) / \partial X_{k,r,c}|$.
- **Tình huống 1 (Phòng thủ sớm đòn kép hàng đáy)**:
  + `Heuristic` bỏ lọt vì chưa có chuỗi 3 quân; ngược lại ResNet dự đoán chặn sớm tại **Cột 3 (`P = 54,2%`)** và Saliency đạt cực đại **`1,00` đúng tại ô khóa đòn kép `(Hàng 1, Cột 3)`**.
- **Tình huống 2 (Đòn kết liễu đường chéo khe giữa)**:
  + Mạng dồn **98,9% xác suất vào Cột 3** (`Value = +0,601`), chiếu sáng chính xác các mắt xích trên đường chéo chiến thắng.

---

## CHƯƠNG 5: THỰC NGHIỆM ĐỐI KHÁNG VÀ PHÂN TÍCH KẾT QUẢ

### Slide 11: Giải đấu Vòng tròn Round-Robin Đối xứng 3.000 Ván (Mục 5.1)
- *Hình chèn trên Slide*: `results/figures/round_robin_heatmap.png`
- **Quy chuẩn công bằng**: 15 cặp × 200 ván (`100` khai cuộc 4-ply × 2 chiều đổi màu quân Đỏ/Vàng), kèm khoảng tin cậy Wilson 95% & Bootstrap 95%.
- **Bảng xếp hạng chung cuộc (`1.000` ván / tác tử)**:
  1. **Hạng 1 — `Mixed-MCTS PUCT (200 sims)`**: `705W - 90D - 205L` $\rightarrow$ **Score = 75,00%** (thắng `MCTS-1000` **62,50%**, vượt `Alpha-Beta d=5` **54,25%**).
  2. **Hạng 2 — `Alpha-Beta (depth 5)`**: `716W - 64D - 220L` $\rightarrow$ **Score = 74,80%** (`p95 ~ 61 ms`).
  3. **Hạng 3 — `MCTS-UCT (1.000 sims)`**: `596W - 27D - 377L` $\rightarrow$ **Score = 60,95%**.
  4. **Hạng 4 — `Policy-Value NN (0 search)`**: `460W - 87D - 453L` $\rightarrow$ **Score = 50,35%** (thắng `Heuristic` **64,25%** chỉ trong `~2,9 ms/nước`!).
  5. **Hạng 5 — `Heuristic`**: **38,50%** (thắng `Random` **99,50%**).
  6. **Hạng 6 — `Random`**: **0,40%**.

### Slide 12: Giải đáp RQ1 & Ablation A1–A2 (Động lực Duyệt cây & Điểm Giao thoa) (Mục 5.2a)
- *Hình chèn trên Slide*: `results/figures/timed_crossover_rq1.png`, `ablation_a1_nodes.png`, `ablation_a2_scaling.png`
- **Giải đấu cùng ngân sách thời gian (RQ1 — `50ms`, `100ms`, `300ms`)**:
  + Nhờ hệ số nhánh nhỏ ($b \le 7$) và Bitboard $O(1)$, `Alpha-Beta` đạt điểm **0,650** (50ms), **0,690** (100ms) và **0,605** (300ms) trước `MCTS-UCT`.
- **Ablation A1 (Cắt tỉa $\alpha$-$\beta$ & Center-First)**:
  + Giảm **80,45%** nút ở Depth 4, **87,89%** ở Depth 5 và **93,07% nút ở Depth 6** (`18.886` xuống `1.309` nút, nhanh gấp **62 lần**) mà giữ nguyên nghiệm tối ưu Minimax.
- **Ablation A2 (Điểm giao thoa MCTS vs Alpha-Beta Depth 4)**:
  + Điểm số MCTS tăng từ `0,065` (100 sims) lên **0,540 tại 2.000 sims** và **0,585 tại 5.000 sims** $\rightarrow$ **Cross-over tại ~1.500–2.000 mô phỏng**.

### Slide 13: Ablation A3 & A4 — Chứng minh "Duyệt Ít Hơn Nhưng Chất Lượng Hơn" (Mục 5.2b)
- *Hình chèn trên Slide*: `results/figures/ablation_a3_puct_value.png` & `first_player_advantage.png`
- **Ablation A3 (Tại cùng ngân sách nhỏ `200 mô phỏng`)**:
  + Khi gặp `MCTS-500`: `MCTS-UCT` thuần chỉ đạt **`32,5%`**, nhưng khi tích hợp mạng vào `PUCT_Prior_Rollout` và `PUCT_Prior_ValueHead`, điểm số vọt lên **`69,5%` và `68,5%`** (+37% điểm số!).
  + Khi gặp tác tử thầy `Alpha-Beta (depth 4)`: `MCTS-UCT` đạt `14,5%`, còn `PUCT_Prior_Rollout` đạt **`62,5%`** (`CI [0,535; 0,710]`) — **học trò vượt qua thầy dạy!**
- **Ablation A4 (Lợi thế người đi trước trên `3.000` ván)**:
  + Quân Đỏ (P1) thắng **51,80%** vs Quân Vàng (P2) thắng **42,57%** ($\Delta W = +9,23\%$), khẳng định tính bắt buộc của thiết kế đổi bên đối xứng.

### Slide 14: Bảng Tiến hóa Đa Phiên bản (v1 $\rightarrow$ v6) & Phân tích Đánh đổi Độ trễ (Mục 5.3)
- **Bảng tổng hợp tiến hóa 6 phiên bản tác tử (`1.000` ván/phiên bản)**:
  + `v1 (Random)`: `1` nút | `0,01 ms` | Score = **0,40%**
  + `v2 (Heuristic)`: `~14` nút | `0,25 ms` | Score = **38,50%**
  + `v3 (ResNet 0-Search)`: `1` lượt CNN | `3,86 ms` | Score = **50,35%**
  + `v4 (MCTS-UCT 1000)`: `1.000` sims | `148,8 ms` | Score = **60,95%**
  + `v5 (Alpha-Beta d=5)`: `~339` nút | `61,5 ms` | Score = **74,80%**
  + `v6 (Mixed-MCTS PUCT 200)`: **Chỉ `200` sims** | `709,1 ms` | Score = **75,00% (Hạng 1)**
- **Kết luận đánh đổi**: `v6` giảm **5 lần số mô phỏng** so với `v4` (`200` vs `1.000` sims) nhưng tăng điểm tổng thể từ `60,95%` lên `75,00%`.

### Slide 15: Demo Hệ thống Giao diện Đa nền tảng & Kết luận
- **Trình diễn trực tiếp qua `RUN_FAST.bat`**:
  + **Web App (`http://localhost:5000`)** & **Pygame Desktop 60 FPS**: Đấu trực tiếp với 6 cấp độ AI, đổi bên Đi trước/Đi sau, hoàn tác (`Undo`), chế độ Máy đấu Máy (`AI vs AI`) và hiển thị Telemetry độ trễ/nút duyệt thời gian thực.
- **Kết luận & Hướng phát triển**:
  + Giải quyết trọn vẹn RQ1–RQ3 trên **4.600+ ván thực nghiệm** và **57/57 unit tests Pass (100%)**.
  + Hướng mở rộng: Bổ sung Transposition Table cho Alpha-Beta và huấn luyện vòng lặp tự chơi tăng cường (*Iterative Self-Play RL*) trên bàn cờ lớn (Gomoku 15×15).
