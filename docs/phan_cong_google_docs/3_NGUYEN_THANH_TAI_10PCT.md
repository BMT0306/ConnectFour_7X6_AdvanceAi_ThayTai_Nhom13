# PHẦN GÕ GOOGLE DOCS: NGUYỄN THÀNH TÀI (TỶ LỆ ĐÓNG GÓP: 10% - THÀNH VIÊN)

> **Vai trò**: Trục Hỗ trợ Thí nghiệm, Bảng biểu & Rà soát Số liệu Báo cáo Google Docs (Chương 4–5).
> **Các phần phụ trách gõ lên Google Docs**:
> 1. **Chương 1**: Mục 1.3 (Ba câu hỏi nghiên cứu định lượng RQ1 – RQ3).
> 2. **Chương 5**: Mục 5.2.5 (Thí nghiệm Ablation A4: Định lượng lợi thế của người đi trước Đỏ vs Vàng trên 3.000 ván đấu).
> 3. **Toàn bộ Bảng biểu & Danh mục Bảng biểu**:
>    - Danh mục Bảng biểu ở phần đầu báo cáo.
>    - Trực tiếp tạo bảng và nhập liệu cho tất cả các bảng dữ liệu trong toàn bài (Bảng 2.1, 2.2, 3.1, 4.1, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8), đảm bảo số liệu trên Google Docs khớp 100% với file Excel `NHAT_KY_THI_NGHIEM.xlsx` và Google Sheets.

---
## PHẦN 1: DANH MỤC BẢNG BIỂU (ĐẦU BÁO CÁO)

### Danh mục Bảng biểu

- **Bảng 1.1: Tổng hợp khảo sát các nhóm chương trình chơi Connect Four phổ biến** ... Trang 13
- **Bảng 2.1: Kết quả kiểm chuẩn Perft từ độ sâu 1 đến độ sâu 6 trên bàn cờ 7×6** ... Trang 19
- **Bảng 3.1: So sánh cơ chế giữa MCTS-UCT thuần, Biased MCTS và MixedMCTSAgent (PUCT)** ... Trang 24
- **Bảng 4.1: Kết quả huấn luyện và kiểm định mạng Connect4PolicyValueNet qua 10 epochs** ... Trang 29
- **Bảng 5.1: Kết quả chi tiết 15 cặp đấu trong giải đấu Round-Robin 3.000 ván (200 ván/cặp)** ... Trang 34
- **Bảng 5.2: Kết quả đối đầu giữa Alpha-Beta (Iterative Deepening) và MCTS-UCT dưới cùng ngân sách thời gian** ... Trang 36
- **Bảng 5.3: Kết quả Ablation A1 — Số nút duyệt và thời gian chạy khi bật/tắt cắt tỉa và sắp xếp nước đi** ... Trang 37
- **Bảng 5.4: Kết quả Ablation A2 — Tỷ lệ điểm của MCTS-UCT khi tăng số mô phỏng trước Alpha-Beta (depth = 4)** ... Trang 39
- **Bảng 5.5: Kết quả Ablation A3 — So sánh 4 biến thể trước hai mốc chuẩn mcts_500 và alphabeta_d4** ... Trang 40
- **Bảng 5.6: Bảng xếp hạng 6 cấp độ trong giải đấu giới hạn 100 ms/nước (1.500 ván, best_or_random)** ... Trang 43
- **Bảng 5.7: Kết quả đối đầu chi tiết 15 cặp trong giải đấu 6 cấp độ giới hạn 100 ms/nước (100 ván/cặp)** ... Trang 44
- **Bảng 5.8: Đối chiếu điểm xếp hạng Bradley-Terry MLE Elo giữa Giải Mặc định (3.000 ván) và Giải 100 ms/nước (1.500 ván)** ... Trang 47
- **Bảng 5.9: Bảng tổng hợp tiến hóa 6 phiên bản tác tử AI và sự đánh đổi giữa độ trễ suy luận, tỷ lệ thắng và điểm Elo** ... Trang 48

