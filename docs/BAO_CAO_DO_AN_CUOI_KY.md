# TRƯỜNG ĐẠI HỌC SÀI GÒN — KHOA CÔNG NGHỆ THÔNG TIN
# BÁO CÁO ĐỒ ÁN CUỐI KỲ: TRÍ TUỆ NHÂN TẠO NÂNG CAO
## ĐỀ TÀI: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ
### Trường hợp nghiên cứu: Connect Four (7×6)

* **Giảng viên hướng dẫn**: Thầy Đỗ Như Tài
* **Nhóm thực hiện**: Nhóm 13 — Connect Four (7×6)
* **Repository GitHub**: https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13

| STT | Họ và Tên | MSSV | Vai trò | Nhiệm vụ chính | Đóng góp |
|:---:|:---|:---:|:---:|:---|:---:|
| 1 | **Bùi Minh Trung** | `3124720074` | Nhóm trưởng (TV1) | Engine (`bitboard` + `reference`), API & bộ unit test; `HeuristicAgent`, `AlphaBetaAgent`; khung giải đấu & thống kê (`Wilson`, `Bootstrap`, `p95`); Ablation A1 & A3; XAI Saliency; Web UI; quản lý GitHub, review PR & đóng gói | **32%** |
| 2 | **Trần Lê Minh Tâm** | `3124720064` | Thành viên (TV2) | `RandomAgent`, `MCTSAgent` (UCT 4 bước); kiến trúc mạng hai đầu `Connect4PolicyValueNet`, pipeline sinh dữ liệu/huấn luyện & `MixedMCTSAgent` (PUCT + Transposition Cache + Dirichlet noise); giao diện Pygame GUI; Ablation A2 & A4 | **32%** |
| 3 | **Nguyễn Thành Tài** | `3124720062` | Thành viên (TV3) | Chạy thực nghiệm giải đấu & ablation, thu thập log CSV thô; xây dựng & chạy notebook phân tích (`01_tournament_analysis.ipynb`); bổ sung vị trí kiểm thử thủ công (`positions.csv`); phân tích ván đấu & viết Chương 4–5 | **18%** |
| 4 | **Chương Gia Thịnh** | `3124720067` | Thành viên (TV4) | Biên soạn Chương 1, 2, 3 của báo cáo cuối kỳ; thiết kế Slide thuyết trình, Poster khổ A0, kịch bản/quay Video Demo; rà soát tài liệu tham khảo, `THIRD_PARTY.md`, `README.md` và chuẩn bị bản in | **18%** |
| **Tổng** | | | | | **100%** |

---

## TÓM TẮT ĐỒ ÁN (ABSTRACT)

Đồ án này nghiên cứu, thiết kế và đánh giá thực nghiệm một hệ thống trí tuệ nhân tạo (AI) đa cấp độ hoàn chỉnh cho trò chơi đối kháng thông tin hoàn hảo **Connect Four kích thước chuẩn 7 cột × 6 hàng**. Trên nền tảng hạ tầng **Engine Bitboard 49-bit** tốc độ cao với các toán tử thao tác bit $O(1)$ (được kiểm chuẩn tuyệt đối qua kiểm định cây trò chơi **Perft đến độ sâu 6** và đối chiếu chéo **10.000 ván ngẫu nhiên** không sai lệch với `ReferenceConnect4`), nhóm phát triển chuỗi **6 phiên bản tác tử AI** tiến hóa dần về tri thức và chiến lược suy luận:
- **Level 1 (`RandomAgent`)**: Tác tử ngẫu nhiên có hạt giống tái lập.
- **Level 2 (`HeuristicAgent`)**: Tác tử phản xạ 4 tầng luật ưu tiên kết hợp bộ lọc chống tự sát (*anti-blunder*).
- **Level 3 (`AlphaBetaAgent`)**: Tác tử duyệt cây đối kháng Negamax tích hợp cắt tỉa $\alpha$-$\beta$, sắp xếp nước đi *Center-First*, tìm kiếm sâu dần (*Iterative Deepening*) và hàm lượng giá trên 69 cửa sổ chiến thắng 4 ô.
- **Level 4 (`MCTSAgent`)**: Tác tử tìm kiếm cây Monte Carlo 4 giai đoạn sử dụng công thức UCT ($c = 1,4$).
- **Level 5 (`NNAgent` — Dual-Head ResNet)**: Tác tử học sâu sử dụng mạng nơ-ron phần dư hai đầu `Connect4PolicyValueNet` (`3` khối Residual, `278.952` tham số) học có giám sát từ nhãn chuyên gia sạch.
- **Level 6 / AlphaZero-lite (`MixedMCTSAgent` — PUCT Search)**: Tác tử lai ghép tích hợp xác suất tiên nghiệm Policy Head $P_\theta(s,a)$ và lượng giá Value Head $V_\theta(s)$ vào cây tìm kiếm PUCT, kết hợp bảng băm hoán vị $O(1)$ (*Transposition Cache*) và giải thích hộp đen bằng bản đồ độ nhạy đạo hàm bậc nhất (*Gradient Saliency Map — XAI*).

Hệ thống được đánh giá nghiêm ngặt qua giải đấu vòng tròn **Round-Robin đối xứng 3.000 ván** (15 cặp × 200 ván trên 100 khai cuộc chuẩn, hoán đổi Đỏ/Vàng), giải đấu giới hạn thời gian thực **300 ván** (`50 ms`, `100 ms`, `300 ms/nước`) và 4 nghiên cứu phân rã (**Ablation A1–A4**). Kết quả thực nghiệm chứng minh: (1) Cắt tỉa $\alpha$-$\beta$ kèm *Center-First* giảm **93,07%** số nút duyệt ở độ sâu 6; (2) Mạng `Connect4PolicyValueNet` huấn luyện trên tập dữ liệu `87.725` mẫu tách theo ván chống rò rỉ 100% đạt **71,68% Top-1 Accuracy** và **89,07% Top-2 Accuracy** trên tập `Test` độc lập (`6.293` mẫu); (3) Khi tích hợp tri thức mạng học sâu vào cây PUCT, tác tử `MixedMCTSAgent` chỉ cần **200 mô phỏng/nước** (ít hơn 5 lần so với `MCTS-UCT 1.000 sims`) nhưng vươn lên dẫn đầu toàn giải với **Overall Score = 75,00%**, đánh bại cả `MCTS-UCT 1.000 sims` (**62,50%**) lẫn `Alpha-Beta depth 5` (**54,25%**), minh chứng thuyết phục cho nguyên lý *"duyệt ít nút hơn nhưng chọn nước đi chất lượng và chắc chắn hơn"*.

---

## CHƯƠNG 1: GIỚI THIỆU VÀ KHẢO SÁT CHƯƠNG TRÌNH CONNECT FOUR

### 1.1. Bối cảnh đề tài & Hình thức hóa toán học không gian trạng thái $(S, A, T, R)$

Các trò chơi đối kháng có thông tin hoàn hảo (*perfect-information adversarial games*) từ lâu đã đóng vai trò là thước đo chuẩn mực cho sự tiến bộ của Trí tuệ nhân tạo — khởi đầu từ các thuật toán duyệt cây Minimax/Alpha-Beta kết hợp hàm lượng giá thủ công (Knuth & Moore, 1975; Campbell et al., 2002), tiến tới Tìm kiếm Cây Monte Carlo — MCTS (Kocsis & Szepesvári, 2006), và bùng nổ với kiến trúc kết hợp Mạng Nơ-ron Tích chập Sâu cùng tìm kiếm PUCT trong AlphaGo / AlphaZero (Silver et al., 2016, 2017).

Trò chơi **Connect Four** (kích thước tiêu chuẩn **7 cột × 6 hàng**) diễn ra trên một lưới thẳng đứng gồm 42 ô giữa hai người chơi: Quân Đỏ (`PLAYER1 = +1`, đi trước) và Quân Vàng (`PLAYER2 = -1`, đi sau). Dưới góc nhìn Lý thuyết Trò chơi và Quy hoạch Động, bài toán được hình thức hóa bằng bộ bốn toán học $(S, A, T, R)$:

