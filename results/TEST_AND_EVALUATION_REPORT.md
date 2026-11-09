# BÁO CÁO KẾT QUẢ KIỂM THỬ TỰ ĐỘNG & ĐÁNH GIÁ THỰC NGHIỆM TOÀN DIỆN
**Dự án**: Xây dựng và Đánh giá Game AI Đa Cấp Độ — Connect Four (7×6)  
**Nhóm thực hiện**: Nhóm 13 (Nhóm trưởng: Bùi Minh Trung — MSSV `3124720074`)  
**Thời điểm ghi nhận**: `2026-11-08T20:58:51` | **Nền tảng**: `Windows-11-10.0.26300-SP0` | **Python**: `3.13.2`

---

## 1. Tổng hợp Kết quả Bộ Kiểm thử Tự động (`pytest`)

Toàn bộ bộ kiểm thử tự động được thực thi qua kịch bản `scripts/run_test_suite_and_save.py` và lưu biên bản gốc tại thư mục `results/test_results/`:
- `results/test_results/test_evaluation_summary.json` — Tóm tắt chỉ số kiểm thử dạng JSON.
- `results/test_results/unit_test_cases.csv` — Bảng kết quả và thời gian chạy từng test case (57 dòng).
- `results/test_results/pytest_junit.xml` — Biên bản chuẩn JUnit XML.
- `results/test_results/pytest_full_output.txt` — Log console đầy đủ.

| Chỉ số Kiểm thử | Giá trị Đạt được | Đánh giá Chuẩn Nghiệm thu |
|:---|:---:|:---:|
| **Tổng số bài kiểm thử (`total_tests`)** | **57** | Bao phủ toàn bộ 9 phân hệ cốt lõi |
| **Số bài đạt (`passed`)** | **57 / 57 (100,0%)** | Đạt tuyệt đối (`0 failed, 0 errors, 0 skipped`) |
| **Tổng thời gian chạy** | `34,72 giây` | Nhanh, tự động hóa hoàn toàn |
| **Số thế cờ chiến thuật thủ công (`positions.csv`)** | **33 thế cờ** | Vượt xa ngưỡng tối thiểu 30 thế cờ của rubric |
| **Đối chiếu chéo Bitboard vs Reference Engine** | **10.000 ván ngẫu nhiên** | Khớp 100% ở mọi bước đi và hoàn tác `undo()` |
| **Trạng thái Checkpoint Mạng Nơ-ron** | `policy_net_best.pt` (`1.113,06 KB`) | Đã nạp tự động và vượt qua kiểm thử chiến thuật |

### Phân tích Chi tiết theo Từng Mô-đun Kiểm thử
1. **`tests/test_engine.py` (14 tests — 100% PASS)**: Kiểm chứng trọng lực thả quân, phát hiện đủ 4 hướng thắng (ngang, dọc, chéo chính, chéo phụ), ván hòa 42 nước, thắng ở nước thứ 42 không bị tính nhầm là hòa, hoàn tác `undo()` khôi phục bitboard chính xác từng trạng thái, mã hóa tensor canon hóa `2×6×7`, khóa trạng thái bất biến với thứ tự nước đi, và **kiểm định toán học Perft** khớp lý thuyết đến độ sâu 5 (`7; 49; 238; 1.120; 4.263` nút, không có trạng thái thắng trước nước thứ 7).
2. **`tests/test_crosscheck.py` (1 test nặng — `15,54s` — 100% PASS)**: Thực thi `10.000` ván ngẫu nhiên song song giữa `Connect4` (bitboard 49-bit) và `ReferenceConnect4` (mảng 2D độc lập), xác nhận `0` sai lệch.
3. **`tests/test_agents.py` (3 tests — 100% PASS)**: Kiểm chứng tính hợp lệ, tính tất định theo `seed` của `RandomAgent` và thông báo lỗi rõ ràng của factory `make_agent`.
4. **`tests/test_heuristic.py` (4 tests — 100% PASS)**: Kiểm chứng thứ tự 4 luật ưu tiên (thắng ngay → chặn thua → lọc nước tự sát trao chiến thắng tầng trên → ưu tiên cột giữa), không làm biến đổi trạng thái gốc và thắng áp đảo `RandomAgent`.
5. **`tests/test_alphabeta.py` (8 tests — 100% PASS)**: Đối chiếu khớp tuyệt đối giá trị Minimax độc lập không cắt tỉa, xác nhận bật/tắt cắt tỉa và sắp xếp Center-First chỉ giảm mạnh số nút duyệt chứ không đổi nghiệm, tìm đúng đường ép thắng 3-ply, tính đối xứng gương của hàm lượng giá 69 cửa sổ, và tuân thủ ngân sách thời gian Iterative Deepening.
6. **`tests/test_mcts.py` (8 tests — 100% PASS)**: Xác nhận tính tái lập theo `seed`, chọn ngay nước thắng trực tiếp, bỏ qua tìm kiếm khi chỉ còn 1 nước hợp lệ, tuân thủ `Budget(time_s=...)` và thắng áp đảo `RandomAgent`.
7. **`tests/test_match.py` & `tests/test_metrics.py` (9 tests — 100% PASS)**: Kiểm chứng sinh khai cuộc không trùng lặp chưa kết thúc ván, tự động đổi bên đối xứng `2 × N` ván, xuất log CSV chuẩn, công thức điểm chuẩn hóa, khoảng tin cậy Wilson 95% và Bootstrap 95% (`10.000` resamples).
8. **`tests/test_positions.py` (1 test duyệt `33` thế cờ — 100% PASS)**: Kiểm chứng toàn bộ 33 thế cờ chiến thuật biên soạn thủ công trong `tests/data/positions.csv` trên cả 2 engine và các tác tử.
9. **`tests/test_nn_and_puct.py` (6 tests — 100% PASS) & `tests/test_train_pipeline.py` (3 tests — 100% PASS)**: Kiểm chứng kiến trúc `Connect4PolicyValueNet`, mặt nạ nước hợp lệ (cột đầy có xác suất `0,0`), sửa lỗi nhiễu Dirichlet (`gammavariate`) và bảo toàn chuẩn hóa xác suất trong `Transposition Cache`, tương thích `ReferenceConnect4`, bản đồ nhiệt `compute_saliency_map`, giữ nhãn chuyên gia sạch dưới $\epsilon$ cao, đối xứng lật gương ngang, **0% rò rỉ chéo (gốc + gương)** giữa `Train / Val / Test`, và kiểm tra năng lực giải thế cờ thắng/chặn trực tiếp của checkpoint thực tế `policy_net_best.pt`.