---



---
## PHẦN 2: CHƯƠNG 1 (MỤC 1.3 — BA CÂU HỎI NGHIÊN CỨU RQ1 – RQ3)

### 1.3. Các câu hỏi nghiên cứu định lượng (RQ1 – RQ3)

Để việc đánh giá có số liệu rõ ràng thay vì chỉ nhận xét cảm tính, nhóm đặt ra ba câu hỏi nghiên cứu (Research Questions) xuyên suốt báo cáo:

- **Câu hỏi nghiên cứu 1 (RQ1 — So sánh Alpha-Beta và MCTS thuần theo ngân sách tính toán)**: Khi cấp cùng một khoảng thời gian suy nghĩ cho mỗi nước đi (`50 ms`, `100 ms` và `300 ms`), thuật toán `MCTS-UCT` thuần có thắng được `Alpha-Beta` (chạy chế độ tìm kiếm sâu dần Iterative Deepening) trên trò chơi có số nhánh nhỏ như Connect Four hay không? Nếu giữ cố định `Alpha-Beta` ở độ sâu `depth = 4`, `MCTS-UCT` cần khoảng bao nhiêu lượt mô phỏng mỗi nước để bắt kịp và vượt qua?
- **Câu hỏi nghiên cứu 2 (RQ2 — Đánh giá khả năng học bắt chước của mạng nơ-ron hai đầu)**: Mạng `Connect4PolicyValueNet` (gồm 3 khối Residual) sau khi huấn luyện có giám sát trên tập dữ liệu sạch sinh từ `Alpha-Beta (depth = 4)` sẽ đạt độ chính xác dự đoán nước đi Top-1 và Top-2 là bao nhiêu trên tập kiểm tra độc lập? Nếu chỉ dùng mạng này để chọn ngay cột có xác suất cao nhất mà không duyệt cây (`0 search`), sức mạnh của nó đứng ở đâu khi đấu với `HeuristicAgent`, `MCTSAgent` và `AlphaBetaAgent`?
- **Câu hỏi nghiên cứu 3 (RQ3 — Hiệu quả khi ghép mạng nơ-ron vào cây tìm kiếm PUCT và giải thích mô hình)**: Khi sử dụng xác suất tiên nghiệm Policy Head $P_\theta(s,a)$ và giá trị ước lượng Value Head $V_\theta(s)$ để dẫn đường cho cây tìm kiếm PUCT (`MixedMCTSAgent`), tỷ lệ thắng thay đổi như thế nào so với `MCTS-UCT` thuần ở cùng mức 200 mô phỏng? Đồng thời, bản đồ độ nhạy đạo hàm (Saliency Map) cho thấy mạng nơ-ron đã dựa vào những vùng ô cờ nào để phát hiện các nước chặn hoặc nước thắng?

Về phạm vi thực hiện, nhóm cam kết không sử dụng các bộ giải hoàn hảo (exact solvers) hay cơ sở dữ liệu khai cuộc giải sẵn trên mạng. Toàn bộ dữ liệu huấn luyện, trọng số mạng nơ-ron và kết quả hơn 6.100 ván đấu trong báo cáo đều được chạy thực tế từ mã nguồn của nhóm trên một máy tính cá nhân thông thường.

---



---
## PHẦN 3: CHƯƠNG 5 (MỤC 5.2.5 — ABLATION A4: LỢI THẾ NGƯỜI ĐI TRƯỚC)

#### 5.2.5. Thí nghiệm Ablation A4: Định lượng lợi thế của người đi trước trên 3.000 ván đấu