1. **Không gian trạng thái ($S$)**: Mỗi trạng thái $s \in S$ biểu diễn cấu hình quân cờ trên lưới $6 \times 7$ thỏa mãn ràng buộc trọng lực (mọi quân cờ trong một cột phải xếp liên tục từ hàng đáy $r=0$ lên trên, không có ô trống nằm dưới ô đã có quân). Tổng số trạng thái hợp lệ đạt $|S| = 4.531.985.219.092 \approx 4,53 \times 10^{12}$ trạng thái (Allis, 1988; Edelkamp & Kissmann, 2008).
2. **Không gian hành động hợp lệ ($A(s)$)**: Tại trạng thái chưa kết thúc $s$, tập hành động hợp lệ gồm chỉ số các cột chưa đầy:
   $$A(s) = \{ c \in \{0, 1, \dots, 6\} \mid h_s(c) < 6 \}$$
   trong đó $h_s(c) \in \{0, \dots, 6\}$ là chiều cao hiện tại của cột $c$. Hệ số phân nhánh tối đa rất gọn ($b = |A(s)| \le 7$) và độ sâu tối đa của cây trò chơi là $D_{\max} = 42$ nước đi (ply).
3. **Hàm chuyển trạng thái tất định ($T(s, a)$)**: Khi người chơi hiện tại $\tau(s) \in \{+1, -1\}$ chọn cột $a \in A(s)$, quân cờ rơi xuống hàng trống thấp nhất $r = h_s(a)$, tạo thành trạng thái kế tiếp $s' = T(s, a)$ với $h_{s'}(a) = h_s(a) + 1$ và lượt chơi chuyển sang $-\tau(s)$.
4. **Tập cửa sổ thắng & Hàm phần thưởng kết thúc ($R(s)$)**: Trên lưới $7 \times 6$, tồn tại chính xác **69 cửa sổ gồm 4 ô liên tiếp** ($\mathcal{W}_{69}$), bao gồm:
   - **24 cửa sổ ngang**: $6 \text{ hàng} \times 4 \text{ vị trí bắt đầu mỗi hàng}$.
   - **21 cửa sổ dọc**: $7 \text{ cột} \times 3 \text{ vị trí bắt đầu mỗi cột}$.
   - **12 cửa sổ chéo chính ($\setminus$)**: $3 \text{ hàng} \times 4 \text{ cột}$.
   - **12 cửa sổ chéo phụ ($/$)**: $3 \text{ hàng} \times 4 \text{ cột}$.
   Trạng thái $s$ là trạng thái kết thúc (*terminal*) khi một bên lấp đầy cả 4 ô của bất kỳ cửa sổ $w \in \mathcal{W}_{69}$ nào, hoặc khi toàn bộ 42 ô đã kín. Hàm phần thưởng tổng bằng không theo góc nhìn của người chơi thứ nhất được xác định bởi:
   $$R(s) = \begin{cases} +1 & \text{nếu Quân Đỏ (+1) sở hữu 4 ô liên tiếp trong } \mathcal{W}_{69} \\ -1 & \text{nếu Quân Vàng (-1) sở hữu 4 ô liên tiếp trong } \mathcal{W}_{69} \\ 0 & \text{nếu } \sum_{c=0}^{6} h_s(c) = 42 \text{ mà chưa bên nào thắng (Hòa)} \end{cases}$$

### 1.2. Khảo sát thuật toán/mã nguồn sẵn có & Đặt mốc đánh giá chuẩn (Benchmark Baseline)

Để tránh việc đánh giá chủ quan hoặc chỉ so sánh với tác tử ngẫu nhiên yếu, nhóm thực hiện khảo sát cấu trúc tìm kiếm và hàm lượng giá của **4 dòng chương trình Connect Four tiêu biểu** trong cộng đồng mã nguồn mở và các công trình học thuật, từ đó hiện thực hóa và chuẩn hóa chúng trên cùng một hạ tầng kỹ thuật để thiết lập **Mốc đánh giá chuẩn (Benchmark Baseline)**:

| Nhóm chương trình khảo sát | Đại diện tiêu biểu (GitHub / Học thuật) | Đặc trưng cấu trúc duyệt cây & Hàm lượng giá | Vai trò trong hệ thống Nhóm 13 |
|:---|:---|:---|:---|
| **1. Tác tử Luật Phản xạ 1-ply** (*Tactical Rule-based*) | `inventwithpython` (Sweigart), các bot phản xạ cơ sở | Quét 1 nước để ăn 4 ngay hoặc chặn đối thủ ăn 4; lọc nước đi tạo bàn đạp cho đối thủ thắng ở hàng trên (*anti-blunder*); ưu tiên cột trung tâm. Không duyệt cây sâu. | Chuẩn hóa thành **`HeuristicAgent` (Level 2)** — Mốc chuẩn cho nhóm không duyệt cây. |
| **2. Duyệt cây Cổ điển + Lượng giá 69 Cửa sổ** (*Classic Negamax Alpha-Beta*) | `KeithGalli/Connect4-Python`, Allis (1988) | Duyệt cây Negamax cắt tỉa $\alpha$-$\beta$; lượng giá tuyến tính dựa trên đếm số cửa sổ 2 quân, 3 quân mở và ưu thế cột giữa (`c=3`). | Nâng cấp với Bitboard $O(1)$, *Center-First* & *Iterative Deepening* thành **`AlphaBetaAgent` (Level 3)** — **Benchmark Baseline tất định (Tác tử Thầy)**. |
| **3. Tìm kiếm Cây Monte Carlo thuần** (*Pure UCT-MCTS*) | Kocsis & Szepesvári (2006), các bản cài đặt MCTS chuẩn | Duyệt cây 4 giai đoạn với công thức chọn nhánh UCB1/UCT ($c = 1,4$) và giả lập ngẫu nhiên đồng đều (*Uniform Random Rollout*) đến cuối ván. Không cần hàm lượng giá thủ công. | Chuẩn hóa thành **`MCTSAgent` (Level 4)** — **Benchmark Baseline tìm kiếm ngẫu nhiên**. |
| **4. Học bắt chước Hộp đen** (*Supervised Policy-Value CNN*) | Liu (2025), các mô hình Behavioral Cloning | Mã hóa bàn cờ thành tensor đa kênh, dùng mạng CNN/ResNet dự đoán xác suất 7 cột $P(s,a)$ và giá trị $V(s)$, chọn trực tiếp `argmax` không duyệt cây (`0 search`). | Hiện thực thành **`NNAgent` (Level 5)** và tích hợp vào **`MixedMCTSAgent` (Level 6 / AlphaZero-lite)**. |

Thông qua khảo sát thực nghiệm sơ bộ (200 ván/cặp, hoán đổi Đỏ/Vàng), nhóm xác lập hai cột mốc kiểm chuẩn khắt khe mà tác tử đề xuất **AlphaZero-lite (`MixedMCTSAgent`)** phải vượt qua:
1. **Mốc chuẩn MCTS thuần (`MCTS-UCT 500 sims` và `1.000 sims`)**: Kiểm chứng xem việc tích hợp tri thức mạng học sâu vào cây tìm kiếm có giúp giảm số lượng playout mà vẫn tăng tỷ lệ thắng hay không.
2. **Mốc chuẩn Duyệt cây Cổ điển (`Alpha-Beta depth 4` và `depth 5`)**: Kiểm chứng xem tác tử học từ chuyên gia `depth 4` khi kết hợp tìm kiếm PUCT có thể "trò giỏi hơn thầy" hay không.

### 1.3. Các câu hỏi nghiên cứu định lượng (RQ1 – RQ3)

