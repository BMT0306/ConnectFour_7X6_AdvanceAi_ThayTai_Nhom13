# THIẾT KẾ NỘI DUNG POSTER KHOA HỌC KHỔ A0
## ĐỀ TÀI: XÂY DỰNG VÀ ĐÁNH GIÁ GAME AI ĐA CẤP ĐỘ (CONNECT FOUR 7×6)
**Trường Đại học Sài Gòn — Khoa Công Nghệ Thông Tin**  
**Học phần: Trí tuệ nhân tạo nâng cao — GVHD: Thầy Đỗ Như Tài**  
**Nhóm 13**: Bùi Minh Trung (`3124720074` - NT), Trần Lê Minh Tâm (`3124720064`), Nguyễn Thành Tài (`3124720062`), Chương Gia Thịnh (`3124720067`)

---

### [PANEL 1] ĐẶT VẤN ĐỀ & CÂU HỎI NGHIÊN CỨU
- **Bài toán Connect Four (7×6)**: Trò chơi đối kháng tổng bằng không, thông tin hoàn hảo, khoảng $4,5 \times 10^{12}$ trạng thái hợp lệ và 69 đường thắng 4 ô (24 ngang, 21 dọc, 24 chéo).
- **Mục tiêu khoa học**: Đặt các phương pháp AI kinh điển (Luật ưu tiên, Minimax Alpha-Beta, MCTS-UCT) và AI học sâu hiện đại (Policy-Value ResNet, PUCT *AlphaGo-/AlphaZero-inspired*) lên cùng một bàn cân thực nghiệm công bằng, kiểm soát chặt thiên lệch đi trước và rò rỉ dữ liệu.
- **Ba câu hỏi nghiên cứu (RQ)**:
  1. **RQ1**: Dưới cùng ngân sách thời gian (`50ms`, `100ms`, `300ms`/nước), MCTS thuần có vượt qua Alpha-Beta không, và điểm giao thoa nằm ở đâu?
  2. **RQ2**: Mạng `Connect4PolicyValueNet` học có giám sát từ nhãn sạch của `Alpha-Beta (d=4)` mạnh đến mức nào khi suy luận trực tiếp (`0 search`)?
  3. **RQ3**: Kết hợp Policy Prior $P(s,a)$ và Value Head $V(s)$ vào PUCT (`MixedMCTSAgent`) giúp vượt qua MCTS-UCT thuần và chính tác tử thầy ra sao?

---

### [PANEL 2] KIẾN TRÚC LÕI BITBOARD 49-BIT & KIỂM THỬ 100% PASS
- **Engine Bitboard 49-bit (`Connect4`)**:
  + Mã hóa bàn cờ bằng hai số nguyên 64-bit (`_pos`, `_mask`), mỗi cột 7 bit (6 ô quân + 1 bit đệm chống tràn cột).
  + Kiểm tra 4 quân liên tiếp bằng phép dịch bit song song $O(1)$, khóa trạng thái duy nhất `pos + mask`.
- **Kiểm định chất lượng phần mềm (`57/57` Unit Tests Pass — `100%`)**:
  + Đối chiếu chéo `10.000` ván ngẫu nhiên với `ReferenceConnect4` (mảng 2D): sai lệch `0%`.
  + Kiểm định Perft ply 1–5 khớp tuyệt đối lý thuyết (`7; 49; 238; 1.120; 4.263`) + `33` thế cờ chiến thuật thủ công (`positions.csv`).

---

### [PANEL 3] HỆ PHÂN CẤP 6 TÁC TỬ & QUY TRÌNH HỌC SÂU CHỐNG RÒ RỈ
| Cấp độ | Tác tử | Cơ chế cốt lõi & Tối ưu kỹ thuật | Độ trễ p95 |
|:---:|:---|:---|:---:|
| **Cấp 1** | `RandomAgent` | Chọn đều ngẫu nhiên hợp lệ theo seed cố định | `0,01 ms` |
| **Cấp 2** | `HeuristicAgent` | 4 tầng luật: Thắng ngay → Chặn thua → Lọc nước tự sát → Ưu tiên cột giữa | `0,25 ms` |
| **Cấp 3** | `AlphaBetaAgent` | Negamax + $\alpha$-$\beta$ pruning + Center-First + Iterative Deepening + 69 cửa sổ | `62,8 ms` (d=5) |
| **Cấp 4** | `MCTSAgent` | Cây UCT đa tầng ($c=1,4$), chọn nhanh thắng/chặn tại gốc, rollout bitboard | `152,8 ms` (1000) |
| **Cấp 5** | `NNAgent` | **Policy-Value ResNet** (3 khối Residual, 64 kênh, 278.952 tham số), Masked Softmax | `3,75 ms` |
| **Mở rộng** | `MixedMCTSAgent` | Tìm kiếm cây **PUCT** ($c_{\text{puct}}=1,5$) dẫn đường bởi ResNet + Transposition Cache | `699,1 ms` (200) |

