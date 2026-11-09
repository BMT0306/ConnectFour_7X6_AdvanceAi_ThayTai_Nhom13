# TRƯỜNG ĐẠI HỌC SÀI GÒN — KHOA CÔNG NGHỆ THÔNG TIN
# BÁO CÁO ĐỒ ÁN CUỐI KỲ: TRÍ TUỆ NHÂN TẠO NÂNG CAO
## ĐỀ TÀI: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ
### Trường hợp nghiên cứu: Connect Four (7×6)

* **Giảng viên hướng dẫn**: Thầy Đỗ Như Tài
* **Nhóm thực hiện**: Nhóm 13 — Connect Four (7×6)
* **Repository GitHub**: https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13

| STT | Họ và Tên | MSSV | Vai trò | Nhiệm vụ chính | Đóng góp |
|:---:|:---|:---:|:---:|:---|:---:|
| 1 | **Bùi Minh Trung** | `3124720074` | Nhóm trưởng (TV1) | Engine (`bitboard` + `reference`), API & bộ unit test; `HeuristicAgent`, `AlphaBetaAgent`; khung giải đấu & thống kê (`Wilson`, `Bootstrap`, `p95`); Ablation A1 & A3; XAI Saliency; Web/Docker UI; quản lý GitHub, review PR & đóng gói | **32%** |
| 2 | **Trần Lê Minh Tâm** | `3124720064` | Thành viên (TV2) | `RandomAgent`, `MCTSAgent` (UCT 4 bước); kiến trúc mạng hai đầu `Connect4PolicyValueNet`, pipeline sinh dữ liệu/huấn luyện & `MixedMCTSAgent` (PUCT + Transposition Cache + Dirichlet noise); giao diện Pygame GUI; Ablation A2 & A4 | **32%** |
| 3 | **Nguyễn Thành Tài** | `3124720062` | Thành viên (TV3) | Chạy thực nghiệm giải đấu & ablation, thu thập log CSV thô; xây dựng & chạy notebook phân tích (`01_tournament_analysis.ipynb`); bổ sung vị trí kiểm thử thủ công (`positions.csv`); phân tích ván đấu & viết Chương 4 | **18%** |
| 4 | **Chương Gia Thịnh** | `3124720067` | Thành viên (TV4) | Biên soạn Chương 1, 2, 3, 5 của báo cáo cuối kỳ; thiết kế Slide thuyết trình, Poster khổ A0, kịch bản/quay Video Demo; rà soát tài liệu tham khảo, `THIRD_PARTY.md`, `README.md` và chuẩn bị bản in | **18%** |
| **Tổng** | | | | | **100%** |

---

## TÓM TẮT ĐỒ ÁN (ABSTRACT)

Đồ án này nghiên cứu, thiết kế và đánh giá thực nghiệm một hệ thống trí tuệ nhân tạo (AI) đa cấp độ hoàn chỉnh cho trò chơi đối kháng thông tin hoàn hảo **Connect Four kích thước chuẩn 7 cột × 6 hàng**. Trên nền tảng lõi **Engine Bitboard 49-bit** tốc độ cao (được kiểm chứng tuyệt đối qua kiểm định Perft đến độ sâu 5 và đối chiếu chéo 10.000 ván ngẫu nhiên không sai lệch với `ReferenceConnect4`), nhóm xây dựng chuỗi **6 tác tử AI** tăng tiến rõ rệt về tri thức và chiến lược suy luận: Cấp 1 (`RandomAgent`), Cấp 2 (`HeuristicAgent` dựa trên 4 tầng luật ưu tiên), Cấp 3 (`AlphaBetaAgent` kết hợp Negamax, cắt tỉa $\alpha$-$\beta$, sắp xếp Center-First và Iterative Deepening), Cấp 4 (`MCTSAgent` dùng cây UCT đa tầng), Cấp 5 (`NNAgent` dùng mạng học sâu `Connect4PolicyValueNet` gồm 3 khối Residual và 278.952 tham số học có giám sát từ nhãn chuyên gia sạch), và Cấp mở rộng (`MixedMCTSAgent` tích hợp Policy Prior và Value Head vào công thức tìm kiếm cây PUCT theo cảm hứng từ AlphaGo/AlphaZero, kèm cơ chế giải thích hộp đen bằng bản đồ độ nhạy đạo hàm bậc nhất — *Gradient Saliency Map*).

Để đảm bảo tính khách quan và khả năng tái lập khoa học, mọi tác tử được đặt vào khung giải đấu vòng tròn **Round-Robin 3.000 ván** (15 cặp × 200 ván, gồm 100 khai cuộc 4 nước cố định theo hạt giống và luân phiên đổi bên đi trước/đi sau), kết hợp giải đấu giới hạn thời gian thực **300 ván** (50 ms, 100 ms, 300 ms/nước) và 4 nghiên cứu phân rã (**Ablation A1–A4**). Kết quả thực nghiệm cho thấy: (1) Cắt tỉa $\alpha$-$\beta$ kèm Center-First giảm **93,07%** số nút duyệt ở độ sâu 6; (2) Mạng `Connect4PolicyValueNet` huấn luyện trên tập dữ liệu tách theo ván chống rò rỉ 100% (kể cả ảnh gương ngang) đạt **71,68% Top-1 Accuracy** và **89,07% Top-2 Accuracy** trên tập `Test` độc lập (`6.293` mẫu), tự mình đánh bại `HeuristicAgent` với điểm số **64,25%** chỉ trong `2,74 ms/nước` mà không cần tìm kiếm cây; (3) Khi kết hợp mạng nơ-ron vào tìm kiếm cây PUCT với chỉ **200 mô phỏng** (`MixedMCTSAgent`), tác tử lai vươn lên đứng đầu bảng xếp hạng toàn giải (**Score = 75,00%**), đánh bại cả `MCTS-UCT 1.000 sims` (**62,50%**) lẫn `Alpha-Beta depth 5` (**54,25%**).

---

## CHƯƠNG 1. GIỚI THIỆU

### 1.1. Bối cảnh đề tài
Các trò chơi đối kháng có thông tin hoàn hảo (perfect-information adversarial games) từ lâu đã đóng vai trò là thước đo chuẩn mực cho sự tiến bộ của Trí tuệ nhân tạo — khởi đầu từ chiến thắng lịch sử của Deep Blue trong cờ vua (1997) dựa trên tìm kiếm cắt tỉa chuyên sâu và hàm lượng giá thủ công, cho tới bước ngoặt của AlphaGo (Silver et al., 2016) và AlphaZero (Silver et al., 2017) kết hợp mạng nơ-ron tích chập sâu với tìm kiếm cây Monte Carlo (MCTS). Việc triển khai đồng thời cả hai trường phái — **AI kinh điển dựa trên tri thức/tìm kiếm** và **AI học sâu dữ liệu** — trên cùng một môi trường chuẩn cho phép định lượng minh bạch sự đánh đổi giữa tốc độ tính toán, độ sâu chiến thuật, chi phí huấn luyện và khả năng giải thích quyết định.

### 1.2. Trò chơi Connect Four (7×6) dưới góc nhìn Lý thuyết Trò chơi
Connect Four diễn ra trên lưới thẳng đứng gồm 7 cột và 6 hàng (42 ô). Hai người chơi (Quân Đỏ — `PLAYER1` đi trước; Quân Vàng — `PLAYER2` đi sau) luân phiên thả quân vào một trong các cột chưa đầy; dưới tác dụng trọng lực, quân cờ rơi xuống ô trống thấp nhất của cột đó. Ván đấu kết thúc ngay khi một bên tạo được chuỗi **4 quân liên tiếp** cùng màu theo chiều ngang, dọc hoặc một trong hai đường chéo (tổng cộng có **69 cửa sổ 4 ô** trên bàn cờ 7×6), hoặc hòa khi toàn bộ 42 ô đã kín.

