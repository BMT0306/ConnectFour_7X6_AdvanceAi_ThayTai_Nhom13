# PHẦN GÕ GOOGLE DOCS: BÙI MINH TRUNG (TỶ LỆ ĐÓNG GÓP: 40% - NHÓM TRƯỞNG)

> **Vai trò**: Trục kỹ thuật lõi & Hạ tầng AI.
> **Các phần phụ trách gõ lên Google Docs**:
> 1. Trang bìa, Bảng phân công nhiệm vụ, Lời nói đầu, Tóm tắt đồ án, Mục lục tổng quan.
> 2. **Chương 2**: Toàn bộ Chương 2 (Hạ tầng Kỹ thuật và Cấu trúc Dữ liệu Bitboard 49-bit, Perft Depth 1-6).
> 3. **Chương 3**: Mục 3.1 (Nhóm tác tử Cổ điển Cấp 1, Cấp 2, Cấp 3) & Mục 3.4 (Cơ chế kiểm soát thời gian thực và Fallback an toàn `best_or_random`).
> 4. **Chương 5**: Mục 5.1 (Quy chuẩn giải đấu Round-Robin 3.000 ván), Mục 5.2.1 (RQ1 - Giải đấu tính giờ), Mục 5.2.2 (Ablation A1 - Cắt tỉa Alpha-Beta & Center-First), Mục 5.2.6 (Giải đấu 6 Cấp độ Giới hạn 100 ms/nước - 1.500 ván).
> 5. **Chương 6**: Toàn bộ Kết luận chung và Hướng phát triển.

---
## PHẦN 1: TRANG BÌA, PHÂN CÔNG, LỜI NÓI ĐẦU, TÓM TẮT & MỤC LỤC

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
| 1 | Bùi Minh Trung | 3124720074 | Nhóm trưởng | Thiết kế lõi `Connect4` Bitboard 49-bit và `ReferenceConnect4`; viết bộ unit test; cài đặt `HeuristicAgent`, `AlphaBetaAgent`, cơ chế kiểm soát timeout `best_or_random`; xây dựng khung giải đấu & thống kê (`Wilson`, `Bootstrap`, `p95`), chạy giải 6 cấp độ 100 ms & Ablation A1, A3; cài đặt Saliency XAI, Web UI (`http.server`), review/fix lỗi self-play Elo & cache 60 FPS, quản lý GitHub, khung báo cáo Google Docs và đóng gói bài nộp. | **40%** |
| 2 | Trần Lê Minh Tâm | 3124720064 | Thành viên | Cài đặt `RandomAgent`, `MCTSAgent` (UCT 4 bước); xây dựng Data Pipeline chống rò rỉ gương, mạng `Connect4PolicyValueNet` (`model.py`), `MixedMCTSAgent` (PUCT + `Transposition Cache` + Dirichlet); xây dựng **Hệ thống Xếp hạng Elo Bradley-Terry MLE (`compute_elo.py`)** và nâng cấp giao diện Pygame 60 FPS (**chế độ Solo 2-Slot AI vs AI, Start/Pause, khai cuộc 4-ply ngẫu nhiên, cập nhật Elo thực tế**); chạy Ablation A2, A4; **trực tiếp test game thực tế, quay Video Demo và đề xuất ý tưởng fix code**. | **40%** |
| 3 | Nguyễn Thành Tài | 3124720062 | Thành viên | Đồng bộ log CSV/Elo lên Google Drive, cập nhật Nhật ký thí nghiệm Google Sheets/Excel 5 sheets (`docs/NHAT_KY_THI_NGHIEM.xlsx`), soạn bộ 33 thế cờ kiểm thử thủ công (`positions.csv`); **trực tiếp chỉnh sửa nội dung Báo cáo trên Google Docs (Chương 4–5, bảng biểu số liệu & Elo) và hoàn thiện file Slide thuyết trình PPTX**. | **10%** |
| 4 | Chương Gia Thịnh | 3124720067 | Thành viên | Chuẩn hóa Danh mục tài liệu tham khảo (bổ sung Hunter 2004, Elo 1978), Danh mục từ viết tắt, tệp `THIRD_PARTY.md`, `README.md`; **trực tiếp chỉnh sửa nội dung Báo cáo trên Google Docs (Chương 1–3, văn phong/trình bày), chỉnh sửa Slide PPTX và hoàn thiện Kịch bản trình bày (`KICH_BAN_TRINH_BAY.md`)**. | **10%** |
| **Tổng** | | | | | **100%** |

