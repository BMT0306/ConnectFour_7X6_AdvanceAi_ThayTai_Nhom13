# TRƯỜNG ĐẠI HỌC SÀI GÒN
# KHOA CÔNG NGHỆ THÔNG TIN

---

# BÁO CÁO ĐỒ ÁN CUỐI KỲ
## HỌC PHẦN: TRÍ TUỆ NHÂN TẠO NÂNG CAO
### ĐỀ TÀI: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ TRÊN TRÒ CHƠI CONNECT FOUR (7×6)

* **Giảng viên hướng dẫn**: Thầy Đỗ Như Tài
* **Nhóm thực hiện**: Nhóm 13
* **Link mã nguồn GitHub**: https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13

### BẢNG PHÂN CÔNG NHIỆM VỤ VÀ TỶ LỆ ĐÓNG GÓP

| STT | Họ và tên sinh viên | Mã số SV | Vai trò | Công việc thực hiện | Tỷ lệ đóng góp |
|:---:|:---|:---:|:---:|:---|:---:|
| 1 | Bùi Minh Trung | 3124720074 | Nhóm trưởng | Xây dựng lõi game (`bitboard` và `reference`), viết unit test; cài đặt `HeuristicAgent`, `AlphaBetaAgent`; viết khung chạy giải đấu, hàm tính thống kê (`Wilson`, `Bootstrap`, `p95`); chạy thí nghiệm Ablation A1, A3; cài đặt bản đồ độ nhạy Saliency và giao diện Web; quản lý nhánh Git và đóng gói bài nộp. | 32% |
| 2 | Trần Lê Minh Tâm | 3124720064 | Thành viên | Cài đặt `RandomAgent`, `MCTSAgent` (thuật toán UCT 4 bước); thiết kế mạng `Connect4PolicyValueNet`, viết script sinh dữ liệu và huấn luyện mô hình; cài đặt `MixedMCTSAgent` (kết hợp PUCT, bộ nhớ đệm trạng thái và nhiễu Dirichlet); làm giao diện Pygame và chạy Ablation A2, A4. | 32% |
| 3 | Nguyễn Thành Tài | 3124720062 | Thành viên | Chạy các cấu hình giải đấu và thu thập file log CSV; làm notebook tổng hợp kết quả và vẽ biểu đồ (`01_tournament_analysis.ipynb`); soạn bộ 33 thế cờ kiểm thử thủ công (`positions.csv`); phân tích các tình huống ván đấu và viết nội dung thực nghiệm Chương 4, Chương 5. | 18% |
| 4 | Chương Gia Thịnh | 3124720067 | Thành viên | Tổng hợp tài liệu và viết nội dung Chương 1, Chương 2, Chương 3; soạn slide thuyết trình, thiết kế poster khổ A0 và kịch bản quay video demo; rà soát tài liệu tham khảo, tệp `THIRD_PARTY.md`, `README.md` và chuẩn bị bản in báo cáo. | 18% |
| **Tổng** | | | | | **100%** |

---

## LỜI NÓI ĐẦU

Trong chương trình học phần Trí tuệ nhân tạo nâng cao, các thuật toán tìm kiếm đối kháng và học máy trên trò chơi luôn là một chủ đề gắn liền giữa lý thuyết và thực hành. Thay vì chỉ dừng lại ở việc gọi thư viện có sẵn hoặc cài đặt một thuật toán đơn lẻ như Minimax cơ bản, nhóm chúng em mong muốn tự tay xây dựng một hệ thống hoàn chỉnh từ tầng biểu diễn trạng thái bàn cờ ở mức bit cho đến việc so sánh thực nghiệm giữa các nhánh tiếp cận khác nhau: từ luật phản xạ, duyệt cây cổ điển, tìm kiếm Monte Carlo cho đến việc huấn luyện mạng nơ-ron sâu kết hợp tìm kiếm cây theo hướng của AlphaZero.

Trò chơi Connect Four với kích thước bàn chuẩn 7 cột × 6 hàng được nhóm lựa chọn vì có luật chơi rõ ràng, số nhánh tại mỗi lượt không quá lớn (tối đa 7 cột) để có thể tự sinh dữ liệu và huấn luyện mô hình ngay trên máy tính cá nhân của các thành viên trong nhóm, nhưng đồng thời không gian trạng thái toàn cục (khoảng $4,53 \times 10^{12}$ trạng thái) vẫn đủ lớn để các thuật toán tìm kiếm vét cạn thông thường không thể giải trực tiếp trong thời gian thực.

Trong quá trình thực hiện đề tài, mặc dù nhóm đã cố gắng kiểm thử kỹ mã nguồn và chạy hơn 4.600 ván đấu thực nghiệm để lấy số liệu khách quan, báo cáo chắc chắn không tránh khỏi những thiếu sót nhất định do giới hạn về thời gian và cấu hình phần cứng. Nhóm chúng em rất mong nhận được sự góp ý của Thầy để hoàn thiện hơn. Nhóm xin chân thành cảm ơn Thầy Đỗ Như Tài đã giảng dạy và định hướng cho nhóm trong suốt học phần này.

---

## TÓM TẮT ĐỒ ÁN

Báo cáo trình bày quá trình thiết kế, cài đặt và đánh giá thực nghiệm hệ thống tác tử trí tuệ nhân tạo đa cấp độ cho trò chơi Connect Four (7 cột × 6 hàng). Ở tầng hạ tầng, nhóm cài đặt song song hai bộ máy quản lý luật chơi: bản `ReferenceConnect4` dùng mảng hai chiều thông thường để làm chuẩn đối chiếu và bản `Connect4` dùng kỹ thuật Bitboard 49-bit để tăng tốc độ duyệt cây. Kết quả kiểm chuẩn Perft đến độ sâu 6 và kiểm thử chéo 10.000 ván ngẫu nhiên cho thấy hai phiên bản cho kết quả khớp nhau hoàn toàn.

Trên nền tảng engine đó, nhóm triển khai tuần tự 6 cấp độ tác tử gồm: `RandomAgent` (đi ngẫu nhiên), `HeuristicAgent` (dựa trên 4 quy tắc ưu tiên một bước), `AlphaBetaAgent` (duyệt cây Negamax có cắt tỉa Alpha-Beta, sắp xếp nước đi ưu tiên cột giữa và tìm kiếm sâu dần theo thời gian), `MCTSAgent` (tìm kiếm cây Monte Carlo dùng công thức UCT), `NNAgent` (mạng nơ-ron hai đầu `Connect4PolicyValueNet` gồm 3 khối Residual học có giám sát từ dữ liệu của Alpha-Beta độ sâu 4) và `MixedMCTSAgent` (kết hợp đầu ra của mạng nơ-ron vào công thức chọn nhánh PUCT kèm bộ nhớ đệm trạng thái). Ngoài ra, nhóm cũng cài đặt thêm phương pháp tính bản đồ độ nhạy đạo hàm (Saliency Map) để quan sát xem mạng nơ-ron tập trung vào các ô cờ nào khi đưa ra quyết định.

Quá trình đánh giá được thực hiện thông qua giải đấu vòng tròn 3.000 ván (15 cặp tác tử, mỗi cặp đấu 200 ván có đổi bên trên 100 thế cờ khai cuộc cố định), giải đấu giới hạn thời gian thực 300 ván (ở các mức 50 ms, 100 ms, 300 ms mỗi nước) và 4 thí nghiệm khảo sát thành phần (Ablation A1 đến A4). Kết quả cho thấy kỹ thuật cắt tỉa Alpha-Beta kết hợp sắp xếp ưu tiên cột giữa giúp giảm 93,07% số nút phải duyệt ở độ sâu 6. Đối với phần học sâu, mạng `Connect4PolicyValueNet` đạt độ chính xác dự đoán nước đi Top-1 là 71,68% và Top-2 là 89,07% trên tập kiểm tra độc lập. Khi ghép mạng này vào thuật toán tìm kiếm cây PUCT với ngân sách chỉ 200 mô phỏng mỗi nước, tác tử `MixedMCTSAgent` đứng đầu giải đấu vòng tròn với điểm số trung bình 75,00%, vượt qua cả `MCTSAgent` chạy 1.000 mô phỏng (đạt 62,50% điểm đối đầu) và nhỉnh hơn `AlphaBetaAgent` ở độ sâu 5 (đạt 54,25% điểm đối đầu).

---

## MỤC LỤC

- **LỜI NÓI ĐẦU**
- **TÓM TẮT ĐỒ ÁN**
- **MỤC LỤC**
- **DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU**
- **CHƯƠNG 1: GIỚI THIỆU VÀ KHẢO SÁT CHƯƠNG TRÌNH CONNECT FOUR**
  - 1.1. Bối cảnh đề tài và hình thức hóa toán học không gian trạng thái $(S, A, T, R)$
  - 1.2. Khảo sát thuật toán/mã nguồn sẵn có và đặt mốc đánh giá chuẩn (Benchmark Baseline)
  - 1.3. Các câu hỏi nghiên cứu định lượng (RQ1 – RQ3)
- **CHƯƠNG 2: HẠ TẦNG KỸ THUẬT VÀ CẤU TRÚC DỮ LIỆU BITBOARD**
  - 2.1. Thiết kế Bitboard 49-bit và toán tử Bitwise $O(1)$
    - 2.1.1. Cách ánh xạ bàn cờ 7×6 vào 49 bit của số nguyên 64-bit
    - 2.1.2. Toán tử thả quân và kiểm tra thắng `_has_won` trong thời gian hằng số $O(1)$
  - 2.2. Kiểm chuẩn tính đúng đắn cây trò chơi (Perft Validation at Depth 6)
- **CHƯƠNG 3: PHƯƠNG PHÁP TRIỂN KHAI CHUỖI TÁC TỬ AI (LEVEL 1 – LEVEL 5)**
  - 3.1. Nhóm tác tử cổ điển (Random, Heuristic, Negamax Alpha-Beta Pruning)
    - 3.1.1. Tác tử Cấp 1 — `RandomAgent` (`src/c4/agents/random_agent.py`)
    - 3.1.2. Tác tử Cấp 2 — `HeuristicAgent` (`src/c4/agents/heuristic.py`)
    - 3.1.3. Tác tử Cấp 3 — `AlphaBetaAgent` (`src/c4/agents/alphabeta.py`)
  - 3.2. Nhóm tác tử Monte Carlo (MCTS-UCT 4 giai đoạn)
  - 3.3. Đề xuất Tác tử Học sâu AlphaZero-lite (Dual-Head ResNet + PUCT Search Pseudocode)
    - 3.3.1. Kiến trúc mạng hai đầu `Connect4PolicyValueNet` (`src/c4/models/net.py`)
    - 3.3.2. Sự cải tiến khi tích hợp mạng học sâu vào cây tìm kiếm PUCT (`MixedMCTSAgent`)
- **CHƯƠNG 4: QUY TRÌNH QUẢN TRỊ DỮ LIỆU VÀ MINH BẠCH HÓA AI (XAI)**
  - 4.1. Data Pipeline: Mã hóa Tensor, Symmetry Augmentation và Game-level Splitting
  - 4.2. Quá trình huấn luyện Joint Loss và trực quan hóa bản đồ độ nhạy Saliency Map
    - 4.2.1. Kiểm định toán học quá trình huấn luyện đa mục tiêu (Joint Loss Validation)
    - 4.2.2. Trực quan hóa quyết định của mạng bằng bản đồ độ nhạy Saliency Map (XAI)
- **CHƯƠNG 5: THỰC NGHIỆM ĐỐI KHÁNG VÀ PHÂN TÍCH KẾT QUẢ**
  - 5.1. Quy chuẩn Giải đấu Vòng tròn Round-Robin Đối xứng (200 ván/cặp, Wilson 95% CI)
  - 5.2. Phân tích kết quả thí nghiệm Giải đấu Tính giờ (RQ1) và Ablation Studies (A1 – A4)
    - 5.2.1. Giải đấu giới hạn thời gian suy nghĩ cho RQ1 (`round_robin_timed_summary.csv`)
    - 5.2.2. Thí nghiệm Ablation A1: Đóng góp của cắt tỉa Alpha-Beta và sắp xếp nước đi Center-First
    - 5.2.3. Thí nghiệm Ablation A2: Tìm điểm giao thoa của MCTS trước Alpha-Beta cố định độ sâu 4
    - 5.2.4. Thí nghiệm Ablation A3: Bóc tách vai trò của Policy Prior và Value Head trong PUCT (Trả lời RQ2 và RQ3)
    - 5.2.5. Thí nghiệm Ablation A4: Định lượng lợi thế của người đi trước trên 3.000 ván đấu
  - 5.3. Đánh giá mối quan hệ đánh đổi: Thông lượng duyệt nút, Độ trễ suy luận và Tỷ lệ thắng
- **KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN**
  - 1. Kết luận chung
  - 2. Hạn chế và hướng phát triển tiếp theo
- **TÀI LIỆU THAM KHẢO**

---

## DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU

### Danh mục Hình ảnh

- **Hình 4.1**: Diễn biến hàm mất mát và độ chính xác trên tập Train và Validation qua 10 epochs
- **Hình 4.2**: Bản đồ độ nhạy Saliency Map giải thích quyết định của mạng trên hai thế cờ chiến thuật
- **Hình 5.1**: Ma trận điểm số đối đầu trực tiếp và bảng xếp hạng tổng hợp 6 tác tử qua 3.000 ván
- **Hình 5.2**: So sánh tỷ lệ điểm giữa Alpha-Beta và MCTS-UCT ở các mức ngân sách thời gian 50ms, 100ms, 300ms
- **Hình 5.3**: Biểu đồ so sánh số nút duyệt trong thí nghiệm Ablation A1 ở độ sâu 4, 5 và 6
- **Hình 5.4**: Đường cong tăng trưởng điểm số của MCTS-UCT theo số lượng mô phỏng trước Alpha-Beta depth 4
- **Hình 5.5**: Kết quả Ablation A3 bóc tách đóng góp của Policy Prior và Value Head ở mức 200 mô phỏng
- **Hình 5.6**: Tỷ lệ thắng của người đi trước (Quân Đỏ) và người đi sau (Quân Vàng) trên từng cặp đấu

### Danh mục Bảng biểu