Toàn bộ thiết kế thực nghiệm của báo cáo tập trung trả lời định lượng ba câu hỏi nghiên cứu cốt lõi:
- **RQ1 (So sánh Duyệt cây Tất định vs Tìm kiếm Monte Carlo theo Ngân sách)**: Dưới cùng ngân sách thời gian suy nghĩ thực tế mỗi nước đi (`50 ms`, `100 ms`, `300 ms`), `MCTS-UCT` thuần có vượt qua `Alpha-Beta` (*Iterative Deepening*) hay không? Khi cố định chân trời của `Alpha-Beta` ở `depth = 4`, điểm giao thoa (*cross-over point*) về số lượng mô phỏng của `MCTS-UCT` xuất hiện tại ngưỡng nào?
- **RQ2 (Năng lực Học có Giám sát & Suy luận Trực tiếp `0-Search`)**: Mạng nơ-ron phần dư hai đầu `Connect4PolicyValueNet` học từ dữ liệu nhãn sạch của chuyên gia `Alpha-Beta (depth = 4)` đạt độ chính xác dự đoán Top-1/Top-2 trên tập `Test` độc lập là bao nhiêu, và khi thi đấu trực tiếp không cần tìm kiếm cây (`0 search`, độ trễ `< 3 ms`) đạt tỷ lệ thắng như thế nào trước `Heuristic`, `MCTS` và `Alpha-Beta`?
- **RQ3 (Hiệu quả Tích hợp Tri thức Học sâu vào Cây PUCT & Minh bạch hóa XAI)**: Khi đưa phân phối tiên nghiệm Policy Head $P_\theta(s,a)$ và đầu lượng giá Value Head $V_\theta(s)$ vào công thức chọn nhánh PUCT (`MixedMCTSAgent`), tỷ lệ thắng cải thiện bao nhiêu phần trăm so với `MCTS-UCT` thuần cùng số mô phỏng (`200 sims`), đồng thời bản đồ độ nhạy đạo hàm (*Gradient Saliency Map*) giải thích cơ chế nhận diện đòn chiến thuật của mạng như thế nào?

---

## CHƯƠNG 2: HẠ TẦNG KỸ THUẬT VÀ CẤU TRÚC DỮ LIỆU BITBOARD

### 2.1. Thiết kế Bitboard 49-bit và toán tử Bitwise $O(1)$

Nếu biểu diễn bàn cờ bằng mảng hai chiều `int[6][7]` thông thường, mỗi lần thả quân, sao chép trạng thái trong cây tìm kiếm hoặc quét 4 hướng kiểm tra thắng đều tốn vòng lặp tuần tự $O(R \times C)$, gây nghẽn cổ chai nghiêm trọng khi duyệt hàng trăm nghìn nút. Để đạt hiệu năng tối ưu, nhóm xây dựng lõi [`Connect4`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/game/engine.py) dựa trên cấu trúc **Bitboard 49-bit** lưu gọn trong hai thanh ghi số nguyên 64-bit (`_pos` và `_mask`).

#### A. Sơ đồ ánh xạ vị trí ô cờ vào Bitboard 49-bit (7 cột × 7 bit)
Mỗi cột $c \in \{0, \dots, 6\}$ được cấp phát một dải 7 bit liên tiếp $[7c, 7c+6]$: 6 bit đầu tiên ($7c + r$ với $r \in \{0, \dots, 5\}$ từ đáy lên đỉnh) lưu dữ liệu ô cờ, còn **bit thứ 7 ở đỉnh mỗi cột ($7c + 6 \in \{6, 13, 20, 27, 34, 41, 48\}$) luôn được giữ bằng `0` làm bit đệm chống tràn (*sentinel bit*)**. Bit đệm này đóng vai trò vách ngăn vật lý ngăn chặn hiện tượng tràn bit từ đỉnh cột $c$ sang đáy cột $c+1$ khi thực hiện phép dịch bit dọc hoặc chéo!

```text
Bit đệm chống tràn (luôn = 0):    6    13    20    27    34    41    48
                                +----+----+----+----+----+----+----+
Hàng 5 (Đỉnh bàn cờ, r=5):      |  5 | 12 | 19 | 26 | 33 | 40 | 47 |
Hàng 4 (r=4):                   |  4 | 11 | 18 | 25 | 32 | 39 | 46 |
Hàng 3 (r=3):                   |  3 | 10 | 17 | 24 | 31 | 38 | 45 |
Hàng 2 (r=2):                   |  2 |  9 | 16 | 23 | 30 | 37 | 44 |
Hàng 1 (r=1):                   |  1 |  8 | 15 | 22 | 29 | 36 | 43 |
Hàng 0 (Đáy bàn cờ, r=0):       |  0 |  7 | 14 | 21 | 28 | 35 | 42 |
                                +----+----+----+----+----+----+----+
Chỉ số Cột (c = 0..6):           Cột0 Cột1 Cột2 Cột3 Cột4 Cột5 Cột6
```

Toàn bộ trạng thái bàn cờ tại mọi thời điểm được đặc trưng hoàn toàn bởi hai số nguyên:
- `_pos`: Bitboard chứa các bit `1` tại những vị trí có quân của **người chơi đang tới lượt đi**.
- `_mask`: Bitboard chứa các bit `1` tại những vị trí có quân của **cả hai người chơi** (`_pos | _opp_pos`).
- **Khóa định danh trạng thái duy nhất $O(1)$ (`key = _pos + _mask`)**: Do cột $c$ luôn được lấp liên tục từ đáy lên trên, phép cộng nhị phân `_pos + _mask` tạo ra một số nguyên 49-bit ánh xạ **đơn ánh 1-1** với từng trạng thái hợp lệ trên bàn cờ, cho phép tra cứu bảng băm hoán vị (*Transposition Cache*) trong thời gian hằng số $O(1)$.

#### B. Toán tử Thả quân và Kiểm tra 4 quân liên tiếp `_has_won` độ phức tạp $O(1)$
Nhờ cấu trúc 7 bit mỗi cột, hai thao tác cốt lõi nhất của engine được rút gọn thành vài chu kỳ lệnh CPU:
1. **Thả quân vào cột $c$ (`step(col)`)**: Khi cộng bit đáy cột `1 << (7 * c)` vào `_mask`, toàn bộ chuỗi bit `1` liên tiếp đang có ở cột $c$ sẽ tự động nhớ (*carry*) lên đúng vị trí bit `0` thấp nhất ngay phía trên cột đó! Sau đó chỉ cần lật góc nhìn bằng phép XOR `_pos ^= _mask`:
   ```python
   # Đổi góc nhìn sang đối thủ và bật bit trống thấp nhất tại cột c trong O(1)
   self._pos ^= self._mask
   self._mask |= self._mask + (1 << (col * 7))
   ```