### QUY TRÌNH QUẢN LÝ CỘNG TÁC, PHÂN CÔNG TRỤC DỌC – NGANG VÀ ĐÁNH GIÁ QUÁ TRÌNH

Để bảo đảm tính minh bạch, truy vết được toàn bộ quá trình thực hiện và đánh giá công bằng giữa 4 thành viên, nhóm áp dụng quy trình quản trị cộng tác đa nền tảng (chi tiết đầy đủ tại `docs/QUAN_LY_CONG_TAC_VA_NHAT_KY.md`):

| Mảng quản lý | Công cụ áp dụng | Nơi lưu trữ / Quy ước nhóm |
|---|---|---|
| **Quản lý mã nguồn (Code)** | **GitHub** | `https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13` |
| **Lưu trữ kết quả thí nghiệm** | **Google Drive** | `https://drive.google.com/drive/folders/1k-q-cuTi3Rb_eYnrmfmrr_6-C35j7M6K?usp=sharing` |
| **Nhật ký thí nghiệm** | **Google Sheets / Excel** | `docs/NHAT_KY_THI_NGHIEM.xlsx` (5 sheets chuẩn đối chiếu Baseline–Variant, EXP-01..EXP-11) |
| **Vẽ hình, Slide & Poster** | **Google Slides / PowerPoint** | `docs/SLIDE_THUYET_TRINH_CONNECT_FOUR_NHOM13.pptx` (39 slides) & `docs/POSTER_CONNECT_FOUR_NHOM13.pdf` (`.pptx`) |
| **Kế hoạch & Viết báo cáo** | **Google Docs** | Bản soạn thảo trực tuyến đồng chỉnh sửa cho 4 thành viên (`BAO_CAO_DO_AN_CUOI_KY.docx`) |

- **Phân công Trục dọc × Trục ngang**: Trục dọc phân định người đầu mối chịu trách nhiệm cho từng nhóm công việc (Code & Hạ tầng AI: Trung; Mô hình AI, Elo, Test Game, Demo & Fix Idea: Tâm; Nhật ký thí nghiệm & Rà soát số liệu: Tài; Báo cáo Google Docs, Slide & Kịch bản: Tài & Thịnh dưới sự rà soát của Nhóm trưởng). Trục ngang chia nhỏ từ giai đoạn M1 (Engine) đến M5 (UI, Video & Tài liệu) kèm **Nhật ký công việc 7 tuần** cho mọi thành viên (ghi nhận cả chu trình review PR nhánh `feature/tam-ai-solo-elo`).
- **Đánh giá dựa vào người yếu nhất (Weakest-Link Evaluation)**: Mọi thành viên được kiểm tra chéo 4 chỉ số quá trình học tập (C1: Hiểu thuật toán, Bitboard & thang Elo Bradley-Terry; C2: Tự chạy test/Elo/log CSV; C3: Độ chính xác khi chỉnh sửa Google Docs/PPT; C4: Kỷ luật cập nhật nhật ký tuần). Mức điểm nền tối thiểu của thành viên thấp nhất trong nhóm phải đạt $\ge 7,0/10$ (kết quả đánh giá chéo toàn nhóm hiện tại đạt ngưỡng tối thiểu `8,00/10`).

---

## LỜI NÓI ĐẦU

Trong chương trình học phần Trí tuệ nhân tạo nâng cao, các thuật toán tìm kiếm đối kháng và học máy trên trò chơi luôn là một chủ đề gắn liền giữa lý thuyết và thực hành. Thay vì chỉ dừng lại ở việc gọi thư viện có sẵn hoặc cài đặt một thuật toán đơn lẻ như Minimax cơ bản, nhóm chúng em mong muốn tự tay xây dựng một hệ thống hoàn chỉnh từ tầng biểu diễn trạng thái bàn cờ ở mức bit cho đến việc so sánh thực nghiệm giữa các nhánh tiếp cận khác nhau: từ luật phản xạ, duyệt cây cổ điển, tìm kiếm Monte Carlo cho đến việc huấn luyện mạng nơ-ron sâu kết hợp tìm kiếm cây theo hướng của AlphaZero.

