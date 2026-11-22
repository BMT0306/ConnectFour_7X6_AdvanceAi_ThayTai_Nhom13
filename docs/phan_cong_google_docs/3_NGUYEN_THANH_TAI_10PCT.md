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
## PHẦN 4: HỆ THỐNG TOÀN BỘ CÁC BẢNG BIỂU SỐ LIỆU ĐỂ TÀI TẠO BẢNG & NHẬP TRÊN GOOGLE DOCS
*(Khi các bạn Trung và Tâm gõ khung sườn, Tài sẽ vào trực tiếp từng mục để Insert Table (Chèn bảng), định dạng kẻ khung và nhập các số liệu sau để lưu vết chỉnh sửa của tài khoản Tài)*:

### Bảng 2.1: Số vị trí hợp lệ Perft từ Depth 1 đến 6
| Độ sâu (Depth) | Số vị trí duyệt được (Nodes) | Trạng thái kiểm chuẩn |
|:---:|:---:|:---:|
| 1 | 7 | Khớp tuyệt đối |
| 2 | 49 | Khớp tuyệt đối |
| 3 | 294 | Khớp tuyệt đối |
| 4 | 1.946 | Khớp tuyệt đối |
| 5 | 11.758 | Khớp tuyệt đối |
| 6 | 77.294 | Khớp tuyệt đối (0 sai số) |

### Bảng 2.2: So sánh tốc độ thực thi giữa Bitboard và Mảng 2 chiều
| Thao tác kiểm tra | Mảng 2 chiều (NumPy/List) | Bitboard 49-bit | Tốc độ tăng tốc |
|:---|:---:|:---:|:---:|
| Thả quân và kiểm tra hợp lệ | ~1,85 µs | **~0,11 µs** | **16,8×** |
| Kiểm tra trạng thái thắng | ~4,20 µs | **~0,04 µs** | **105,0×** |

### Bảng 3.1: So sánh hiệu năng và độ phức tạp của 6 cấp độ AI
| Cấp độ | Tác tử AI | Thuật toán nền tảng | Độ phức tạp / Nước | Bộ nhớ RAM |
|:---:|:---|:---|:---:|:---:|
| 1 | `RandomAgent` | Chọn mẫu ngẫu nhiên đồng đều | $O(1)$ | $< 1$ MB |
| 2 | `HeuristicAgent` | Đánh giá 69 cửa sổ 4 ô | $O(b)$ | $< 2$ MB |
| 3 | `AlphaBetaAgent` | Negamax + Center-First ($d=4,5$) | $O(b^{d/2})$ | $< 5$ MB |
| 4 | `MCTSAgent` | UCT 4 bước (1.000 sims) | $O(N \cdot d)$ | $\sim 15$ MB |
| 5 | `NNAgent` | Policy-Value ResNet (0-search) | $O(C_{CNN})$ | $\sim 50$ MB |
| 6 | `MixedMCTSAgent` | PUCT + Cache + ResNet (200 sims) | $O(N \cdot (C_{CNN} + d))$ | $\sim 65$ MB |

### Bảng 4.1: Bảng kiểm tra chất lượng dữ liệu huấn luyện
| Thuộc tính tập dữ liệu | Giá trị thực tế | Ý nghĩa / Chuẩn kiểm soát |
|:---|:---:|:---|
| Tổng số mẫu trạng thái bàn cờ | **87.725** | Sinh từ 3.000 ván tự đấu |
| Chia tập Train / Val / Test | **70% / 15% / 15%** | Chia theo Ván đấu (Game-level) |
| Top-1 Accuracy trên Test set | **71,68%** | Độ chính xác dự đoán nước đi tốt nhất |
| Top-2 Accuracy trên Test set | **89,07%** | Nước đi nằm trong top 2 lựa chọn hàng đầu |
| Value MSE Loss trên Test set | **0,0641** | Độ lệch dự đoán thắng/hòa/thua |

### Bảng 5.1: Bảng xếp hạng tổng hợp Giải đấu Vòng tròn 3.000 ván (Mặc định)
| Hạng | Tác tử (Level) | Điểm số (Score) | Số ván Thắng - Hòa - Thua | Tỷ lệ thắng (Winrate) | Độ trễ p95 (ms) |
|:---:|:---|:---:|:---:|:---:|:---:|
| **1** | `MixedMCTSAgent` (L6) | **75,00%** | 689 - 122 - 189 | 68,90% | 709,2 ms |
| **2** | `AlphaBetaAgent` (L3) | **74,80%** | 711 - 74 - 215 | 71,10% | 61,5 ms |
| **3** | `MCTSAgent` (L4) | **60,95%** | 563 - 93 - 344 | 56,30% | 664,8 ms |
| **4** | `NNAgent` (L5) | **50,35%** | 460 - 87 - 453 | 46,00% | 3,8 ms |
| **5** | `HeuristicAgent` (L2) | **38,50%** | 352 - 66 - 582 | 35,20% | 0,3 ms |
| **6** | `RandomAgent` (L1) | **0,40%** | 4 - 0 - 996 | 0,40% | 0,02 ms |

### Bảng 5.6: Kết quả giải đấu 6 Cấp độ 100 ms/nước (1.500 ván)
| Hạng | Tác tử (Level) | Điểm số (Score) | Thắng - Hòa - Thua | Winrate | Thời gian TB (ms) | Tỷ lệ Timeout |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **1** | `AlphaBetaAgent` (L3) | **78,80%** | 372 - 44 - 84 | 74,40% | 73,0 ms | 68,9% |
| **2** | `MCTSAgent` (L4) | **63,00%** | 310 - 10 - 180 | 62,00% | 99,9 ms | 98,7% |
| **3** | `MixedMCTSAgent` (L6) | **61,10%** | 282 - 47 - 171 | 56,40% | 98,4 ms | 96,3% |
| **4** | `NNAgent` (L5) | **53,20%** | 239 - 54 - 207 | 47,80% | 3,8 ms | 0,0% |
| **5** | `HeuristicAgent` (L2) | **43,50%** | 204 - 27 - 269 | 40,80% | 0,3 ms | 0,0% |
| **6** | `RandomAgent` (L1) | **0,40%** | 2 - 0 - 498 | 0,40% | 0,02 ms | 0,0% |

### Bảng 5.8: Bảng xếp hạng Elo Bradley-Terry MLE toàn diện (Mặc định vs 100ms)
| Cấp độ AI | Elo Mặc định (3.000 ván) | Phân hạng Mặc định | Elo 100ms (1.500 ván) | Phân hạng 100ms | Biến động (Δ Elo) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Cấp 6: MixedMCTS** | **2114,8** | Master | **2018,7** | Candidate Master | `-96,1` |
| **Cấp 3: AlphaBeta** | **2113,1** | Master | **2125,8** | Master | `+12,7` |
| **Cấp 4: MCTS** | **2004,3** | Candidate Master | **2038,5** | Candidate Master | `+34,2` |
| **Cấp 5: NNAgent** | **1922,3** | Expert | **1929,6** | Expert | `+7,3` |
| **Cấp 2: Heuristic** | **1822,2** | Class A | **1856,2** | Class A | `+34,0` |
| **Cấp 1: Random** | **1000,0** | Novice (Base) | **1000,0** | Novice (Base) | `0,0` |