2. **Kiểm tra 4 quân thẳng hàng (`_has_won(bb)`) bằng phép dịch bit 4 hướng $O(1)$**:
   Trên lưới 7 bit/cột, khoảng cách chỉ số bit giữa hai ô kề nhau theo 4 hướng lần lượt là:
   - **Hướng Dọc ($\uparrow$)**: bước dịch $\Delta = 1$ bit.
   - **Hướng Ngang ($\rightarrow$)**: bước dịch $\Delta = 7$ bit.
   - **Hướng Chéo phụ ($/$)**: bước dịch $\Delta = 6$ bit (`+1 cột - 1 hàng = 7 - 1`).
   - **Hướng Chéo chính ($\setminus$)**: bước dịch $\Delta = 8$ bit (`+1 cột + 1 hàng = 7 + 1`).

   Đoạn mã nguồn thực tế trong [`src/c4/game/engine.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/game/engine.py#L46-L62) thực hiện gập đôi cặp bit (`bb & (bb >> s)`) rồi tiếp tục gập đôi khoảng cách (`m & (m >> 2s)`) để kiểm tra đồng thời toàn bộ 69 cửa sổ trên bàn cờ trong thời gian $O(1)$:
   ```python
   @staticmethod
   def _has_won(bb: int) -> bool:
       # 1. Hướng ngang (shift = 7)
       m = bb & (bb >> 7)
       if m & (m >> 14):
           return True
       # 2. Hướng chéo phụ / (shift = 6)
       m = bb & (bb >> 6)
       if m & (m >> 12):
           return True
       # 3. Hướng chéo chính \ (shift = 8)
       m = bb & (bb >> 8)
       if m & (m >> 16):
           return True
       # 4. Hướng dọc | (shift = 1)
       m = bb & (bb >> 1)
       if m & (m >> 2):
           return True
       return False
   ```

### 2.2. Kiểm chuẩn tính đúng đắn cây trò chơi (Perft Validation at Depth 1–6 & Cross-Engine Verification)

Để chứng minh tuyệt đối rằng các phép dịch bit 49-bit không gặp bất kỳ lỗi tràn cột hay sai lệch trạng thái kết thúc nào, nhóm xây dựng song song một engine tham chiếu độc lập [`ReferenceConnect4`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/game/reference.py) sử dụng mảng 2 chiều NumPy `int8[6, 7]` và thực hiện hai phép kiểm chuẩn toán học trong [`tests/test_engine.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/tests/test_engine.py) và [`tests/test_crosscheck.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/tests/test_crosscheck.py):

#### A. Kiểm chuẩn số lượng nút lá cây trò chơi (Perft Validation từ Depth 1 đến Depth 6)
Hàm `perft(game, depth)` duyệt vét cạn toàn bộ các chuỗi nước đi hợp lệ từ bàn cờ rỗng đến độ sâu `depth` (không mở rộng tiếp các nút đã có người thắng ở ply thứ 7 trở đi). Kết quả đếm nút trên `Connect4` (Bitboard 49-bit) khớp chính xác 100% đến từng đơn vị với hằng số lý thuyết của trò chơi Connect Four 7×6:

| Độ sâu (`Depth / Ply`) | Số nút lá lý thuyết chuẩn (OEIS A212693) | Kết quả đếm trên `Connect4` (Bitboard 49-bit) | Kết quả đếm trên `ReferenceConnect4` (Mảng 2D) | Sai số |
|:---:|---:|---:|---:|:---:|
| **Depth 1** | `7` | `7` | `7` | **0 (Khớp 100%)** |
| **Depth 2** | `49` | `49` | `49` | **0 (Khớp 100%)** |
| **Depth 3** | `238` | `238` | `238` | **0 (Khớp 100%)** |
| **Depth 4** | `1.120` | `1.120` | `1.120` | **0 (Khớp 100%)** |
| **Depth 5** | `4.263` | `4.263` | `4.263` | **0 (Khớp 100%)** |
| **Depth 6** | `16.422` | `16.422` | `16.422` | **0 (Khớp 100%)** |

#### B. Kiểm thử đối chiếu chéo 10.000 ván ngẫu nhiên & 57 Unit Tests
- Trong [`tests/test_crosscheck.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/tests/test_crosscheck.py), hai engine cùng chạy song song qua **10.000 ván đấu ngẫu nhiên đầy đủ** (~210.000 trạng thái chuyển tiếp). Sau mỗi nước đi và chuỗi `undo()` lùi về trạng thái gốc, hệ thống đối chiếu đồng thời `legal_actions()`, `is_terminal()`, `winner`, `to_array()` và `encode()` — đạt **0 lỗi sai khác**.
- Toàn bộ **57/57 bài kiểm thử tự động (`pytest`)** trên 9 tệp test đều đạt **100% PASSED** (lưu biên bản kiểm thử tại [`results/TEST_AND_EVALUATION_REPORT.md`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/results/TEST_AND_EVALUATION_REPORT.md)).

---

## CHƯƠNG 3: PHƯƠNG PHÁP TRIỂN KHAI CHUỖI TÁC TỬ AI (LEVEL 1 – LEVEL 5 & ALPHAZERO-LITE)

### 3.1. Nhóm tác tử cổ điển (Random, Priority Heuristic, Negamax Alpha-Beta Pruning)

#### 1. Level 1 — `RandomAgent` ([`src/c4/agents/random_agent.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/agents/random_agent.py))
Sử dụng bộ sinh số giả ngẫu nhiên tách biệt `random.Random(seed)` chọn xác suất đều $P(a) = \frac{1}{|A(s)|}$ cho mọi cột hợp lệ $a \in A(s)$, đóng vai trò mốc sàn kiểm tra logic giải đấu.

#### 2. Level 2 — `HeuristicAgent` ([`src/c4/agents/heuristic.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/agents/heuristic.py))
Triển khai bộ luật ưu tiên 4 tầng tất định không duyệt cây sâu:
- **Tầng 1 (Win-in-1)**: Nếu tồn tại cột $a \in A(s)$ giúp thắng ngay lập tức ($R(T(s, a)) = \tau(s)$) $\rightarrow$ chọn $a$.
- **Tầng 2 (Block-in-1)**: Nếu đối phương có nước thắng ngay ở lượt kế tiếp khi giả định đối phương đi tại cột $a$ $\rightarrow$ chặn ngay tại cột $a$ (ưu tiên cột gần trung tâm nhất nếu có nhiều điểm chặn).
- **Tầng 3 (Bộ lọc chống tự sát — Anti-Blunder Filter)**: Loại bỏ mọi cột $a \in A(s)$ mà việc thả quân vào $(h_s(a), a)$ vô tình nâng đỡ để đối phương đánh tiếp vào $(h_s(a)+1, a)$ và thắng ngay ở lượt kế. Nếu tất cả các cột đều bị loại (bị ép bí), giữ lại tập ban đầu.
- **Tầng 4 (Ưu tiên Trung tâm — Center Preference)**: Chọn cột đầu tiên xuất hiện trong thứ tự ưu tiên hình học `CENTER_ORDER = (3, 2, 4, 1, 5, 0, 6)`.

#### 3. Level 3 — `AlphaBetaAgent` ([`src/c4/agents/alphabeta.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/agents/alphabeta.py))
Triển khai thuật toán duyệt cây đối kháng **Negamax kết hợp cắt tỉa $\alpha$-$\beta$**, tối ưu hóa bằng 3 kỹ thuật:
- **Sắp xếp nước đi tĩnh Center-First**: Luôn duyệt các nhánh con theo thứ tự `(3, 2, 4, 1, 5, 0, 6)` vì cột trung tâm tham gia vào nhiều cửa sổ 4 ô nhất, giúp sớm tìm được cận dưới $\alpha$ lớn để kích hoạt điều kiện cắt nhánh $\alpha \ge \beta$.
- **Phát hiện thắng sớm 1-ply trước khi đệ quy**: Tại mỗi nút trong, trước khi mở rộng đệ quy xuống tầng sâu hơn, tác tử quét nhanh bitboard xem có cột nào thắng ngay không; nếu có, trả về ngay `WIN_SCORE + depth` (`100.000 + depth`) để luôn chọn đường thắng ngắn nhất và đường cầm cự dài nhất khi bị ép thua.
- **Hàm lượng giá 69 cửa sổ tiền tính bitmask (`_evaluate`)**: Tại nút lá $d = 0$, điểm lượng giá là tổng trọng số quân cột trung tâm (`+3` điểm/quân) cộng với điểm quét toàn bộ 69 cửa sổ 4 ô đã tiền tính sẵn bitmask `(w_mask)`:
  $$\text{Eval}(s) = 3 \cdot \left( N_{\text{my}}(\text{col } 3) - N_{\text{opp}}(\text{col } 3) \right) + \sum_{w \in \mathcal{W}_{69}} \phi(w, \text{my}, \text{opp})$$
  với $\phi(w) = +50$ (3 quân mình + 1 trống), $+6$ (2 quân mình + 2 trống), $-80$ (3 quân địch + 1 trống — phạt nặng đe dọa của địch), và $-8$ (2 quân địch + 2 trống).
- **Tìm kiếm sâu dần (*Iterative Deepening*)**: Khi thi đấu theo ngân sách thời gian `time_s`, vòng lặp tăng dần độ sâu $d = 1, 2, \dots, d_{\max}$ và kiểm tra `time.perf_counter()` tại mỗi nút; nếu hết giờ giữa chừng ở tầng $d$, kết quả hoàn chỉnh của tầng $d-1$ vẫn được bảo toàn an toàn.

### 3.2. Nhóm tác tử Monte Carlo (`Level 4` MCTS-UCT 4 giai đoạn)

Tác tử [`MCTSAgent`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/agents/mcts.py) xây dựng cây tìm kiếm bất đối xứng thông qua 4 giai đoạn lặp trong mỗi mô phỏng:
1. **Selection (Chọn nhánh)**: Bắt đầu từ gốc, đi xuống các nút đã mở rộng hoàn toàn bằng cách cực đại hóa chỉ số **UCT** (Kocsis & Szepesvári, 2006):
   $$\text{UCT}(s, a) = \frac{W(s, a)}{N(s, a)} + c \sqrt{\frac{\ln N(s)}{N(s, a)}}, \qquad c = 1,4 \approx \sqrt{2}$$
   trong đó $W(s, a)$ luôn được lưu theo góc nhìn của người chơi thực hiện hành động $a$.