Trò chơi Connect Four với kích thước bàn chuẩn 7 cột × 6 hàng được nhóm lựa chọn vì có luật chơi rõ ràng, số nhánh tại mỗi lượt không quá lớn (tối đa 7 cột) để có thể tự sinh dữ liệu và huấn luyện mô hình ngay trên máy tính cá nhân của các thành viên trong nhóm, nhưng đồng thời không gian trạng thái toàn cục (khoảng $4,53 \times 10^{12}$ trạng thái) vẫn đủ lớn để các thuật toán tìm kiếm vét cạn thông thường không thể giải trực tiếp trong thời gian thực.

Trong quá trình thực hiện đề tài, mặc dù nhóm đã cố gắng kiểm thử kỹ mã nguồn và chạy hơn 6.100 ván đấu thực nghiệm để lấy số liệu khách quan, báo cáo chắc chắn không tránh khỏi những thiếu sót nhất định do giới hạn về thời gian và cấu hình phần cứng. Nhóm chúng em rất mong nhận được sự góp ý của Thầy để hoàn thiện hơn. Nhóm xin chân thành cảm ơn Thầy Đỗ Như Tài đã giảng dạy và định hướng cho nhóm trong suốt học phần này.

---

## TÓM TẮT ĐỒ ÁN

Báo cáo trình bày quá trình thiết kế, cài đặt và đánh giá thực nghiệm hệ thống tác tử trí tuệ nhân tạo đa cấp độ cho trò chơi Connect Four (7 cột × 6 hàng). Ở tầng hạ tầng, nhóm cài đặt song song hai bộ máy quản lý luật chơi: bản `ReferenceConnect4` dùng mảng hai chiều thông thường để làm chuẩn đối chiếu và bản `Connect4` dùng kỹ thuật Bitboard 49-bit để tăng tốc độ duyệt cây. Kết quả kiểm chuẩn Perft đến độ sâu 6 và kiểm thử chéo 10.000 ván ngẫu nhiên cho thấy hai phiên bản cho kết quả khớp nhau hoàn toàn.

Trên nền tảng engine đó, nhóm triển khai tuần tự 6 cấp độ tác tử gồm: `RandomAgent` (đi ngẫu nhiên), `HeuristicAgent` (dựa trên 4 quy tắc ưu tiên một bước), `AlphaBetaAgent` (duyệt cây Negamax có cắt tỉa Alpha-Beta, sắp xếp nước đi ưu tiên cột giữa và tìm kiếm sâu dần theo thời gian), `MCTSAgent` (tìm kiếm cây Monte Carlo dùng công thức UCT), `NNAgent` (mạng nơ-ron hai đầu `Connect4PolicyValueNet` gồm 3 khối Residual học có giám sát từ dữ liệu của Alpha-Beta độ sâu 4) và `MixedMCTSAgent` (kết hợp đầu ra của mạng nơ-ron vào công thức chọn nhánh PUCT kèm bộ nhớ đệm trạng thái). Ngoài ra, nhóm còn xây dựng mô-đun giải thích bản đồ độ nhạy đạo hàm (Saliency Map XAI), **hệ thống chuẩn hóa thứ hạng Elo theo mô hình Bradley-Terry MLE** (`scripts/compute_elo.py`) và **chế độ đấu Solo AI-vs-AI 2 khe** trên giao diện Pygame 60 FPS có cập nhật Elo thời gian thực.