Theo phân loại của Russell & Norvig (2021), Connect Four là môi trường **quan sát đầy đủ** (fully observable), **xác định** (deterministic), **hữu hạn rời rạc** (discrete, tối đa 42 nước đi, hệ số nhánh $b \le 7$), **tuần tự theo lượt** (turn-based) và **đối kháng tổng bằng không** (zero-sum). Không gian trạng thái hợp lệ của trò chơi vào khoảng $4,53 \times 10^{12}$ trạng thái (Allis, 1988; Edelkamp & Kissmann, 2008). Dù trò chơi đã được Victor Allis chứng minh toán học năm 1988 là người đi trước thắng nếu chơi tối ưu tuyệt đối (khi đi cột trung tâm đầu tiên), độ lớn $4,5 \times 10^{12}$ vẫn khiến tìm kiếm vét cạn trực tiếp hoàn toàn bất khả thi trong thời gian thực nếu thiếu kỹ thuật biểu diễn bitboard, cắt tỉa nhánh hoặc dẫn đường bằng mạng nơ-ron.

### 1.3. Mục tiêu và Ba Câu hỏi Nghiên cứu (Research Questions)
Đề tài hướng tới xây dựng hệ thống phần mềm và thực nghiệm hoàn chỉnh nhằm trả lời định lượng ba câu hỏi nghiên cứu:
- **RQ1 (So sánh Tìm kiếm Đối kháng và Tìm kiếm Ngẫu nhiên theo Ngân sách)**: Dưới cùng ngân sách thời gian suy nghĩ mỗi nước đi (`50 ms`, `100 ms`, `300 ms`), `MCTS-UCT` thuần có vượt qua `Alpha-Beta` (Iterative Deepening) hay không? Khi cố định độ sâu của `Alpha-Beta` (`depth = 4`), điểm giao thoa (cross-over point) về số lượng mô phỏng của `MCTS` xuất hiện tại ngưỡng nào?
- **RQ2 (Sức mạnh Học bắt chước Có giám sát — Behavioral Cloning)**: Mô hình mạng nơ-ron tích chập sâu `Connect4PolicyValueNet` học có giám sát từ nhãn nước đi sạch của chuyên gia `Alpha-Beta (depth = 4)` đạt độ chính xác dự đoán trên tập `Test` độc lập là bao nhiêu, và khi suy luận trực tiếp không kèm tìm kiếm cây (`0 search`) đạt sức mạnh đối kháng tới mức nào so với `Heuristic`, `MCTS` và chính tác tử thầy?
- **RQ3 (Hiệu quả Lai ghép Mạng Nơ-ron với Tìm kiếm Cây PUCT & Giải thích AI)**: Việc tích hợp xác suất tiên nghiệm Policy Prior $P(s, a)$ và đầu lượng giá Value Head $V(s)$ vào công thức chọn nút PUCT (`MixedMCTSAgent`, lấy cảm hứng từ AlphaGo/AlphaZero) cải thiện tỷ lệ thắng ra sao so với `MCTS-UCT` thuần cùng ngân sách mô phỏng, đồng thời bản đồ độ nhạy đạo hàm (Saliency Map) cho thấy mạng nơ-ron chú ý vào những cấu trúc chiến thuật nào trên bàn cờ?

### 1.4. Phạm vi và Cam kết Trung thực Học thuật
- **Trong phạm vi**: Engine Bitboard 49-bit và Reference Engine 2D; 6 cấp tác tử (`Random`, `Heuristic`, `Alpha-Beta`, `MCTS-UCT`, `Policy-Value ResNet`, `Mixed-MCTS PUCT`); giải thích quyết định bằng Gradient Saliency; bộ kiểm thử tự động `pytest` 57 test cases; khung giải đấu Round-Robin đa chế độ, 4 nghiên cứu phân rã A1–A4; ứng dụng CLI, Pygame GUI và FastAPI Web App + Docker.
- **Ngoài phạm vi & Giới hạn trung thực**: Đồ án **tuyệt đối không sử dụng bất kỳ bộ giải tối ưu (exact solver) hay cơ sở dữ liệu khai cuộc hoàn hảo bên ngoài nào**. Toàn bộ trọng số mô hình và hơn **4.600 ván đấu thực nghiệm** đều được sinh, huấn luyện và thi đấu thực tế trên CPU cá nhân từ mã nguồn của nhóm. Cách tiếp cận `MixedMCTSAgent` được định danh chính xác là **AlphaGo-/AlphaZero-inspired** (dùng mạng Policy-Value huấn luyện có giám sát kết hợp tìm kiếm PUCT, chưa chạy vòng lặp tự chơi tăng cường nhiều thế hệ trên cụm GPU).

---

## CHƯƠNG 2. CƠ SỞ LÝ THUYẾT VÀ CÔNG TRÌNH LIÊN QUAN

### 2.1. Tìm kiếm Đối kháng: Negamax, Cắt tỉa Alpha-Beta và Iterative Deepening
Trong trò chơi tổng bằng không hai người chơi đối xứng điểm số $u_{\text{max}}(s) = -u_{\text{min}}(s)$, thuật toán Minimax được rút gọn thanh thoát về dạng **Negamax**:

$$V(s, d) = \begin{cases} \text{eval}(s) & \text{nếu } d = 0 \text{ hoặc } s \text{ kết thúc} \\ \max_{a \in A(s)} \left( -V(\text{step}(s, a), d - 1) \right) & \text{ngược lại} \end{cases}$$

Kỹ thuật **cắt tỉa Alpha-Beta** duy trì cửa sổ $[\alpha, \beta]$ biểu diễn điểm thấp nhất bên đang đi đã nắm chắc ($\alpha$) và điểm cao nhất đối phương cho phép ($\beta$). Bất cứ khi nào tìm thấy hành động làm $\alpha \ge \beta$, toàn bộ các nhánh con còn lại tại nút đó đều bị cắt bỏ mà **không làm thay đổi kết quả toán học của Minimax**. Trong trường hợp sắp xếp nước đi lý tưởng (duyệt nước tốt nhất trước tiên), độ phức tạp số nút lá giảm từ $O(b^d)$ xuống xấp xỉ $O(b^{d/2})$ — tức cho phép tìm kiếm sâu gần gấp đôi với cùng chi phí tính toán. Trong Connect Four, các cột trung tâm tham gia vào nhiều cửa sổ 4 ô nhất, do đó thứ tự ưu tiên tĩnh **Center-First** `(3, 2, 4, 1, 5, 0, 6)` đóng vai trò xấp xỉ sắp xếp nước đi rất hiệu quả. Khi thi đấu theo giới hạn thời gian thực, **Iterative Deepening** tăng dần độ sâu $d = 1, 2, \dots, d_{\max}$ và kiểm tra đồng hồ `time.perf_counter()` để luôn bảo toàn nghiệm hoàn chỉnh của tầng sâu nhất đã hoàn tất.

### 2.2. Tìm kiếm Cây Monte Carlo (MCTS) với Công thức UCT
Khác với Alpha-Beta cần hàm lượng giá thủ công đặc thù miền, **MCTS** (Kocsis & Szepesvári, 2006) ước lượng giá trị trạng thái thông qua lấy mẫu ngẫu nhiên có định hướng, gồm 4 pha lặp lại: *Selection*, *Expansion*, *Simulation (Rollout)* và *Backpropagation*. Tại pha *Selection*, nút con $a$ được chọn nhằm cực đại hóa chỉ số **UCT** (Upper Confidence Bounds applied to Trees):

$$\text{UCT}(s, a) = \frac{W(s, a)}{N(s, a)} + c \sqrt{\frac{\ln N(s)}{N(s, a)}}$$

trong đó $N(s, a)$ là số lượt đi qua nhánh $(s, a)$, $W(s, a)$ là tổng điểm tích lũy theo góc nhìn của người chơi vừa thực hiện hành động $a$, và hằng số $c = 1,4 \approx \sqrt{2}$ điều tiết cân bằng giữa **khai thác** nhánh đang có tỷ lệ thắng cao với **khám phá** các nhánh ít được thăm.

### 2.3. Mạng Nơ-ron Tích chập Residual (Policy-Value ResNet) và Tìm kiếm PUCT
Để khắc phục nhược điểm "mù chiến thuật" của các pha rollout ngẫu nhiên đồng đều trong MCTS truyền thống, kiến trúc **Policy-Value Network** (Silver et al., 2017; Liu, 2025) mã hóa trạng thái bàn cờ thành tensor không gian đa kênh $X \in \mathbb{R}^{2 \times 6 \times 7}$ theo góc nhìn chuẩn hóa (canonical view) của bên sắp đi, trích xuất đặc trưng qua các khối tích chập có kết nối tắt (**Residual Blocks**) rồi phân nhánh thành hai đầu ra:
1. **Policy Head** xuất vector xác suất tiên nghiệm $P(s, a)$ trên 7 cột sau khi che mặt nạ các cột đã đầy (legal move masking).
2. **Value Head** xuất ước lượng kỳ vọng thắng cuộc vô hướng $V_\theta(s) \in [-1, +1]$ qua hàm kích hoạt $\tanh$.