---

## 2. Đánh giá Chất lượng Mô hình Học sâu (`Connect4PolicyValueNet`)

Nguồn dữ liệu và lịch sử huấn luyện lưu tại `data/dataset_summary.json` và `checkpoints/training_history.json`:
- **Tập dữ liệu sạch chống rò rỉ**: Sinh từ `2.500` ván `AlphaBeta(depth=4)`, tách nguyên vẹn theo ván (`1.750` Train / `375` Val / `375` Test), khử trùng lặp và lọc bỏ toàn bộ trạng thái trùng gốc hoặc trùng ảnh lật gương ngang giữa các tập (`0%` rò rỉ). Quy mô cuối: **75.036 mẫu Train**, **6.396 mẫu Val**, **6.293 mẫu Test**.
- **Hội tụ có điều chuẩn**: Huấn luyện 10 epochs (`batch_size=256`, `lr=0,0015`, `weight_decay=0,001`, `label_smoothing=0,05`), đạt cực tiểu kiểm định tại **Epoch 6** (`Val Loss = 1,1336`, `Val Top-1 Acc = 72,09%`, `Val Top-2 Acc = 89,13%`).
- **Hiệu năng trên tập `Test` độc lập (`6.293` mẫu chưa từng thấy)**:
  + **Top-1 Accuracy**: **71,68%** (gấp hơn `5×` mức ngẫu nhiên `14,29%`).
  + **Top-2 Accuracy**: **89,07%**.
  + **Policy Cross-Entropy**: `0,7535` | **Value MSE**: `0,7884` (`MAE = 0,6360`).
  + **Độ trễ suy luận đơn lẻ CPU**: Trung bình **`1,909 ms`**, phân vị `p95 = 2,475 ms`.

---

## 3. Đánh giá Kết quả Giải đấu Đối kháng & Nghiên cứu Phân rã (`results/tables/`)

### 3.1. Giải đấu Round-Robin 6 Tác tử — 3.000 Ván (`round_robin_default_summary.csv`)
Thứ bậc sức mạnh phân tầng rõ ràng, hợp lý tuyệt đối về mặt khoa học trên `1.000` ván/tác tử:
1. **`Mixed-MCTS PUCT` (200 sims)**: `705W – 90D – 205L` $\rightarrow$ **Score = 75,00%** (Hạng 1 — đánh bại `MCTS-1000` với điểm **62,50%** và vượt `Alpha-Beta depth 5` với điểm **54,25%**).
2. **`Alpha-Beta` (depth 5)**: `716W – 64D – 220L` $\rightarrow$ **Score = 74,80%** (Hạng 2 — `p95 ~ 63 ms`).
3. **`MCTS-UCT` (1.000 sims)**: `596W – 27D – 377L` $\rightarrow$ **Score = 60,95%** (Hạng 3 — `p95 ~ 153 ms`).
4. **`Policy-Value NN` (0 search)**: `460W – 87D – 453L` $\rightarrow$ **Score = 50,35%** (Hạng 4 — thắng `Heuristic` **64,25%** chỉ với `p95 ~ 3,8 ms` không cần tìm kiếm cây).
5. **`Heuristic`**: `350W – 70D – 580L` $\rightarrow$ **Score = 38,50%** (Hạng 5 — thắng `Random` **99,50%**).
6. **`Random`**: `4W – 0D – 996L` $\rightarrow$ **Score = 0,40%** (Hạng 6).