Khi tổng hợp toàn bộ 3.000 ván của giải đấu vòng tròn theo màu quân (`results/tables/ablation_a4_first_player_bias.csv`), nhóm thu được thống kê:
- **Bên cầm Quân Đỏ (Đi trước — Player 1) thắng**: `1.554 / 3.000` ván, chiếm **51,80%** (khoảng tin cậy Wilson 95%: `[50,01%; 53,58%]`).
- **Bên cầm Quân Vàng (Đi sau — Player 2) thắng**: `1.277 / 3.000` ván, chiếm **42,57%**.
- **Số ván Hòa**: `169 / 3.000` ván, chiếm **5,63%**.
- **Độ chênh lệch tỷ lệ thắng ròng ($\Delta W = W_{\text{Đỏ}} - W_{\text{Vàng}}$)**: **+9,23%** nghiêng về bên đi trước.

![Hình 5.6: Tỷ lệ thắng của người đi trước (Quân Đỏ) và người đi sau (Quân Vàng) trên từng cặp đấu](../results/figures/first_player_advantage.png)

Như minh họa trên Hình 5.6, ở những cặp đấu giữa hai tác tử mạnh tương đương nhau, lợi thế đi trước thể hiện càng rõ: chẳng hạn ở cặp `mcts` vs `mixed_mcts`, bên đi trước thắng tới 65,5% số ván trong khi bên đi sau chỉ thắng 30,5% ($\Delta W = +35,0\%$); ở cặp `alphabeta` vs `mixed_mcts`, bên đi trước thắng 55,0% so với 32,5% của bên đi sau ($\Delta W = +22,5\%$). Số liệu này phù hợp với kết quả chứng minh lý thuyết của Victor Allis (1988) rằng Connect Four là trò chơi có lợi thế thuộc về người đi trước, đồng thời cho thấy quy định bắt buộc đổi bên đối xứng trong giải đấu của nhóm là hoàn toàn cần thiết để kết quả đánh giá không bị lệch.



---
## PHẦN 4: HỆ THỐNG TOÀN BỘ CÁC BẢNG BIỂU SỐ LIỆU CHUẨN (TRÍCH XUẤT 100% TỪ BÁO CÁO & LOG CSV)
*(Khi các bạn Trung và Tâm gõ khung sườn, Tài vào trực tiếp từng mục để Insert Table (Chèn bảng), định dạng kẻ khung và nhập đúng từng con số dưới đây để lưu vết chỉnh sửa trên Google Docs Version History)*:

**Bảng 1.1: Tổng hợp khảo sát các nhóm chương trình chơi Connect Four phổ biến**

| STT | Nhóm tiếp cận | Nguồn tham khảo tiêu biểu | Cách thức hoạt động và đặc điểm chính | Cách nhóm kế thừa và chuẩn hóa trong đồ án |
|:---:|:---|:---|:---|:---|
| 1 | Luật ưu tiên trực tiếp (Rule-based 1-ply) | Mã nguồn minh họa của Al Sweigart (`inventwithpython`), các bot cơ sở | Không duyệt cây nhiều tầng; chỉ kiểm tra nếu có cột thắng ngay ở lượt hiện tại thì đánh, nếu đối thủ sắp thắng ở lượt kế tiếp thì chặn, kết hợp ưu tiên cột giữa. | Nhóm cài đặt thành `HeuristicAgent` (Level 2), đồng thời bổ sung thêm bước lọc bỏ các cột tạo bàn đạp cho đối phương thắng ngay ở hàng phía trên. |
| 2 | Duyệt cây Minimax / Negamax có cắt tỉa Alpha-Beta | Kho mã nguồn `KeithGalli/Connect4-Python`, luận văn của Allis (1988) | Duyệt cây đến độ sâu cố định $d$, tại nút lá dùng hàm đánh giá cộng điểm theo số lượng quân trong 69 cửa sổ 4 ô và cộng điểm thưởng cho cột trung tâm. | Nhóm cài đặt lại trên nền Bitboard 49-bit thành `AlphaBetaAgent` (Level 3), bổ sung sắp xếp nước đi ưu tiên cột giữa và chế độ duyệt sâu dần theo thời gian thực. |
| 3 | Tìm kiếm cây Monte Carlo thuần (UCT-MCTS) | Thuật toán UCT của Kocsis & Szepesvári (2006) | Xây dựng cây tìm kiếm 4 bước dựa trên công thức cân bằng UCB1/UCT; đánh giá nút lá bằng cách đi ngẫu nhiên đến cuối ván (Rollout) mà không cần hàm lượng giá. | Nhóm chuẩn hóa thành `MCTSAgent` (Level 4), có thêm bước kiểm tra nhanh nước thắng/chặn trực tiếp tại nút gốc để tránh mất lượt mô phỏng vô ích. |
| 4 | Mạng nơ-ron sâu và tìm kiếm cây có định hướng | AlphaZero (Silver et al., 2017), sách *AlphaGo Simplified* (Liu, 2025) | Dùng mạng tích chập hai đầu dự đoán xác suất 7 cột $P(s,a)$ và giá trị thế cờ $V(s)$, sau đó dùng trực tiếp hoặc đưa vào công thức chọn nhánh PUCT. | Nhóm xây dựng mạng `Connect4PolicyValueNet` (`NNAgent` - Level 5) và tích hợp vào cây tìm kiếm có bộ nhớ đệm thành `MixedMCTSAgent` (Level 6). |