Hàm mất mát đa nhiệm kết hợp Cross-Entropy có làm mượt nhãn (*Label Smoothing* $\alpha_{\text{ls}}$) cho Policy, sai số bình phương trung bình (MSE) cho Value và điều chuẩn trọng số $L_2$:

$$\mathcal{L}(\theta) = -\sum_{a=0}^{6} \tilde{\pi}_a \log P_\theta(a \mid s) + \lambda_v \left( z - V_\theta(s) \right)^2 + \lambda_{\text{wd}} \|\theta\|_2^2$$

Khi tích hợp vào cây tìm kiếm, công thức **PUCT** (Predictor + UCT) sử dụng trực tiếp $P_\theta(s, a)$ để định hướng khám phá vào các nhánh giàu triển vọng ngay từ những mô phỏng đầu tiên:

$$a^* = \arg\max_{a \in A(s)} \left[ Q(s, a) + c_{\text{puct}} \cdot P_\theta(s, a) \cdot \frac{\sqrt{\sum_b N(s, b)}}{1 + N(s, a)} \right]$$

### 2.4. Giải thích Hộp đen Mạng Nơ-ron bằng Bản đồ Độ nhạy (Gradient Saliency Map)
Theo phương pháp giải thích dựa trên đạo hàm của Simonyan et al. (2014), để lý giải vì sao mạng chọn cột $a^* = \arg\max_a z_a(X)$ tại trạng thái $X \in \mathbb{R}^{2 \times 6 \times 7}$, ta lan truyền ngược đạo hàm bậc nhất của logit $z_{a^*}$ theo đầu vào và tổng hợp độ lớn trên hai kênh quân cờ:

$$S_{r, c} = \sum_{k \in \{0, 1\}} \left| \frac{\partial z_{a^*}(X)}{\partial X_{k, r, c}} \right|, \qquad \hat{S}_{r, c} = \frac{S_{r, c}}{\max_{r', c'} S_{r', c'} + \varepsilon}$$

Ma trận $\hat{S} \in [0, 1]^{6 \times 7}$ cho biết mức độ nhạy cảm chiến thuật của từng ô trên bàn cờ đối với quyết định của mạng nơ-ron.

---

## CHƯƠNG 3. PHƯƠNG PHÁP VÀ THIẾT KẾ HỆ THỐNG

### 3.1. Kiến trúc Phần mềm Phân tầng
Hệ thống được tổ chức thành gói Python chuẩn cài đặt qua `pyproject.toml` với ranh giới trách nhiệm tách biệt:
- `src/c4/game/`: Định nghĩa giao diện trừu tượng `Connect4Base`, lõi tốc độ cao `Connect4` (bitboard 49-bit) và bản đối chiếu `ReferenceConnect4` (mảng 2D).
- `src/c4/agents/`: Giao diện chung `Agent`, cấu trúc ngân sách `Budget(time_s, simulations, depth)` và 6 lớp tác tử độc lập với tầng giao diện.
- `src/c4/models/` & `src/c4/train/`: Mạng `Connect4PolicyValueNet`, mô-đun giải thích `compute_saliency_map`, quy trình sinh dữ liệu đa nhân `gen_data.py` và huấn luyện `train_policy.py`.
- `src/c4/eval/` & `scripts/`: Bộ điều phối ván đấu công bằng `match.py`, thống kê `metrics.py`, kịch bản giải đấu `run_tournament.py`, phân rã `run_ablation.py`, kiểm thử tự động `run_test_suite_and_save.py`.
- `src/c4/ui/`: Ba giao diện độc lập gồm CLI (`cli.py`), Pygame Desktop (`gui.py`) và FastAPI Web Server (`web_server.py` + `Dockerfile`).

### 3.2. Thiết kế Lõi Engine Bitboard 49-bit (`src/c4/game/engine.py`)
Theo bố cục bitboard kinh điển của Pons, bàn cờ 7×6 được ánh xạ vào 49 bit thấp của số nguyên 64-bit theo thứ tự cột: cột $c \in \{0..6\}$ chiếm dải bit $[7c, 7c+5]$ từ đáy lên đỉnh, còn bit thứ 7 của mỗi cột ($7c+6$) luôn bằng `0` đóng vai trò **bit đệm chống tràn (sentinel bit)** ngăn các phép dịch bit chéo/dọc tràn sang cột kế cận. Trạng thái chỉ cần lưu hai số nguyên:
- `_pos`: bitboard các quân của người chơi **đang đến lượt**.
- `_mask`: bitboard hợp của **tất cả các quân** đã đánh trên bàn.

Nhờ biểu diễn này:
1. **Thả quân $O(1)$**: Quân mới tại cột $c$ nằm ngay ở bit thấp nhất phía trên cột đó thông qua phép cộng nhị phân `new_mask = _mask | (_mask + bottom_mask(c))`, sau đó lật góc nhìn sang đối thủ bằng phép XOR `_pos ^= _mask`.
2. **Kiểm tra thắng $O(1)$**: Hàm `_has_won(bb)` kiểm tra đồng thời toàn bộ bàn cờ chỉ bằng 4 cặp phép dịch bit và phép AND theo 4 hướng dịch bước $s \in \{1 \text{ (dọc)}, 7 \text{ (ngang)}, 6 \text{ (chéo phụ)}, 8 \text{ (chéo chính)}\}$: `m = bb & (bb >> s); if m & (m >> 2s): return True`.
3. **Khóa băm duy nhất 1-1**: Tổng số nguyên `key() = _pos + _mask` xác định duy nhất mọi trạng thái hợp lệ trên bàn cờ, phục vụ cực nhanh cho bảng băm trạng thái của `MixedMCTSAgent` và khử trùng lặp tập dữ liệu huấn luyện.

### 3.3. Thiết kế Chi tiết Sáu Cấp độ Tác tử AI
1. **Cấp 1 — `RandomAgent`**: Sử dụng bộ sinh ngẫu nhiên độc lập `random.Random(seed)` chọn đồng đều một cột trong `legal_actions()`, đảm bảo tính tái lập tuyệt đối.
2. **Cấp 2 — `HeuristicAgent`**: Thực thi tuần tự 4 quy tắc ưu tiên tất định: (i) Nếu có cột tạo chiến thắng ngay lập tức → đánh ngay; (ii) Nếu đối thủ có điểm thắng ở lượt kế tiếp → chặn ngay theo thứ tự ưu tiên gần trung tâm; (iii) **Lọc chống tự sát (Anti-blunder)**: Loại bỏ các nước đi mà ngay sau khi thả quân, ô trống chồng trực tiếp lên nó giúp đối thủ thắng ngay ở lượt kế (nếu mọi nước đều nguy hiểm mới buộc giữ lại toàn bộ); (iv) Chọn cột gần trung tâm nhất theo dãy `(3, 2, 4, 1, 5, 0, 6)`.
3. **Cấp 3 — `AlphaBetaAgent`**: Cài đặt đệ quy Negamax có cắt tỉa $\alpha$-$\beta$ và sắp xếp nước đi Center-First. Trước khi gọi đệ quy ở các nút, tác tử kiểm tra nhanh thắng trực tiếp để cắt sớm ở điểm cực đại `WIN_SCORE + depth` (ưu tiên thắng nhanh nhất và kéo dài tối đa nếu bị ép thua). Tại độ sâu giới hạn $d=0$, hàm lượng giá tĩnh cộng điểm thưởng cột trung tâm (`+3 × hiệu số quân cột 4`) với điểm lượng giá toàn bộ **69 cửa sổ 4 ô** đã tiền tính sẵn chỉ số bitmask (`+50` cho 3 quân mình + 1 trống, `+6` cho 2 quân mình + 2 trống, `-80` cho 3 quân địch + 1 trống đe dọa trực tiếp, `-8` cho 2 quân địch + 2 trống). Hỗ trợ đầy đủ cả chế độ cố định `depth` và Iterative Deepening theo `time_s`.
4. **Cấp 4 — `MCTSAgent`**: Duyệt cây đa tầng thực thụ lưu `(visits, wins, untried, children)` tại mọi nút mở rộng. Trước khi chạy vòng lặp mô phỏng, tác tử kiểm tra nhanh tại gốc nếu có nước thắng ngay hoặc nước bắt buộc chặn thua duy nhất để phản xạ tức thì. Sau khi hết ngân sách `simulations` hoặc `time_s`, chọn hành động có số lượt thăm `visits` lớn nhất (**robust child**).
5. **Cấp 5 — `NNAgent` (`Connect4PolicyValueNet`)**: Nhận tensor canon hóa `(1, 2, 6, 7)`, đi qua lớp tích chập đầu vào `Conv2d(2→64, 3×3) + BN + ReLU`, tiếp nối bởi **3 khối Residual** (mỗi khối gồm 2 lớp `Conv2d(64→64, 3×3) + BN` và kết nối tắt cộng trực tiếp), rồi tách thành Policy Head (`Conv2d(64→2, 1×1) → Linear(84→7)`) và Value Head (`Conv2d(64→1, 1×1) → Linear(42→64) → ReLU → Linear(64→1) → Tanh`). Tổng số tham số khả huấn luyện là **278.952**. Suy luận dưới `torch.inference_mode()` gán $-\infty$ cho các cột bất hợp lệ trước khi chọn `argmax` (khi `temperature = 0`).
6. **Cấp mở rộng — `MixedMCTSAgent` (PUCT)**: Tích hợp `Connect4PolicyValueNet` vào cây tìm kiếm PUCT ($c_{\text{puct}} = 1,5$). Để tăng tốc trên CPU, tác tử trang bị **Transposition Cache (`_cache`)** lưu cặp `(base_priors, leaf_value)` theo khóa bitboard `game.key()`, tránh gọi lại mạng nơ-ron khi các đường đi khác nhau dẫn tới cùng một thế cờ. Hỗ trợ tham số `use_value_head: bool` (khi `True` dùng trực tiếp $V_\theta(s)$ tại nút lá; khi `False` dùng rollout nhanh để phục vụ Ablation A3) và tùy chọn nhiễu khám phá Dirichlet tại gốc sử dụng `rng.gammavariate` chuẩn xác, đồng thời sao chép mảng xác suất để không làm bẩn bộ nhớ đệm.

