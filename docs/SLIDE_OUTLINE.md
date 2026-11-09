# DÀN Ý SLIDE BÁO CÁO BẢO VỆ ĐỒ ÁN CUỐI KỲ
## Đề tài: Xây Dựng và Đánh Giá Game AI Đa Cấp Độ trên Connect Four (7×6)
**Nhóm 13 — Môn Trí Tuệ Nhân Tạo Nâng Cao — GVHD: Thầy Đỗ Như Tài**

---

### Slide 1: Trang bìa (Title Slide)
- **Tên đề tài**: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ — TRƯỜNG HỢP NGHIÊN CỨU: CONNECT FOUR (7×6)
- **Học phần**: Trí tuệ nhân tạo nâng cao (Advanced Artificial Intelligence)
- **Giảng viên hướng dẫn**: Thầy Đỗ Như Tài
- **Nhóm thực hiện (Nhóm 13)**:
  + Bùi Minh Trung (`3124720074`) — Nhóm trưởng (32%)
  + Trần Lê Minh Tâm (`3124720064`) — Thành viên (32%)
  + Nguyễn Thành Tài (`3124720062`) — Thành viên (18%)
  + Chương Gia Thịnh (`3124720067`) — Thành viên (18%)

---

### Slide 2: Đặt vấn đề và Ba câu hỏi nghiên cứu (RQ1–RQ3)
- **Bối cảnh**: Đối chiếu định lượng giữa AI kinh điển dựa trên tri thức/tìm kiếm (Rule-based, Alpha-Beta, MCTS) và AI học sâu có giám sát (Policy-Value ResNet, PUCT *AlphaGo-/AlphaZero-inspired*).
- **Trò chơi Connect Four (7×6)**: Thông tin hoàn hảo, xác định, tổng bằng không; không gian trạng thái xấp xỉ $4,5 \times 10^{12}$, 69 cửa sổ thắng 4 ô; người đi trước thắng nếu chơi tối ưu (Allis, 1988).
- **Ba câu hỏi nghiên cứu cốt lõi**:
  1. **RQ1**: Dưới cùng ngân sách thời gian mỗi nước (`50ms`, `100ms`, `300ms`), MCTS thuần có vượt qua Alpha-Beta không? Khi cố định độ sâu Alpha-Beta, điểm giao thoa nằm ở đâu?
  2. **RQ2**: Mạng `Connect4PolicyValueNet` học có giám sát từ nhãn sạch của `Alpha-Beta (depth=4)` đạt độ chính xác và sức mạnh thi đấu tới mức nào khi không tìm kiếm cây (`0 search`)?
  3. **RQ3**: Tích hợp Policy Prior $P(s,a)$ và Value Head $V(s)$ vào công thức chọn nút PUCT (`MixedMCTSAgent`) cải thiện hiệu năng ra sao so với MCTS-UCT thuần và chính tác tử thầy?

---

### Slide 3: Kiến trúc hệ thống phân tầng
- **Tầng Core Engine (`src/c4/game/`)**:
  + `Connect4` Bitboard 49-bit (7 cột × 7 bit có bit đệm chống tràn) kiểm tra thắng $O(1)$ bằng phép dịch bit.
  + `ReferenceConnect4` mảng 2D độc lập dùng để kiểm thử chéo (`10.000` ván ngẫu nhiên + kiểm định Perft).
- **Tầng Hệ phân cấp 6 Tác tử AI (`src/c4/agents/`)**:
  + Cấp 1 `RandomAgent` → Cấp 2 `HeuristicAgent` → Cấp 3 `AlphaBetaAgent` → Cấp 4 `MCTSAgent` (UCT) → Cấp 5 `NNAgent` (Policy-Value ResNet) → Mở rộng `MixedMCTSAgent` (PUCT + Transposition Cache + Dirichlet Noise).