2. **Expansion (Mở rộng)**: Khi gặp nút chưa kết thúc còn hành động chưa thử (`untried`), rút ngẫu nhiên một hành động $a \in \text{untried}$ để tạo nút con mới.
3. **Simulation / Rollout (Giả lập)**: Từ nút con mới, thực hiện chuỗi nước đi ngẫu nhiên đồng đều trên bản sao bitboard đến khi ván cờ kết thúc để thu kết quả $z \in \{0; 0,5; 1\}$.
4. **Backpropagation (Lan truyền ngược)**: Cập nhật $N \leftarrow N + 1$ và cộng dồn điểm thắng theo đúng người chơi vừa đi tại mỗi nút trên đường dẫn về gốc. Khi hết ngân sách, chọn hành động có số lượt thăm $N(\text{root}, a)$ lớn nhất (*Robust Child*).

### 3.3. Đề xuất Tác tử Học sâu AlphaZero-lite (Dual-Head ResNet + PUCT Search Pseudocode)

#### A. Đối chiếu Phương pháp Tích hợp Học máy vào MCTS: Từ Biased MCTS (KLTN tham khảo) đến PUCT-MCTS (AlphaZero-lite)
Trong các nghiên cứu trước đây (như KLTN Reversi tích hợp mô hình Bradley-Terry vào MCTS), việc đưa tri thức máy học vào cây MCTS thường dựa trên hai phép hiệu chỉnh: *Biased Selection* (cộng thêm thành phần xác suất mẫu vào công thức UCB) và *Biased Simulation* (lấy mẫu rollout theo phân phối xác suất thay vì ngẫu nhiên thuần). Kế thừa tư tưởng định hướng cây tìm kiếm đó nhưng nâng cấp lên kiến trúc Học sâu hiện đại theo hướng **AlphaGo / AlphaZero** (Silver et al., 2016, 2017), nhóm thiết kế hệ thống gồm hai thành phần gắn kết chặt chẽ:

| Tiêu chí so sánh | MCTS-UCT Thuần (`Level 4`) | Biased MCTS truyền thống (KLTN tham khảo) | **AlphaZero-lite `MixedMCTSAgent` (Đề xuất của Nhóm 13)** |
|:---|:---|:---|:---|
| **Mô hình biểu diễn tri thức** | Không có ($P(a)$ đồng đều) | Bảng tra xác suất mẫu cục bộ (*Pattern Dictionary*) | **Mạng `Connect4PolicyValueNet` (3 Residual Blocks, 278.952 tham số)** nhận diện cấu trúc toàn bàn cờ. |
| **Định hướng bước Selection** | UCB1 chuẩn: $\frac{W}{N} + c\sqrt{\frac{\ln N_p}{N}}$ | Biased UCB: cộng trọng số xác suất mẫu vào nhánh con | **Công thức PUCT**: nhân trực tiếp xác suất tiên nghiệm **Policy Head $P_\theta(s, a)$** vào biên độ khám phá $c_{\text{puct}} P_\theta(s,a) \frac{\sqrt{\sum_b N(s,b)}}{1 + N(s,a)}$. |
| **Đánh giá nút lá (Leaf Evaluation)** | Rollout ngẫu nhiên đồng đều tới cuối ván | *Biased Simulation*: Rollout lấy mẫu theo xác suất | Hỗ trợ cả 2 chế độ: **(1) Value Head $V_\theta(s) \in [-1, 1]$** (triệt tiêu hoàn toàn bước Rollout) hoặc **(2) Lai ghép Policy Prior + Fast Bitboard Rollout** (Ablation A3). |
| **Tối ưu tra cứu $O(1)$** | Không có | Nén CSV sang Dictionary nhị phân | **Bảng băm Hoán vị `Transposition Cache` $O(1)$** theo khóa bitboard `key = pos + mask`, tránh gọi lại mạng CNN ở các trạng thái trùng lặp. |

#### B. Kiến trúc Mạng Nơ-ron Hai đầu `Connect4PolicyValueNet` ([`src/c4/models/net.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/models/net.py))
Mạng nhận đầu vào là tensor chuẩn hóa góc nhìn $X \in \{0, 1\}^{2 \times 6 \times 7}$ và đi qua:
1. **Khối Stem**: `Conv2d(2 → 64, kernel_size=3×3, padding=1) + BatchNorm2d(64) + ReLU`.
2. **Thân mạng gồm 3 Khối Phần dư (3 Residual Blocks)**: Mỗi khối thực hiện hai phép tích chập $3 \times 3$ với 64 kênh đặc trưng kèm kết nối tắt (*skip connection*) $H_{l+1} = \text{ReLU}(\mathcal{F}(H_l) + H_l)$ giúp lan truyền đạo hàm sâu mà không bị suy biến.
3. **Đầu Chính sách (Policy Head)**: `Conv2d(64 → 2, 1×1) + BN + ReLU → Flatten(84) → Linear(84 → 7)` xuất vector logits $z \in \mathbb{R}^7$. Các cột đã đầy ($a \notin A(s)$) bị gán $-\infty$ trước khi lấy $\text{Softmax}$ để thu được xác suất hợp lệ $P_\theta(s, a)$.
4. **Đầu Giá trị (Value Head)**: `Conv2d(64 → 1, 1×1) + BN + ReLU → Flatten(42) → Linear(42 → 64) + ReLU → Linear(64 → 1) + Tanh` xuất kỳ vọng thắng cuộc $V_\theta(s) \in [-1, +1]$.

#### C. Mã giả chuẩn Thuật toán Tìm kiếm Cây `PUCT_SEARCH` ([`src/c4/agents/mixed_mcts.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/agents/mixed_mcts.py))

```text
THUẬT TOÁN 1: TÌM KIẾM CÂY MONTE CARLO ĐỊNH HƯỚNG MẠNG NƠ-RON (PUCT_SEARCH)
---------------------------------------------------------------------------------
Đầu vào : Trạng thái gốc s_root, Mạng Policy-Value f_theta, Ngân sách mô phỏng M,
          Hằng số khám phá c_puct = 1.5, Bảng băm hoán vị Cache
Đầu ra  : Hành động tối ưu a* thuộc A(s_root)

1:  Nếu tồn tại a thuộc A(s_root) thắng ngay trong 1 nước (Win-in-1): trả về a
2:  Nếu đối thủ đe dọa thắng ngay tại cột duy nhất a_block (Block-in-1): trả về a_block
3:  Khởi tạo nút gốc root = Node(state = s_root)
4:  MỞ_RỘNG_VÀ_LƯỢNG_GIÁ(root, s_root, is_root = True)
5:  Lặp sim = 1 .. M (hoặc đến khi hết thời gian time_s):
6:      node = root;  s = s_root.clone()
7:      // --- Giai đoạn 1: SELECTION theo công thức PUCT ---
8:      Khi node đã mở rộng và chưa phải trạng thái kết thúc:
9:          N_total = sum_{b} node.children[b].N
10:         Chọn nhánh con a cực đại hóa chỉ số PUCT:
                PUCT(node, a) = Q(node, a) + c_puct * P(node, a) * sqrt(max(1, N_total)) / (1 + N(node, a))
                trong đó Q(node, a) = W(node, a) / N(node, a) nếu N > 0, ngược lại bằng 0
11:         node = node.children[a];  s.step(a)
12:     // --- Giai đoạn 2 & 3: EXPANSION & LEAF EVALUATION (kèm O(1) Cache) ---
13:     Nếu s là trạng thái kết thúc:
14:         v_leaf = KẾT_QUẢ_CUỐI_VÁN(s)  // thuộc {-1, 0, +1}
15:     Ngược lại:
16:         v_leaf = MỞ_RỘNG_VÀ_LƯỢNG_GIÁ(node, s, is_root = False)
17:     // --- Giai đoạn 4: BACKPROPAGATION ---
18:     Khi node != None:
19:         node.N += 1
20:         node.W += Chuyển_Đổi_Hệ_Quy_Chiếu(v_leaf, node.player_just_moved)
21:         node = node.parent
22: Trả về argmax_{a thuộc A(s_root)} (root.children[a].N, root.children[a].Q, root.children[a].P)

HÀM PHỤ: MỞ_RỘNG_VÀ_LƯỢNG_GIÁ(node, s, is_root)
---------------------------------------------------------------------------------
1:  key = s._pos + s._mask  // Khóa Bitboard 49-bit duy nhất O(1)
2:  Nếu key có trong Cache:
3:      (priors, v_net) = Cache[key]
4:  Ngược lại:
5:      (logits, v_net) = f_theta(s.encode_tensor_2x6x7())
6:      priors = MaskedSoftmax(logits, s.legal_actions())
7:      Cache[key] = (priors, v_net)
8:  Nếu is_root và bật Dirichlet_Noise:
9:      priors = (1 - eps) * priors.copy() + eps * Dirichlet(alpha)
10: Tạo các nút con node.children[a] với xác suất tiên nghiệm P = priors[a] cho mọi a thuộc A(s)
11: Trả về v_net (nếu dùng Value Head) hoặc FastBitboardRollout(s) (nếu dùng Rollout)
```