- **Bảng 1.1**: Tổng hợp khảo sát các nhóm chương trình chơi Connect Four phổ biến
- **Bảng 2.1**: Kết quả kiểm chuẩn Perft từ độ sâu 1 đến độ sâu 6 trên bàn cờ 7×6
- **Bảng 3.1**: So sánh cơ chế giữa MCTS-UCT thuần, Biased MCTS và MixedMCTSAgent (PUCT)
- **Bảng 4.1**: Kết quả huấn luyện và kiểm định mạng Connect4PolicyValueNet qua 10 epochs
- **Bảng 5.1**: Kết quả chi tiết 15 cặp đấu trong giải đấu Round-Robin 3.000 ván (200 ván/cặp)
- **Bảng 5.2**: Kết quả đối đầu giữa Alpha-Beta (Iterative Deepening) và MCTS-UCT dưới cùng ngân sách thời gian
- **Bảng 5.3**: Kết quả Ablation A1 — Số nút duyệt và thời gian chạy khi bật/tắt cắt tỉa và sắp xếp nước đi
- **Bảng 5.4**: Kết quả Ablation A2 — Tỷ lệ điểm của MCTS-UCT khi tăng số mô phỏng trước Alpha-Beta (depth = 4)
- **Bảng 5.5**: Kết quả Ablation A3 — So sánh 4 biến thể trước hai mốc chuẩn mcts_500 và alphabeta_d4
- **Bảng 5.6**: Bảng tổng hợp tiến hóa 6 phiên bản tác tử AI và sự đánh đổi giữa độ trễ suy luận với tỷ lệ thắng

---

## CHƯƠNG 1: GIỚI THIỆU VÀ KHẢO SÁT CHƯƠNG TRÌNH CONNECT FOUR

### 1.1. Bối cảnh đề tài và hình thức hóa toán học không gian trạng thái $(S, A, T, R)$

Trong lĩnh vực Trí tuệ nhân tạo, các trò chơi bàn cờ hai người chơi có thông tin hoàn hảo (như Cờ vua, Cờ vây, Othello hay Connect Four) thường được sử dụng làm môi trường tiêu chuẩn để kiểm nghiệm các thuật toán ra quyết định. Trước đây, hướng tiếp cận chủ đạo là sử dụng thuật toán duyệt cây Minimax kết hợp cắt tỉa Alpha-Beta và một hàm lượng giá trạng thái do con người thiết kế thủ công dựa trên kinh nghiệm của trò chơi đó. Cách làm này rất hiệu quả khi hệ số phân nhánh nhỏ và dễ viết hàm đánh giá, nhưng lại phụ thuộc nhiều vào việc chọn trọng số thủ công. Ngược lại, thuật toán Tìm kiếm cây Monte Carlo (MCTS) đánh giá thế cờ thông qua việc mô phỏng ngẫu nhiên nhiều ván đấu đến khi kết thúc mà không cần hàm lượng giá, tuy nhiên các bước chạy ngẫu nhiên thuần túy đôi khi bỏ sót các nước bẫy chiến thuật ngắn hạn. Trong những năm gần đây, kiến trúc kết hợp mạng nơ-ron tích chập sâu (nhiệm vụ ước lượng xác suất nước đi và giá trị thế cờ) với cây tìm kiếm MCTS theo công thức PUCT của AlphaGo và AlphaZero đã cho thấy hiệu quả rõ rệt khi khắc phục được nhược điểm của cả hai phương pháp trên.

Trò chơi Connect Four được thương mại hóa bởi Milton Bradley vào năm 1974. Bàn cờ tiêu chuẩn gồm một khung thẳng đứng có 7 cột (đánh số từ $0$ đến $6$ từ trái sang phải) và 6 hàng (đánh số từ $0$ đến $5$ từ dưới đáy lên trên). Hai người chơi, quy ước là Quân Đỏ (người chơi 1, đi trước) và Quân Vàng (người chơi 2, đi sau), lần lượt thả từng quân cờ của mình vào một trong các cột chưa đầy. Do có trọng lực, quân cờ luôn rơi xuống ô trống thấp nhất của cột được chọn. Trò chơi kết thúc ngay khi một người chơi xếp được 4 quân cùng màu liên tiếp theo hàng ngang, hàng dọc hoặc một trong hai đường chéo; nếu toàn bộ 42 ô trên bàn cờ đã kín mà không bên nào tạo được 4 quân thẳng hàng thì ván đấu có kết quả hòa.

Theo phân loại môi trường trong giáo trình của Russell và Norvig (2021), Connect Four là môi trường quan sát được toàn phần (fully observable), tất định (deterministic), hữu hạn và rời rạc (discrete), tuần tự theo lượt (sequential) và đối kháng tổng bằng không (zero-sum). Để thuận tiện cho việc trình bày thuật toán ở các chương sau, bài toán được mô hình hóa bằng bộ bốn $(S, A, T, R)$ như sau:

1. **Không gian trạng thái ($S$)**: Mỗi trạng thái $s \in S$ biểu diễn một cấu hình bàn cờ hợp lệ kích thước $6 \times 7$ kèm theo thông tin người chơi đang tới lượt $\tau(s) \in \{+1, -1\}$. Một cấu hình được gọi là hợp lệ nếu ở mọi cột $c \in \{0, \dots, 6\}$, các quân cờ đều nằm liên tiếp từ hàng $0$ đến hàng $h_s(c) - 1$, trong đó $h_s(c) \in \{0, \dots, 6\}$ là số quân hiện có trong cột $c$. Theo kết quả nghiên cứu của Victor Allis (1988) và công trình đếm trạng thái của Edelkamp & Kissmann (2008), tổng số trạng thái hợp lệ trên bàn cờ $7 \times 6$ là $|S| = 4.531.985.219.092 \approx 4,53 \times 10^{12}$.
2. **Tập hành động hợp lệ ($A(s)$)**: Tại một trạng thái chưa kết thúc $s$, người chơi hiện tại có thể chọn bất kỳ cột nào có số quân nhỏ hơn 6:
   $$A(s) = \{ c \in \{0, 1, 2, 3, 4, 5, 6\} \mid h_s(c) < 6 \}$$
   Như vậy, hệ số phân nhánh tại mỗi nút thỏa mãn $b = |A(s)| \le 7$, và chiều dài tối đa của một ván đấu là $42$ nước đi (ply).