- **Huấn luyện ResNet chuẩn ML (`data/dataset_summary.json`)**: `2.500` ván chuyên gia tách theo ván **70/15/15**, lọc chéo cả ảnh gương ngang (`0%` overlap), điều chuẩn `label_smoothing=0,05`, `weight_decay=1e-3` → Tập **Test độc lập (`6.293` mẫu)** đạt **71,68% Top-1 Acc** & **89,07% Top-2 Acc**.

---

### [PANEL 4] KẾT QUẢ GIẢI ĐẤU ROUND-ROBIN 3.000 VÁN & CHẾ ĐỘ TÍNH GIỜ (RQ1)
*(Chèn biểu đồ `results/figures/round_robin_heatmap.png` và `results/figures/timed_crossover_rq1.png`)*
- **Bảng xếp hạng toàn giải Round-Robin (15 cặp × 200 ván = 3.000 ván, đổi bên đối xứng)**:
  1. **`Mixed-MCTS (200 sims)`**: **75,00%** (`705W–90D–205L`) — thắng `MCTS-1000` **62,50%** và vượt `Alpha-Beta d=5` **54,25%**!
  2. **`Alpha-Beta (depth 5)`**: **74,80%** (`716W–64D–220L`) — thắng `MCTS-1000` **68,50%** và thắng `NN` **76,50%**.
  3. **`MCTS-UCT (1.000 sims)`**: **60,95%** (`596W–27D–377L`) — thắng `Heuristic` **76,75%** và thắng `NN` **59,00%**.
  4. **`Policy-Value NN (0 search)`**: **50,35%** (`460W–87D–453L`) — thắng áp đảo `Heuristic` **64,25%** mà không cần tìm kiếm cây!
  5. **`Heuristic`**: **38,50%** (`350W–70D–580L`) — thắng `Random` **99,50%**.
  6. **`Random`**: **0,40%** (`4W–0D–996L`).
- **Giải đáp RQ1 (Chế độ A — Cùng thời gian suy nghĩ)**: Ở cả 3 mức `50ms`, `100ms`, `300ms/nước` (`100` ván/mức), `Alpha-Beta` đạt Score **0,650 – 0,690 – 0,605** trước `MCTS-UCT` nhờ nhánh tìm kiếm hẹp ($b \le 7$) và cắt tỉa sâu; khi giữ cố định `Alpha-Beta d=4` (Ablation A2), `MCTS` vượt lên tại mốc **2.000 simulations** (`Score = 0,540`).

---

### [PANEL 5] NGHIÊN CỨU PHÂN RÃ (ABLATION A1–A4) & EXPLAINABLE AI
*(Chèn biểu đồ `results/figures/ablation_a1_nodes.png`, `results/figures/ablation_a3_puct_value.png`, `results/figures/xai_saliency_double_threat.png`)*
- **Ablation A1**: Cắt tỉa $\alpha$-$\beta$ + Center-First tiết kiệm **80,45% → 87,89% → 93,07%** số nút duyệt ở độ sâu `4 → 5 → 6` (`18.886` xuống còn `1.309` nút).
- **Ablation A3 (RQ2 & RQ3)**: Ở cùng ngân sách `200` mô phỏng khi đấu `MCTS-500`, bổ sung Policy Prior nâng điểm từ **0,325** (`MCTS-UCT`) lên **0,695** (`PUCT+Rollout`) và **0,685** (`PUCT+ValueHead`), đồng thời đánh bại chính tác tử thầy `Alpha-Beta d=4` (**0,625**).
- **Ablation A4 (First-Player Bias)**: Trên `3.000` ván, quân Đỏ (đi trước) thắng **51,80%** so với quân Vàng **42,57%** ($\Delta = +9,23\%$).
- **Explainable AI (Gradient Saliency)**: Bản đồ nhiệt $|\partial z_{a^*} / \partial X|$ chứng minh mạng ResNet tự học được khái niệm phòng thủ đòn kép sớm và nhận diện mắt xích thắng đường chéo (`P = 98,9%`).

---

### [PANEL 6] KẾT LUẬN, ĐÓNG GÓP & TÁI LẬP MÃ NGUỒN MỞ
1. **Đóng góp kỹ thuật**: Xây dựng trọn vẹn hệ sinh thái Connect Four AI từ Bitboard 49-bit, 6 cấp tác tử, XAI Saliency, GUI Pygame & Web FastAPI/Docker đến bộ khung giải đấu thống kê chuẩn khoa học.
2. **Cam kết trung thực học thuật**: Không dùng solver ngoài; mọi bảng biểu xuất tự động từ hơn **4.600 ván đấu thực tế** lưu log CSV và kiểm chứng bằng `57` bài test tự động.
3. **Truy cập Repository & Demo**: `https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13` (hỗ trợ chạy lại 1 lệnh qua YAML + Seed cố định).