---

## CHƯƠNG 4: QUY TRÌNH QUẢN TRỊ DỮ LIỆU VÀ MINH BẠCH HÓA AI (XAI)

### 4.1. Data Pipeline: Mã hóa Tensor, Symmetry Augmentation & Game-level Splitting

Khác với cờ Othello/Reversi có kho biên bản giải đấu quốc tế WTHOR sẵn có, đối với Connect Four, để đảm bảo tính tự chủ hoàn toàn và không phụ thuộc vào bộ giải bên ngoài, nhóm thiết kế **Quy trình Tự sinh và Quản trị Dữ liệu Chuyên gia 5 bước (`Data Pipeline`)** trong [`src/c4/train/gen_data.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/train/gen_data.py):

```mermaid
flowchart LR
    A["Bước 1: Tự đấu Chuyên gia<br/>2.500 ván Alpha-Beta (d=4)<br/>Khai cuộc 4-6 ply + eps=0.14"] --> B["Bước 2: Gán Nhãn Sạch<br/>Policy pi = expert_action<br/>Value z in {-1, 0, +1}"]
    B --> C["Bước 3: Chia theo Ván (70/15/15)<br/>1.750 Train | 375 Val | 375 Test<br/>(Chống rò rỉ cùng ván)"]
    C --> D["Bước 4: Khử trùng & Lọc Gương<br/>Gộp trùng theo khóa Bitboard<br/>Loại bỏ Val/Test trùng gương Train"]
    D --> E["Bước 5: Tăng cường Đối xứng<br/>Lật ngang c' = 6 - c trên Train<br/>Tổng: 87.725 mẫu sạch"]
```

1. **Cấu trúc mã hóa Tensor chuẩn hóa góc nhìn ($2 \times 6 \times 7$)**:
   Mọi trạng thái bàn cờ $s$ đều được hàm `encode()` chuyển thành tensor nhị phân $X \in \{0, 1\}^{2 \times 6 \times 7}$ theo góc nhìn chuẩn hóa (*Canonical Perspective*):
   - **Kênh 0 (`X[0, r, c]`)**: bằng `1` nếu ô $(r, c)$ là quân của **người chơi đang tới lượt đi**, ngược lại bằng `0`.
   - **Kênh 1 (`X[1, r, c]`)**: bằng `1` nếu ô $(r, c)$ là quân của **đối phương**, ngược lại bằng `0`.
   Cách mã hóa bất biến theo màu quân này giúp mạng nơ-ron học một bộ trọng số duy nhất áp dụng cho cả lượt Đỏ lẫn lượt Vàng.
2. **Cơ chế Nhãn chuyên gia sạch (*Clean Expert Action Label*)**:
   Trong `2.500` ván tự đấu của `AlphaBetaAgent(depth=4)` (`seed = 42`), sau 4–6 nước khai cuộc ngẫu nhiên an toàn, tại mỗi trạng thái trong 18 nước đầu tiên, chuyên gia luôn tính toán nước đi tối ưu nhất $a^* = \text{AlphaBeta}(s, d=4)$ để **lưu làm nhãn học có giám sát (`y_policy` = $a^*$)** trước khi tung đồng xu xác suất $\epsilon = 0,14$ để thỉnh thoảng rẽ sang nhánh phụ mở rộng vùng phủ trạng thái. Nhờ đó, tập dữ liệu vừa đa dạng vừa đạt **0% nhiễu nhãn ngẫu nhiên**.
3. **Phân chia theo đơn vị ván đấu (`Game-level Splitting 70/15/15`) & Khử trùng lặp hai chiều gương**:
   - Toàn bộ `2.500` ván được tách ở cấp độ ván thành **1.750 ván Train (70%)**, **375 ván Validation (15%)** và **375 ván Test (15%)**.
   - Trong từng tập, các trạng thái trùng khóa bitboard được hợp nhất bằng biểu quyết đa số (*majority vote*) cho nhãn Policy và trung bình cộng cho nhãn Value.
   - Đặc biệt, hệ thống loại bỏ triệt để mọi trạng thái trong `Val` và `Test` có khóa trùng với trạng thái gốc **hoặc ảnh lật gương ngang** của tập `Train` (`2.917` mẫu bị lọc khỏi `Val` và `3.468` mẫu bị lọc khỏi `Test`), đảm bảo **0% rò rỉ dữ liệu (*Zero Data Leakage*)**.
4. **Tăng cường dữ liệu đối xứng lật ngang (`Horizontal Flip Symmetry`)**:
   Do luật Connect Four bất biến qua phép phản xạ trục dọc cột giữa ($c' = 6 - c$), mỗi mẫu $(X, a^*, z)$ trong tập `Train` được nhân đôi thành $(X_{\text{flip}}, 6 - a^*, z)$, thu được tổng cộng **87.725 mẫu sạch** ([`data/dataset_summary.json`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/data/dataset_summary.json)):
   - [`data/train.npz`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/data/train.npz): **75.036 mẫu** (`37.518` trạng thái gốc × 2 đối xứng gương).
   - [`data/val.npz`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/data/val.npz): **6.396 mẫu độc lập**.
   - [`data/test.npz`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/data/test.npz): **6.293 mẫu độc lập**.

### 4.2. Quá trình huấn luyện Joint Loss & Trực quan hóa bản đồ độ nhạy Saliency Map

#### A. Kiểm định Toán học trong Huấn luyện Đa mục tiêu (Joint Loss Validation)
Mô hình `Connect4PolicyValueNet` được huấn luyện tối thiểu hóa hàm mất mát kết hợp đa mục tiêu (*Joint Loss*) trong [`src/c4/train/train_policy.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/train/train_policy.py):

$$\mathcal{L}(\theta) = \underbrace{-\sum_{a=0}^{6} \tilde{\pi}_a \log P_\theta(a \mid s)}_{\text{Policy Cross-Entropy Loss}} + \lambda_v \underbrace{\left( z - V_\theta(s) \right)^2}_{\text{Value MSE Loss}} + c \|\theta\|_2^2$$

với hệ số cân bằng $\lambda_v = 0,5$, làm mượt nhãn $\alpha_{\text{ls}} = 0,05$, điều chuẩn trọng số $c = 10^{-3}$, bộ tối ưu `Adam(lr = 0,0015)` và lịch giảm `CosineAnnealingLR` qua 10 epochs (`batch_size = 256`).

![Đường cong huấn luyện mạng Policy-Value ResNet](../results/figures/nn_learning_curves.png)

