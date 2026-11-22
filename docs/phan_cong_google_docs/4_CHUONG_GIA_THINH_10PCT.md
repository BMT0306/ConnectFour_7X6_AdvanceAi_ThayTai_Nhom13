# PHẦN GÕ GOOGLE DOCS: CHƯƠNG GIA THỊNH (TỶ LỆ ĐÓNG GÓP: 10% - THÀNH VIÊN)

> **Vai trò**: Trục Văn phong, Khảo sát Học thuật, Báo cáo Google Docs (Chương 1–3) & Danh mục Tham khảo.
> **Các phần phụ trách gõ lên Google Docs**:
> 1. **Phần Đầu**: Danh mục các cụm từ viết tắt & Danh mục Hình ảnh.
> 2. **Chương 1**:
>    - Mục 1.1: Bối cảnh đề tài và hình thức hóa toán học không gian trạng thái $(S, A, T, R)$.
>    - Mục 1.2: Khảo sát thuật toán/mã nguồn sẵn có và đặt mốc đánh giá chuẩn (Benchmark Baseline).
> 3. **Phần Cuối**: Toàn bộ Danh mục Tài liệu tham khảo chuẩn học thuật IEEE/APA.
> 4. **Rà soát Thể thức**: Trực tiếp đọc soát lỗi chính tả, căn lề 2 bên (Justify), chuẩn hóa cỡ chữ/font (Times New Roman 13pt), định dạng Heading 1/2/3 và kiểm tra trích dẫn tài liệu tham khảo trong toàn bộ tài liệu Google Docs.

---
## PHẦN 1: DANH MỤC CỤM TỪ VIẾT TẮT & DANH MỤC HÌNH ẢNH

## DANH MỤC CÁC CỤM TỪ VIẾT TẮT

| Từ viết tắt | Tiếng Anh đầy đủ | Giải thích tiếng Việt |
|---|---|---|
| **AI** | Artificial Intelligence | Trí tuệ nhân tạo |
| **CI** | Confidence Interval | Khoảng tin cậy thống kê (Bootstrap 95%, Wilson 95%) |
| **CNN** | Convolutional Neural Network | Mạng nơ-ron tích chập |
| **FIDE** | Fédération Internationale des Échecs | Hệ thống cập nhật Elo Logistic chuẩn quốc tế ($K = 32$) |
| **GUI** | Graphical User Interface | Giao diện đồ họa người dùng (Pygame 60 FPS) |
| **ID** | Iterative Deepening | Tìm kiếm sâu dần theo giới hạn thời gian |
| **MAE / MSE** | Mean Absolute / Squared Error | Sai số tuyệt đối / bình phương trung bình |
| **MCTS** | Monte Carlo Tree Search | Tìm kiếm cây Monte Carlo |
| **MLE** | Maximum Likelihood Estimation | Ước lượng Hợp lý Cực đại (thuật toán Bradley-Terry MM) |
| **NN** | Neural Network | Mạng nơ-ron học sâu (`Connect4PolicyValueNet`) |
| **PUCT** | Predictor + Upper Confidence Bounds applied to Trees | Công thức chọn nhánh có dẫn đường xác suất tiên nghiệm |
| **RQ** | Research Question | Câu hỏi nghiên cứu định lượng |
| **UCT** | Upper Confidence Bounds applied to Trees | Công thức cân bằng khám phá – khai thác trong MCTS thuần |
| **XAI** | Explainable Artificial Intelligence | Trí tuệ nhân tạo có khả năng giải thích (Saliency Map) |

---



### Danh mục Hình ảnh

- **Hình 2.1: Sơ đồ kiến trúc ánh xạ Bitboard 49-bit với bit đệm Sentinel bảo vệ ranh giới cột** ... Trang 17
- **Hình 3.1: Sơ đồ kiến trúc mạng tích chập hai đầu Connect4PolicyValueNet (3 khối ResNet)** ... Trang 23
- **Hình 4.1: Diễn biến hàm mất mát và độ chính xác trên tập Train và Validation qua 10 epochs** ... Trang 29
- **Hình 4.2: Bản đồ độ nhạy Saliency Map giải thích quyết định của mạng trên hai thế cờ chiến thuật** ... Trang 31
- **Hình 5.1: Ma trận điểm số đối đầu trực tiếp và bảng xếp hạng tổng hợp 6 tác tử qua 3.000 ván** ... Trang 35
- **Hình 5.2: So sánh tỷ lệ điểm giữa Alpha-Beta và MCTS-UCT ở các mức ngân sách thời gian 50ms, 100ms, 300ms** ... Trang 37
- **Hình 5.3: Biểu đồ so sánh số nút duyệt trong thí nghiệm Ablation A1 ở độ sâu 4, 5 và 6** ... Trang 38
- **Hình 5.4: Đường cong tăng trưởng điểm số của MCTS-UCT theo số lượng mô phỏng trước Alpha-Beta depth 4** ... Trang 39
- **Hình 5.5: Kết quả Ablation A3 bóc tách đóng góp của Policy Prior và Value Head ở mức 200 mô phỏng** ... Trang 41
- **Hình 5.6: Tỷ lệ thắng của người đi trước (Quân Đỏ) và người đi sau (Quân Vàng) trên từng cặp đấu** ... Trang 42
- **Hình 5.7: Giải đấu vòng tròn 6 cấp độ giới hạn 100 ms/nước (1.500 ván) và phân tích tỷ lệ timeout** ... Trang 45
- **Hình 5.8: So sánh điểm xếp hạng Bradley-Terry MLE Elo và biến động Δ Elo giữa giải Mặc định và 100 ms/nước** ... Trang 47
- **Hình 5.9: Giao diện Web App (localhost:5000) chạy thực tế chế độ Người vs Máy gặp Mixed-MCTS (200 sims, Cache 9)** ... Trang 51
- **Hình 5.10: Giao diện Desktop Pygame 60 FPS chạy thực tế chế độ Người vs Máy gặp Cấp 6 Mixed-MCTS (2114,8 Elo)** ... Trang 52
- **Hình 5.11: Chế độ Solo Máy vs Máy 2-Slot trên Pygame giữa Alpha-Beta và Mixed-MCTS kèm cập nhật Elo thời gian thực** ... Trang 53



---
## PHẦN 2: CHƯƠNG 1 (MỤC 1.1 VÀ MỤC 1.2 — BỐI CẢNH, TOÁN HỌC & KHẢO SÁT BASELINE)

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



---
## PHẦN 3: DANH MỤC TÀI LIỆU THAM KHẢO CHUẨN HỌC THUẬT

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
10. D. R. Hunter (2004), "MM algorithms for generalized Bradley-Terry models", *The Annals of Statistics*, vol. 32, no. 1, tr. 384–406.
11. A. E. Elo (1978), *The Rating of Chessplayers, Past and Present*, Arco Publishing, New York.