**Bảng 2.1: Kết quả kiểm chuẩn Perft từ độ sâu 1 đến độ sâu 6 trên bàn cờ 7×6**

| Độ sâu (Ply) | Số nút lý thuyết (OEIS A212693) | Kết quả đếm từ `Connect4` (Bitboard 49-bit) | Kết quả đếm từ `ReferenceConnect4` (Mảng 2D) | Kết luận |
|:---:|---:|---:|---:|:---:|
| Depth 1 | 7 | 7 | 7 | Khớp 100% |
| Depth 2 | 49 | 49 | 49 | Khớp 100% |
| Depth 3 | 238 | 238 | 238 | Khớp 100% |
| Depth 4 | 1.120 | 1.120 | 1.120 | Khớp 100% |
| Depth 5 | 4.263 | 4.263 | 4.263 | Khớp 100% |
| Depth 6 | 16.422 | 16.422 | 16.422 | Khớp 100% |


**Bảng 3.1: So sánh cơ chế giữa MCTS-UCT thuần, Biased MCTS và MixedMCTSAgent (PUCT)**

| Tiêu chí | MCTS-UCT thuần (`MCTSAgent`) | Biased MCTS truyền thống (tham khảo KLTN) | `MixedMCTSAgent` (AlphaZero-lite của nhóm) |
|:---|:---|:---|:---|
| Nguồn tri thức định hướng | Không có (coi mọi nhánh chưa thử như nhau) | Bảng tra xác suất các mẫu hình cục bộ (Pattern Dictionary) | Mạng `Connect4PolicyValueNet` (3 khối ResNet, 278.952 tham số) nhìn toàn bộ bàn cờ $2 \times 6 \times 7$. |
| Công thức chọn nhánh (Selection) | Chỉ số UCT chuẩn với hệ số $c = 1,4$ | Cộng thêm thành phần xác suất mẫu vào UCB | Công thức **PUCT**: nhân trực tiếp xác suất tiên nghiệm $P_\theta(s,a)$ của Policy Head vào thành phần khám phá. |
| Cách đánh giá nút lá (Leaf Evaluation) | Chạy Rollout ngẫu nhiên đến cuối ván | Chạy *Biased Simulation* lấy mẫu theo xác suất | Hỗ trợ cả hai chế độ: dùng trực tiếp **Value Head $V_\theta(s)$** (bỏ hẳn bước Rollout) hoặc kết hợp **Policy Prior + Fast Rollout** để làm thí nghiệm đối chứng. |
| Cơ chế tăng tốc tra cứu $O(1)$ | Không có | Lưu từ điển mẫu ra file nhị phân | Dùng **Bảng băm trạng thái (`Transposition Cache`)** theo khóa Bitboard `key = _pos + _mask` để không phải gọi lại mạng CNN khi gặp lại cùng một thế cờ. |


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