### 3.4. Quy trình Sinh Dữ liệu Sạch Chống Rò rỉ và Huấn luyện Có Điều chuẩn
Một lỗ hổng phổ biến trong học bắt chước trò chơi là vừa dùng $\epsilon$-greedy để khám phá trạng thái mới nhưng lại lưu luôn nước đi ngẫu nhiên làm nhãn huấn luyện (gây nhiễu nhãn ~10–15%), hoặc tách ngẫu nhiên từng mẫu dẫn đến hai trạng thái kế tiếp trong cùng một ván lọt vào cả Train và Test, thậm chí trạng thái lật gương của Train xuất hiện trong Test. Quy trình `gen_data.py` của nhóm giải quyết triệt để cả ba vấn đề:
1. **Nhãn chuyên gia sạch 100%**: Sinh `2.500` ván tự đấu từ `AlphaBetaAgent(depth=4)` với khai cuộc ngẫu nhiên 4–6 nước. Ở 18 nước đầu, chuyên gia luôn tính nước tối ưu `expert_action` để **lưu làm nhãn Policy sạch**, sau đó mới tung đồng xu $\epsilon = 0,14$ để thỉnh thoảng bước sang nhánh phụ làm giàu dữ liệu; từ nước thứ 19 trở đi chơi chuẩn $\epsilon = 0$ để nhãn kết cục ván đấu $z \in \{-1, 0, +1\}$ phản ánh chính xác giá trị thế cờ.
2. **Tách theo ván (Game-level Split) & Khử trùng lặp hai chiều gương**: Tách nguyên vẹn từng ván thành **1.750 ván Train (70%) / 375 ván Val (15%) / 375 ván Test (15%)**. Trong mỗi tập, các thế cờ trùng khóa được gộp lại bằng biểu quyết đa số cho nhãn hành động và trung bình cộng cho nhãn giá trị. Tiếp theo, toàn bộ thế cờ trong `Val` và `Test` có khóa trùng với trạng thái gốc **hoặc ảnh lật gương ngang** của `Train` đều bị loại bỏ hoàn toàn (`2.917` mẫu bị lọc khỏi `Val` và `3.468` mẫu bị lọc khỏi `Test`), đảm bảo **độ trùng lặp giữa Train/Val/Test bằng 0% tuyệt đối**.
3. **Tăng cường dữ liệu đối xứng chỉ trên Train**: Chỉ tập `Train` (`37.518` thế cờ độc nhất) được nhân đôi qua phép lật gương ngang bàn cờ ($c' = 6 - c$), thu được **75.036 mẫu Train**, **6.396 mẫu Val** và **6.293 mẫu Test**.
4. **Huấn luyện điều chuẩn (`train_policy.py`)**: Tối ưu bằng `Adam` (`lr = 1,5e-3`, `weight_decay = 1e-3`) kết hợp lịch giảm tốc độ học `CosineAnnealingLR` trong 10 epochs (`batch_size = 256`), `label_smoothing = 0,05` và trọng số đầu giá trị $\lambda_v = 0,5$. Hàm đánh giá trên `Val`/`Test` sử dụng Cross-Entropy chuẩn không làm mượt để đo trung thực xác suất dự đoán.

### 3.5. Thiết kế Giải đấu Công bằng và Độ đo Thống kê
- **Kiểm soát thiên lệch khai cuộc & màu quân**: Sinh tập `100` khai cuộc 4 nước hợp lệ khác nhau cố định theo `seed = 42` (`50` khai cuộc cho giải tính giờ và Ablation A2/A3). Với mỗi khai cuộc $o_i$, hai tác tử $(A, B)$ bắt buộc chơi đủ **2 ván đối xứng** ($A$ cầm Đỏ đi trước, sau đó $B$ cầm Đỏ đi trước) $\Rightarrow 200$ ván/cặp. Các nước trong khai cuộc không tính vào thời gian suy nghĩ.
- **Độ đo hiệu năng & Khoảng tin cậy**:
  + Điểm chuẩn hóa tổng bằng không: $\text{Score}_A = \frac{W_A + 0,5 \cdot D}{N} \in [0, 1]$.
  + **Khoảng tin cậy Wilson 95%** cho tỷ lệ thắng nhị phân $W_A / N$ (ổn định ngay cả khi tỷ lệ thắng sát `0%` hoặc `100%`).
  + **Khoảng tin cậy Bootstrap 95%** (`10.000` lần lấy mẫu lại có hoàn lại) cho $\text{Score}_A$ (xử lý chính xác biến ngẫu nhiên 3 giá trị $\{0; 0,5; 1\}$ có ván hòa).
  + **Độ trễ thực thi**: Đo độc lập từng nước đi bằng `time.perf_counter()` (không tính chi phí `clone()` của khung giải đấu), báo cáo trung bình cộng (`Mean_Time_ms`) và phân vị thứ 95 (`p95_Time_ms`).

---

## CHƯƠNG 4. THỰC NGHIỆM, KẾT QUẢ VÀ THẢO LUẬN

### 4.1. Môi trường Thực nghiệm
Toàn bộ quá trình sinh dữ liệu, huấn luyện mô hình, kiểm thử tự động và chạy giải đấu được thực hiện trên cùng một máy tính cá nhân để đảm bảo tính nhất quán về độ trễ:
- **Hệ điều hành**: Windows 11 (`10.0.26300-SP0`), kiến trúc x86_64, CPU 16 luồng xử lý logic (`os.cpu_count() = 16`).
- **Môi trường phần mềm**: Python `3.13`, PyTorch `2.14.1+cpu` (giới hạn `torch.set_num_threads(1)` trong từng tác tử để đo công bằng thời gian đơn luồng), NumPy, Pandas, Matplotlib, Pytest, FastAPI & Pygame-ce.

### 4.2. Kiểm thử Tính Đúng đắn Phần mềm (`results/test_results/`)
Bộ kiểm thử tự động gồm **57 bài kiểm thử đơn vị và tích hợp (`pytest`)** trải rộng trên 9 tệp kiểm thử đạt tỷ lệ **100% PASSED**:
1. **Kiểm định toán học Perft (`test_engine.py`)**: Số lượng nút lá từ bàn cờ rỗng khớp chính xác tuyệt đối với hằng số chuẩn của Connect Four ở mọi độ sâu kiểm tra: ply 1 = `7`, ply 2 = `49`, ply 3 = `238`, ply 4 = `1.120`, ply 5 = `4.263`.
2. **Kiểm thử đối chiếu chéo quy mô lớn (`test_crosscheck.py`)**: Chạy **10.000 ván ngẫu nhiên hoàn chỉnh** song song trên `Connect4` (bitboard 49-bit) và `ReferenceConnect4` (mảng 2D), đối chiếu `legal_actions()`, `is_terminal()`, `winner`, `to_array()` và `encode()` sau từng nước đi và sau chuỗi `undo()` ngược về bàn cờ rỗng — ghi nhận **0 sai lệch**.
3. **Bộ 33 thế cờ chiến thuật thủ công (`tests/data/positions.csv` & `test_positions.py`)**: Kiểm chứng `HeuristicAgent`, `AlphaBetaAgent` và `MCTSAgent` trên 33 thế cờ biên soạn có chủ đích (thắng ngang/dọc/chéo khe giữa, chặn thua khẩn cấp, tránh ô tự sát cột kề và xử lý đòn kép).
4. **Kiểm thử học sâu, PUCT & Pipeline dữ liệu (`test_nn_and_puct.py`, `test_train_pipeline.py`)**: Xác nhận mặt nạ cột đầy gán xác suất bằng `0` tuyệt đối, tính bất biến của Transposition Cache dưới nhiễu Dirichlet, không rò rỉ dữ liệu qua phép lật gương và khả năng giải thế cờ thắng/chặn trực tiếp của checkpoint `policy_net_best.pt`.

### 4.3. Kết quả Huấn luyện Mạng `Connect4PolicyValueNet` (Trả lời phần học có giám sát của RQ2)
Quá trình huấn luyện 10 epochs trên `75.036` mẫu Train hoàn tất trong `462,26 giây` trên CPU (`checkpoints/training_history.json`). Nhờ kết hợp `label_smoothing = 0,05`, `weight_decay = 1e-3` và lịch giảm tốc độ học Cosine, hàm mất mát kiểm định `Val Loss` hội tụ mượt mà từ `1,3859` (Epoch 1) xuống điểm cực tiểu **`1,1336` tại Epoch 6** (`Val Top-1 Acc = 72,09%`, `Val Top-2 Acc = 89,13%`) mà không xảy ra hiện tượng phân kỳ quá khớp.

![Đường cong huấn luyện mạng Policy-Value ResNet](../results/figures/nn_learning_curves.png)

Đánh giá độc lập checkpoint tốt nhất (Epoch 6) trên **tập `Test` gồm 6.293 thế cờ chưa từng xuất hiện** (từ 375 ván hoàn toàn tách biệt, 0% trùng lặp gốc và gương):
- **Độ chính xác dự đoán nước đi chuyên gia Top-1 (`Test Top-1 Accuracy`)**: **71,68%** (cao gấp **5,02 lần** mức đoán ngẫu nhiên `14,29%` trên 7 cột).
- **Độ chính xác Top-2 (`Test Top-2 Accuracy`)**: **89,07%** — tức trong gần 9/10 thế cờ bất kỳ, nước đi tối ưu của `Alpha-Beta (depth=4)` nằm trong 2 cột có xác suất cao nhất của mạng, tạo tiền đề lý tưởng làm phân phối tiên nghiệm $P(s,a)$ cho PUCT!
- **Sai số đầu giá trị (`Test Value MSE / MAE`)**: `MSE = 0,7884`, `MAE = 0,6360` trên miền $[-1, +1]$; **Policy Cross-Entropy**: `0,7535`.
- **Độ trễ suy luận đơn lẻ trên CPU**: Trung bình **`1,909 ms`**, phân vị `p95 = 2,475 ms`.

### 4.4. Kết quả Giải đấu Round-Robin Toàn diện 6 Tác tử — Chế độ B (3.000 Ván)
Bảng dưới đây trình bày kết quả toàn bộ **15 cặp đấu đối kháng** (200 ván/cặp, tổng cộng **3.000 ván**, trích xuất trực tiếp từ `results/tables/round_robin_default_summary.csv`) với cấu hình mặc định: `Alpha-Beta (depth = 5)`, `MCTS-UCT (1.000 sims)`, `Mixed-MCTS PUCT (200 sims, use_value_head = True)`, `Policy-Value NN (temperature = 0, 0 search)`.

| Cặp đấu (`Agent_A` vs `Agent_B`) | Số ván | `A` Thắng | Hòa | `B` Thắng | `A_Score` | Bootstrap 95% CI | `A_WinRate` (Wilson 95% CI) | `p95 A` (ms) | `p95 B` (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `random` vs `heuristic` | 200 | 1 | 0 | 199 | **0,0050** | `[0,0000; 0,0150]` | `0,5% [0,09%; 2,78%]` | 0,008 | 0,242 |
| `random` vs `alphabeta` | 200 | 0 | 0 | 200 | **0,0000** | `[0,0000; 0,0000]` | `0,0% [0,00%; 1,88%]` | 0,013 | 63,545 |
| `random` vs `mcts` | 200 | 0 | 0 | 200 | **0,0000** | `[0,0000; 0,0000]` | `0,0% [0,00%; 1,88%]` | 0,009 | 150,624 |
| `random` vs `nn` | 200 | 3 | 0 | 197 | **0,0150** | `[0,0000; 0,0350]` | `1,5% [0,51%; 4,32%]` | 0,013 | 3,571 |
| `random` vs `mixed_mcts` | 200 | 0 | 0 | 200 | **0,0000** | `[0,0000; 0,0000]` | `0,0% [0,00%; 1,88%]` | 0,015 | 754,913 |
| `heuristic` vs `alphabeta` | 200 | 25 | 17 | 158 | **0,1675** | `[0,1225; 0,2175]` | `12,5% [8,61%; 17,80%]` | 0,238 | 56,930 |
| `heuristic` vs `mcts` | 200 | 41 | 11 | 148 | **0,2325** | `[0,1775; 0,2901]` | `20,5% [15,49%; 26,63%]` | 0,265 | 151,596 |
| `heuristic` vs `nn` | 200 | 59 | 25 | 116 | **0,3575** | `[0,2950; 0,4200]` | `29,5% [23,61%; 36,16%]` | 0,241 | 3,502 |
| `heuristic` vs `mixed_mcts` | 200 | 26 | 17 | 157 | **0,1725** | `[0,1250; 0,2225]` | `13,0% [9,03%; 18,37%]` | 0,252 | 705,554 |
| `alphabeta` vs `mcts` | 200 | 135 | 4 | 61 | **0,6850** | `[0,6200; 0,7475]` | `67,5% [60,73%; 73,61%]` | 63,603 | 154,284 |
| `alphabeta` vs `nn` | 200 | 144 | 18 | 38 | **0,7650** | `[0,7100; 0,8175]` | `72,0% [65,41%; 77,76%]` | 62,754 | 3,988 |
| `alphabeta` vs `mixed_mcts` | 200 | 79 | 25 | 96 | **0,4575** | `[0,3925; 0,5225]` | `39,5% [32,98%; 46,41%]` | 60,570 | 699,058 |
| `mcts` vs `nn` | 200 | 116 | 4 | 80 | **0,5900** | `[0,5225; 0,6575]` | `58,0% [51,07%; 64,63%]` | 152,758 | 4,505 |
| `mcts` vs `mixed_mcts` | 200 | 71 | 8 | 121 | **0,3750** | `[0,3100; 0,4400]` | `35,5% [29,20%; 42,35%]` | 134,974 | 692,486 |
| `nn` vs `mixed_mcts` | 200 | 29 | 40 | 131 | **0,2450** | `[0,1950; 0,2950]` | `14,5% [10,29%; 20,05%]` | 3,754 | 693,428 |

![Ma trận điểm đối đầu và Bảng xếp hạng tổng thể 6 tác tử](../results/figures/round_robin_heatmap.png)

**Tổng hợp bảng xếp hạng trên 1.000 ván thi đấu của mỗi tác tử**:
1. **Hạng 1 — `Mixed-MCTS PUCT (200 sims)`**: `705 Thắng – 90 Hòa – 205 Thua` $\rightarrow$ **Overall Score = 75,00%**. Đáng chú ý, dù chỉ dùng **200 mô phỏng** (ít hơn 5 lần so với `MCTS-UCT 1.000 sims`), `Mixed-MCTS` đánh bại `MCTS-UCT` với tỷ số thuyết phục `121W – 8D – 71L` (**Score = 62,50%**, khoảng tin cậy 95% `[0,560; 0,690]` nằm hoàn toàn trên ngưỡng `0,50`) và thậm chí nhỉnh hơn cả `Alpha-Beta depth 5` (`96W – 25D – 79L`, **Score = 54,25%**) dù mạng bên trong nó chỉ học từ chuyên gia `depth 4`!
2. **Hạng 2 — `Alpha-Beta (depth 5)`**: `716 Thắng – 64 Hòa – 220 Thua` $\rightarrow$ **Overall Score = 74,80%**, với độ trễ cực kỳ gọn nhẹ (`Mean ~ 21,9 ms`, `p95 ~ 63 ms`).
3. **Hạng 3 — `MCTS-UCT (1.000 sims)`**: `596 Thắng – 27 Hòa – 377 Thua` $\rightarrow$ **Overall Score = 60,95%** (`p95 ~ 153 ms`).
4. **Hạng 4 — `Policy-Value NN (0 search)`**: `460 Thắng – 87 Hòa – 453 Thua` $\rightarrow$ **Overall Score = 50,35%**. Chỉ bằng một lượt truyền thẳng `~2,9 ms` không tìm kiếm cây, mạng học sâu thắng `Random` **98,50%**, đánh bại `Heuristic` có ý nghĩa thống kê với tỷ số `116W – 25D – 59L` (**Score = 64,25%**, CI `[0,580; 0,705]`), giành được **80 trận thắng (Score = 41,00%)** trước `MCTS-1000` và **38 trận thắng + 18 hòa (Score = 23,50%)** trước `Alpha-Beta depth 5`.
5. **Hạng 5 — `Heuristic`**: `350 Thắng – 70 Hòa – 580 Thua` $\rightarrow$ **Overall Score = 38,50%** (thắng `Random` `199/200` ván = **99,50%** trong `0,12 ms/nước`).
6. **Hạng 6 — `Random`**: `4 Thắng – 0 Hòa – 996 Thua` $\rightarrow$ **Overall Score = 0,40%**.

### 4.5. Kết quả Giải đấu Cùng Ngân sách Thời gian (Chế độ A — RQ1) và Các Nghiên cứu Phân rã (Ablation A1–A4)

#### 4.5.1. Giải đấu Giới hạn Thời gian Thực Chế độ A (`results/tables/round_robin_timed_summary.csv`)
Để trả lời trực diện **RQ1**, `Alpha-Beta` (chế độ Iterative Deepening) và `MCTS-UCT` thi đấu đơn luồng độc lập ở 3 ngưỡng thời gian thực **50 ms, 100 ms và 300 ms / nước** (`100` ván/mức = `300` ván):

| Ngân sách Thời gian | Số ván | `Alpha-Beta` Thắng | Hòa | `MCTS` Thắng | `Alpha-Beta Score` | Bootstrap 95% CI | `p95 Alpha-Beta` | `p95 MCTS` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **50 ms / nước** | 100 | 64 | 2 | 34 | **0,6500** | `[0,5550; 0,7400]` | `51,59 ms` | `50,89 ms` |
| **100 ms / nước** | 100 | 68 | 2 | 30 | **0,6900** | `[0,6000; 0,7750]` | `101,52 ms` | `100,93 ms` |
| **300 ms / nước** | 100 | 59 | 3 | 38 | **0,6050** | `[0,5100; 0,7000]` | `301,22 ms` | `300,85 ms` |

![Chế độ A: Alpha-Beta vs MCTS dưới cùng ngân sách thời gian](../results/figures/timed_crossover_rq1.png)

**Phân tích cơ chế**: Khác với cờ vây ($b \approx 250$) nơi Alpha-Beta gãy đổ do bùng nổ nhánh và thiếu hàm lượng giá tốt, Connect Four có hệ số nhánh rất hẹp ($b \le 7$) và cấu trúc hình học 69 cửa sổ 4 ô rõ ràng. Trong `50–100 ms`, Iterative Deepening trên bitboard dễ dàng đạt độ sâu 5–6 ply với độ chính xác chiến thuật tất định, nên thắng áp đảo `MCTS-UCT` (`0,650` và `0,690`). Khi nâng ngân sách lên `300 ms`, `MCTS-UCT` thực hiện được hàng chục nghìn mô phỏng mỗi nước nên thu hẹp đáng kể khoảng cách (tăng điểm từ `0,310` lên `0,395`), song `Alpha-Beta` vẫn giữ ưu thế có ý nghĩa thống kê (`CI [0,510; 0,700] > 0,50`).

#### 4.5.2. Ablation A1: Đóng góp của Cắt tỉa Alpha-Beta và Thứ tự Center-First (`ablation_a1_results.csv`)
Trên thế cờ trung tâm chuẩn sau 2 nước khai cuộc cột 4, bảng sau đối chiếu số nút duyệt và thời gian thực thi khi bật/tắt cắt tỉa và sắp xếp Center-First ở độ sâu `4, 5, 6`:

| Độ sâu | Cấu hình | Số nút duyệt | Thời gian (ms) | Nước chọn | Giá trị Minimax | Mức giảm nút (%) |
|:---:|:---|---:|---:|:---:|:---:|---:|
| **Depth 4** | `Pruning OFF, Ordering OFF` (Minimax thuần) | 399 | 56,74 | Cột 4 | `0` | `0,00%` |
| **Depth 4** | `Pruning ON, Ordering OFF` | 208 | 17,38 | Cột 4 | `0` | `47,87%` |
| **Depth 4** | `Pruning ON, Ordering ON` (Đầy đủ) | **78** | **3,82** | Cột 4 | `0` | **80,45%** |
| **Depth 5** | `Pruning OFF, Ordering OFF` | 2.800 | 459,06 | Cột 4 | `+8` | `0,00%` |
| **Depth 5** | `Pruning ON, Ordering OFF` | 852 | 69,63 | Cột 4 | `+8` | `69,57%` |
| **Depth 5** | `Pruning ON, Ordering ON` (Đầy đủ) | **339** | **24,95** | Cột 4 | `+8` | **87,89%** |
| **Depth 6** | `Pruning OFF, Ordering OFF` | 18.886 | 3.306,82 | Cột 4 | `-2` | `0,00%` |
| **Depth 6** | `Pruning ON, Ordering OFF` | 3.950 | 295,21 | Cột 4 | `-2` | `79,09%` |
| **Depth 6** | `Pruning ON, Ordering ON` (Đầy đủ) | **1.309** | **53,38** | Cột 4 | `-2` | **93,07%** |

![Ablation A1: Hiệu quả cắt tỉa Alpha-Beta và Center-First](../results/figures/ablation_a1_nodes.png)

**Nhận xét**: Cả 4 cấu hình ở cùng độ sâu luôn trả về **cùng một giá trị Minimax và cùng nước đi tối ưu**, chứng minh cắt tỉa $\alpha$-$\beta$ bảo toàn tính tối ưu toán học. Ở `Depth 6`, chỉ bật cắt tỉa giảm `79,09%` nút, nhưng khi kết hợp thêm sắp xếp **Center-First**, mức tiết kiệm vọt lên **93,07%** (`18.886` xuống `1.309` nút, tốc độ nhanh gấp **61,9 lần**: từ `3.306,8 ms` xuống `53,4 ms`), vì các cột trung tâm sớm thiết lập cận $\alpha$ cao làm gãy hàng loạt nhánh biên.

#### 4.5.3. Ablation A2: Quy mô Mô phỏng MCTS đối đầu Alpha-Beta Cố định Depth 4 (`ablation_a2_results.csv`)
Khi giữ đối thủ cố định là `Alpha-Beta (depth = 4)` (`100` ván mỗi mức):
- `100 sims`: `5W – 3D – 92L` $\rightarrow$ `Score = 0,065` (`CI [0,025; 0,115]`, `p95 = 4,62 ms`)
- `500 sims`: `29W – 3D – 68L` $\rightarrow$ `Score = 0,305` (`CI [0,220; 0,395]`, `p95 = 28,20 ms`)
- `1.000 sims`: `42W – 0D – 58L` $\rightarrow$ `Score = 0,420` (`CI [0,320; 0,520]`, `p95 = 71,40 ms`)
- **`2.000 sims`**: `51W – 6D – 43L` $\rightarrow$ **`Score = 0,540`** (`CI [0,445; 0,635]`, `p95 = 118,43 ms`) — **vượt mốc cân bằng 0,50!**
- **`5.000 sims`**: `57W – 3D – 40L` $\rightarrow$ **`Score = 0,585`** (`CI [0,490; 0,680]`, `p95 = 287,94 ms`)

![Ablation A2: Quy mô mô phỏng MCTS đối đầu Alpha-Beta Depth 4](../results/figures/ablation_a2_scaling.png)

Như vậy, đối với một chân trời tìm kiếm cố định `depth = 4`, điểm giao thoa (cross-over point) của `MCTS-UCT` nằm trong khoảng **1.500 – 2.000 mô phỏng/nước**.

#### 4.5.4. Ablation A3: Bóc tách Vai trò của Policy Prior và Value Head trong PUCT (`ablation_a3_results.csv` — Trả lời RQ2 & RQ3)
Để tách bạch đóng góp của từng thành phần học sâu, 4 biến thể (`NN_Policy_Only` không tìm kiếm, `MCTS_UCT_Rollout` 200 sims, `PUCT_Prior_Rollout` 200 sims và `PUCT_Prior_ValueHead` 200 sims) cùng thi đấu `100` ván trước hai mốc chuẩn `MCTS (500 sims)` và tác tử thầy `Alpha-Beta (depth 4)`:

| Biến thể Tác tử | Ngân sách | Đối thủ | W / D / L | `Score` | Bootstrap 95% CI | `Mean Time` (ms) |
|:---|:---:|:---|:---:|:---:|:---:|---:|
| `NN_Policy_Only` | `0 sims` | `mcts_500` | `43 / 2 / 55` | **0,4400** | `[0,3450; 0,5350]` | 2,99 |
| `MCTS_UCT_Rollout` | `200 sims` | `mcts_500` | `32 / 1 / 67` | **0,3250** | `[0,2350; 0,4200]` | 12,92 |
| `PUCT_Prior_Rollout` | `200 sims` | `mcts_500` | `68 / 3 / 29` | **0,6950** | `[0,6050; 0,7800]` | 151,09 |
| `PUCT_Prior_ValueHead` | `200 sims` | `mcts_500` | `67 / 3 / 30` | **0,6850** | `[0,5950; 0,7700]` | 447,53 |
| `NN_Policy_Only` | `0 sims` | `alphabeta_d4` | `33 / 13 / 54` | **0,3950** | `[0,3050; 0,4850]` | 2,85 |
| `MCTS_UCT_Rollout` | `200 sims` | `alphabeta_d4` | `13 / 3 / 84` | **0,1450** | `[0,0800; 0,2150]` | 13,30 |
| `PUCT_Prior_Rollout` | `200 sims` | `alphabeta_d4` | `56 / 13 / 31` | **0,6250** | `[0,5350; 0,7100]` | 151,23 |
| `PUCT_Prior_ValueHead` | `200 sims` | `alphabeta_d4` | `45 / 12 / 43` | **0,5100** | `[0,4150; 0,6050]` | 425,47 |

![Ablation A3: Đóng góp của Policy Prior và Value Head trong PUCT](../results/figures/ablation_a3_puct_value.png)

**Hai phát hiện khoa học nổi bật từ Ablation A3**:
1. **Sức mạnh đột phá của Policy Prior**: Ở cùng mức `200` mô phỏng, `MCTS-UCT` thuần thua nặng cả `MCTS-500` (`0,325`) lẫn `Alpha-Beta d=4` (`0,145`) vì lãng phí ngân sách ít ỏi vào các cột biên kém chất lượng. Chỉ cần đưa phân phối tiên nghiệm $P_\theta(s,a)$ vào công thức PUCT, điểm số nhảy vọt **+37,0%** trước `MCTS-500` (`0,325 → 0,695`) và **+48,0%** trước `Alpha-Beta d=4` (`0,145 → 0,625`), giúp trò vượt qua chính thầy dạy mình có ý nghĩa thống kê (`CI [0,535; 0,710] > 0,50`)!
2. **So sánh Rollout và Supervised Value Head (Liên hệ trực tiếp với AlphaGo 2016)**: Biến thể `PUCT_Prior_Rollout` nhanh hơn **2,8 lần** (`151 ms` so với `425 ms`) vì chỉ gọi mạng CNN khi mở rộng nút trong để lấy prior $P(s,a)$, còn tại nút lá tận dụng rollout bitboard siêu tốc thay vì tốn thêm một lượt truyền thẳng CNN. Hơn nữa, trước đối thủ chiến thuật sắc bén `Alpha-Beta d=4`, `PUCT_Prior_Rollout` đạt điểm cao hơn `PUCT_Prior_ValueHead` (`0,625` so với `0,510`). Nguyên nhân là đầu Value Head huấn luyện thuần túy có giám sát trên kết cục ván đấu (`Test Value MSE = 0,788`) đôi khi có sai số ước lượng ở các thế cờ chiến thuật hẹp, trong khi rollout ngẫu nhiên kiểm chứng trực tiếp điều kiện thắng/thua cuối ván — hoàn toàn tương đồng với phát hiện kinh điển của **AlphaGo (Silver et al., 2016)** khi kết hợp SL Policy Prior cùng Fast Rollout!

#### 4.5.5. Ablation A4: Phân tích Lợi thế Người đi trước trên 3.000 Ván (`ablation_a4_first_player_bias.csv`)
Tổng hợp toàn bộ `3.000` ván của 15 cặp đấu Round-Robin:
- **Quân Đỏ (Đi trước — P1) thắng**: `1.554 / 3.000` ván (**51,80%**, khoảng tin cậy Wilson 95% `[50,01%; 53,58%]`).
- **Quân Vàng (Đi sau — P2) thắng**: `1.277 / 3.000` ván (**42,57%**).
- **Hòa**: `169 / 3.000` ván (**5,63%**).
- **Độ chênh lệch tỷ lệ thắng ròng ($\Delta W = W_{\text{Đỏ}} - W_{\text{Vàng}}$)**: **+9,23%** nghiêng về người đi trước! Đặc biệt ở các cặp đấu giữa hai tác tử tìm kiếm mạnh ngang sức, ưu thế đi trước càng bộc lộ rõ rệt: trong `mcts` vs `mixed_mcts`, bên đi trước thắng tới **65,50%** so với **30,50%** của bên đi sau ($\Delta W = +35,0\%$); trong `alphabeta` vs `mixed_mcts`, bên đi trước thắng **55,00%** so với **32,50%** ($\Delta W = +22,5\%$). Kết quả này phù hợp hoàn toàn với định lý lý thuyết trò chơi của Allis (1988) và chứng minh thực nghiệm rằng bất kỳ giải đấu Connect Four nào không đổi bên đối xứng đều sẽ bị sai lệch nghiêm trọng.

![Ablation A4: Lợi thế người đi trước trên toàn bộ các cặp đấu](../results/figures/first_player_advantage.png)

### 4.6. Phân tích Chiến thuật Tiêu biểu và Giải thích Mạng Nơ-ron (Explainable AI)
Hình dưới đây trình bày bản đồ độ nhạy đạo hàm bậc nhất $|\partial z_{a^*} / \partial X|$ (`results/figures/xai_saliency_double_threat.png`) trên hai tình huống chiến thuật kinh điển phân hóa rõ năng lực của các cấp tác tử:

![Explainable AI: Bản đồ độ nhạy Saliency trên hai tình huống chiến thuật](../results/figures/xai_saliency_double_threat.png)

1. **Tình huống 1 — Phòng thủ sớm trước Đòn kép hàng đáy (`moves = [3, 0, 4]`, lượt O — Vàng)**:
   - Quân Đỏ (`X`) đã chiếm hai ô trung tâm liên tiếp tại `(Hàng 1, Cột 4)` và `(Hàng 1, Cột 5)` với hai đầu mở thông thoáng ở Cột 3 và Cột 6.
   - **Sai lầm điển hình của `HeuristicAgent` (Cấp 2)**: Do trên bàn chưa có chuỗi 3 quân nào của `X`, tầng luật chặn thua của `HeuristicAgent` không kích hoạt và tác tử ngây thơ thả quân vào Cột 4 (`Hàng 2`). Ngay lượt kế, `X` đánh vào Cột 3 tạo chuỗi 3 quân mở hai đầu `(Cột 3, 4, 5)` mà `O` không thể chặn đồng thời cả Cột 2 lẫn Cột 6 — dẫn tới thua tất yếu!
   - **Quyết định & Giải thích của `Connect4PolicyValueNet` (Cấp 5) và `Alpha-Beta` (Cấp 3)**: Mạng dự đoán chính xác nước chặn sớm tại **Cột 3** với xác suất cao nhất **54,2%** (cùng phương án đối xứng Cột 6 đạt **14,9%**) và lượng giá thế cờ hơi bất lợi nhẹ cho bên đi sau (`Value = -0,188`). Bản đồ Saliency đạt cực đại chuẩn hóa **`1,00` ngay tại ô trống `(Hàng 1, Cột 3)`**, tiếp theo là `(Hàng 1, Cột 2)` (`0,62`) và quân `X` tại `(Hàng 1, Cột 4)` (`0,43`) — chứng minh mạng CNN đã thực sự học được cấu trúc hình học của đòn kép mở hai đầu chứ không chỉ học vẹt.
2. **Tình huống 2 — Đòn kết liễu Đường chéo Khe giữa (`moves = [0, 1, 1, 2, 3, 2, 3, 3, 3, 6]`, lượt X — Đỏ)**:
   - `X` đang sở hữu 3 quân nằm rải trên đường chéo chính tại `(Hàng 1, Cột 1)`, `(Hàng 2, Cột 2)` và `(Hàng 4, Cột 4)`, khuyết đúng mắt xích khe giữa tại `(Hàng 3, Cột 3)` (hiện đã có 2 quân lót sẵn ở Cột 3 nên thả Cột 3 sẽ rơi đúng vào Hàng 3).
   - Mạng nơ-ron dồn gần như tuyệt đối xác suất **98,9% vào Cột 3** (`Value = +0,601`), đồng thời bản đồ nhiệt chiếu sáng dọc theo đường chéo chiến thắng và khu vực đỉnh Cột 3–4 (`1,00` tại `(Hàng 5, Cột 4)`, `0,85` tại `(Hàng 3, Cột 2)` và `(Hàng 5, Cột 3)`).

---

## CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Tổng kết Câu trả lời cho Ba Câu hỏi Nghiên cứu
1. **Trả lời RQ1**: Trong miền Connect Four 7×6 có hệ số nhánh nhỏ ($b \le 7$), dưới cùng ngân sách thời gian suy nghĩ tương tác (`50 ms`, `100 ms`, `300 ms/nước`), `Alpha-Beta` tích hợp Iterative Deepening, cắt tỉa Center-First (giảm tới `93,07%` nút) và hàm lượng giá 69 cửa sổ luôn duy trì ưu thế có ý nghĩa thống kê trước `MCTS-UCT` thuần (`Score = 0,650; 0,690; 0,605`), dù khoảng cách thu hẹp dần khi ngân sách tăng lên `300 ms`. Khi cố định chân trời của `Alpha-Beta` ở `depth = 4` (Ablation A2), điểm giao thoa (cross-over point) để `MCTS-UCT` vượt lên nằm tại ngưỡng **1.500 – 2.000 mô phỏng/nước** (`Score = 0,540` ở 2.000 mô phỏng).
2. **Trả lời RQ2**: Mạng `Connect4PolicyValueNet` học có giám sát từ nhãn sạch của `Alpha-Beta (depth = 4)` trên tập dữ liệu tách theo ván chống rò rỉ đạt **71,68% Top-1 Accuracy** và **89,07% Top-2 Accuracy** trên tập `Test` độc lập. Khi thi đấu trực tiếp không cần tìm kiếm cây (`0 search`, độ trễ `~2,8 ms/nước`), mạng thắng áp đảo `HeuristicAgent` (**64,25%**), đạt **41,00%** điểm trước `MCTS-1000` và đạt **39,50%** điểm trước chính tác tử thầy `Alpha-Beta (depth = 4)` (Ablation A3).
3. **Trả lời RQ3**: Khi ghép mạng `Connect4PolicyValueNet` vào công thức tìm kiếm cây PUCT (`MixedMCTSAgent`), chỉ với **200 mô phỏng**, tác tử lai tăng vọt **+36% đến +37% điểm số** so với `MCTS-UCT` cùng ngân sách khi gặp `MCTS-500`, vượt qua cả tác tử thầy `Alpha-Beta depth 4` (`Score = 0,625` với `PUCT+Rollout`) và vươn lên dẫn đầu toàn giải đấu Round-Robin 3.000 ván (**Overall Score = 75,00%**, thắng `MCTS-1000` **62,50%** và vượt `Alpha-Beta depth 5` **54,25%**). Bên cạnh đó, bản đồ độ nhạy đạo hàm Saliency Map cung cấp lời giải thích trực quan, minh bạch cho từng quyết định chiến thuật của mạng nơ-ron.

### 5.2. Đóng góp Thực tiễn của Đề tài
- Xây dựng mã nguồn chuẩn kỹ thuật phần mềm (100% pass trên `57` bài test tự động, kiểm định chéo 10.000 ván và Perft), kèm bộ giao diện đa nền tảng (CLI, Pygame Desktop, FastAPI Web App + Docker).
- Thiết lập quy trình chuẩn mực về chống rò rỉ dữ liệu đối xứng gương trong học máy cho trò chơi bàn cờ và khung giải đấu thống kê có khả năng tái lập 100% từ cấu hình YAML.

### 5.3. Hạn chế và Hướng Phát triển
- **Hạn chế**: Đầu ra Value Head hiện được huấn luyện có giám sát trên kết cục ván đấu của `Alpha-Beta (depth = 4)` trên CPU nên độ chính xác ước lượng thế cờ phức tạp chưa đạt mức tự chơi tăng cường quy mô lớn; mặt khác `AlphaBetaAgent` chưa tích hợp bảng băm hoán vị (Transposition Table Zobrist/Bitboard key) và sắp xếp nước đi động (Killer Moves / History Heuristic).
- **Hướng phát triển**: (1) Bổ sung Transposition Table cho `AlphaBetaAgent` để đạt độ sâu 9–11 ply trong `100 ms`; (2) Triển khai vòng lặp **AlphaZero Self-Play Reinforcement Learning** sinh dữ liệu từ chính phân phối thăm $\pi_{\text{PUCT}}$ qua nhiều thế hệ; (3) Mở rộng kiến trúc ResNet + PUCT sang các trò chơi có hệ số nhánh lớn hơn như **Gomoku / Caro (15×15)** hoặc **Othello (8×8)** — nơi ưu thế của PUCT so với Alpha-Beta sẽ còn bộc lộ mạnh mẽ hơn nữa.

---

## TÀI LIỆU THAM KHẢO

1. V. L. Allis, *A Knowledge-Based Approach of Connect-Four — The Game is Solved: White Wins*, Master's thesis, Vrije Universiteit Amsterdam, 1988.
2. L. Kocsis and C. Szepesvári, "Bandit Based Monte-Carlo Planning," in *Proc. 17th European Conference on Machine Learning (ECML)*, Berlin, Heidelberg: Springer, 2006, pp. 282–293.
3. D. Silver et al., "Mastering the game of Go with deep neural networks and tree search," *Nature*, vol. 529, no. 7587, pp. 484–489, 2016.
4. D. Silver et al., "Mastering the game of Go without human knowledge," *Nature*, vol. 550, no. 7676, pp. 354–359, 2017.
5. S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. Hoboken, NJ: Pearson, 2021.
6. R. S. Sutton and A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed. Cambridge, MA: MIT Press, 2018.
7. M. Liu, *AlphaGo Simplified: Rule-Based AI and Deep Learning in Everyday Games*, Boca Raton, FL: CRC Press, 2025.
8. K. Simonyan, A. Vedaldi, and A. Zisserman, "Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps," in *ICLR Workshop*, 2014.
9. S. Edelkamp and P. Kissmann, "Symbolic Classification of General Two-Player Games," in *KI 2008: Advances in Artificial Intelligence*, Springer, 2008, pp. 185–192.