### 3.2. Giải đấu Giới hạn Thời gian Thực Chế độ A — RQ1 (`round_robin_timed_summary.csv`)
Trên `100` ván mỗi mức đơn luồng độc lập, `Alpha-Beta` (Iterative Deepening) duy trì ưu thế thống kê trước `MCTS-UCT` ở cả 3 mức thời gian tương tác:
- **50 ms/nước**: `Alpha-Beta` thắng `64 – 2 – 34` (**Score = 0,650**, CI `[0,555; 0,740]`, `p95 = 51,59 ms` vs `50,89 ms`).
- **100 ms/nước**: `Alpha-Beta` thắng `68 – 2 – 30` (**Score = 0,690**, CI `[0,600; 0,775]`, `p95 = 101,52 ms` vs `100,93 ms`).
- **300 ms/nước**: `Alpha-Beta` thắng `59 – 3 – 38` (**Score = 0,605**, CI `[0,510; 0,700]`, `p95 = 301,22 ms` vs `300,85 ms`).

### 3.3. Tổng hợp 4 Nghiên cứu Phân rã (Ablation A1–A4)
- **Ablation A1 (`ablation_a1_results.csv`)**: Cắt tỉa $\alpha$-$\beta$ + Center-First giảm **80,45%** nút ở depth 4 (`399 → 78`), **87,89%** ở depth 5 (`2.800 → 339`) và **93,07%** ở depth 6 (`18.886 → 1.309` nút, nhanh gấp `61,9×`), bảo toàn tuyệt đối nghiệm Minimax.
- **Ablation A2 (`ablation_a2_results.csv`)**: Đối đầu `Alpha-Beta depth 4`, `MCTS-UCT` tăng điểm đơn điệu theo số mô phỏng (`0,065 → 0,305 → 0,420 → 0,540 → 0,585` ứng với `100 → 500 → 1.000 → 2.000 → 5.000` sims), xác định điểm giao thoa tại **~1.500–2.000 mô phỏng**.
- **Ablation A3 (`ablation_a3_results.csv`)**: Ở cùng `200` mô phỏng khi gặp `MCTS-500`, bổ sung Policy Prior giúp nhảy vọt từ `0,325` (`MCTS-UCT`) lên **0,695** (`PUCT+Rollout`) và **0,685** (`PUCT+ValueHead`); khi gặp chính tác tử thầy `Alpha-Beta depth 4`, `PUCT+Rollout` đạt **0,625** (`CI [0,535; 0,710]`) và `PUCT+ValueHead` đạt **0,510**.
- **Ablation A4 (`ablation_a4_first_player_bias.csv`)**: Trên toàn bộ `3.000` ván, quân Đỏ (đi trước) thắng **51,80%** (`1.554` ván) so với quân Vàng **42,57%** (`1.277` ván), Hòa `5,63%` ($\Delta W = +9,23\%$).

---

## 4. Kết luận Nghiệm thu Đề tài theo Bảng chấm điểm Học phần

1. **Tính đúng đắn kỹ thuật & Kiểm thử**: Đạt xuất sắc (`57/57` unit tests pass `100%`, đối chiếu chéo `10.000` ván, Perft ply 1–5, `33` thế cờ chiến thuật).
2. **Độ sâu thuật toán & Giá trị mở rộng**: Hoàn thiện đầy đủ 6 cấp tác tử (bao gồm Policy-Value ResNet có checkpoint thực tế, PUCT-MCTS vượt tác tử thầy và Explainable AI Saliency Heatmap).
3. **Phương pháp thực nghiệm & Thống kê**: Hơn `4.600` ván thực nghiệm có log CSV thô, kiểm soát khai cuộc & đổi bên đối xứng, khoảng tin cậy Wilson/Bootstrap 95%, độ trễ `p95`, đủ 4 Ablations A1–A4 và 7 biểu đồ 300 DPI.
4. **Mức điểm kỳ vọng theo Rubric**: **Đạt vững chắc mức 9,0 – 9,5 / 10** (khi nhóm kết hợp bảo vệ tốt và cập nhật lịch sử commit đồng đều cho TV4).