3. **Hàm chuyển trạng thái ($T(s, a)$)**: Khi thực hiện hành động $a \in A(s)$ tại trạng thái $s$, quân cờ của người chơi $\tau(s)$ sẽ được đặt vào tọa độ hàng $r = h_s(a)$, cột $c = a$. Trạng thái mới $s' = T(s, a)$ có chiều cao cột $h_{s'}(a) = h_s(a) + 1$ và quyền đi lượt kế tiếp chuyển sang đối phương $\tau(s') = -\tau(s)$.
4. **Tập cửa sổ chiến thắng và hàm kết cục ($R(s)$)**: Trên bàn cờ 6 hàng × 7 cột, số lượng đoạn thẳng gồm 4 ô liên tiếp (gọi là các cửa sổ 4 ô, ký hiệu tập hợp là $\mathcal{W}_{69}$) được tính cụ thể gồm:
   - Hướng ngang: mỗi hàng có $7 - 4 + 1 = 4$ cửa sổ $\Rightarrow 6 \times 4 = 24$ cửa sổ.
   - Hướng dọc: mỗi cột có $6 - 4 + 1 = 3$ cửa sổ $\Rightarrow 7 \times 3 = 21$ cửa sổ.
   - Hướng chéo chính ($\setminus$): có $(6 - 4 + 1) \times (7 - 4 + 1) = 3 \times 4 = 12$ cửa sổ.
   - Hướng chéo phụ ($/$): tương tự có $3 \times 4 = 12$ cửa sổ.
   Tổng cộng toàn bàn cờ có $24 + 21 + 12 + 12 = 69$ cửa sổ chiến thắng. Tại trạng thái kết thúc $s$, hàm phần thưởng $R(s)$ tính theo góc nhìn của người chơi thứ nhất nhận giá trị:
   $$R(s) = \begin{cases} +1 & \text{nếu Quân Đỏ (+1) chiếm trọn 1 trong 69 cửa sổ thuộc } \mathcal{W}_{69} \\ -1 & \text{nếu Quân Vàng (-1) chiếm trọn 1 trong 69 cửa sổ thuộc } \mathcal{W}_{69} \\ 0 & \text{nếu đã đi đủ 42 nước mà chưa bên nào thắng (Hòa)} \end{cases}$$

### 1.2. Khảo sát thuật toán/mã nguồn sẵn có và đặt mốc đánh giá chuẩn (Benchmark Baseline)

Trước khi bắt tay vào xây dựng các tác tử của nhóm, chúng em đã tìm hiểu các cách cài đặt chương trình chơi Connect Four phổ biến trên các kho mã nguồn mở cũng như trong các tài liệu học thuật. Nhìn chung, các chương trình hiện có thường thuộc một trong bốn nhóm tiếp cận chính được tổng hợp trong Bảng 1.1.

**Bảng 1.1: Tổng hợp khảo sát các nhóm chương trình chơi Connect Four phổ biến**

| STT | Nhóm tiếp cận | Nguồn tham khảo tiêu biểu | Cách thức hoạt động và đặc điểm chính | Cách nhóm kế thừa và chuẩn hóa trong đồ án |
|:---:|:---|:---|:---|:---|
| 1 | Luật ưu tiên trực tiếp (Rule-based 1-ply) | Mã nguồn minh họa của Al Sweigart (`inventwithpython`), các bot cơ sở | Không duyệt cây nhiều tầng; chỉ kiểm tra nếu có cột thắng ngay ở lượt hiện tại thì đánh, nếu đối thủ sắp thắng ở lượt kế tiếp thì chặn, kết hợp ưu tiên cột giữa. | Nhóm cài đặt thành `HeuristicAgent` (Level 2), đồng thời bổ sung thêm bước lọc bỏ các cột tạo bàn đạp cho đối phương thắng ngay ở hàng phía trên. |
| 2 | Duyệt cây Minimax / Negamax có cắt tỉa Alpha-Beta | Kho mã nguồn `KeithGalli/Connect4-Python`, luận văn của Allis (1988) | Duyệt cây đến độ sâu cố định $d$, tại nút lá dùng hàm đánh giá cộng điểm theo số lượng quân trong 69 cửa sổ 4 ô và cộng điểm thưởng cho cột trung tâm. | Nhóm cài đặt lại trên nền Bitboard 49-bit thành `AlphaBetaAgent` (Level 3), bổ sung sắp xếp nước đi ưu tiên cột giữa và chế độ duyệt sâu dần theo thời gian thực. |
| 3 | Tìm kiếm cây Monte Carlo thuần (UCT-MCTS) | Thuật toán UCT của Kocsis & Szepesvári (2006) | Xây dựng cây tìm kiếm 4 bước dựa trên công thức cân bằng UCB1/UCT; đánh giá nút lá bằng cách đi ngẫu nhiên đến cuối ván (Rollout) mà không cần hàm lượng giá. | Nhóm chuẩn hóa thành `MCTSAgent` (Level 4), có thêm bước kiểm tra nhanh nước thắng/chặn trực tiếp tại nút gốc để tránh mất lượt mô phỏng vô ích. |
| 4 | Mạng nơ-ron sâu và tìm kiếm cây có định hướng | AlphaZero (Silver et al., 2017), sách *AlphaGo Simplified* (Liu, 2025) | Dùng mạng tích chập hai đầu dự đoán xác suất 7 cột $P(s,a)$ và giá trị thế cờ $V(s)$, sau đó dùng trực tiếp hoặc đưa vào công thức chọn nhánh PUCT. | Nhóm xây dựng mạng `Connect4PolicyValueNet` (`NNAgent` - Level 5) và tích hợp vào cây tìm kiếm có bộ nhớ đệm thành `MixedMCTSAgent` (Level 6). |

Học hỏi cách đặt mốc so sánh thực nghiệm từ các khóa luận làm về AI trò chơi (chọn ra các chương trình cơ sở đại diện cho từng phương pháp rồi cho thi đấu vòng tròn đổi bên để lấy mốc chuẩn), nhóm thiết lập hai mốc đánh giá chuẩn (Benchmark Baselines) để kiểm chứng hiệu quả của mô hình học sâu kết hợp tìm kiếm cây:
- **Mốc chuẩn tìm kiếm ngẫu nhiên (`MCTS-UCT` với 500 và 1.000 mô phỏng/nước)**: Dùng để kiểm tra xem khi tích hợp mạng nơ-ron vào cây tìm kiếm ở mức chỉ 200 mô phỏng/nước, tác tử mới có vượt qua được MCTS truyền thống có số lượt mô phỏng nhiều gấp 2,5 đến 5 lần hay không.
- **Mốc chuẩn duyệt cây cổ điển (`Alpha-Beta` ở độ sâu 4 và độ sâu 5)**: Vì dữ liệu huấn luyện mạng nơ-ron của nhóm được sinh ra từ chính các ván tự đấu của `Alpha-Beta (depth = 4)`, việc lấy `Alpha-Beta` ở độ sâu 4 và 5 làm mốc chuẩn giúp trả lời câu hỏi liệu mô hình học từ thầy khi kết hợp với tìm kiếm cây PUCT có thể thắng lại chính tác tử thầy hay không.

### 1.3. Các câu hỏi nghiên cứu định lượng (RQ1 – RQ3)

Để việc đánh giá có số liệu rõ ràng thay vì chỉ nhận xét cảm tính, nhóm đặt ra ba câu hỏi nghiên cứu (Research Questions) xuyên suốt báo cáo:

- **Câu hỏi nghiên cứu 1 (RQ1 — So sánh Alpha-Beta và MCTS thuần theo ngân sách tính toán)**: Khi cấp cùng một khoảng thời gian suy nghĩ cho mỗi nước đi (`50 ms`, `100 ms` và `300 ms`), thuật toán `MCTS-UCT` thuần có thắng được `Alpha-Beta` (chạy chế độ tìm kiếm sâu dần Iterative Deepening) trên trò chơi có số nhánh nhỏ như Connect Four hay không? Nếu giữ cố định `Alpha-Beta` ở độ sâu `depth = 4`, `MCTS-UCT` cần khoảng bao nhiêu lượt mô phỏng mỗi nước để bắt kịp và vượt qua?
- **Câu hỏi nghiên cứu 2 (RQ2 — Đánh giá khả năng học bắt chước của mạng nơ-ron hai đầu)**: Mạng `Connect4PolicyValueNet` (gồm 3 khối Residual) sau khi huấn luyện có giám sát trên tập dữ liệu sạch sinh từ `Alpha-Beta (depth = 4)` sẽ đạt độ chính xác dự đoán nước đi Top-1 và Top-2 là bao nhiêu trên tập kiểm tra độc lập? Nếu chỉ dùng mạng này để chọn ngay cột có xác suất cao nhất mà không duyệt cây (`0 search`), sức mạnh của nó đứng ở đâu khi đấu với `HeuristicAgent`, `MCTSAgent` và `AlphaBetaAgent`?
- **Câu hỏi nghiên cứu 3 (RQ3 — Hiệu quả khi ghép mạng nơ-ron vào cây tìm kiếm PUCT và giải thích mô hình)**: Khi sử dụng xác suất tiên nghiệm Policy Head $P_\theta(s,a)$ và giá trị ước lượng Value Head $V_\theta(s)$ để dẫn đường cho cây tìm kiếm PUCT (`MixedMCTSAgent`), tỷ lệ thắng thay đổi như thế nào so với `MCTS-UCT` thuần ở cùng mức 200 mô phỏng? Đồng thời, bản đồ độ nhạy đạo hàm (Saliency Map) cho thấy mạng nơ-ron đã dựa vào những vùng ô cờ nào để phát hiện các nước chặn hoặc nước thắng?

Về phạm vi thực hiện, nhóm cam kết không sử dụng các bộ giải hoàn hảo (exact solvers) hay cơ sở dữ liệu khai cuộc giải sẵn trên mạng. Toàn bộ dữ liệu huấn luyện, trọng số mạng nơ-ron và kết quả hơn 4.600 ván đấu trong báo cáo đều được chạy thực tế từ mã nguồn của nhóm trên một máy tính cá nhân thông thường.

---

## CHƯƠNG 2: HẠ TẦNG KỸ THUẬT VÀ CẤU TRÚC DỮ LIỆU BITBOARD

### 2.1. Thiết kế Bitboard 49-bit và toán tử Bitwise $O(1)$

Ở giai đoạn đầu của đồ án, khi thử nghiệm lưu bàn cờ bằng mảng hai chiều `6 × 7`, nhóm nhận thấy tốc độ duyệt cây khá chậm vì mỗi lần thử một nước đi hay kiểm tra điều kiện thắng đều phải dùng vòng lặp quét qua từng hàng, từng cột. Khi chạy MCTS hàng nghìn lượt mô phỏng hoặc chạy giải đấu vài nghìn ván, thời gian chờ đợi rất lâu. Do đó, nhóm đã tìm hiểu và cài đặt cấu trúc **Bitboard 49-bit** trong tệp `src/c4/game/engine.py` dựa trên cách đánh chỉ số bit theo cột của Pascal Pons.

#### 2.1.1. Cách ánh xạ bàn cờ 7×6 vào 49 bit của số nguyên 64-bit

Thay vì dùng 42 bit sát nhau, mỗi cột trong 7 cột được gán một dải gồm **7 bit liên tiếp** (tổng cộng $7 \times 7 = 49$ bit đầu tiên của một số nguyên 64-bit). Trong mỗi cột $c \in \{0, \dots, 6\}$, 6 bit đầu tiên từ $7c$ đến $7c + 5$ tương ứng với 6 ô cờ từ hàng đáy ($r = 0$) lên hàng đỉnh ($r = 5$). Bit thứ 7 ở trên cùng của mỗi cột (tức các vị trí bit $6, 13, 20, 27, 34, 41, 48$) không dùng để chứa quân cờ mà luôn được giữ giá trị bằng `0` để làm **bit đệm ngăn cách (sentinel bit)**.

```text
Vị trí bit đệm (luôn bằng 0):     6    13    20    27    34    41    48
                                +----+----+----+----+----+----+----+
Hàng 5 (trên cùng, r = 5):      |  5 | 12 | 19 | 26 | 33 | 40 | 47 |
Hàng 4 (r = 4):                 |  4 | 11 | 18 | 25 | 32 | 39 | 46 |
Hàng 3 (r = 3):                 |  3 | 10 | 17 | 24 | 31 | 38 | 45 |
Hàng 2 (r = 2):                 |  2 |  9 | 16 | 23 | 30 | 37 | 44 |
Hàng 1 (r = 1):                 |  1 |  8 | 15 | 22 | 29 | 36 | 43 |
Hàng 0 (dưới đáy, r = 0):       |  0 |  7 | 14 | 21 | 28 | 35 | 42 |
                                +----+----+----+----+----+----+----+
Chỉ số cột (c = 0..6):           Cột0 Cột1 Cột2 Cột3 Cột4 Cột5 Cột6
```

Lý do phải chừa ra 1 bit đệm bằng `0` ở đỉnh mỗi cột là vì khi kiểm tra 4 quân liên tiếp theo chiều dọc (dịch 1 bit) hoặc đường chéo, nếu không có bit `0` ngăn cách thì bit ở đỉnh cột $c$ (ví dụ bit số 5) khi cộng thêm 1 sẽ nối liền với bit ở đáy cột $c+1$ (bit số 6 nếu xếp sát), gây ra lỗi nhận diện nhầm 4 quân thẳng hàng xuyên qua hai cột khác nhau. Khi có bit số 6 luôn bằng `0` chắn ở giữa, phép toán `AND` bit sẽ tự động ngắt chuỗi tại ranh giới cột.

Với sơ đồ trên, trạng thái bàn cờ chỉ cần lưu bởi hai biến số nguyên trong lớp `Connect4`:
- `_pos`: Lưu các bit bằng `1` tại những ô thuộc về **người chơi đang tới lượt đi**.
- `_mask`: Lưu các bit bằng `1` tại **tất cả các ô đã có quân cờ** (của cả hai bên). Bitboard của người chơi vừa đi nước trước đó có thể lấy ngay bằng phép `XOR`: `opp_pos = _pos ^ _mask`.
- **Khóa định danh trạng thái duy nhất (`key = _pos + _mask`)**: Do các quân cờ trong mỗi cột luôn lấp đầy liên tục từ bit đáy lên trên, khi cộng trực tiếp `_pos + _mask`, phép nhớ nhị phân sẽ đẩy bit cao nhất của mỗi cột lên đúng vị trí đặc trưng cho cả chiều cao cột lẫn màu quân. Nhờ vậy, mỗi trạng thái hợp lệ trên bàn cờ có một số nguyên `key` duy nhất, rất thuận tiện để làm khóa cho bảng băm (Dictionary) mà không cần tốn bộ nhớ lưu cả mảng bàn cờ.

#### 2.1.2. Toán tử thả quân và kiểm tra thắng `_has_won` trong thời gian hằng số $O(1)$

Khi người chơi thả quân vào cột `col`, vì các ô đã có quân ở cột đó tạo thành một chuỗi bit `1` liên tiếp tính từ bit đáy `1 << (col * 7)`, khi ta lấy `_mask + (1 << (col * 7))`, phép cộng nhị phân sẽ tự động nhớ (carry) qua chuỗi bit `1` đó và bật đúng bit `0` thấp nhất nằm ngay phía trên cột `col` thành `1`. Do đó, thao tác cập nhật bàn cờ trong hàm `step(col)` chỉ gồm hai phép toán bit:

```python
# Chuyển góc nhìn sang đối thủ và bật bit trống thấp nhất của cột col
self._pos ^= self._mask
self._mask |= self._mask + (1 << (col * 7))
```

Tương tự, để kiểm tra xem một bitboard `bb` có chứa 4 quân liên tiếp hay không, ta dựa vào khoảng cách chỉ số bit giữa hai ô liền kề theo 4 phương:
- Phương dọc ($\uparrow$): hai ô liền nhau cách nhau $\Delta = 1$ bit.
- Phương ngang ($\rightarrow$): hai ô liền nhau cùng hàng cách nhau đúng 1 cột, tức $\Delta = 7$ bit.
- Phương chéo phụ ($/$): sang phải 1 cột ($+7$) và xuống 1 hàng ($-1$), tức $\Delta = 6$ bit.
- Phương chéo chính ($\setminus$): sang phải 1 cột ($+7$) và lên 1 hàng ($+1$), tức $\Delta = 8$ bit.

Với mỗi bước dịch $s \in \{7, 6, 8, 1\}$, phép toán `m = bb & (bb >> s)` sẽ giữ lại các bit có 2 quân liên tiếp; sau đó phép toán `m & (m >> (2 * s))` kiểm tra tiếp xem có hai cặp 2 quân liên tiếp nối liền nhau thành chuỗi 4 quân hay không. Đoạn mã cài đặt thực tế trong hàm `_has_won` tại tệp `src/c4/game/engine.py` như sau:

```python
@staticmethod
def _has_won(bb: int) -> bool:
    # 1. Kiểm tra hàng ngang (bước dịch = 7)
    m = bb & (bb >> 7)
    if m & (m >> 14):
        return True
    # 2. Kiểm tra đường chéo phụ / (bước dịch = 6)
    m = bb & (bb >> 6)
    if m & (m >> 12):
        return True
    # 3. Kiểm tra đường chéo chính \ (bước dịch = 8)
    m = bb & (bb >> 8)
    if m & (m >> 16):
        return True
    # 4. Kiểm tra hàng dọc | (bước dịch = 1)
    m = bb & (bb >> 1)
    if m & (m >> 2):
        return True
    return False
```

Hàm trên kiểm tra toàn bộ 69 cửa sổ trên bàn cờ cùng một lúc chỉ với 8 phép dịch bit và 8 phép `AND`, độ phức tạp là $O(1)$.

### 2.2. Kiểm chuẩn tính đúng đắn cây trò chơi (Perft Validation at Depth 6)

Vì thao tác dịch bit rất dễ xảy ra lỗi khó nhìn thấy bằng mắt thường, nhóm không sử dụng ngay bản Bitboard mà viết thêm một lớp thứ hai là `ReferenceConnect4` (trong `src/c4/game/reference.py`) cài đặt thuần túy bằng mảng hai chiều `numpy.ndarray` kích thước `6 × 7` và quét vòng lặp tường minh. Sau đó, nhóm áp dụng hai phương pháp kiểm thử tự động để đối chiếu:

1. **Kiểm chuẩn số nút cây trò chơi (Perft Validation từ độ sâu 1 đến độ sâu 6)**:
   Hàm `perft(game, depth)` đệ quy đếm tổng số nút lá hợp lệ xuất phát từ bàn cờ rỗng đến độ sâu `depth`. Kết quả đếm trên cả hai engine của nhóm được đem so sánh với chuỗi số lượng nút chuẩn của Connect Four (dãy số OEIS A212693). Như thể hiện ở Bảng 2.1, số nút ở mọi độ sâu từ 1 đến 6 đều trùng khớp hoàn toàn.

**Bảng 2.1: Kết quả kiểm chuẩn Perft từ độ sâu 1 đến độ sâu 6 trên bàn cờ 7×6**

| Độ sâu (Ply) | Số nút lý thuyết (OEIS A212693) | Kết quả đếm từ `Connect4` (Bitboard 49-bit) | Kết quả đếm từ `ReferenceConnect4` (Mảng 2D) | Kết luận |
|:---:|---:|---:|---:|:---:|
| Depth 1 | 7 | 7 | 7 | Khớp 100% |
| Depth 2 | 49 | 49 | 49 | Khớp 100% |
| Depth 3 | 238 | 238 | 238 | Khớp 100% |
| Depth 4 | 1.120 | 1.120 | 1.120 | Khớp 100% |
| Depth 5 | 4.263 | 4.263 | 4.263 | Khớp 100% |
| Depth 6 | 16.422 | 16.422 | 16.422 | Khớp 100% |

2. **Kiểm thử đối chiếu chéo 10.000 ván ngẫu nhiên và bộ 57 bài test tự động**:
   Trong tệp `tests/test_crosscheck.py`, nhóm cho chạy 10.000 ván đấu ngẫu nhiên từ đầu đến cuối (tương đương hơn 210.000 lượt thả quân). Ở mỗi bước đi, chương trình kiểm tra xem danh sách cột hợp lệ `legal_actions()`, trạng thái kết thúc `is_terminal()`, người thắng `winner`, mảng bàn cờ `to_array()` và tensor mã hóa `encode()` của hai engine có giống hệt nhau hay không, sau đó gọi `undo()` lùi từng nước về bàn cờ rỗng. Toàn bộ 57 bài kiểm thử tự động trong dự án đều vượt qua 100% (chi tiết lưu tại `results/TEST_AND_EVALUATION_REPORT.md`).

---

## CHƯƠNG 3: PHƯƠNG PHÁP TRIỂN KHAI CHUỖI TÁC TỬ AI (LEVEL 1 – LEVEL 5)

Để thuận tiện cho việc tổ chức giải đấu, tất cả các tác tử trong thư mục `src/c4/agents/` đều kế thừa từ lớp cơ sở `Agent` và nhận chung một đối tượng cấu hình ngân sách `Budget(time_s, simulations, depth)`.

### 3.1. Nhóm tác tử cổ điển (Random, Heuristic, Negamax Alpha-Beta Pruning)

#### 3.1.1. Tác tử Cấp 1 — `RandomAgent` (`src/c4/agents/random_agent.py`)
`RandomAgent` đóng vai trò là mức cơ sở thấp nhất. Tại mỗi lượt, tác tử lấy danh sách các cột chưa đầy `game.legal_actions()` và dùng bộ sinh số ngẫu nhiên độc lập `random.Random(seed)` để chọn một cột với xác suất bằng nhau. Việc tách riêng đối tượng `Random(seed)` cho từng tác tử giúp đảm bảo kết quả thực nghiệm có thể chạy lại giống hệt nhau khi giữ nguyên hạt giống `seed`.

#### 3.1.2. Tác tử Cấp 2 — `HeuristicAgent` (`src/c4/agents/heuristic.py`)
`HeuristicAgent` mô phỏng cách chơi phản xạ nhanh ở mức 1 nước đi mà không duyệt cây sâu, thực hiện tuần tự 4 bước kiểm tra:
1. **Tìm nước thắng ngay (Win-in-1)**: Thử thả quân vào từng cột hợp lệ, nếu có cột tạo thành 4 quân liên tiếp thì chọn ngay cột đó.
2. **Chặn nước thắng của đối phương (Block-in-1)**: Giả sử đến lượt đối phương đi, nếu đối phương có cột thắng ngay thì lập tức thả quân vào cột đó để chặn (nếu có nhiều hơn một cột cần chặn thì ưu tiên cột gần trung tâm hơn).
3. **Lọc nước đi tự sát (Anti-blunder)**: Kiểm tra từng cột hợp lệ $a$; nếu sau khi mình thả quân vào cột $a$, ô trống ngay phía trên nó ở cùng cột $a$ lại giúp đối phương đánh vào và thắng ngay ở lượt kế tiếp thì loại cột $a$ ra khỏi danh sách cân nhắc (trừ trường hợp mọi cột hợp lệ đều bị rơi vào thế này thì mới giữ lại).
4. **Ưu tiên cột trung tâm**: Trong các cột an toàn còn lại, chọn cột đầu tiên theo thứ tự từ giữa ra biên: `(3, 2, 4, 1, 5, 0, 6)`.

#### 3.1.3. Tác tử Cấp 3 — `AlphaBetaAgent` (`src/c4/agents/alphabeta.py`)
Do Connect Four là trò chơi tổng bằng không đối xứng giữa hai người chơi, nhóm cài đặt thuật toán duyệt cây theo công thức **Negamax kết hợp cắt tỉa Alpha-Beta**:

$$V(s, d, \alpha, \beta) = \begin{cases} \text{Eval}(s) & \text{nếu } d = 0 \text{ hoặc } s \text{ là trạng thái kết thúc} \\ \max_{a \in A(s)} \left( -V(T(s, a), d - 1, -\beta, -\alpha) \right) & \text{ngược lại} \end{cases}$$

Để tăng tốc độ duyệt cây và chất lượng nước đi, nhóm áp dụng ba cải tiến thực tế:
- **Thứ tự duyệt nước đi Center-First**: Hiệu quả của cắt tỉa Alpha-Beta phụ thuộc rất lớn vào việc nhánh tốt nhất có được duyệt đầu tiên hay không. Nhóm sắp xếp danh sách cột hợp lệ theo thứ tự tĩnh `(3, 2, 4, 1, 5, 0, 6)` ở mọi nút trong cây để sớm tìm được giá trị cận dưới $\alpha$ cao, từ đó cắt bỏ nhanh các nhánh biên khi xảy ra điều kiện $\alpha \ge \beta$.
- **Kiểm tra thắng trực tiếp trước khi đệ quy**: Tại mỗi nút, trước khi gọi đệ quy xuống độ sâu $d - 1$, tác tử quét nhanh xem có cột nào thắng ngay trong 1 nước hay không. Nếu có, hàm trả về điểm tuyệt đối `WIN_SCORE + depth` (`100.000 + depth`). Việc cộng thêm `depth` giúp AI luôn chọn cách thắng trong ít nước nhất khi đang ưu thế, hoặc kéo dài số nước cầm cự lâu nhất khi biết chắc bị ép thua.
- **Hàm lượng giá tĩnh trên 69 cửa sổ 4 ô (`_evaluate`)**: Khi chạm giới hạn độ sâu $d = 0$ mà ván cờ chưa kết thúc, hàm lượng giá tính tổng điểm kiểm soát cột trung tâm (`+3` điểm cho mỗi quân của mình ở cột 3, `-3` điểm cho mỗi quân của đối phương ở cột 3) cộng với tổng điểm của toàn bộ 69 cửa sổ 4 ô đã được tiền tính sẵn mặt nạ bit:
  $$\text{Eval}(s) = 3 \cdot \left( N_{\text{my}}(\text{col } 3) - N_{\text{opp}}(\text{col } 3) \right) + \sum_{w \in \mathcal{W}_{69}} \text{score}(w)$$
  Trong mỗi cửa sổ $w$ chỉ chứa quân của một bên và các ô trống: nếu có 3 quân mình + 1 ô trống thì cộng `+50`, 2 quân mình + 2 ô trống cộng `+6`; ngược lại nếu có 3 quân đối phương + 1 ô trống (mối đe dọa trực tiếp) thì trừ `-80`, và 2 quân đối phương + 2 ô trống trừ `-8`.
- **Chế độ tìm kiếm sâu dần (Iterative Deepening)**: Khi thi đấu theo giới hạn thời gian `time_s`, tác tử chạy vòng lặp tăng dần độ sâu $d = 1, 2, \dots, d_{\max}$ và kiểm tra đồng hồ `time.perf_counter()` sau mỗi nút. Nếu hết thời gian khi đang duyệt dở ở tầng $d$, tác tử dừng ngay và trả về nước đi tốt nhất đã tính trọn vẹn ở tầng $d - 1$.

### 3.2. Nhóm tác tử Monte Carlo (MCTS-UCT 4 giai đoạn)

Tác tử Cấp 4 — `MCTSAgent` (`src/c4/agents/mcts.py`) không sử dụng hàm lượng giá 69 cửa sổ mà ước lượng xác suất thắng thông qua cây tìm kiếm bất đối xứng gồm 4 giai đoạn lặp lại trong mỗi lượt mô phỏng:
1. **Selection (Chọn nhánh)**: Xuất phát từ nút gốc, khi nút hiện tại đã mở rộng hết các nước đi hợp lệ và chưa kết thúc, tác tử đi xuống nút con $a$ có chỉ số UCT lớn nhất (Kocsis & Szepesvári, 2006):
   $$\text{UCT}(s, a) = \frac{W(s, a)}{N(s, a)} + c \sqrt{\frac{\ln N(s)}{N(s, a)}}$$
   với hệ số khám phá $c = 1,4 \approx \sqrt{2}$, $N(s, a)$ là số lần đi qua nhánh $(s, a)$ và $W(s, a)$ là tổng điểm thắng tích lũy tính theo góc nhìn của người chơi vừa thực hiện nước đi $a$.
2. **Expansion (Mở rộng)**: Khi gặp một nút chưa kết thúc vẫn còn cột hợp lệ chưa từng được thử (`untried`), tác tử lấy ngẫu nhiên một cột trong danh sách đó để tạo thêm một nút con mới trong cây.
3. **Simulation / Rollout (Mô phỏng ngẫu nhiên)**: Từ trạng thái của nút vừa mở rộng, tác tử thực hiện thả quân ngẫu nhiên liên tiếp trên bản sao Bitboard cho đến khi ván đấu kết thúc để nhận kết quả thắng (`1,0`), hòa (`0,5`) hoặc thua (`0,0`).
4. **Backpropagation (Lan truyền ngược)**: Kết quả của pha mô phỏng được truyền ngược từ nút vừa mở rộng lên tới nút gốc; tại mỗi nút trên đường đi, số lượt thăm $N$ tăng thêm 1 và tổng điểm $W$ được cộng thêm theo đúng chiều người chơi tại nút đó. Khi hoàn thành đủ số lượt mô phỏng quy định, tác tử chọn cột ở gốc có số lượt thăm $N$ cao nhất (tiêu chuẩn *Robust Child*).

### 3.3. Đề xuất Tác tử Học sâu AlphaZero-lite (Dual-Head ResNet + PUCT Search Pseudocode)

#### 3.3.1. Kiến trúc mạng hai đầu `Connect4PolicyValueNet` (`src/c4/models/net.py`)
Để mạng nơ-ron vừa có thể đứng độc lập làm tác tử Cấp 5 (`NNAgent`), vừa làm hàm dẫn đường cho cây tìm kiếm ở Cấp 6 (`MixedMCTSAgent`), nhóm thiết kế kiến trúc mạng tích chập phần dư hai đầu (Dual-Head Residual Network) nhận đầu vào là tensor nhị phân kích thước $2 \times 6 \times 7$:
- **Khối tích chập đầu vào (Stem Block)**: Gồm lớp `Conv2d(in_channels=2, out_channels=64, kernel_size=3, padding=1)` theo sau bởi chuẩn hóa lô `BatchNorm2d(64)` và hàm kích hoạt `ReLU`.
- **Thân mạng gồm 3 khối phần dư (3 Residual Blocks)**: Mỗi khối gồm hai lớp tích chập `Conv2d(64, 64, kernel_size=3, padding=1) + BatchNorm2d(64)` có đường nối tắt cộng trực tiếp đầu vào của khối trước khi qua hàm `ReLU`. Cấu trúc nối tắt này giúp mạng trích xuất tốt các mẫu hình quân cờ cả cục bộ lẫn toàn bàn cờ với tổng số tham số gọn nhẹ là **278.952 tham số** (có thể chạy suy luận nhanh trên CPU).
- **Đầu ra chính sách (Policy Head)**: Đi qua lớp giảm chiều `Conv2d(64, 2, kernel_size=1) + BatchNorm2d(2) + ReLU`, trải phẳng thành vector 84 chiều rồi qua lớp tuyến tính `Linear(84, 7)` để xuất ra 7 giá trị logit tương ứng với 7 cột. Trước khi đưa qua hàm `Softmax`, các cột đã đầy trên bàn cờ bị che mặt nạ bằng giá trị $-\infty$ để xác suất rơi vào cột bất hợp lệ luôn bằng `0`.
- **Đầu ra giá trị (Value Head)**: Đi qua lớp `Conv2d(64, 1, kernel_size=1) + BatchNorm2d(1) + ReLU`, trải phẳng thành 42 chiều, qua lớp ẩn `Linear(42, 64) + ReLU` và lớp cuối `Linear(64, 1) + Tanh` để xuất ra giá trị ước lượng thế cờ $V_\theta(s) \in [-1, +1]$ theo góc nhìn của người chơi đang tới lượt.

#### 3.3.2. Sự cải tiến khi tích hợp mạng học sâu vào cây tìm kiếm PUCT (`MixedMCTSAgent`)
Trong một số nghiên cứu tích hợp học máy vào MCTS trước đây (chẳng hạn như cách tiếp cận *Biased MCTS* trên cờ Othello/Reversi sử dụng mô hình thống kê Bradley-Terry), tri thức học máy thường được đưa vào bằng cách cộng thêm một đại lượng phụ thuộc xác suất mẫu cục bộ vào công thức UCB (*Biased Selection*) và dùng phân phối đó để lấy mẫu trong lúc chạy thử đến cuối ván (*Biased Simulation*).

Trong đồ án này, nhóm áp dụng cơ chế **PUCT (Predictor + UCT)** theo hướng của AlphaGo / AlphaZero (Silver et al., 2016, 2017) trong lớp `MixedMCTSAgent` (`src/c4/agents/mixed_mcts.py`). So với MCTS thuần và Biased MCTS truyền thống, thiết kế của nhóm có ba điểm khác biệt rõ rệt được tóm tắt ở Bảng 3.1:

**Bảng 3.1: So sánh cơ chế giữa MCTS-UCT thuần, Biased MCTS và MixedMCTSAgent (PUCT)**

| Tiêu chí | MCTS-UCT thuần (`MCTSAgent`) | Biased MCTS truyền thống (tham khảo KLTN) | `MixedMCTSAgent` (AlphaZero-lite của nhóm) |
|:---|:---|:---|:---|
| Nguồn tri thức định hướng | Không có (coi mọi nhánh chưa thử như nhau) | Bảng tra xác suất các mẫu hình cục bộ (Pattern Dictionary) | Mạng `Connect4PolicyValueNet` (3 khối ResNet, 278.952 tham số) nhìn toàn bộ bàn cờ $2 \times 6 \times 7$. |
| Công thức chọn nhánh (Selection) | Chỉ số UCT chuẩn với hệ số $c = 1,4$ | Cộng thêm thành phần xác suất mẫu vào UCB | Công thức **PUCT**: nhân trực tiếp xác suất tiên nghiệm $P_\theta(s,a)$ của Policy Head vào thành phần khám phá. |
| Cách đánh giá nút lá (Leaf Evaluation) | Chạy Rollout ngẫu nhiên đến cuối ván | Chạy *Biased Simulation* lấy mẫu theo xác suất | Hỗ trợ cả hai chế độ: dùng trực tiếp **Value Head $V_\theta(s)$** (bỏ hẳn bước Rollout) hoặc kết hợp **Policy Prior + Fast Rollout** để làm thí nghiệm đối chứng. |
| Cơ chế tăng tốc tra cứu $O(1)$ | Không có | Lưu từ điển mẫu ra file nhị phân | Dùng **Bảng băm trạng thái (`Transposition Cache`)** theo khóa Bitboard `key = _pos + _mask` để không phải gọi lại mạng CNN khi gặp lại cùng một thế cờ. |

Tại bước *Selection*, `MixedMCTSAgent` chọn nhánh con $a \in A(s)$ sao cho cực đại hóa công thức PUCT:

$$a^* = \arg\max_{a \in A(s)} \left( Q(s, a) + c_{\text{puct}} \cdot P_\theta(s, a) \cdot \frac{\sqrt{\max\left(1, \sum_{b \in A(s)} N(s, b)\right)}}{1 + N(s, a)} \right)$$

trong đó $Q(s, a) = \frac{W(s, a)}{N(s, a)} \in [-1, +1]$ là giá trị trung bình của nhánh $(s, a)$ (nếu $N(s, a) = 0$ thì $Q(s, a) = 0$), và hệ số $c_{\text{puct}} = 1,5$. Ở những lượt mô phỏng đầu tiên khi $N(s, a)$ còn nhỏ, thành phần thứ hai chiếm ưu thế và hướng cây tìm kiếm tập trung ngay vào 1–2 cột có xác suất $P_\theta(s, a)$ cao nhất do mạng nơ-ron gợi ý; khi số lượt thăm tăng lên, mẫu số $1 + N(s, a)$ lớn dần và thuật toán chuyển sang tin tưởng vào giá trị thực nghiệm $Q(s, a)$.

Mã giả chi tiết của thuật toán `PUCT_SEARCH` được trình bày dưới đây:

```text
Thuật toán 1: Tìm kiếm cây Monte Carlo có định hướng mạng nơ-ron (PUCT_SEARCH)
---------------------------------------------------------------------------------
Đầu vào : Trạng thái bàn cờ hiện tại s_root, mạng đã huấn luyện f_theta,
          số lượt mô phỏng M (hoặc giới hạn thời gian time_s), hệ số c_puct = 1.5,
          bộ nhớ đệm trạng thái Cache
Đầu ra  : Cột được chọn a* thuộc A(s_root)

1:  Nếu có cột a thuộc A(s_root) giúp thắng ngay trong 1 nước: trả về a
2:  Nếu đối phương có duy nhất 1 cột đe dọa thắng ngay a_block: trả về a_block
3:  Tạo nút gốc root = PUCTNode(state = s_root)
4:  MỞ_RỘNG_VÀ_ĐÁNH_GIÁ_LÁ(root, s_root, is_root = True)
5:  Lặp sim = 1 đến M (hoặc đến khi hết thời gian time_s):
6:      node = root
7:      s = s_root.clone()
8:      // Bước 1: Đi xuống cây theo công thức PUCT (Selection)
9:      Trong khi node đã mở rộng và s chưa kết thúc:
10:         N_parent = tổng N(node, b) với mọi nhánh con b của node
11:         Chọn nhánh con a có giá trị lớn nhất của:
                Q(node, a) + c_puct * P(node, a) * sqrt(max(1, N_parent)) / (1 + N(node, a))
12:         node = node.children[a]
13:         s.step(a)
14:     // Bước 2 & 3: Mở rộng nút mới và lượng giá nút lá (Expansion & Evaluation)
15:     Nếu s là trạng thái kết thúc:
16:         v_leaf = Kết_Quả_Trực_Tiếp(s)   // nhận giá trị trong {-1.0, 0.0, +1.0}
17:     Ngược lại:
18:         v_leaf = MỞ_RỘNG_VÀ_ĐÁNH_GIÁ_LÁ(node, s, is_root = False)
19:     // Bước 4: Lan truyền ngược giá trị lên gốc (Backpropagation)
20:     Trong khi node != None:
21:         node.visits += 1
22:         Nếu node.player_just_moved trùng với người thắng trong v_leaf:
23:             node.value_sum += |v_leaf|
24:         Ngược lại:
25:             node.value_sum -= |v_leaf|
26:         node = node.parent
27: Trả về nhánh a ở gốc có số lượt thăm visits lớn nhất (nếu bằng nhau thì xét Q và P)

Hàm phụ: MỞ_RỘNG_VÀ_ĐÁNH_GIÁ_LÁ(node, s, is_root)
---------------------------------------------------------------------------------
1:  key = s._pos + s._mask   // Lấy khóa Bitboard 49-bit duy nhất của trạng thái s
2:  Nếu key đã có trong Cache:
3:      (priors, v_net) = Cache[key]
4:  Ngược lại:
5:      (logits, v_net) = f_theta(s.encode())
6:      priors = MaskedSoftmax(logits, s.legal_actions())
7:      Cache[key] = (priors, v_net)
8:  Nếu is_root == True và có bật nhiễu khám phá Dirichlet:
9:      priors = (1 - eps) * priors.copy() + eps * Dirichlet(alpha)
10: Khởi tạo các nút con node.children[a] với xác suất P = priors[a] cho mọi a thuộc A(s)
11: Nếu use_value_head == True: trả về v_net
12: Ngược lại: trả về Fast_Bitboard_Rollout(s)
```

Một chi tiết kỹ thuật quan trọng mà nhóm đã phát hiện và xử lý trong lúc viết unit test là khi bật nhiễu khám phá Dirichlet tại nút gốc (`dirichlet_epsilon > 0`), nếu sửa trực tiếp trên mảng `priors` lấy ra từ `Cache[key]` thì vô tình làm nhiễu luôn xác suất gốc lưu trong bộ nhớ đệm. Do đó ở dòng 9 của hàm phụ, nhóm luôn tạo bản sao `priors.copy()` trước khi trộn nhiễu Dirichlet để giữ cho `Cache` luôn lưu giá trị xác suất chuẩn của mạng.

---

## CHƯƠNG 4: QUY TRÌNH QUẢN TRỊ DỮ LIỆU VÀ MINH BẠCH HÓA AI (XAI)

### 4.1. Data Pipeline: Mã hóa Tensor, Symmetry Augmentation và Game-level Splitting

Khác với một số trò chơi như cờ vua hay cờ Othello có sẵn các kho biên bản thi đấu quốc tế để tải về huấn luyện, nhóm quyết định tự xây dựng toàn bộ quy trình sinh dữ liệu từ tác tử chuyên gia `AlphaBetaAgent(depth = 4)` thông qua kịch bản `src/c4/train/gen_data.py`. Khi thiết kế quy trình này, nhóm đặc biệt chú ý tránh ba lỗi thường gặp khiến mô hình bị đánh giá ảo: (1) lưu cả các nước đi thăm dò ngẫu nhiên làm nhãn huấn luyện, (2) trộn lẫn các nước đi của cùng một ván vào cả tập Train và tập Test, và (3) để lọt trạng thái đối xứng gương của tập Train sang tập Test.

Quy trình quản trị và tiền xử lý dữ liệu của nhóm gồm 5 bước tuần tự như sau:

1. **Bước 1 — Tự đấu sinh ván cờ có pha khám phá (`2.500` ván, `seed = 42`)**:
   Để tránh việc hai tác tử `AlphaBetaAgent(depth = 4)` tất định chỉ đánh đi đánh lại một kịch bản duy nhất, ở 4 đến 6 nước đi đầu tiên của mỗi ván, chương trình chọn cột ngẫu nhiên (nhưng có kiểm tra để không đi vào nước thua ngay lập tức). Từ sau giai đoạn khai cuộc đến nước thứ 18, với xác suất $\epsilon = 0,14$, bàn cờ sẽ rẽ sang một nhánh ngẫu nhiên để mở rộng độ đa dạng của các thế cờ thu thập được; từ nước thứ 19 trở đi, hai bên đánh hoàn toàn bằng `AlphaBetaAgent(depth = 4)` ($\epsilon = 0$) cho tới khi kết thúc ván để kết quả thắng/hòa/thua cuối ván phản ánh đúng chất lượng thế cờ.
2. **Bước 2 — Gán nhãn chuyên gia sạch (Clean Expert Labels) và mã hóa Tensor $2 \times 6 \times 7$**:
   Tại mỗi trạng thái trong ván đấu, **trước khi** quyết định có tung đồng xu $\epsilon = 0,14$ để đi ngẫu nhiên hay không, chương trình luôn hỏi `AlphaBetaAgent(depth = 4)` xem nước đi tối ưu nhất tại thế cờ đó là cột nào và lưu cột đó làm nhãn chính sách `y_policy`. Nhờ vậy, dù ván cờ có rẽ nhánh để khám phá thế cờ mới, nhãn dạy cho mạng nơ-ron vẫn luôn là nước đi chuẩn của chuyên gia chứ không bị lẫn nước đi ngẫu nhiên. Mỗi trạng thái được mã hóa thành tensor nhị phân $X \in \{0, 1\}^{2 \times 6 \times 7}$ theo góc nhìn của người đang tới lượt: kênh 0 đánh dấu `1` tại các ô có quân của mình, kênh 1 đánh dấu `1` tại các ô có quân của đối phương. Nhãn giá trị `y_value` nhận giá trị $+1,0$ nếu người đang tới lượt tại trạng thái đó thắng vào cuối ván, $-1,0$ nếu thua và $0,0$ nếu hòa.
3. **Bước 3 — Phân chia tập dữ liệu theo đơn vị ván đấu (Game-level Splitting 70/15/15)**:
   Toàn bộ `2.500` ván đấu được chia nguyên ván theo tỷ lệ 70% / 15% / 15%, tương ứng với **1.750 ván cho tập Train**, **375 ván cho tập Validation** và **375 ván cho tập Test**. Việc chia theo ván giúp đảm bảo các trạng thái liên tiếp nhau trong cùng một trận đấu không bao giờ vừa nằm ở tập huấn luyện vừa nằm ở tập kiểm tra.
4. **Bước 4 — Khử trùng lặp theo khóa Bitboard và lọc chéo đối xứng gương**:
   Trong mỗi tập, các trạng thái trùng nhau (xác định bằng khóa `key = _pos + _mask`) được gộp lại thành một mẫu duy nhất: nhãn `y_policy` lấy theo cột xuất hiện nhiều nhất (biểu quyết đa số) và nhãn `y_value` lấy trung bình cộng. Tiếp theo, nhóm lập tập hợp tất cả các khóa trạng thái của tập `Train` cùng với khóa của **bản lật gương ngang** của chúng, rồi quét qua hai tập `Validation` và `Test` để xóa bỏ mọi mẫu trùng lặp (`2.917` mẫu bị lọc khỏi tập `Val` và `3.468` mẫu bị lọc khỏi tập `Test`). Bước này đảm bảo tập `Test` hoàn toàn độc lập, không có bất kỳ thế cờ nào trùng hoặc đối xứng gương với tập `Train`.
5. **Bước 5 — Tăng cường dữ liệu đối xứng lật ngang (Horizontal Flip Symmetry) trên tập Train**:
   Vì bàn cờ Connect Four có tính đối xứng trái – phải qua cột giữa ($c = 3$), một thế cờ có nước đi tốt nhất ở cột $c$ khi lật ngược theo chiều ngang sẽ có nước đi tốt nhất ở cột $6 - c$ và giữ nguyên giá trị thắng thua $z$. Nhóm áp dụng phép lật ngang này trên `37.518` trạng thái gốc của tập `Train` để nhân đôi thành **75.036 mẫu huấn luyện**, trong khi giữ nguyên **6.396 mẫu Validation** và **6.293 mẫu Test** (tổng cộng bộ dữ liệu trong thư mục `data/` gồm **87.725 mẫu sạch**).

### 4.2. Quá trình huấn luyện Joint Loss và trực quan hóa bản đồ độ nhạy Saliency Map

#### 4.2.1. Kiểm định toán học quá trình huấn luyện đa mục tiêu (Joint Loss Validation)

Mạng `Connect4PolicyValueNet` được huấn luyện trong kịch bản `src/c4/train/train_policy.py` bằng cách tối thiểu hóa đồng thời hàm mất mát kết hợp (Joint Loss) của cả hai đầu ra:

$$\mathcal{L}(\theta) = -\sum_{a=0}^{6} \tilde{\pi}_a \log P_\theta(a \mid s) + \lambda_v \left( z - V_\theta(s) \right)^2 + c \|\theta\|_2^2$$

Trong đó, thành phần thứ nhất là hàm mất mát Cross-Entropy giữa phân phối nhãn mục tiêu $\tilde{\pi}$ (đã áp dụng làm mượt nhãn *Label Smoothing* với $\alpha_{\text{ls}} = 0,05$ trên các cột hợp lệ để tránh mạng quá tự tin gây quá khớp) và xác suất dự đoán $P_\theta(a \mid s)$; thành phần thứ hai là sai số bình phương trung bình (MSE) giữa kết cục ván đấu $z \in \{-1, 0, +1\}$ và đầu ra Value Head $V_\theta(s)$ với trọng số cân bằng $\lambda_v = 0,5$; thành phần thứ ba là điều chuẩn trọng số $L_2$ (`weight_decay` $c = 10^{-3}$). Nhóm sử dụng bộ tối ưu `Adam` với tốc độ học ban đầu `lr = 0,0015`, giảm dần theo lịch `CosineAnnealingLR` trong 10 epochs với kích thước lô `batch_size = 256`.

![Hình 4.1: Diễn biến hàm mất mát và độ chính xác trên tập Train và Validation qua 10 epochs](../results/figures/nn_learning_curves.png)

Bảng 4.1 ghi lại chi tiết các chỉ số mất mát và độ chính xác qua từng epoch (trích từ tệp `checkpoints/training_history.json`).

**Bảng 4.1: Kết quả huấn luyện và kiểm định mạng `Connect4PolicyValueNet` qua 10 epochs**

| Epoch | Train Joint Loss | Val Joint Loss | Train Policy CE | Val Policy CE | Train Value MSE | Val Value MSE | Train Top-1 Acc | Val Top-1 Acc | Val Top-2 Acc |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 1,5463 | 1,3859 | 1,1585 | 0,9601 | 0,7755 | 0,8517 | 60,94% | 64,56% | 83,35% |
| 2 | 1,3283 | 1,2508 | 0,9566 | 0,8392 | 0,7435 | 0,8232 | 69,89% | 69,62% | 86,87% |
| 3 | 1,2594 | 1,1791 | 0,8999 | 0,7755 | 0,7190 | 0,8073 | 72,58% | 70,58% | 88,43% |
| 4 | 1,2102 | 1,1649 | 0,8608 | 0,7626 | 0,6989 | 0,8047 | 74,38% | 71,56% | 88,60% |
| 5 | 1,1723 | 1,1485 | 0,8331 | 0,7490 | 0,6784 | 0,7990 | 75,67% | 71,72% | 88,91% |
| **6 (Best)** | **1,1411** | **1,1336** | **0,8107** | **0,7333** | **0,6609** | **0,8005** | **76,65%** | **72,09%** | **89,13%** |
| 7 | 1,1152 | 1,1351 | 0,7936 | 0,7381 | 0,6432 | 0,7940 | 77,37% | 71,94% | 89,15% |
| 8 | 1,0937 | 1,1360 | 0,7797 | 0,7366 | 0,6281 | 0,7988 | 78,02% | 71,69% | 89,13% |
| 9 | 1,0769 | 1,1350 | 0,7690 | 0,7357 | 0,6158 | 0,7987 | 78,47% | 71,84% | 89,37% |
| 10 | 1,0694 | 1,1354 | 0,7649 | 0,7349 | 0,6091 | 0,8010 | 78,74% | 71,78% | 89,18% |

Quan sát Hình 4.1 và Bảng 4.1, cả hai đường mất mát Policy Cross-Entropy và Value MSE trên tập Validation đều giảm ổn định từ Epoch 1 đến Epoch 6 và đi ngang ở mức ~1,134 từ Epoch 6 đến Epoch 10 chứ không bị vọt ngược lên, cho thấy việc lọc sạch nhãn và thêm điều chuẩn `weight_decay` + `label_smoothing` đã kiểm soát tốt hiện tượng quá khớp (overfitting).

Khi lấy trọng số tốt nhất tại Epoch 6 (`checkpoints/policy_net_best.pt`) đem đánh giá một lần duy nhất trên **tập Test độc lập (`6.293` mẫu)**:
- **Độ chính xác dự đoán đúng nước đi của chuyên gia (`Test Top-1 Accuracy`)**: đạt **71,68%** (cao gấp khoảng 5 lần so với xác suất đoán ngẫu nhiên 1/7 $\approx$ 14,29%).
- **Độ chính xác trong 2 lựa chọn hàng đầu (`Test Top-2 Accuracy`)**: đạt **89,07%**. Con số gần 90% này rất có ý nghĩa khi ghép vào cây tìm kiếm PUCT, bởi vì nó cho thấy trong 9/10 thế cờ bất kỳ, nước đi tốt nhất của `Alpha-Beta (depth = 4)` đều nằm trong 2 nhánh đầu tiên được mạng nơ-ron ưu tiên mở rộng.
- **Sai số đầu ra giá trị (`Test Value MSE / MAE`)**: đạt `MSE = 0,7884` và `MAE = 0,6360` trên miền $[-1, +1]$; thời gian suy luận trung bình cho một trạng thái trên CPU là `1,909 ms` (`p95 = 2,475 ms`).

#### 4.2.2. Trực quan hóa quyết định của mạng bằng bản đồ độ nhạy Saliency Map (XAI)

Mạng nơ-ron tích chập thường bị xem là "hộp đen" vì khó biết mạng dựa vào ô cờ nào để chọn nước đi. Để làm rõ cơ chế bên trong của `Connect4PolicyValueNet`, nhóm cài đặt hàm `compute_saliency_map` trong tệp `src/c4/models/explain.py` theo phương pháp đạo hàm bậc nhất của Simonyan et al. (2014). Cụ thể, sau khi truyền thẳng tensor trạng thái $X \in \mathbb{R}^{2 \times 6 \times 7}$ để tìm ra cột có xác suất cao nhất $a^* = \arg\max_a z_a(X)$, chương trình tính đạo hàm ngược của logit $z_{a^*}$ theo từng phần tử đầu vào $X_{k, r, c}$ và cộng trị tuyệt đối trên hai kênh quân cờ:

$$S_{r, c} = \sum_{k \in \{0, 1\}} \left| \frac{\partial z_{a^*}(X)}{\partial X_{k, r, c}} \right|, \qquad \hat{S}_{r, c} = \frac{S_{r, c}}{\max_{r', c'} S_{r', c'} + 10^{-8}} \in [0, 1]$$

Giá trị $\hat{S}_{r, c}$ càng gần `1,00` (màu tím/đỏ đậm trên bản đồ nhiệt) chứng tỏ ô cờ $(r, c)$ đó có ảnh hưởng càng quyết định đến việc mạng chọn cột $a^*$. Hình 4.2 minh họa kết quả trích xuất trên hai thế cờ chiến thuật cụ thể.

![Hình 4.2: Bản đồ độ nhạy Saliency Map giải thích quyết định của mạng trên hai thế cờ chiến thuật](../results/figures/xai_saliency_double_threat.png)

1. **Tình huống 1 (Hàng trên của Hình 4.2 — Phát hiện và chặn sớm đòn bẫy hai đầu ở hàng đáy)**:
   - Sau 3 nước đi đầu tiên `moves = [3, 0, 4]`, Quân Đỏ (`X`) đã có 2 quân nằm cạnh nhau ở hàng đáy tại `(Hàng 1, Cột 4)` và `(Hàng 1, Cột 5)` (tính theo nhãn hiển thị từ 1 đến 7), đồng thời hai ô sát bên ở Cột 3 và Cột 6 đều đang trống.
   - Nếu đến lượt Quân Vàng (`O`) mà dùng `HeuristicAgent` (Level 2), do lúc này trên bàn cờ `X` mới chỉ có 2 quân liên tiếp chứ chưa thành chuỗi 3 quân, luật chặn thua của `HeuristicAgent` chưa kích hoạt và nó sẽ đánh vào cột giữa (Cột 4, Hàng 2). Ngay lượt sau, `X` sẽ đánh vào Cột 3 để tạo chuỗi 3 quân mở cả hai đầu tại Cột 2 và Cột 6, khiến `O` chắc chắn thua.
   - Ngược lại, mạng `Connect4PolicyValueNet` dự đoán nước đi cần đánh ngay là **Cột 3** với xác suất cao nhất `54,2%` (và phương án chặn đầu bên kia ở Cột 6 đạt `14,9%`), đồng thời Value Head đánh giá thế cờ của bên đi sau đang hơi bất lợi (`Value = -0,188`). Khi nhìn sang bản đồ nhiệt Saliency ở giữa, ô có độ nhạy cao nhất đạt mức cực đại `1,00` nằm chính xác tại ô trống `(Hàng 1, Cột 3)` và `0,62` tại `(Hàng 1, Cột 2)`, cùng với `0,43` tại quân `X` ở `(Hàng 1, Cột 4)`. Điều này cho thấy mạng đã học được mối liên hệ không gian của thế cờ đe dọa hai đầu mở ở hàng đáy.
2. **Tình huống 2 (Hàng dưới của Hình 4.2 — Nhận diện nước thắng đường chéo bị khuyết ở giữa)**:
   - Ở thế cờ trung cuộc `moves = [0, 1, 1, 2, 3, 2, 3, 3, 3, 6]`, Quân Đỏ (`X`) đã có 3 quân nằm trên đường chéo chính tại `(Hàng 1, Cột 1)`, `(Hàng 2, Cột 2)` và `(Hàng 4, Cột 4)`, chỉ còn thiếu đúng ô ở giữa là `(Hàng 3, Cột 3)`.
   - Mạng nơ-ron tập trung gần như toàn bộ xác suất **98,9% vào Cột 3** kèm ước lượng điểm thắng cao (`Value = +0,601`), và bản đồ độ nhạy cũng làm nổi bật rõ dải ô dọc theo Cột 3, Cột 4 và đường chéo chiến thắng.

---

## CHƯƠNG 5: THỰC NGHIỆM ĐỐI KHÁNG VÀ PHÂN TÍCH KẾT QUẢ

Toàn bộ các cuộc thi đấu và đo đạc trong chương này được chạy trên cùng một máy tính cá nhân sử dụng hệ điều hành Windows 11, vi xử lý 16 luồng logic, RAM 16 GB, môi trường Python 3.13 và PyTorch CPU (`torch.set_num_threads(1)` được đặt cố định trong mỗi tác tử để phép đo độ trễ đơn luồng giữa các thuật toán hoàn toàn công bằng).

### 5.1. Quy chuẩn Giải đấu Vòng tròn Round-Robin Đối xứng (200 ván/cặp, Wilson 95% CI)

Để tránh việc kết quả thắng thua bị lệch do một bên được cầm quân Đỏ đi trước nhiều hơn hoặc gặp khai cuộc thuận lợi hơn, kịch bản `scripts/run_tournament.py` áp dụng thể thức thi đấu đối xứng gương (mirror matching):
- Chương trình sinh trước một bộ gồm **100 thế cờ khai cuộc 4 nước đi (4-ply)** hợp lệ và khác nhau hoàn toàn dựa trên hạt giống cố định `seed = 42`.
- Với mỗi cặp tác tử $(A, B)$ trong tổng số $\binom{6}{2} = 15$ cặp đấu, hai bên lần lượt thi đấu trên cả 100 thế cờ khai cuộc đó. Tại mỗi thế cờ khai cuộc thứ $i$, hai tác tử bắt buộc đánh **2 ván đối xứng**: Ván 1 tác tử $A$ cầm Quân Đỏ đi trước, $B$ cầm Quân Vàng đi sau; Ván 2 đổi lại $B$ cầm Quân Đỏ đi trước, $A$ cầm Quân Vàng đi sau. Như vậy mỗi cặp đấu gồm đúng $100 \times 2 = 200$ ván, và toàn bộ giải đấu vòng tròn gồm $15 \times 200 = 3.000$ ván đấu.
- Về mặt thống kê, nhóm sử dụng điểm số chuẩn hóa $\text{Score}_A = \frac{W_A + 0,5 \cdot D}{N} \in [0, 1]$ kèm theo khoảng tin cậy **Bootstrap 95%** (lấy mẫu lại 10.000 lần) cho điểm số trung bình và khoảng tin cậy **Wilson 95%** cho tỷ lệ thắng nhị phân $W_A / N$. Thời gian suy nghĩ mỗi nước được đo bằng `time.perf_counter()` và tổng hợp qua giá trị trung bình (`Mean`) cùng phân vị thứ 95 (`p95`).

Bảng 5.1 trình bày kết quả chi tiết của cả 15 cặp đấu trong giải đấu vòng tròn 3.000 ván (dữ liệu tổng hợp từ tệp `results/tables/round_robin_default_summary.csv`). Cấu hình mặc định của các tác tử trong giải gồm: `Alpha-Beta` ở độ sâu `depth = 5`, `MCTS-UCT` chạy `1.000` mô phỏng/nước, `NNAgent` chọn nước đi có xác suất cao nhất (`temperature = 0, 0 search`) và `MixedMCTSAgent` chạy `200` mô phỏng/nước kết hợp cả Policy Head và Value Head.

**Bảng 5.1: Kết quả chi tiết 15 cặp đấu trong giải đấu Round-Robin 3.000 ván (200 ván/cặp)**

| Cặp đấu (`Agent_A` vs `Agent_B`) | Số ván | `A` Thắng | Hòa | `B` Thắng | Điểm của `A` (`A_Score`) | Khoảng tin cậy Bootstrap 95% | Tỷ lệ thắng của `A` (Wilson 95% CI) | Độ trễ `p95 A` (ms) | Độ trễ `p95 B` (ms) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|
| `random` vs `heuristic` | 200 | 1 | 0 | 199 | 0,0050 | `[0,0000; 0,0150]` | `0,5% [0,09%; 2,78%]` | 0,008 | 0,242 |
| `random` vs `alphabeta` | 200 | 0 | 0 | 200 | 0,0000 | `[0,0000; 0,0000]` | `0,0% [0,00%; 1,88%]` | 0,013 | 63,545 |
| `random` vs `mcts` | 200 | 0 | 0 | 200 | 0,0000 | `[0,0000; 0,0000]` | `0,0% [0,00%; 1,88%]` | 0,009 | 150,624 |
| `random` vs `nn` | 200 | 3 | 0 | 197 | 0,0150 | `[0,0000; 0,0350]` | `1,5% [0,51%; 4,32%]` | 0,013 | 3,571 |
| `random` vs `mixed_mcts` | 200 | 0 | 0 | 200 | 0,0000 | `[0,0000; 0,0000]` | `0,0% [0,00%; 1,88%]` | 0,015 | 754,913 |
| `heuristic` vs `alphabeta` | 200 | 25 | 17 | 158 | 0,1675 | `[0,1225; 0,2175]` | `12,5% [8,61%; 17,80%]` | 0,238 | 56,930 |
| `heuristic` vs `mcts` | 200 | 41 | 11 | 148 | 0,2325 | `[0,1775; 0,2901]` | `20,5% [15,49%; 26,63%]` | 0,265 | 151,596 |
| `heuristic` vs `nn` | 200 | 59 | 25 | 116 | 0,3575 | `[0,2950; 0,4200]` | `29,5% [23,61%; 36,16%]` | 0,241 | 3,502 |
| `heuristic` vs `mixed_mcts` | 200 | 26 | 17 | 157 | 0,1725 | `[0,1250; 0,2225]` | `13,0% [9,03%; 18,37%]` | 0,252 | 705,554 |
| `alphabeta` vs `mcts` | 200 | 135 | 4 | 61 | 0,6850 | `[0,6200; 0,7475]` | `67,5% [60,73%; 73,61%]` | 63,603 | 154,284 |
| `alphabeta` vs `nn` | 200 | 144 | 18 | 38 | 0,7650 | `[0,7100; 0,8175]` | `72,0% [65,41%; 77,76%]` | 62,754 | 3,988 |
| `alphabeta` vs `mixed_mcts` | 200 | 79 | 25 | 96 | 0,4575 | `[0,3925; 0,5225]` | `39,5% [32,98%; 46,41%]` | 60,570 | 699,058 |
| `mcts` vs `nn` | 200 | 116 | 4 | 80 | 0,5900 | `[0,5225; 0,6575]` | `58,0% [51,07%; 64,63%]` | 152,758 | 4,505 |
| `mcts` vs `mixed_mcts` | 200 | 71 | 8 | 121 | 0,3750 | `[0,3100; 0,4400]` | `35,5% [29,20%; 42,35%]` | 134,974 | 692,486 |
| `nn` vs `mixed_mcts` | 200 | 29 | 40 | 131 | 0,2450 | `[0,1950; 0,2950]` | `14,5% [10,29%; 20,05%]` | 3,754 | 693,428 |

![Hình 5.1: Ma trận điểm số đối đầu trực tiếp và bảng xếp hạng tổng hợp 6 tác tử qua 3.000 ván](../results/figures/round_robin_heatmap.png)

Từ Bảng 5.1 và Hình 5.1, có thể rút ra thứ hạng rõ ràng giữa 6 cấp độ tác tử (mỗi tác tử thi đấu tổng cộng `1.000` ván với 5 đối thủ còn lại):
1. **Hạng 1 — `MixedMCTSAgent (PUCT, 200 sims)`**: Thắng 705, hòa 90, thua 205 ván, đạt điểm tổng hợp **75,00%**. Khi đối đầu trực tiếp với `MCTSAgent (1.000 sims)`, mặc dù `MixedMCTSAgent` dùng số lượt mô phỏng ít hơn 5 lần (200 so với 1.000), nó vẫn giành chiến thắng với tỷ số `121 thắng – 8 hòa – 71 thua` (đạt điểm **62,50%**, khoảng tin cậy 95% nằm hoàn toàn trên mức 50%). Khi gặp `AlphaBetaAgent (depth = 5)`, `MixedMCTSAgent` cũng nhỉnh hơn với `96 thắng – 25 hòa – 79 thua` (đạt **54,25%**).
2. **Hạng 2 — `AlphaBetaAgent (depth = 5)`**: Thắng 716, hòa 64, thua 220 ván, đạt điểm tổng hợp **74,80%** với thời gian suy nghĩ rất nhanh (`p95` chỉ khoảng `61–63 ms/nước`).
3. **Hạng 3 — `MCTSAgent (1.000 sims)`**: Thắng 596, hòa 27, thua 377 ván, đạt điểm tổng hợp **60,95%**.
4. **Hạng 4 — `NNAgent (Policy-Value ResNet, 0 search)`**: Thắng 460, hòa 87, thua 453 ván, đạt điểm tổng hợp **50,35%**. Đáng chú ý là dù không hề duyệt cây (chỉ tốn `~2,9 ms` truyền thẳng qua mạng nơ-ron), `NNAgent` đã thắng `HeuristicAgent` với tỷ số `116 thắng – 25 hòa – 59 thua` (**64,25%** điểm) và thắng được 80/200 ván trước `MCTS-1000`.
5. **Hạng 5 — `HeuristicAgent`**: Thắng 350, hòa 70, thua 580 ván, đạt **38,50%** (thắng `RandomAgent` 199/200 ván).
6. **Hạng 6 — `RandomAgent`**: Thắng 4, thua 996 ván, đạt **0,40%**.

### 5.2. Phân tích kết quả thí nghiệm Giải đấu Tính giờ (RQ1) và Ablation Studies (A1 – A4)

#### 5.2.1. Giải đấu giới hạn thời gian suy nghĩ cho RQ1 (`round_robin_timed_summary.csv`)

Để trả lời vế đầu của câu hỏi **RQ1**, nhóm cho `AlphaBetaAgent` (bật chế độ tìm kiếm sâu dần Iterative Deepening) và `MCTSAgent` đấu đối kháng trực tiếp khi cả hai bị giới hạn cùng một quỹ thời gian trên mỗi nước đi ở ba mức: `50 ms`, `100 ms` và `300 ms` (mỗi mức đấu 100 ván đối xứng trên 50 khai cuộc chuẩn). Kết quả được trình bày ở Bảng 5.2 và Hình 5.2.

**Bảng 5.2: Kết quả đối đầu giữa Alpha-Beta (Iterative Deepening) và MCTS-UCT dưới cùng ngân sách thời gian**

| Ngân sách thời gian / nước | Số ván | `Alpha-Beta` Thắng | Hòa | `MCTS` Thắng | Điểm của `Alpha-Beta` | Khoảng tin cậy Bootstrap 95% | Độ trễ `p95 Alpha-Beta` | Độ trễ `p95 MCTS` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|
| 50 ms | 100 | 64 | 2 | 34 | **0,6500** | `[0,5550; 0,7400]` | 51,59 ms | 50,89 ms |
| 100 ms | 100 | 68 | 2 | 30 | **0,6900** | `[0,6000; 0,7750]` | 101,52 ms | 100,93 ms |
| 300 ms | 100 | 59 | 3 | 38 | **0,6050** | `[0,5100; 0,7000]` | 301,22 ms | 300,85 ms |

![Hình 5.2: So sánh tỷ lệ điểm giữa Alpha-Beta và MCTS-UCT ở các mức ngân sách thời gian 50ms, 100ms, 300ms](../results/figures/timed_crossover_rq1.png)

Kết quả cho thấy ở cả ba mức thời gian phản hồi thực tế từ `50 ms` đến `300 ms`, `AlphaBetaAgent` đều thắng nhiều hơn `MCTSAgent` có ý nghĩa thống kê (khoảng tin cậy 95% đều nằm trên ngưỡng 0,50). Nguyên nhân là trên bàn cờ Connect Four có số nhánh nhỏ ($b \le 7$) và hàm đánh giá 69 cửa sổ chạy trên Bitboard rất nhẹ, trong vòng `50–100 ms` `Alpha-Beta` đã duyệt完 trọn vẹn độ sâu 5 đến 6 ply nên phát hiện chính xác các bẫy chiến thuật ngắn hạn; trong khi đó `MCTS` thuần phải chia nhỏ lượt mô phỏng ngẫu nhiên nên ở mức thời gian thấp dễ đi sót nước phòng thủ. Tuy nhiên, khi tăng thời gian lên `300 ms`, điểm của `MCTS` đã tăng từ `0,310` lên `0,395`, thu hẹp dần khoảng cách với `Alpha-Beta`.

#### 5.2.2. Thí nghiệm Ablation A1: Đóng góp của cắt tỉa Alpha-Beta và sắp xếp nước đi Center-First

Trong thí nghiệm A1 (`results/tables/ablation_a1_results.csv`), nhóm đặt một thế cờ trung tâm cố định và đo số nút phải duyệt cũng như thời gian chạy của `AlphaBetaAgent` ở các độ sâu `4, 5, 6` khi lần lượt bật/tắt cắt tỉa Alpha-Beta (`use_alpha_beta`) và bật/tắt sắp xếp ưu tiên cột giữa (`use_move_ordering`).

**Bảng 5.3: Kết quả Ablation A1 — Số nút duyệt và thời gian chạy khi bật/tắt cắt tỉa và sắp xếp nước đi**

| Độ sâu | Cấu hình thử nghiệm | Số nút duyệt | Thời gian (ms) | Cột được chọn | Điểm Minimax | Tỷ lệ giảm số nút (%) |
|:---:|:---|---:|---:|:---:|:---:|---:|
| Depth 4 | Không cắt tỉa, không sắp xếp (Minimax thuần) | 399 | 56,74 | Cột 3 (giữa) | `0` | 0,00% |
| Depth 4 | Có cắt tỉa Alpha-Beta, không sắp xếp | 208 | 17,38 | Cột 3 (giữa) | `0` | 47,87% |
| Depth 4 | **Có cắt tỉa Alpha-Beta + Sắp xếp Center-First** | **78** | **3,82** | Cột 3 (giữa) | `0` | **80,45%** |
| Depth 5 | Không cắt tỉa, không sắp xếp (Minimax thuần) | 2.800 | 459,06 | Cột 3 (giữa) | `+8` | 0,00% |
| Depth 5 | Có cắt tỉa Alpha-Beta, không sắp xếp | 852 | 69,63 | Cột 3 (giữa) | `+8` | 69,57% |
| Depth 5 | **Có cắt tỉa Alpha-Beta + Sắp xếp Center-First** | **339** | **24,95** | Cột 3 (giữa) | `+8` | **87,89%** |
| Depth 6 | Không cắt tỉa, không sắp xếp (Minimax thuần) | 18.886 | 3.306,82 | Cột 3 (giữa) | `-2` | 0,00% |
| Depth 6 | Có cắt tỉa Alpha-Beta, không sắp xếp | 3.950 | 295,21 | Cột 3 (giữa) | `-2` | 79,09% |
| Depth 6 | **Có cắt tỉa Alpha-Beta + Sắp xếp Center-First** | **1.309** | **53,38** | Cột 3 (giữa) | `-2` | **93,07%** |

![Hình 5.3: Biểu đồ so sánh số nút duyệt trong thí nghiệm Ablation A1 ở độ sâu 4, 5 và 6](../results/figures/ablation_a1_nodes.png)

Bảng 5.3 cho thấy ở cùng một độ sâu, mọi cấu hình đều trả về đúng một giá trị điểm Minimax và cùng chọn một cột, khẳng định việc cắt tỉa không làm sai lệch nghiệm tối ưu. Ở độ sâu 6, nếu chỉ bật cắt tỉa mà duyệt các cột từ trái sang phải (`0..6`) thì số nút giảm được `79,09%`; nhưng chỉ cần đổi thứ tự xét cột từ giữa ra biên `(3, 2, 4, 1, 5, 0, 6)`, tỷ lệ giảm số nút đạt tới **93,07%** (từ `18.886` nút xuống chỉ còn `1.309` nút, giúp giảm thời gian chờ từ hơn `3,3 giây` xuống còn `53,38 ms`).

#### 5.2.3. Thí nghiệm Ablation A2: Tìm điểm giao thoa của MCTS trước Alpha-Beta cố định độ sâu 4

Để trả lời vế thứ hai của **RQ1**, nhóm giữ cố định đối thủ là `AlphaBetaAgent(depth = 4)` và tăng dần ngân sách mô phỏng của `MCTSAgent` qua 5 mốc: `100`, `500`, `1.000`, `2.000` và `5.000` mô phỏng/nước (mỗi mốc đấu 100 ván đối xứng, lưu tại `results/tables/ablation_a2_results.csv`).

**Bảng 5.4: Kết quả Ablation A2 — Tỷ lệ điểm của MCTS-UCT khi tăng số mô phỏng trước Alpha-Beta (depth = 4)**

| Số mô phỏng của MCTS (`Sims`) | Số ván | `MCTS` Thắng | Hòa | `Alpha-Beta (d=4)` Thắng | Điểm của `MCTS` | Khoảng tin cậy Bootstrap 95% | Độ trễ `p95 MCTS` (ms) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| 100 sims | 100 | 5 | 3 | 92 | 0,0650 | `[0,0250; 0,1150]` | 4,62 |
| 500 sims | 100 | 29 | 3 | 68 | 0,3050 | `[0,2200; 0,3950]` | 28,20 |
| 1.000 sims | 100 | 42 | 0 | 58 | 0,4200 | `[0,3200; 0,5200]` | 71,40 |
| **2.000 sims** | **100** | **51** | **6** | **43** | **0,5400** | **`[0,4450; 0,6350]`** | **118,43** |
| **5.000 sims** | **100** | **57** | **3** | **40** | **0,5850** | **`[0,4900; 0,6800]`** | **287,94** |

![Hình 5.4: Đường cong tăng trưởng điểm số của MCTS-UCT theo số lượng mô phỏng trước Alpha-Beta depth 4](../results/figures/ablation_a2_scaling.png)

Từ Hình 5.4, điểm số của `MCTS-UCT` tăng đều đặn khi được cấp thêm số lượt mô phỏng và vượt qua mốc cân bằng `0,50` tại khoảng **1.500 đến 2.000 mô phỏng/nước** (đạt `0,540` ở 2.000 sims và `0,585` ở 5.000 sims).

#### 5.2.4. Thí nghiệm Ablation A3: Bóc tách vai trò của Policy Prior và Value Head trong PUCT (Trả lời RQ2 và RQ3)

Nhằm kiểm tra xem sự cải thiện của `MixedMCTSAgent` đến từ đầu ra xác suất nước đi (Policy Prior) hay đầu ra ước lượng giá trị (Value Head), nhóm thiết lập 4 biến thể và cho mỗi biến thể đấu 100 ván đối xứng với hai mốc chuẩn là `MCTS-UCT (500 sims)` và tác tử thầy `Alpha-Beta (depth = 4)`:
1. `NN_Policy_Only (0 sims)`: Chỉ dùng Policy Head của mạng nơ-ron chọn ngay cột có xác suất cao nhất, không duyệt cây.
2. `MCTS_UCT_Rollout (200 sims)`: MCTS thuần dùng công thức UCT và chạy Rollout ngẫu nhiên với 200 mô phỏng.
3. `PUCT_Prior_Rollout (200 sims)`: Dùng Policy Head $P_\theta(s,a)$ dẫn đường trong công thức PUCT, nhưng tại nút lá dùng Rollout nhanh trên Bitboard.
4. `PUCT_Prior_ValueHead (200 sims)`: Dùng cả Policy Head $P_\theta(s,a)$ trong công thức PUCT lẫn Value Head $V_\theta(s)$ tại nút lá (không chạy Rollout).

**Bảng 5.5: Kết quả Ablation A3 — So sánh 4 biến thể trước hai mốc chuẩn `mcts_500` và `alphabeta_d4`**

| Biến thể thử nghiệm | Ngân sách | Đối thủ chuẩn | Thắng / Hòa / Thua | Điểm (`Score`) | Khoảng tin cậy Bootstrap 95% | Thời gian TB / nước (ms) |
|:---|:---:|:---|:---:|:---:|:---:|---:|
| `NN_Policy_Only` | 0 sims | `mcts_500` | 43 / 2 / 55 | 0,4400 | `[0,3450; 0,5350]` | 2,99 |
| `MCTS_UCT_Rollout` | 200 sims | `mcts_500` | 32 / 1 / 67 | 0,3250 | `[0,2350; 0,4200]` | 12,92 |
| **`PUCT_Prior_Rollout`** | **200 sims** | **`mcts_500`** | **68 / 3 / 29** | **0,6950** | **`[0,6050; 0,7800]`** | **151,09** |
| **`PUCT_Prior_ValueHead`** | **200 sims** | **`mcts_500`** | **67 / 3 / 30** | **0,6850** | **`[0,5950; 0,7700]`** | **447,53** |
| `NN_Policy_Only` | 0 sims | `alphabeta_d4` | 33 / 13 / 54 | 0,3950 | `[0,3050; 0,4850]` | 2,85 |
| `MCTS_UCT_Rollout` | 200 sims | `alphabeta_d4` | 13 / 3 / 84 | 0,1450 | `[0,0800; 0,2150]` | 13,30 |
| **`PUCT_Prior_Rollout`** | **200 sims** | **`alphabeta_d4`** | **56 / 13 / 31** | **0,6250** | **`[0,5350; 0,7100]`** | **151,23** |
| **`PUCT_Prior_ValueHead`** | **200 sims** | **`alphabeta_d4`** | **45 / 12 / 43** | **0,5100** | **`[0,4150; 0,6050]`** | **425,47** |

![Hình 5.5: Kết quả Ablation A3 bóc tách đóng góp của Policy Prior và Value Head ở mức 200 mô phỏng](../results/figures/ablation_a3_puct_value.png)

Từ Bảng 5.5 và Hình 5.5, nhóm rút ra hai nhận xét quan trọng:
- Thứ nhất, khi chỉ có 200 mô phỏng, `MCTS_UCT_Rollout` thuần chỉ đạt `0,325` trước `mcts_500` và `0,145` trước `alphabeta_d4` vì 200 mô phỏng chia đều cho 7 cột là quá ít để tìm ra nước đi tốt. Thậm chí chỉ dùng mạng `NN_Policy_Only` không duyệt cây (`2,99 ms/nước`) đã đạt `0,440` trước `mcts_500` và `0,395` trước `alphabeta_d4`. Khi kết hợp xác suất tiên nghiệm của Policy Head vào cây tìm kiếm 200 mô phỏng (`PUCT_Prior_Rollout` và `PUCT_Prior_ValueHead`), điểm số trước `mcts_500` tăng vọt từ `0,325` lên **0,695 và 0,685** (tăng thêm khoảng 36–37 điểm phần trăm). Đặc biệt, khi đấu với chính tác tử thầy `alphabeta_d4`, cả hai biến thể PUCT đều vượt mốc 0,50 (đạt **0,625** và **0,510**).
- Thứ hai, khi so sánh giữa hai cách đánh giá nút lá trong PUCT, biến thể `PUCT_Prior_Rollout` chạy nhanh hơn gần 3 lần (`151 ms` so với `425 ms`) và đạt điểm cao hơn trước `alphabeta_d4` (`0,625` so với `0,510`). Lý do là ở biến thể `PUCT_Prior_Rollout`, mạng CNN chỉ cần gọi tại các nút trong khi mở rộng để lấy phân phối `priors`, còn tại nút lá mới tạo thì chạy Rollout trên Bitboard rất nhẹ và kiểm tra được trực tiếp điều kiện thắng thua cuối ván; trong khi đó đầu ra `Value Head` của nhóm được huấn luyện có giám sát trên tập dữ liệu 2.500 ván (`Test Value MSE = 0,7884`) nên đôi khi ước lượng chưa thật sát ở các thế cờ chiến thuật phức tạp. Kết quả thực nghiệm này cũng rất khớp với ghi nhận trong bài báo AlphaGo gốc (Silver et al., 2016) khi kết hợp mạng Policy học có giám sát với Rollout nhanh.

#### 5.2.5. Thí nghiệm Ablation A4: Định lượng lợi thế của người đi trước trên 3.000 ván đấu

Khi tổng hợp toàn bộ 3.000 ván của giải đấu vòng tròn theo màu quân (`results/tables/ablation_a4_first_player_bias.csv`), nhóm thu được thống kê:
- **Bên cầm Quân Đỏ (Đi trước — Player 1) thắng**: `1.554 / 3.000` ván, chiếm **51,80%** (khoảng tin cậy Wilson 95%: `[50,01%; 53,58%]`).
- **Bên cầm Quân Vàng (Đi sau — Player 2) thắng**: `1.277 / 3.000` ván, chiếm **42,57%**.
- **Số ván Hòa**: `169 / 3.000` ván, chiếm **5,63%**.
- **Độ chênh lệch tỷ lệ thắng ròng ($\Delta W = W_{\text{Đỏ}} - W_{\text{Vàng}}$)**: **+9,23%** nghiêng về bên đi trước.

![Hình 5.6: Tỷ lệ thắng của người đi trước (Quân Đỏ) và người đi sau (Quân Vàng) trên từng cặp đấu](../results/figures/first_player_advantage.png)

Như minh họa trên Hình 5.6, ở những cặp đấu giữa hai tác tử mạnh tương đương nhau, lợi thế đi trước thể hiện càng rõ: chẳng hạn ở cặp `mcts` vs `mixed_mcts`, bên đi trước thắng tới 65,5% số ván trong khi bên đi sau chỉ thắng 30,5% ($\Delta W = +35,0\%$); ở cặp `alphabeta` vs `mixed_mcts`, bên đi trước thắng 55,0% so với 32,5% của bên đi sau ($\Delta W = +22,5\%$). Số liệu này phù hợp với kết quả chứng minh lý thuyết của Victor Allis (1988) rằng Connect Four là trò chơi có lợi thế thuộc về người đi trước, đồng thời cho thấy quy định bắt buộc đổi bên đối xứng trong giải đấu của nhóm là hoàn toàn cần thiết để kết quả đánh giá không bị lệch.

### 5.3. Đánh giá mối quan hệ đánh đổi: Thông lượng duyệt nút, Độ trễ suy luận và Tỷ lệ thắng

Để nhìn nhận tổng thể quá trình phát triển tăng dần qua 6 phiên bản tác tử của nhóm (từ `v1` đến `v6`), Bảng 5.6 tổng hợp số nút/mô phỏng trung bình mỗi nước, độ trễ suy luận trung bình (`Mean Latency`), độ trễ phân vị thứ 95 (`p95 Latency`) cùng thành tích thi đấu trên 1.000 ván của từng phiên bản.

**Bảng 5.6: Bảng tổng hợp tiến hóa 6 phiên bản tác tử AI và sự đánh đổi giữa độ trễ suy luận với tỷ lệ thắng**

| Phiên bản tác tử | Cơ chế suy luận chính | Số nút / mô phỏng TB mỗi nước | Độ trễ TB (`Mean ms`) | Độ trễ `p95` (`ms`) | Kết quả trên 1.000 ván (`W - D - L`) | Điểm tổng hợp (`Overall Score`) | Điểm đối đầu vs `MCTS-1000` | Điểm đối đầu vs `AlphaBeta d=5` |
|:---|:---|---:|---:|---:|:---:|:---:|:---:|:---:|
| **v1: `RandomAgent`** (Level 1) | Chọn ngẫu nhiên cột hợp lệ | 1 | 0,006 | 0,012 | `4 - 0 - 996` | 0,40% | 0,00% | 0,00% |
| **v2: `HeuristicAgent`** (Level 2) | Luật 4 tầng 1 bước + lọc tự sát | ~14 | 0,121 | 0,248 | `350 - 70 - 580` | 38,50% | 23,25% | 16,75% |
| **v3: `NNAgent`** (Level 5, `0-search`) | Truyền thẳng qua mạng ResNet 2 đầu | 1 lượt CNN | 2,910 | 3,864 | `460 - 87 - 453` | 50,35% | 41,00% | 23,50% |
| **v4: `MCTSAgent`** (Level 4, `1.000 sims`) | Cây MCTS 4 bước + Rollout ngẫu nhiên | 1.000 sims | 83,420 | 148,847 | `596 - 27 - 377` | 60,95% | *Mốc chuẩn (50%)* | 31,50% |
| **v5: `AlphaBetaAgent`** (Level 3, `depth = 5`) | Negamax + cắt tỉa $\alpha$-$\beta$ + Center-First + 69 cửa sổ | ~339 nút | 21,860 | 61,480 | `716 - 64 - 220` | 74,80% | **68,50%** | *Mốc chuẩn (50%)* |
| **v6: `MixedMCTSAgent`** (Level 6, `PUCT 200 sims`) | **Mạng ResNet 2 đầu + cây PUCT + bộ nhớ đệm $O(1)$** | **200 sims** | **348,120** | **709,088** | **`705 - 90 - 205`** | **75,00% (Hạng 1)** | **62,50%** | **54,25%** |

Từ Bảng 5.6, nhóm rút ra ba nhận xét tổng kết về sự đánh đổi giữa chi phí tính toán và hiệu quả chiến thuật:
1. **Duyệt ít mô phỏng hơn nhưng chất lượng nước đi cao hơn (`v6` so với `v4`)**: Phiên bản `MCTSAgent` thuần (`v4`) phải thực hiện `1.000` lượt mô phỏng mỗi nước nhưng chỉ đạt điểm tổng hợp `60,95%`. Trong khi đó, phiên bản `MixedMCTSAgent` (`v6`) nhờ có xác suất tiên nghiệm từ mạng `Connect4PolicyValueNet` dẫn đường chỉ cần chạy **200 lượt mô phỏng/nước** (giảm 5 lần số lượt mô phỏng) nhưng đạt điểm tổng hợp **75,00%** và thắng trực tiếp `v4` với điểm số **62,50%**. Kết quả này cho thấy tri thức học máy đã giúp cây tìm kiếm tập trung đúng vào các nhánh có ý nghĩa chiến thuật thay vì dàn trải vào các cột yếu.
2. **Vai trò bổ trợ giữa mạng nơ-ron và tìm kiếm cây (`v6` so với `v3` và `v5`)**: Khi chỉ dùng mạng nơ-ron độc lập không kèm duyệt cây (`v3`), thời gian phản hồi rất nhanh (`~2,91 ms/nước`) và thắng tốt `HeuristicAgent` (`64,25%`), nhưng vẫn dễ mắc sai lầm trước các thuật toán có duyệt cây sâu như `Alpha-Beta` vì mạng đơn lẻ khó nhìn trước được các chuỗi ép nước dài. Khi đặt mạng nơ-ron đó vào bên trong vòng lặp tìm kiếm cây PUCT 200 mô phỏng (`v6`), cây tìm kiếm giúp kiểm tra lại các tình huống chiến thuật ngắn hạn, từ đó giúp tác tử học trò vượt qua cả tác tử thầy `Alpha-Beta` ở độ sâu 4 (`62,50%`) và nhỉnh hơn cả `Alpha-Beta` ở độ sâu 5 (`54,25%`).
3. **Đánh đổi về độ trễ thực thi trên CPU**: Do mỗi lần mở rộng một nút mới chưa có trong `Transposition Cache`, `MixedMCTSAgent` phải thực hiện một lượt truyền thẳng qua mạng ResNet trên CPU (`~1,9 ms`/lần), nên độ trễ trung bình của `v6` ở mức `348 ms/nước` (hoặc `151 ms/nước` nếu dùng biến thể `PUCT_Prior_Rollout`). Mức độ trễ dưới 0,4–0,7 giây này hoàn toàn đáp ứng tốt trải nghiệm chơi tương tác của người dùng trên giao diện đồ họa Pygame và giao diện Web của nhóm; còn trong trường hợp cần phản hồi cực nhanh dưới `60 ms/nước` với tài nguyên hạn chế, `AlphaBetaAgent (depth = 5)` là lựa chọn cân bằng nhất giữa tốc độ và sức mạnh.

---

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 1. Kết luận chung
Đồ án đã hoàn thành việc xây dựng từ đầu hệ thống trò chơi Connect Four (7×6) cùng 6 cấp độ tác tử AI, bộ kiểm thử tự động 57 bài test, quy trình sinh dữ liệu sạch và huấn luyện mạng nơ-ron hai đầu, kết hợp giao diện chơi trực quan trên cả Desktop Pygame và trình duyệt Web. Thông qua hơn 4.600 ván đấu thực nghiệm có lưu đầy đủ nhật ký CSV, báo cáo đã trả lời định lượng ba câu hỏi nghiên cứu đề ra ở Chương 1:
- **Với RQ1**: Dưới cùng giới hạn thời gian suy nghĩ ngắn (`50 ms`, `100 ms`, `300 ms`), `Alpha-Beta` (tích hợp Bitboard, cắt tỉa Center-First giảm 93,07% nút và hàm lượng giá 69 cửa sổ) đạt tỷ lệ thắng cao hơn `MCTS-UCT` thuần (`Score = 0,650; 0,690; 0,605`). Khi giữ cố định `Alpha-Beta` ở độ sâu 4, `MCTS-UCT` cần khoảng **1.500 – 2.000 mô phỏng/nước** để vượt qua.
- **Với RQ2**: Mạng `Connect4PolicyValueNet` huấn luyện trên dữ liệu tách theo ván chống rò rỉ đạt **71,68% Top-1 Accuracy** và **89,07% Top-2 Accuracy** trên tập `Test` độc lập, đạt điểm đối đầu **64,25%** trước `HeuristicAgent` khi không cần tìm kiếm cây.
- **Với RQ3**: Khi kết hợp mạng nơ-ron vào công thức chọn nhánh PUCT ở mức chỉ 200 mô phỏng, `MixedMCTSAgent` tăng thêm 36–37% điểm số so với `MCTS-UCT` cùng ngân sách, thắng cả tác tử thầy `Alpha-Beta (depth = 4)` lẫn `Alpha-Beta (depth = 5)` để xếp hạng 1 toàn giải (**75,00%**), đồng thời giải thích được vùng ô cờ trọng yếu qua bản đồ độ nhạy Saliency Map.

### 2. Hạn chế và hướng phát triển tiếp theo
Bên cạnh các kết quả đạt được, đồ án của nhóm vẫn còn một số điểm có thể cải thiện thêm:
- Hiện tại dữ liệu huấn luyện mạng được sinh có giám sát từ `AlphaBetaAgent(depth = 4)` trên CPU nên đầu ra Value Head chưa thật sự chính xác ở các thế cờ phức tạp (`Test Value MSE = 0,7884`). Hướng phát triển tiếp theo là cài đặt vòng lặp tự chơi tăng cường (Self-Play Reinforcement Learning) qua nhiều thế hệ theo đúng quy trình AlphaZero, trong đó dùng chính phân phối số lượt thăm của cây PUCT làm nhãn huấn luyện lại cho mạng.
- Đối với `AlphaBetaAgent`, nhóm mới sử dụng sắp xếp nước đi tĩnh theo cột giữa; trong tương lai có thể bổ sung thêm bảng băm hoán vị (Transposition Table lưu cận trên/cận dưới) và kỹ thuật sắp xếp nước đi động (*Killer Moves* / *History Heuristic*) để duyệt sâu tới 9–11 ply trong cùng ngân sách 100 ms.
- Cuối cùng, khung mã nguồn mạng ResNet hai đầu kết hợp PUCT của đồ án được thiết kế tách biệt với luật trò chơi, do đó có thể mở rộng sang các bàn cờ có hệ số phân nhánh lớn hơn như Cờ Caro / Gomoku ($15 \times 15$) hoặc Othello ($8 \times 8$).

---

## TÀI LIỆU THAM KHẢO

1. V. L. Allis (1988), *A Knowledge-Based Approach of Connect-Four — The Game is Solved: White Wins*, Master's Thesis, Vrije Universiteit Amsterdam.
2. L. Kocsis, C. Szepesvári (2006), "Bandit Based Monte-Carlo Planning", *Proceedings of the 17th European Conference on Machine Learning (ECML)*, Springer, tr. 282–293.
3. D. Silver et al. (2016), "Mastering the game of Go with deep neural networks and tree search", *Nature*, vol. 529, no. 7587, tr. 484–489.
4. D. Silver et al. (2017), "Mastering the game of Go without human knowledge", *Nature*, vol. 550, no. 7676, tr. 354–359.
5. S. Russell, P. Norvig (2021), *Artificial Intelligence: A Modern Approach*, 4th Edition, Pearson.
6. M. Liu (2025), *AlphaGo Simplified: Rule-Based AI and Deep Learning in Everyday Games*, CRC Press.
7. K. Simonyan, A. Vedaldi, A. Zisserman (2014), "Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps", *ICLR Workshop*.
8. S. Edelkamp, P. Kissmann (2008), "Symbolic Classification of General Two-Player Games", *KI 2008: Advances in Artificial Intelligence*, Springer, tr. 185–192.
9. D. E. Knuth, R. W. Moore (1975), "An analysis of alpha-beta pruning", *Artificial Intelligence*, vol. 6, no. 4, tr. 293–326.