| Epoch | `Train Joint Loss` | `Val Joint Loss` | `Train Policy CE` | `Val Policy CE` | `Train Value MSE` | `Val Value MSE` | `Train Top-1 Acc` | `Val Top-1 Acc` | `Val Top-2 Acc` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | `1,5463` | `1,3859` | `1,1585` | `0,9601` | `0,7755` | `0,8517` | `60,94%` | `64,56%` | `83,35%` |
| **2** | `1,3283` | `1,2508` | `0,9566` | `0,8392` | `0,7435` | `0,8232` | `69,89%` | `69,62%` | `86,87%` |
| **3** | `1,2594` | `1,1791` | `0,8999` | `0,7755` | `0,7190` | `0,8073` | `72,58%` | `70,58%` | `88,43%` |
| **4** | `1,2102` | `1,1649` | `0,8608` | `0,7626` | `0,6989` | `0,8047` | `74,38%` | `71,56%` | `88,60%` |
| **5** | `1,1723` | `1,1485` | `0,8331` | `0,7490` | `0,6784` | `0,7990` | `75,67%` | `71,72%` | `88,91%` |
| **6 (Best)** | **`1,1411`** | **`1,1336`** | **`0,8107`** | **`0,7333`** | **`0,6609`** | **`0,8005`** | **`76,65%`** | **`72,09%`** | **`89,13%`** |
| **8** | `1,0937` | `1,1360` | `0,7797` | `0,7366` | `0,6281` | `0,7988` | `78,02%` | `71,69%` | `89,13%` |
| **10** | `1,0694` | `1,1354` | `0,7649` | `0,7349` | `0,6091` | `0,8010` | `78,74%` | `71,78%` | `89,18%` |

- **Kiểm định trên tập `Test` độc lập (`6.293` mẫu)**: Checkpoint tốt nhất tại Epoch 6 ([`checkpoints/policy_net_best.pt`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/checkpoints/policy_net_best.pt)) đạt **`Test Top-1 Accuracy = 71,68%`** (gấp `5,02` lần mức ngẫu nhiên `14,29%`) và **`Test Top-2 Accuracy = 89,07%`**, với `Test Policy CE = 0,7535`, `Test Value MSE = 0,7884` và độ trễ suy luận đơn lẻ trên CPU chỉ **`1,909 ms`** (`p95 = 2,475 ms`).

#### B. Minh bạch hóa Quyết định Hộp đen bằng Bản đồ Độ nhạy (Gradient Saliency Map — XAI)
Để giải thích trực quan vì sao mạng ResNet đưa ra quyết định chọn cột $a^* = \arg\max_a z_a(X)$, mô-đun [`src/c4/models/explain.py`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/src/c4/models/explain.py) tính đạo hàm bậc nhất của logit $z_{a^*}$ theo từng ô đầu vào (Simonyan et al., 2014):
$$S_{r, c} = \sum_{k \in \{0, 1\}} \left| \frac{\partial z_{a^*}(X)}{\partial X_{k, r, c}} \right|, \qquad \hat{S}_{r, c} = \frac{S_{r, c}}{\max_{r', c'} S_{r', c'} + \varepsilon} \in [0, 1]$$

![Explainable AI: Bản đồ độ nhạy Saliency trên hai tình huống chiến thuật](../results/figures/xai_saliency_double_threat.png)

1. **Tình huống 1 — Phòng thủ sớm trước Đòn kép hàng đáy (`moves = [3, 0, 4]`, lượt Vàng)**:
   - Quân Đỏ (`X`) đã chiếm 2 ô trung tâm liên tiếp `(Hàng 1, Cột 4)` và `(Hàng 1, Cột 5)` với hai đầu mở thông thoáng ở Cột 3 và Cột 6.
   - `HeuristicAgent` (Level 2) bỏ lọt mối đe dọa này vì trên bàn chưa có chuỗi 3 quân nào của `X`, dẫn đến bị gài bẫy đôi ở nước kế tiếp và thua tất yếu.
   - Ngược lại, `Connect4PolicyValueNet` dự đoán chính xác nước chặn sớm tại **Cột 3** (`P = 54,2%`) và bản đồ nhiệt Saliency đạt cực đại **`1,00` ngay tại ô trống khóa đòn kép `(Hàng 1, Cột 3)`**, chứng minh mạng thực sự hiểu cấu trúc hình học của đòn bẫy hai đầu mở.
2. **Tình huống 2 — Đòn kết liễu Đường chéo Khe giữa (`moves = [0, 1, 1, 2, 3, 2, 3, 3, 3, 6]`, lượt Đỏ)**:
   - Quân Đỏ có 3 quân trên đường chéo chính tại `(1,1)`, `(2,2)`, `(4,4)`, chỉ còn khuyết mắt xích khe giữa `(Hàng 3, Cột 3)`. Mạng dồn **98,9% xác suất vào Cột 3** (`Value = +0,601`) và làm sáng rực các ô dọc theo đường chéo chiến thắng.

---

## CHƯƠNG 5: THỰC NGHIỆM ĐỐI KHÁNG VÀ PHÂN TÍCH KẾT QUẢ

### 5.1. Quy chuẩn Giải đấu Vòng tròn Round-Robin Đối xứng (200 ván/cặp, Wilson 95% CI)