- **Tầng Đánh giá & XAI (`src/c4/eval/`, `src/c4/models/explain.py`)**:
  + Giải đấu Round-Robin tự động từ YAML, khai cuộc 4-ply theo seed, đổi bên đối xứng, khoảng tin cậy Wilson 95% & Bootstrap 95%, phân vị độ trễ `p95`, bản đồ Saliency XAI.
- **Tầng Giao diện (`src/c4/ui/`)**: CLI, Pygame Desktop GUI (`Phím S` đổi bên Đỏ/Vàng) và Web App FastAPI + Docker.

---

### Slide 4: Lõi Engine Bitboard 49-bit & Kiểm thử tính đúng đắn
- **Biểu diễn trạng thái 2 số nguyên 64-bit** (`_pos`, `_mask`) và khóa băm trạng thái duy nhất `pos + mask` cho bảng băm/cache.
- **Bộ kiểm thử tự động 57 test cases (`pytest`) đạt 100% Pass**:
  + Đếm nút chính xác (Perft) khớp lý thuyết từ ply 1 đến ply 5 (`7; 49; 238; 1.120; 4.263`).
  + Kiểm thử chéo `10.000` ván ngẫu nhiên giữa `Connect4` và `ReferenceConnect4`: sai lệch `0%`.
  + **33 thế cờ kiểm thử thủ công (`tests/data/positions.csv`)** bao phủ thắng ngang/dọc/chéo, chặn thua trực tiếp, tránh tự sát cột kề và đòn kép (double threat).

---

### Slide 5: Tác tử Cấp 1–4 (Luật & Tìm kiếm Cây)
- **Cấp 1 (`RandomAgent`)**: Mốc cơ sở chọn đều ngẫu nhiên có hạt giống tái lập.
- **Cấp 2 (`HeuristicAgent`)**: 4 tầng luật ưu tiên nghiêm ngặt: Thắng ngay → Chặn thua ngay → Lọc nước trao chiến thắng tầng trên (anti-blunder) → Ưu tiên cột giữa `(3, 2, 4, 1, 5, 0, 6)`.
- **Cấp 3 (`AlphaBetaAgent`)**: Negamax + cắt tỉa $\alpha$-$\beta$ + sắp xếp Center-First + Iterative Deepening theo `time.perf_counter()` + hàm lượng giá 69 cửa sổ 4 ô.
- **Cấp 4 (`MCTSAgent`)**: Cây tìm kiếm đa tầng chuẩn Kocsis & Szepesvári (2006) lưu `(N, W)` tại mọi nút, công thức UCT ($c = 1,4$), tối ưu chọn ngay nước thắng/chặn trực tiếp tại gốc trước khi mô phỏng.

---

### Slide 6: Tác tử Cấp 5 & Mở rộng (Policy-Value ResNet & PUCT-MCTS)
- **Quy trình dữ liệu sạch chống rò rỉ (`gen_data.py`)**:
  + Sinh `2.500` ván từ `AlphaBeta(depth=4)` với khám phá $\epsilon = 0,14$ ở 18 nước đầu nhưng **luôn ghi nhãn chuyên gia sạch**; tàn cuộc chơi chuẩn để thu nhãn giá trị $z \in \{-1, 0, +1\}$.
  + Tách theo ván **70% Train (`1.750` ván) / 15% Val (`375` ván) / 15% Test (`375` ván)**, khử trùng lặp và lọc chéo cả trạng thái gốc lẫn **ảnh gương ngang** (`0%` trùng lặp giữa Train/Val/Test).
  + Tăng cường lật gương ngang chỉ trên Train → `75.036` mẫu Train, `6.396` mẫu Val, `6.293` mẫu Test.
- **Kiến trúc `Connect4PolicyValueNet` (278.952 tham số)**:
  + Đầu vào canon hóa `2 × 6 × 7` → Stem Conv 64 kênh → **3 Residual Blocks** → Hai đầu ra **Policy Head** (Masked Softmax 7 cột) & **Value Head** ($\tanh \in [-1, 1]$).
  + Kết quả trên tập **Test độc lập**: **Top-1 Acc = 71,68%**, **Top-2 Acc = 89,07%** (so với ngẫu nhiên `14,29%`), độ trễ CPU trung bình `1,91 ms`.