**Bảng 5.2: Kết quả đối đầu giữa Alpha-Beta (Iterative Deepening) và MCTS-UCT dưới cùng ngân sách thời gian**

| Ngân sách thời gian / nước | Số ván | `Alpha-Beta` Thắng | Hòa | `MCTS` Thắng | Điểm của `Alpha-Beta` | Khoảng tin cậy Bootstrap 95% | Độ trễ `p95 Alpha-Beta` | Độ trễ `p95 MCTS` |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|
| 50 ms | 100 | 64 | 2 | 34 | **0,6500** | `[0,5550; 0,7400]` | 51,59 ms | 50,89 ms |
| 100 ms | 100 | 68 | 2 | 30 | **0,6900** | `[0,6000; 0,7750]` | 101,52 ms | 100,93 ms |
| 300 ms | 100 | 59 | 3 | 38 | **0,6050** | `[0,5100; 0,7000]` | 301,22 ms | 300,85 ms |


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


**Bảng 5.4: Kết quả Ablation A2 — Tỷ lệ điểm của MCTS-UCT khi tăng số mô phỏng trước Alpha-Beta (depth = 4)**

| Số mô phỏng của MCTS (`Sims`) | Số ván | `MCTS` Thắng | Hòa | `Alpha-Beta (d=4)` Thắng | Điểm của `MCTS` | Khoảng tin cậy Bootstrap 95% | Độ trễ `p95 MCTS` (ms) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| 100 sims | 100 | 5 | 3 | 92 | 0,0650 | `[0,0250; 0,1150]` | 4,62 |
| 500 sims | 100 | 29 | 3 | 68 | 0,3050 | `[0,2200; 0,3950]` | 28,20 |
| 1.000 sims | 100 | 42 | 0 | 58 | 0,4200 | `[0,3200; 0,5200]` | 71,40 |
| **2.000 sims** | **100** | **51** | **6** | **43** | **0,5400** | **`[0,4450; 0,6350]`** | **118,43** |
| **5.000 sims** | **100** | **57** | **3** | **40** | **0,5850** | **`[0,4900; 0,6800]`** | **287,94** |


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


**Bảng 5.6: Bảng xếp hạng 6 cấp độ trong giải đấu giới hạn 100 ms/nước (500 ván/tác tử)**

| Hạng | Tác tử | Kết quả (`W - D - L`) | Điểm tổng hợp (`Score`) | Tổng số nước đi | Số lần chạm ngưỡng giờ (`Timeouts`) | Fallback Random | Độ trễ TB (`Mean ms`) | Độ trễ `p95` (`ms`) |
|:---:|:---|:---:|:---:|---:|---:|---:|---:|---:|
| **1** | **`AlphaBetaAgent`** (ID) | **`372 - 44 - 84`** | **78,80%** | 5.745 | 3.956 (`68,9%`) | `0` | 73,04 | 101,66 |
| **2** | **`MCTSAgent`** (UCT) | `310 - 10 - 180` | **63,00%** | 5.703 | 5.627 (`98,7%`) | `0` | 99,93 | 101,03 |
| **3** | **`MixedMCTSAgent`** (PUCT) | `282 - 47 - 171` | **61,10%** | 6.162 | 5.934 (`96,3%`) | `0` | 98,41 | 103,57 |
| **4** | **`NNAgent`** (0-search) | `239 - 54 - 207` | **53,20%** | 6.169 | 1 (`0,0%`) | `0` | 3,32 | 4,62 |
| **5** | **`HeuristicAgent`** | `191 - 53 - 256` | **43,50%** | 5.736 | 0 (`0,0%`) | `0` | 0,12 | 0,26 |
| **6** | **`RandomAgent`** | `2 - 0 - 498` | **0,40%** | 2.253 | 0 (`0,0%`) | `0` | 0,01 | 0,02 |


**Bảng 5.7: Kết quả đối đầu chi tiết 15 cặp trong giải đấu 6 cấp độ giới hạn 100 ms/nước (100 ván/cặp)**