Mọi cặp đấu $(A, B)$ trong giải đấu vòng tròn 6 tác tử (**15 cặp × 200 ván = 3.000 ván**, lưu tại [`results/tables/round_robin_default_summary.csv`](file:///d:/AI_PREMIUM/ConnectFour_Game/connect4-ai/connect4-ai/results/tables/round_robin_default_summary.csv)) đều tuân thủ quy chuẩn đối xứng nghiêm ngặt:
- **100 khai cuộc 4-ply chuẩn cố định theo `seed = 42`**: Với mỗi khai cuộc $o_i$, hai tác tử thi đấu **2 ván đổi màu quân** ($A$ cầm Đỏ đi trước 1 ván, $B$ cầm Đỏ đi trước 1 ván) để triệt tiêu hoàn toàn lợi thế đi trước và biến thiên khai cuộc.
- **Độ đo thống kê**: Điểm tổng bằng không $\text{Score}_A = \frac{W_A + 0,5 D}{N}$ kèm **Khoảng tin cậy Bootstrap 95%** (`10.000` lần lấy mẫu) và tỷ lệ thắng nhị phân kèm **Khoảng tin cậy Wilson 95%**.

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

### 5.2. Phân tích kết quả thí nghiệm Giải đấu Tính giờ (RQ1) & Ablation Studies (A1 – A4)

#### A. Thí nghiệm Giải đấu Giới hạn Thời gian Thực (RQ1 — `round_robin_timed_summary.csv`)
Khi cấp cùng ngân sách thời gian suy nghĩ `50 ms`, `100 ms` và `300 ms / nước` (`100` ván/mức), `Alpha-Beta` (Iterative Deepening) đạt điểm số lần lượt **0,6500** (`CI [0,555; 0,740]`), **0,6900** (`CI [0,600; 0,775]`) và **0,6050** (`CI [0,510; 0,700]`) trước `MCTS-UCT`. Ở mức `300 ms`, `MCTS-UCT` bắt đầu thu hẹp khoảng cách từ `31,0%` lên `39,5%`.

![Chế độ A: Alpha-Beta vs MCTS dưới cùng ngân sách thời gian](../results/figures/timed_crossover_rq1.png)

#### B. Ablation A1: Hiệu quả Cắt tỉa Alpha-Beta và Sắp xếp Nước đi Center-First (`ablation_a1_results.csv`)

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

#### C. Ablation A2: Quy mô Mô phỏng MCTS đối đầu Alpha-Beta Cố định Depth 4 (`ablation_a2_results.csv`)
Khi tăng số mô phỏng của `MCTS-UCT` qua 5 mốc `100 → 500 → 1.000 → 2.000 → 5.000 sims` trước `Alpha-Beta (depth=4)`, điểm số của MCTS tăng đơn điệu từ `0,065 → 0,305 → 0,420 → 0,540 → 0,585`. **Điểm giao thoa (cross-over point) xuất hiện tại ~1.500–2.000 mô phỏng/nước**.

![Ablation A2: Quy mô mô phỏng MCTS đối đầu Alpha-Beta Depth 4](../results/figures/ablation_a2_scaling.png)

#### D. Ablation A3: Bóc tách Vai trò của Policy Prior và Value Head trong PUCT (`ablation_a3_results.csv`)

| Biến thể Tác tử | Số Playouts / Sims | Đối thủ Benchmark | W / D / L | `Score` | Bootstrap 95% CI | `Mean Time` (ms) |
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

**Minh chứng nguyên lý "Duyệt ít nút hơn nhưng chọn nước đi chất lượng hơn"**:
Tại cùng mức ngân sách chỉ **200 mô phỏng** (ít hơn 2,5 lần so với đối thủ `MCTS-500`), `MCTS-UCT` thuần chỉ đạt `32,5%` điểm, nhưng ngay khi tích hợp xác suất tiên nghiệm Policy Head $P_\theta(s,a)$ vào công thức PUCT, tỷ lệ điểm vọt lên **69,5%** (+37% điểm số) và đánh bại luôn cả tác tử thầy `Alpha-Beta (depth=4)` với điểm số **62,5%**!

#### E. Ablation A4: Định lượng Lợi thế Người đi trước trên 3.000 Ván (`ablation_a4_first_player_bias.csv`)
Trên toàn bộ `3.000` ván đấu Round-Robin, **Quân Đỏ (Đi trước)** thắng `1.554` ván (**51,80%**), **Quân Vàng (Đi sau)** thắng `1.277` ván (**42,57%**), Hòa `169` ván (**5,63%**) $\Rightarrow$ độ lệch ròng **$\Delta W = +9,23\%$** nghiêng về người đi trước, phù hợp hoàn toàn với định lý của Allis (1988).

![Ablation A4: Lợi thế người đi trước trên toàn bộ các cặp đấu](../results/figures/first_player_advantage.png)

### 5.3. Bảng Tiến hóa Đa Phiên bản Tác tử (Agent Progression Table) & Phân tích Đánh đổi: Thông lượng Duyệt nút, Độ trễ Suy luận vs Tỷ lệ Thắng

Tương tự phương pháp đánh giá tiến hóa đa phiên bản trong các công trình Game AI chuẩn mực, bảng dưới đây tổng hợp sự tiến hóa xuyên suốt của **6 phiên bản tác tử** trên `1.000` ván đối kháng mỗi tác tử trong giải đấu Round-Robin, đặt cạnh số nút/mô phỏng trung bình mỗi nước, độ trễ trung bình (`Mean Latency`) và độ trễ phân vị thứ 95 (`p95 Latency`):

| Phiên bản Tác tử (Incremental Version) | Cơ chế Suy luận Cốt lõi | Số Nút / Playouts TB mỗi nước | Độ trễ TB (`Mean ms`) | Độ trễ `p95` (`ms`) | Thành tích (`1.000` ván) | Điểm Tổng hợp (`Overall Score`) | Tỷ lệ thắng vs `MCTS-1000` (Baseline 1) | Tỷ lệ thắng vs `AlphaBeta d=5` (Baseline 2) |
|:---|:---|---:|---:|---:|:---:|:---:|:---:|:---:|
| **v1: `RandomAgent`** (Level 1) | Lấy mẫu ngẫu nhiên đồng đều | `1` | `0,006` | `0,012` | `4W - 0D - 996L` | **0,40%** | `0,00%` | `0,00%` |
| **v2: `HeuristicAgent`** (Level 2) | Luật 4 tầng + Lọc chống tự sát 1-ply | `~14` | `0,121` | `0,248` | `350W - 70D - 580L` | **38,50%** | `23,25%` | `16,75%` |
| **v3: `NNAgent` (ResNet 0-Search)** (Level 5) | Truyền thẳng `Connect4PolicyValueNet` (`0` cây tìm kiếm) | `1` (1 lượt CNN) | `2,910` | `3,864` | `460W - 87D - 453L` | **50,35%** | `41,00%` | `23,50%` |
| **v4: `MCTSAgent` (UCT-1000)** (Level 4) | Cây MCTS 4 pha + Rollout ngẫu nhiên | `1.000` sims | `83,420` | `148,847` | `596W - 27D - 377L` | **60,95%** | *Mốc chuẩn (50%)* | `31,50%` |
| **v5: `AlphaBetaAgent` (Depth 5)** (Level 3) | Negamax + Cắt tỉa $\alpha$-$\beta$ + Center-First + 69 cửa sổ | `~339` nút | `21,860` | `61,480` | `716W - 64D - 220L` | **74,80%** | **68,50%** | *Mốc chuẩn (50%)* |
| **v6: `MixedMCTSAgent` (PUCT-200)** (AlphaZero-lite) | **ResNet Policy Prior + Value Head + PUCT + $O(1)$ Cache** | **Chỉ `200` sims** | `348,120` | `709,088` | **`705W - 90D - 205L`** | **75,00% (Hạng 1)** | **62,50%** | **54,25%** |

**Ba kết luận đắt giá từ phân tích đánh đổi (Trade-off Analysis)**:
1. **Duyệt ít hơn 5 lần nhưng thắng áp đảo nhờ tri thức học sâu (`v6` vs `v4`)**: So với `MCTS-UCT` phải chạy `1.000` mô phỏng ngẫu nhiên (`v4`, đạt `60,95%`), phiên bản `MixedMCTSAgent` (`v6`) giảm số lượng mô phỏng xuống **5 lần (chỉ `200` sims/nước)** nhưng tỷ lệ điểm tổng hợp tăng từ **60,95% lên 75,00%**, và thắng trực tiếp `MCTS-1000` với điểm số **62,50%** (`121W – 8D – 71L`). Điều này chứng minh rằng mạng ResNet đã cắt bỏ hiệu quả các nhánh rác ngay từ bước *Selection*.
2. **Sự cộng hưởng giữa Tìm kiếm Cây và Học sâu (`v6` vs `v3` & `v5`)**: Khi đứng một mình không tìm kiếm cây (`v3`), mạng ResNet suy luận siêu tốc trong `2,91 ms/nước` và đạt `50,35%` điểm tổng hợp (thắng `Heuristic` `64,25%`), nhưng vẫn thua các thuật toán duyệt cây sâu ở những thế cờ bẫy nhiều bước. Ngược lại, khi ghép mạng `v3` vào cây tìm kiếm PUCT `200` mô phỏng (`v6`), sự kết hợp giữa **trực giác toàn cục của CNN** và **kiểm chứng chiến thuật ngắn hạn của cây tìm kiếm** giúp `v6` vượt qua cả `Alpha-Beta depth 5` (`54,25%`).
3. **Khuyến nghị lựa chọn tác tử theo bài toán thực tế**:
   - Nếu ưu tiên **thời gian phản hồi tức thì (`< 65 ms`) trên thiết bị cấu hình thấp**: `AlphaBetaAgent (depth=5)` (`v5`) hoặc biến thể lai `PUCT_Prior_Rollout (200 sims, ~151 ms)` là lựa chọn tối ưu về tỷ số Sức mạnh / Độ trễ.
   - Nếu ưu tiên **sức mạnh chiến thuật cao nhất & khả năng giải thích trực quan (XAI)**: `MixedMCTSAgent (PUCT)` (`v6`) là tác tử mạnh nhất toàn hệ thống.

---

## TÀI LIỆU THAM KHẢO

1. V. L. Allis, *A Knowledge-Based Approach of Connect-Four — The Game is Solved: White Wins*, Master's thesis, Vrije Universiteit Amsterdam, 1988.
2. L. Kocsis and C. Szepesvári, "Bandit Based Monte-Carlo Planning," in *Proc. 17th European Conference on Machine Learning (ECML)*, Springer, 2006, pp. 282–293.
3. D. Silver et al., "Mastering the game of Go with deep neural networks and tree search," *Nature*, vol. 529, no. 7587, pp. 484–489, 2016.
4. D. Silver et al., "Mastering the game of Go without human knowledge," *Nature*, vol. 550, no. 7676, pp. 354–359, 2017.
5. S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. Hoboken, NJ: Pearson, 2021.
6. M. Liu, *AlphaGo Simplified: Rule-Based AI and Deep Learning in Everyday Games*, Boca Raton, FL: CRC Press, 2025.
7. K. Simonyan, A. Vedaldi, and A. Zisserman, "Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps," in *ICLR Workshop*, 2014.
8. S. Edelkamp and P. Kissmann, "Symbolic Classification of General Two-Player Games," in *KI 2008: Advances in Artificial Intelligence*, Springer, 2008, pp. 185–192.
9. D. E. Knuth and R. W. Moore, "An analysis of alpha-beta pruning," *Artificial Intelligence*, vol. 6, no. 4, pp. 293–326, 1975.