Quá trình đánh giá được thực hiện thông qua giải đấu vòng tròn 3.000 ván không giới hạn thời gian (15 cặp, 200 ván/cặp), giải đấu giới hạn thời gian thực 300 ván (`50 / 100 / 300 ms`), **giải đấu vòng tròn đầy đủ 6 cấp độ ở mức 100 ms/nước gồm 1.500 ván** (15 cặp × 100 ván = 50 Đỏ trước + 50 Vàng trước, áp dụng cơ chế `best_or_random` giữ nước tạm thời tốt nhất trước deadline) và 4 thí nghiệm khảo sát thành phần (Ablation A1 đến A4). Kết quả cho thấy cắt tỉa Alpha-Beta kết hợp sắp xếp Center-First giảm 93,07% số nút ở độ sâu 6; mạng `Connect4PolicyValueNet` đạt Top-1 `71,68%` và Top-2 `89,07%` trên tập kiểm tra độc lập. Khi quy đổi sang thang **Bradley-Terry MLE Elo** (neo `Random = 1000,0`), ở chế độ không giới hạn thời gian, `MixedMCTSAgent` (200 sims) dẫn đầu với **2114,8 Elo** (`75,00%`), nhỉnh hơn `AlphaBetaAgent` độ sâu 5 (**2113,1 Elo**, `74,80%`) và `MCTSAgent` 1.000 sims (**2004,3 Elo**, `60,95%`). Ngược lại, khi giới hạn chặt `100 ms/nước` trên CPU, `AlphaBetaAgent` vươn lên hạng 1 áp đảo với **2125,8 Elo** (`78,80%`, `+12,7 Elo`, 0 lần fallback random), trong khi `MixedMCTSAgent` giảm mạnh **`-126,7 Elo`** xuống **1988,1 Elo** (`61,10%`) do độ trễ suy luận CNN giới hạn số lượt mô phỏng trong 100 ms.

---



## MỤC LỤC

- **LỜI NÓI ĐẦU** ................................................................ **Trang 4**
- **TÓM TẮT ĐỒ ÁN** .............................................................. **Trang 5**
- **DANH MỤC CÁC CỤM TỪ VIẾT TẮT** ............................................... **Trang 6**
- **MỤC LỤC** .................................................................... **Trang 7**
- **DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU** ............................................. **Trang 9**
- **CHƯƠNG 1: GIỚI THIỆU VÀ KHẢO SÁT CHƯƠNG TRÌNH CONNECT FOUR** ................. **Trang 11**
  - 1.1. Bối cảnh đề tài và hình thức hóa toán học không gian trạng thái (S, A, T, R) ... Trang 11
  - 1.2. Khảo sát thuật toán/mã nguồn sẵn có và đặt mốc đánh giá chuẩn (Benchmark Baseline) ... Trang 13
  - 1.3. Các câu hỏi nghiên cứu định lượng (RQ1 – RQ3) ....................... Trang 14
- **CHƯƠNG 2: HẠ TẦNG KỸ THUẬT VÀ CẤU TRÚC DỮ LIỆU BITBOARD** .................... **Trang 16**
  - 2.1. Thiết kế Bitboard 49-bit và toán tử Bitwise O(1) .................... Trang 16
    - 2.1.1. Cách ánh xạ bàn cờ 7×6 vào 49 bit của số nguyên 64-bit .......... Trang 16
    - 2.1.2. Toán tử thả quân và kiểm tra thắng _has_won trong thời gian hằng số O(1) ... Trang 17
  - 2.2. Kiểm chuẩn tính đúng đắn cây trò chơi (Perft Validation at Depth 6) ... Trang 19
- **CHƯƠNG 3: PHƯƠNG PHÁP TRIỂN KHAI CHUỖI TÁC TỬ AI (LEVEL 1 – LEVEL 6)** ....... **Trang 20**
  - 3.1. Nhóm tác tử cổ điển (Random, Heuristic, Negamax Alpha-Beta Pruning) ... Trang 20
    - 3.1.1. Tác tử Cấp 1 — RandomAgent ...................................... Trang 20
    - 3.1.2. Tác tử Cấp 2 — HeuristicAgent ................................... Trang 20
    - 3.1.3. Tác tử Cấp 3 — AlphaBetaAgent ................................... Trang 20
  - 3.2. Nhóm tác tử Monte Carlo (MCTS-UCT 4 giai đoạn) ...................... Trang 21
  - 3.3. Đề xuất Tác tử Học sâu AlphaZero-lite (Dual-Head ResNet + PUCT Search Pseudocode) ... Trang 22
    - 3.3.1. Kiến trúc mạng hai đầu Connect4PolicyValueNet ................... Trang 22
    - 3.3.2. Sự cải tiến khi tích hợp mạng học sâu vào cây tìm kiếm PUCT (MixedMCTSAgent) ... Trang 23
  - 3.4. Cơ chế kiểm soát thời gian thực và Fallback an toàn (`best_or_random`) ... Trang 26