- **`MixedMCTSAgent` (PUCT)**: Tích hợp prior $P(s,a)$ vào hằng số khám phá PUCT ($c_{\text{puct}} = 1,5$), kèm bộ nhớ đệm trạng thái (Transposition Cache) và nhiễu Dirichlet tại gốc.

---

### Slide 7: Kết quả Giải đấu Round-Robin Toàn diện 6 Tác tử (3.000 Ván)
- **Thể thức**: 15 cặp đối đầu × 200 ván/cặp (`100` khai cuộc × 2 chiều đổi bên). Hình minh họa: `results/figures/round_robin_heatmap.png`.
- **Bảng xếp hạng sức mạnh tổng hợp (1.000 ván / tác tử)**:
  1. **`Mixed-MCTS PUCT` (200 sims)**: `705W – 90D – 205L` → **Score = 75,00%** (Hạng 1 — vượt cả `Alpha-Beta d=5` với tỷ số `54,25%` và thắng `MCTS-1000` tới `62,50%`!)
  2. **`Alpha-Beta` (depth 5)**: `716W – 64D – 220L` → **Score = 74,80%** (Hạng 2 — `p95 ~ 63 ms`)
  3. **`MCTS-UCT` (1.000 sims)**: `596W – 27D – 377L` → **Score = 60,95%** (Hạng 3 — `p95 ~ 153 ms`)
  4. **`Policy-Value NN` (0 search)**: `460W – 87D – 453L` → **Score = 50,35%** (Hạng 4 — thắng `Heuristic` **64,25%** chỉ với `p95 ~ 3,8 ms`!)
  5. **`Heuristic` (Rule-based)**: `350W – 70D – 580L` → **Score = 38,50%** (Hạng 5 — thắng `Random` **99,50%**)
  6. **`Random` (Baseline)**: `4W – 0D – 996L` → **Score = 0,40%** (Hạng 6)

---

### Slide 8: Giải đáp RQ1 — Chế độ A (Cùng Ngân sách Thời gian) & Ablation A2
- **Chế độ A — Giới hạn thời gian thực mỗi nước (`100` ván/mức, đơn luồng)**:
  + Mức `50 ms/nước`: `Alpha-Beta` đạt **Score = 0,650** (`64W-2D-34L`, CI `[0,555; 0,740]`).
  + Mức `100 ms/nước`: `Alpha-Beta` đạt **Score = 0,690** (`68W-2D-30L`, CI `[0,600; 0,775]`).
  + Mức `300 ms/nước`: `Alpha-Beta` đạt **Score = 0,605** (`59W-3D-38L`, CI `[0,510; 0,700]`) — `MCTS` thu hẹp khoảng cách lên `0,395`.
- **Ablation A2 — Cố định `Alpha-Beta depth 4`, tăng mô phỏng MCTS (`100 → 5.000` sims)**:
  + Điểm số MCTS tăng đơn điệu: `0,065` (100) → `0,305` (500) → `0,420` (1.000) → **0,540** (2.000) → **0,585** (5.000).
  + **Kết luận RQ1**: Trong Connect Four có hệ số nhánh nhỏ ($b \le 7$), Iterative Deepening + Heuristic giúp Alpha-Beta vượt MCTS thuần ở khung thời gian tương tác `50–300 ms`; nếu cố định Alpha-Beta ở `depth 4`, điểm giao thoa (cross-over) xuất hiện tại **~1.500–2.000 mô phỏng**.

---