| Cặp đấu (`A` vs `B`) | Số ván | `A - D - B` | Điểm `A` (`CI 95%`) | Điểm `A` đi trước / đi sau | `A Timeouts` | `B Timeouts` | `Fallback` (`A / B`) |
|:---|:---:|:---:|:---:|:---:|---:|---:|:---:|
| `random` vs `heuristic` | 100 | `0 - 0 - 100` | `0,000 [0,000; 0,000]` | `0,00 / 0,00` | 0 / 495 | 0 / 545 | `0 / 0` |
| `random` vs `alphabeta` | 100 | `0 - 0 - 100` | `0,000 [0,000; 0,000]` | `0,00 / 0,00` | 0 / 410 | 332 / 460 | `0 / 0` |
| `random` vs `mcts` | 100 | `0 - 0 - 100` | `0,000 [0,000; 0,000]` | `0,00 / 0,00` | 0 / 406 | 456 / 456 | `0 / 0` |
| `random` vs `nn` | 100 | `1 - 0 - 99` | `0,010 [0,000; 0,030]` | `0,02 / 0,00` | 0 / 470 | 1 / 519 | `0 / 0` |
| `random` vs `mixed_mcts` | 100 | `1 - 0 - 99` | `0,010 [0,000; 0,030]` | `0,02 / 0,00` | 0 / 472 | 521 / 521 | `0 / 0` |
| `heuristic` vs `alphabeta` | 100 | `8 - 15 - 77` | `0,155 [0,095; 0,220]` | `0,19 / 0,12` | 0 / 1.161 | 810 / 1.197 | `0 / 0` |
| `heuristic` vs `mcts` | 100 | `25 - 4 - 71` | `0,270 [0,185; 0,355]` | `0,19 / 0,35` | 0 / 1.265 | 1.267 / 1.287 | `0 / 0` |
| `heuristic` vs `nn` | 100 | `32 - 19 - 49` | `0,415 [0,330; 0,500]` | `0,39 / 0,44` | 0 / 1.439 | 0 / 1.449 | `0 / 0` |
| `heuristic` vs `mixed_mcts` | 100 | `26 - 15 - 59` | `0,335 [0,255; 0,420]` | `0,31 / 0,36` | 0 / 1.326 | 1.290 / 1.346 | `0 / 0` |
| `alphabeta` vs `mcts` | 100 | `72 - 1 - 27` | `0,725 [0,635; 0,810]` | `0,74 / 0,71` | 955 / 1.347 | 1.307 / 1.324 | `0 / 0` |
| `alphabeta` vs `nn` | 100 | `64 - 16 - 20` | `0,720 [0,640; 0,795]` | `0,71 / 0,73` | 929 / 1.357 | 0 / 1.334 | `0 / 0` |
| `alphabeta` vs `mixed_mcts` | 100 | `59 - 12 - 29` | `0,650 [0,565; 0,735]` | `0,60 / 0,70` | 930 / 1.384 | 1.305 / 1.369 | `0 / 0` |
| `mcts` vs `nn` | 100 | `64 - 2 - 34` | `0,650 [0,555; 0,740]` | `0,62 / 0,68` | 1.278 / 1.299 | 0 / 1.283 | `0 / 0` |
| `mcts` vs `mixed_mcts` | 100 | `48 - 3 - 49` | `0,495 [0,400; 0,590]` | `0,48 / 0,51` | 1.319 / 1.337 | 1.318 / 1.336 | `0 / 0` |
| `nn` vs `mixed_mcts` | 100 | `37 - 17 - 46` | `0,455 [0,365; 0,545]` | `0,44 / 0,47` | 0 / 1.584 | 1.500 / 1.590 | `0 / 0` |


**Bảng 5.8: Đối chiếu điểm xếp hạng Bradley-Terry MLE Elo giữa Giải Mặc định (3.000 ván) và Giải 100 ms/nước (1.500 ván)**