- **CHƯƠNG 4: QUY TRÌNH QUẢN TRỊ DỮ LIỆU VÀ MINH BẠCH HÓA AI (XAI)** ............. **Trang 27**
  - 4.1. Data Pipeline: Mã hóa Tensor, Symmetry Augmentation và Game-level Splitting ... Trang 27
  - 4.2. Quá trình huấn luyện Joint Loss và trực quan hóa bản đồ độ nhạy Saliency Map ... Trang 28
    - 4.2.1. Kiểm định toán học quá trình huấn luyện đa mục tiêu (Joint Loss Validation) ... Trang 28
    - 4.2.2. Trực quan hóa quyết định của mạng bằng bản đồ độ nhạy Saliency Map (XAI) ... Trang 30
- **CHƯƠNG 5: THỰC NGHIỆM ĐỐI KHÁNG VÀ PHÂN TÍCH KẾT QUẢ** ....................... **Trang 33**
  - 5.1. Quy chuẩn Giải đấu Vòng tròn Round-Robin Đối xứng (200 ván/cặp, Wilson 95% CI) ... Trang 33
  - 5.2. Phân tích kết quả thí nghiệm Giải đấu Tính giờ (RQ1) và Ablation Studies (A1 – A4) ... Trang 36
    - 5.2.1. Giải đấu giới hạn thời gian suy nghĩ cho RQ1 .................... Trang 36
    - 5.2.2. Thí nghiệm Ablation A1: Đóng góp của cắt tỉa Alpha-Beta và sắp xếp nước đi Center-First ... Trang 37
    - 5.2.3. Thí nghiệm Ablation A2: Tìm điểm giao thoa của MCTS trước Alpha-Beta cố định độ sâu 4 ... Trang 39
    - 5.2.4. Thí nghiệm Ablation A3: Bóc tách vai trò của Policy Prior và Value Head trong PUCT ... Trang 40
    - 5.2.5. Thí nghiệm Ablation A4: Định lượng lợi thế của người đi trước trên 3.000 ván đấu ... Trang 42
    - 5.2.6. Giải đấu Vòng tròn 6 Cấp độ Giới hạn 100 ms/nước (1.500 ván, best_or_random) ... Trang 43
    - 5.2.7. Chuẩn hóa Sức mạnh Bằng Hệ thống Xếp hạng Elo (Bradley-Terry MLE & FIDE Logistic) ... Trang 46
  - 5.3. Đánh giá mối quan hệ đánh đổi: Thông lượng duyệt nút, Độ trễ suy luận và Tỷ lệ thắng ... Trang 48
  - 5.4. Triển khai Giao diện Ứng dụng và Minh chứng Thực tế Chạy Demo ......... Trang 50
- **KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN** ............................................... **Trang 54**
  - 1. Kết luận chung ........................................................ Trang 54
  - 2. Hạn chế và hướng phát triển tiếp theo ................................. Trang 54
- **TÀI LIỆU THAM KHẢO** ......................................................... **Trang 56**

---

## DANH MỤC HÌNH ẢNH VÀ BẢNG BIỂU



---
## PHẦN 2: CHƯƠNG 2 — HẠ TẦNG KỸ THUẬT VÀ CẤU TRÚC DỮ LIỆU BITBOARD

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

![Hình 2.1: Sơ đồ kiến trúc ánh xạ Bitboard 49-bit với bit đệm Sentinel bảo vệ ranh giới cột](../results/figures/diagram_bitboard_49bit.png)

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

2. **Kiểm thử đối chiếu chéo 10.000 ván ngẫu nhiên và bộ 59 bài test tự động**:
   Trong tệp `tests/test_crosscheck.py`, nhóm cho chạy 10.000 ván đấu ngẫu nhiên từ đầu đến cuối (tương đương hơn 210.000 lượt thả quân). Ở mỗi bước đi, chương trình kiểm tra xem danh sách cột hợp lệ `legal_actions()`, trạng thái kết thúc `is_terminal()`, người thắng `winner`, mảng bàn cờ `to_array()` và tensor mã hóa `encode()` của hai engine có giống hệt nhau hay không, sau đó gọi `undo()` lùi từng nước về bàn cờ rỗng. Toàn bộ **59 bài kiểm thử tự động trên 11 tệp kiểm thử** trong dự án (bao gồm cả kiểm thử timeout `best_or_random`) đều vượt qua 100% (chi tiết lưu tại `results/TEST_AND_EVALUATION_REPORT.md`).