### Slide 9: Các Nghiên cứu Phân rã Ablation A1, A3 & A4
- **Ablation A1 (Cắt tỉa $\alpha$-$\beta$ & Center-First)**:
  + Giảm số nút duyệt: **80,45%** ở depth 4 (`399 → 78`), **87,89%** ở depth 5 (`2.800 → 339`), **93,07%** ở depth 6 (`18.886 → 1.309` nút, tăng tốc `62×`) mà giữ nguyên giá trị Minimax tuyệt đối.
- **Ablation A3 (RQ2 & RQ3 — Vai trò Policy Prior & Value Head ở cùng `200` sims)**:
  + Đấu `MCTS-500`: `MCTS-UCT` chỉ đạt `0,325`, `NN Policy-Only` đạt `0,440`, trong khi `PUCT+Rollout` vọt lên **0,695** và `PUCT+ValueHead` đạt **0,685** (+36% đến +37% điểm số!).
  + Đấu tác tử thầy `Alpha-Beta d=4`: `PUCT+Rollout` đạt **0,625** (`151 ms/nước`) và `PUCT+ValueHead` đạt **0,510** — học trò kết hợp tìm kiếm vượt qua thầy dạy!
- **Ablation A4 (Lợi thế người đi trước trên `3.000` ván)**:
  + Đỏ (đi trước) thắng `1.554` ván (**51,80%**), Vàng (đi sau) thắng `1.277` ván (**42,57%**), Hòa `169` ván → $\Delta W = +9,23\%$, khẳng định vai trò sống còn của thiết kế đổi bên.

---

### Slide 10: Phân tích Chiến thuật & Explainable AI (Saliency Heatmap)
- **Trực quan hóa hộp đen CNN bằng Gradient Saliency $|\partial z_{a^*} / \partial X|$** (`results/figures/xai_saliency_double_threat.png`):
  + **Tình huống 1 (Phòng thủ sớm đòn kép hàng đáy)**: Khi X mới có 2 quân kề nhau ở trung tâm, `Heuristic` bỏ lọt vì chưa xuất hiện chuỗi 3 quân; ngược lại `Connect4PolicyValueNet` và `Alpha-Beta` tập trung độ nhạy cao nhất quanh cặp quân trung tâm và chặn ngay đầu mở trước khi đòn kép hình thành.
  + **Tình huống 2 (Đường chéo thắng khe giữa)**: Mạng dự đoán chính xác Cột 3 với xác suất **98,9%** (`Value = +0,601`), bản đồ nhiệt chiếu sáng đúng các mắt xích trên đường chéo chiến thắng.

---

### Slide 11: Trình diễn Ứng dụng (Pygame Desktop GUI & FastAPI Web App)
- **Chế độ Người vs Máy (`H_AI`)**: Lựa chọn tự do 6 cấp AI, thanh trượt cấu hình `Depth / Simulations`, nút đổi bên cầm Đỏ đi trước hoặc Vàng đi sau.
- **Chế độ Máy vs Máy (`AI_AI`) & Telemetry trực tiếp**: Hiển thị tức thời thời gian suy nghĩ (ms), số nút duyệt, số mô phỏng, tỷ lệ thắng ước lượng và trạng thái nạp checkpoint.

---

### Slide 12: Kết luận, Đóng góp & Hướng phát triển
- **Tổng kết**: Hoàn thành 100% các mốc M1–M8 của Đề cương; kiểm chứng đầy đủ RQ1–RQ3 trên **4.600+ ván thực nghiệm có log thô CSV** và **57 unit tests đạt 100% Pass**.
- **Tính tái lập khoa học**: Cố định seed ở mọi khâu (sinh dữ liệu, huấn luyện ResNet, khai cuộc giải đấu, bootstrap CI) và đóng gói tự động chuẩn nộp bài.
- **Hướng phát triển**: Huấn luyện tự chơi lặp (Iterative Self-Play RL) kiểu AlphaZero để nâng độ chính xác của Value Head ở thế cờ tàn phức tạp và mở rộng sang bàn cờ lớn hơn (Gomoku 15×15).