| Cấp độ Tác tử | Giải Mặc định (3.000 ván) | Elo Mặc định (`Tier`) | Giải 100 ms/nước (1.500 ván) | Elo 100 ms (`Tier`) | Biến động $\Delta\text{Elo}$ |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Level 6: `MixedMCTSAgent` (PUCT)** | `75,00%` (`705-90-205`) | **2114,8** (*Grandmaster*) | `61,10%` (`282-47-171`) | **1988,1** (*Expert*) | **-126,7** |
| **Level 3: `AlphaBetaAgent`** | `74,80%` (`716-64-220`) | **2113,1** (*Grandmaster*) | `78,80%` (`372-44-84`) | **2125,8** (*Grandmaster*) | **+12,7** |
| **Level 4: `MCTSAgent` (UCT)** | `60,95%` (`596-27-377`) | **2004,3** (*Master*) | `63,00%` (`310-10-180`) | **2002,2** (*Master*) | `-2,1` |
| **Level 5: `NNAgent` (0-search)** | `50,35%` (`460-87-453`) | **1922,3** (*Expert*) | `53,20%` (`239-54-207`) | **1929,6** (*Expert*) | `+7,3` |
| **Level 2: `HeuristicAgent`** | `38,50%` (`350-70-580`) | **1822,2** (*Club*) | `43,50%` (`191-53-256`) | **1854,3** (*Club*) | `+32,1` |
| **Level 1: `RandomAgent` (Anchor)** | `0,40%` (`4-0-996`) | **1000,0** (*Novice*) | `0,40%` (`2-0-498`) | **1000,0** (*Novice*) | `0,0` |


**Bảng 5.9: Bảng tổng hợp tiến hóa 6 phiên bản tác tử AI và sự đánh đổi giữa độ trễ suy luận, tỷ lệ thắng và điểm Elo**

| Phiên bản tác tử | Cơ chế suy luận chính | Số nút / mô phỏng TB | Độ trễ TB / `p95` (`ms`) | Điểm Mặc định (`1.000` ván) | Elo Mặc định | Elo `100 ms` ($\Delta$ Elo) | Điểm đối đầu vs `MCTS-1000` | Điểm đối đầu vs `AlphaBeta d=5` |
|:---|:---|---:|---:|:---:|:---:|:---:|:---:|:---:|
| **v1: `RandomAgent`** (L1) | Chọn ngẫu nhiên cột hợp lệ | 1 | `0,006 / 0,012` | `0,40%` | `1000,0` | `1000,0` (`0,0`) | 0,00% | 0,00% |
| **v2: `HeuristicAgent`** (L2) | Luật 4 tầng 1 bước + lọc tự sát | ~14 | `0,121 / 0,248` | `38,50%` | `1822,2` | `1854,3` (`+32,1`) | 23,25% | 16,75% |
| **v3: `NNAgent`** (L5, `0-search`) | Truyền thẳng mạng ResNet 2 đầu | 1 CNN | `2,910 / 3,864` | `50,35%` | `1922,3` | `1929,6` (`+7,3`) | 41,00% | 23,50% |
| **v4: `MCTSAgent`** (L4, `1.000`) | Cây MCTS 4 bước + Rollout | 1.000 | `83,42 / 148,85` | `60,95%` | `2004,3` | `2002,2` (`-2,1`) | *Mốc chuẩn* | 31,50% |
| **v5: `AlphaBetaAgent`** (L3, `d=5`) | Negamax + $\alpha$-$\beta$ + Center-First | ~339 nút | `21,86 / 61,48` | `74,80%` | `2113,1` | **`2125,8` (`+12,7`)** | **68,50%** | *Mốc chuẩn* |
| **v6: `MixedMCTSAgent`** (L6, `200`) | **ResNet 2 đầu + PUCT + Cache $O(1)$** | **200** | **`348,1 / 709,1`** | **`75,00%`** | **`2114,8`** | `1988,1` (`-126,7`) | **62,50%** | **54,25%** |