---



---
## PHẦN 3: CHƯƠNG 3 (MỤC 3.1 VÀ MỤC 3.4)

## CHƯƠNG 3: PHƯƠNG PHÁP TRIỂN KHAI CHUỖI TÁC TỬ AI (LEVEL 1 – LEVEL 6)

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



### 3.4. Cơ chế kiểm soát thời gian thực và Fallback an toàn (`best_or_random`)

Trong điều kiện thi đấu thời gian thực (ví dụ giới hạn `100 ms/nước` cho cả 6 cấp độ tác tử), một tác tử tìm kiếm cây nếu không kiểm soát chặt deadline có thể làm quá giờ hoặc gặp lỗi ngoại lệ khi chưa kịp mở rộng nút nào. Để giải quyết triệt để vấn đề này, nhóm thiết kế cơ chế kiểm soát thời gian hai lớp giữa **các tác tử** (`src/c4/agents/*.py`) và **trọng tài trận đấu** (`src/c4/eval/match.py`):
1. **Lớp 1 — Giữ nước tạm thời tốt nhất (Anytime Best-So-Far)**:
   - `AlphaBetaAgent`: Duyệt sâu dần theo từng tầng $d = 1, 2, \dots$; bất cứ khi nào gặp giới hạn thời gian (`_Timeout`) giữa tầng $d$, hàm trả về ngay nước đi tối ưu đã hoàn thành ở tầng $d - 1$ gần nhất kèm cờ `timed_out = True`, `fallback_random = False`. Nếu hết giờ ngay trước khi xong tầng 1 (`best_move is None`), tác tử chọn an toàn một cột ngẫu nhiên hợp lệ (`fallback_random = True`).
   - `MCTSAgent` và `MixedMCTSAgent`: Kiểm tra deadline ngay tại `sims == 0` (trước khi mở rộng cây hoặc chạy suy luận mạng ResNet tại gốc) và đầu mỗi vòng lặp mô phỏng. Nếu đã có ít nhất một lượt mô phỏng (`root.children` không rỗng), tác tử chọn nhánh có số lượt thăm cao nhất đã tích lũy trước deadline (`timed_out = True`, `fallback_random = False`); ngược lại nếu cây gốc còn rỗng, tác tử không gọi `max()` gây lỗi mà trả về ngay một nước đi ngẫu nhiên hợp lệ (`fallback_random = True`).
2. **Lớp 2 — Trọng tài giải đấu (`timeout_policy = "best_or_random"`)**:
   - Trọng tài `play_game()` trong `match.py` đo thời gian thực tế mỗi nước đi bằng `time.perf_counter()` và đối chiếu với `Budget.time_s`. Với chính sách `best_or_random`, trọng tài tôn trọng nước đi tạm thời tốt nhất mà tác tử vừa trả về khi chạm deadline, đồng thời ghi nhận lại bộ đếm `Timeouts` và `Fallback_Randoms` vào log CSV để phục vụ thống kê. Chỉ khi tác tử vượt quá ngưỡng trễ hoặc bị vô hiệu hóa hoàn toàn (`time_s <= 0`), trọng tài mới ghi nhận nhánh fallback an toàn.

---



---
## PHẦN 4: CHƯƠNG 5 (MỤC 5.1, 5.2.1, 5.2.2 VÀ 5.2.6)

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

Kết quả cho thấy ở cả ba mức thời gian phản hồi thực tế từ `50 ms` đến `300 ms`, `AlphaBetaAgent` đều thắng nhiều hơn `MCTSAgent` có ý nghĩa thống kê (khoảng tin cậy 95% đều nằm trên ngưỡng 0,50). Nguyên nhân là trên bàn cờ Connect Four có số nhánh nhỏ ($b \le 7$) và hàm đánh giá 69 cửa sổ chạy trên Bitboard rất nhẹ, trong vòng `50–100 ms` `Alpha-Beta` đã duyệt trọn vẹn độ sâu 5 đến 6 ply nên phát hiện chính xác các bẫy chiến thuật ngắn hạn; trong khi đó `MCTS` thuần phải chia nhỏ lượt mô phỏng ngẫu nhiên nên ở mức thời gian thấp dễ đi sót nước phòng thủ. Tuy nhiên, khi tăng thời gian lên `300 ms`, điểm của `MCTS` đã tăng từ `0,310` lên `0,395`, thu hẹp dần khoảng cách với `Alpha-Beta`.

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



#### 5.2.6. Giải đấu Vòng tròn 6 Cấp độ Giới hạn 100 ms/nước (`round_robin_levels_timed_summary.csv`)

Để kiểm chứng hiệu năng thực tế của toàn bộ 6 cấp độ tác tử trong cùng một điều kiện thi đấu công bằng dưới giới hạn thời gian trung bình, nhóm cấu hình giải đấu `configs/tournament_levels_timed.yaml` gồm 15 cặp tác tử thi đấu trên 50 thế cờ khai cuộc 4-ply khác nhau. Tại mỗi thế cờ, hai tác tử đổi màu quân Đỏ/Vàng (50 ván Đỏ đi trước + 50 ván Vàng đi trước = **100 ván/cặp**, tổng cộng **1.500 ván**). Cả 6 cấp độ đều nhận chung ngân sách `time_s = 0,10` (100 ms/nước) và chạy dưới chính sách trọng tài `timeout_policy = "best_or_random"` (giữ nước đi tạm thời tốt nhất tính được trước deadline, chỉ chuyển sang chọn ngẫu nhiên hợp lệ nếu chưa kịp tính xong bước đầu tiên).

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

![Hình 5.7: Giải đấu vòng tròn 6 cấp độ giới hạn 100 ms/nước (1.500 ván) và phân tích tỷ lệ timeout](../results/figures/round_robin_levels_timed_100ms.png)

Số liệu ở Bảng 5.6, Bảng 5.7 và Hình 5.7 làm rõ hai kết luận quan trọng về hành vi thực tế của 6 cấp độ dưới áp lực thời gian:
1. **Đảo chiều thứ hạng giữa `Alpha-Beta` và `Mixed-MCTS` khi bị ép `100 ms/nước`**: Khi không giới hạn thời gian (Bảng 5.1), `Mixed-MCTS (200 sims)` đứng đầu với `75,00%`. Nhưng khi mọi tác tử đều chỉ có tối đa `100 ms/nước` trên CPU đơn luồng, `Mixed-MCTS` chạm ngưỡng thời gian ở `96,3%` số nước (`5.934 / 6.162` nước) vì mỗi lần mở rộng nút mới cần ~1,9 ms gọi mạng ResNet nên chỉ kịp thực hiện vài chục mô phỏng, tụt xuống hạng 3 (`61,10%`). Ngược lại, `Alpha-Beta` nhờ Bitboard 49-bit và sắp xếp Center-First tận dụng trọn vẹn 100 ms để hoàn tất tầng sâu 5–6 ply, đạt hạng 1 áp đảo với **78,80%** (thắng `Mixed-MCTS` `59 – 12 – 29` và thắng `MCTS` `72 – 1 – 27`).
2. **Độ an toàn tuyệt đối của cơ chế `best_or_random`**: Trên toàn bộ **31.768 nước đi** của 1.500 ván đấu, mặc dù `MCTS` (`98,7%` nước) và `Mixed-MCTS` (`96,3%` nước) liên tục chạy tới giới hạn `100 ms`, số lần phải rơi vào nhánh `fallback_random` ở cả 6 cấp độ đều bằng **0**. Điều này chứng minh mọi tác tử anytime đều kịp tính ra nước tạm thời hợp lệ trước deadline 100 ms (trừ trường hợp chủ động kiểm thử biên `time_s = 0` trong unit test).



---
## PHẦN 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 1. Kết luận chung
Đồ án đã hoàn thành việc xây dựng từ đầu hệ thống trò chơi Connect Four (7×6) cùng 6 cấp độ tác tử AI, bộ kiểm thử tự động **59 bài test trên 11 tệp kiểm thử**, cơ chế kiểm soát timeout `best_or_random`, **hệ thống xếp hạng Elo chuẩn Bradley-Terry MLE & FIDE Logistic**, quy trình sinh dữ liệu sạch và huấn luyện mạng nơ-ron hai đầu, kết hợp giao diện chơi trực quan trên Desktop Pygame (có chế độ Solo 2-Slot Máy vs Máy cập nhật Elo thực tế) và trình duyệt Web (`http.server`) cùng quy trình quản lý cộng tác 5 công cụ (GitHub, Google Drive, Google Sheets 5 sheet, Google Slides/PowerPoint 39 slides, Google Docs) với phân bổ `40% – 40% – 10% – 10%` và đánh giá theo thành viên yếu nhất. Thông qua hơn **6.100 ván đấu thực nghiệm** có lưu đầy đủ nhật ký CSV và Excel/Sheets, báo cáo đã trả lời định lượng ba câu hỏi nghiên cứu đề ra ở Chương 1:
- **Với RQ1**: Dưới cùng giới hạn thời gian suy nghĩ ngắn (`50 ms`, `100 ms`, `300 ms`), `Alpha-Beta` (tích hợp Bitboard, cắt tỉa Center-First giảm 93,07% nút và hàm lượng giá 69 cửa sổ) đạt tỷ lệ thắng cao hơn `MCTS-UCT` thuần (`Score = 0,650; 0,690; 0,605`), đồng thời dẫn đầu giải 6 cấp độ `100 ms/nước` với **2125,8 Elo** (`78,80%`). Khi giữ cố định `Alpha-Beta` ở độ sâu 4, `MCTS-UCT` cần khoảng **1.500 – 2.000 mô phỏng/nước** để vượt qua.
- **Với RQ2**: Mạng `Connect4PolicyValueNet` huấn luyện trên dữ liệu tách theo ván chống rò rỉ đạt **71,68% Top-1 Accuracy** và **89,07% Top-2 Accuracy** trên tập `Test` độc lập, đạt **1922,3 Elo** (`+100,1 Elo` trên `HeuristicAgent`, thắng đối đầu **64,25%**) dù không cần tìm kiếm cây.
- **Với RQ3**: Khi kết hợp mạng nơ-ron vào công thức chọn nhánh PUCT ở mức chỉ 200 mô phỏng, `MixedMCTSAgent` tăng thêm 36–37% điểm số so với `MCTS-UCT` cùng ngân sách, đạt **2114,8 Elo** (`+192,5 Elo` so với `NNAgent` đơn lẻ và `+110,5 Elo` so với `MCTS-1000`) để xếp hạng 1 toàn giải không giới hạn thời gian (**75,00%**), đồng thời giải thích được vùng ô cờ trọng yếu qua bản đồ độ nhạy Saliency Map.

### 2. Hạn chế và hướng phát triển tiếp theo
Bên cạnh các kết quả đạt được, đồ án của nhóm vẫn còn một số điểm có thể cải thiện thêm:
- Hiện tại dữ liệu huấn luyện mạng được sinh có giám sát từ `AlphaBetaAgent(depth = 4)` trên CPU nên đầu ra Value Head chưa thật sự chính xác ở các thế cờ phức tạp (`Test Value MSE = 0,7884`). Hướng phát triển tiếp theo là cài đặt vòng lặp tự chơi tăng cường (Self-Play Reinforcement Learning) qua nhiều thế hệ theo đúng quy trình AlphaZero, trong đó dùng chính phân phối số lượt thăm của cây PUCT làm nhãn huấn luyện lại cho mạng.
- Độ trễ suy luận ResNet trên CPU đơn luồng làm `MixedMCTSAgent` giảm `-126,7 Elo` khi bị ép `100 ms/nước`; trong tương lai có thể tối ưu bằng xuất mô hình sang ONNX Runtime / lượng tử hóa INT8 hoặc đánh giá theo lô (batched leaf evaluation) trên GPU để tăng gấp 5–10 lần số mô phỏng mỗi giây.
- Đối với `AlphaBetaAgent`, nhóm mới sử dụng sắp xếp nước đi tĩnh theo cột giữa; có thể bổ sung bảng băm hoán vị (Transposition Table lưu cận trên/cận dưới) và kỹ thuật sắp xếp động (*Killer Moves* / *History Heuristic*) để duyệt sâu tới 9–11 ply trong cùng ngân sách 100 ms, đồng thời mở rộng toàn bộ khung ResNet + PUCT + Elo sang các bàn cờ lớn hơn như Cờ Caro / Gomoku ($15 \times 15$) hoặc Othello ($8 \times 8$).

---

