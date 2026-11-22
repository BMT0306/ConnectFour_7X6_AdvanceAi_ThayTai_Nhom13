# QUY TRÌNH QUẢN LÝ CỘNG TÁC, PHÂN CÔNG TRỤC DỌC – TRỤC NGANG VÀ NHẬT KÝ THỰC HIỆN (NHÓM 13)

* **Học phần**: Trí tuệ nhân tạo nâng cao — Trường Đại học Sài Gòn
* **Giảng viên hướng dẫn**: TS. Đỗ Như Tài
* **Đề tài**: Xây dựng và Đánh giá Game AI Đa Cấp Độ trên Trò chơi Connect Four (7×6)

---

## 1. Kiến trúc Công cụ Quản lý Cộng tác (Collaboration Stack)

Để tránh làm việc rời rạc, thất lạc file hoặc xung đột phiên bản giữa 4 thành viên, nhóm áp dụng 5 kênh quản lý chuyên biệt:

| Mảng công việc | Công cụ chuẩn hóa | Địa chỉ / Quy ước lưu trữ | Mục tiêu kiểm soát |
|---|---|---|---|
| **1. Quản lý mã nguồn (Code)** | **GitHub** | `https://github.com/BMT0306/ConnectFour_7X6_AdvanceAi_ThayTai_Nhom13` | Quản lý phiên bản code (`src/`, `tests/`, `configs/`, `scripts/`), kiểm tra commit history từng thành viên. |
| **2. Lưu trữ kết quả thí nghiệm** | **Google Drive** | `https://drive.google.com/drive/folders/1k-q-cuTi3Rb_eYnrmfmrr_6-C35j7M6K?usp=sharing` | Chia sẻ tập trung log CSV thô (`results/logs/`), bảng tổng kết (`results/tables/`), biểu đồ 300 DPI (`results/figures/`), file checkpoint `.pt` và video demo. |
| **3. Nhật ký thí nghiệm** | **Google Sheets / Excel** | `docs/NHAT_KY_THI_NGHIEM.csv` & `.xlsx` (đồng bộ lên Google Sheets) | Ghi lại toàn bộ lịch sử chạy thực nghiệm (Exp_ID, ngày chạy, người chạy, tham số, kết quả, timeout/lỗi, link file Drive) theo chuẩn tham khảo `Working_details_excel.pdf`. |
| **4. Vẽ hình & Trình chiếu (Visual)** | **Google Slides / PowerPoint / Canva** | `docs/SLIDE_THUYET_TRINH_CONNECT_FOUR_NHOM13.pptx` | Thiết kế sơ đồ kiến trúc bằng vector shapes (không dùng text/ASCII sơ sài), đồ thị trực quan và slide bảo vệ nhóm. |
| **5. Kế hoạch & Viết báo cáo** | **Google Docs** | Bản soạn thảo trực tuyến chia sẻ cho 4 thành viên (đồng bộ ra `docs/BAO_CAO_DO_AN_CUOI_KY.docx`) | Phân quyền chỉnh sửa báo cáo theo chương/mục, nhận xét chéo và khóa bản nộp cuối kỳ. |

---

## 2. Phân công theo Trục Dọc × Trục Ngang & Tỷ lệ Đóng góp (40% – 40% – 10% – 10%)

### 2.1. Phân bổ tỷ lệ đóng góp chính thức

| STT | Họ và tên | MSSV | Vai trò | Tỷ lệ | Định hướng trách nhiệm chính |
|:---:|---|---|:---:|:---:|---|
| 1 | **Bùi Minh Trung** | `3124720074` | Nhóm trưởng | **40%** | Trục kỹ thuật lõi (Bitboard, Alpha-Beta, khung giải đấu & timeout/fallback, thống kê, Saliency XAI, Web UI, tổng hợp báo cáo & GitHub). |
| 2 | **Trần Lê Minh Tâm** | `3124720064` | Thành viên | **40%** | Trục Học sâu & Demo (MCTS-UCT, Policy-Value ResNet, Data Pipeline, PUCT MixedMCTS, Pygame GUI, **hỗ trợ test game, quay video demo và đề xuất idea fix code**). |
| 3 | **Nguyễn Thành Tài** | `3124720062` | Thành viên | **10%** | Trục hoàn thiện Báo cáo (Google Docs) & Slide PowerPoint; hỗ trợ cập nhật nhật ký thí nghiệm Google Sheets/Drive và rà soát số liệu bảng biểu. |
| 4 | **Chương Gia Thịnh** | `3124720067` | Thành viên | **10%** | Trục hoàn thiện Báo cáo (Google Docs) & Slide PowerPoint; chuẩn hóa tài liệu tham khảo, kịch bản trình bày (`KICH_BAN_TRINH_BAY.md`) và rà soát lỗi chính tả/định dạng. |

### 2.2. Ma trận phân công Trục dọc (Nhóm việc) × Trục ngang (Chia nhỏ task cho các thành viên)

* **Trục dọc (Vertical Leads)**: Xác định **1 người chịu trách nhiệm đầu mối** cho từng nhóm công việc lớn:
  * **Nhóm Code & Hạ tầng AI**: Bùi Minh Trung (Lead)
  * **Nhóm Test Game, Demo & Fix Idea**: Trần Lê Minh Tâm (Lead)
  * **Nhóm Nhật ký & Rà soát Số liệu Thực nghiệm**: Nguyễn Thành Tài (phối hợp cập nhật Sheets/Docs)
  * **Nhóm Báo cáo Google Docs, Slide PPT & Kịch bản**: Chương Gia Thịnh & Nguyễn Thành Tài (cùng chỉnh sửa trên Google Docs và PowerPoint dưới sự rà soát của Nhóm trưởng)

* **Trục ngang (Horizontal Micro-Tasks)**: Chia nhỏ từng đầu việc xuyên suốt từ đầu đến cuối cho từng thành viên:

| Giai đoạn / Task nhỏ (Trục ngang) | Trung (40%) | Tâm (40%) | Tài (10%) | Thịnh (10%) |
|---|---|---|---|---|
| **M1. Khởi tạo Engine & Luật chơi** | Thiết kế `Connect4` Bitboard 49-bit & `ReferenceConnect4`, Perft Depth 1–6 | Review luật chơi, kiểm thử nước đi hợp lệ | Kiểm tra đối chiếu bảng Perft | Rà soát mô tả toán học $(S, A, T, R)$ trên Google Docs |
| **M2. Xây dựng 6 Cấp độ Tác tử AI** | `HeuristicAgent`, `AlphaBetaAgent`, tối ưu Center-First & Iterative Deepening | `RandomAgent`, `MCTSAgent`, `Connect4PolicyValueNet`, `MixedMCTSAgent` (PUCT), **fix idea cache & timeout** | Đọc hiểu hành vi từng cấp độ để đối chiếu bảng mô tả | Chuẩn hóa bảng phân cấp 6 level trên Slide & Báo cáo |
| **M3. Dữ liệu, Huấn luyện & XAI** | Cài đặt `compute_saliency_map` & lọc rò rỉ dữ liệu | Chạy `gen_data.py`, `train_policy.py` (87.725 mẫu), tinh chỉnh loss & Dirichlet | Cập nhật log quá trình train vào Google Sheets | Bổ sung giải thích quy trình 5 bước vào Google Docs |
| **M4. Giải đấu, Timeout, Elo & Ablation** | Code `match.py` (`best_or_random` timeout), `metrics.py`, cấu hình 100ms 6-level, Ablation A1–A4 & **review/fix lỗi self-play Elo, cache 60 FPS** | Cài đặt **Bradley-Terry MLE Elo (`compute_elo.py`)**, chế độ CLI solo AI-vs-AI & **test game thực tế trên Pygame/Web** | Ghi chép bảng kết quả, đối chiếu log CSV/Elo trên Google Drive & Google Sheets (5 sheets) | Rà soát bảng biểu thống kê & Elo đưa lên Slide |
| **M5. UI, Video Demo & Tài liệu** | Web Server RESTful (`http.server`), khung tổng thể Báo cáo (Google Docs) & Slide gốc, chuẩn hóa GitHub `.github/` | Pygame GUI 60 FPS (**2-slot AI vs AI, Start/Pause, khai cuộc 4-ply, cập nhật Elo thực tế**), **test game + quay Video Demo** | **Chỉnh sửa Báo cáo (Google Docs) & chỉnh sửa file PPT** (Chương 4–5, bảng số liệu & Elo) | **Chỉnh sửa Báo cáo (Google Docs) & chỉnh sửa file PPT** (Chương 1–3, Tài liệu tham khảo Hunter 2004 / Elo 1978, Kịch bản) |

---

## 3. Nhật ký Cộng tác & Tiến độ Hàng tuần (Team Work Log)

| Tuần | Thành viên | Công việc đã thực hiện (Task cụ thể) | Minh chứng đầu ra | Khó khăn / Bài học rút ra |
|:---:|---|---|---|---|
| **Tuần 1** | Trung, Tâm, Tài, Thịnh | Thống nhất đề tài Connect Four 7×6, lập Đề cương (`ConnectFour_Proposal_Nhom13.pdf`), thiết lập GitHub & cấu trúc thư mục `src/c4/`. | Repo GitHub + Proposal PDF | Hiểu rõ giới hạn $4,53 \times 10^{12}$ trạng thái; thống nhất API `Connect4Base` ngay từ đầu. |
| **Tuần 2** | Trung | Cài đặt `Connect4` Bitboard 49-bit, `ReferenceConnect4`, `HeuristicAgent`, `AlphaBetaAgent` và 10.000 ván kiểm thử chéo + Perft. | `engine.py`, `test_engine.py`, `test_crosscheck.py` | Phải đặt 1 bit đệm (sentinel bit) ở đỉnh mỗi cột để phép dịch bit kiểm tra thắng không bị tràn sang cột bên. |
| **Tuần 2** | Tâm | Cài đặt `RandomAgent`, `MCTSAgent` (UCT 4 pha), giao diện Pygame 60 FPS (`gui.py`). | `mcts.py`, `gui.py`, `test_mcts.py` | Rollout ngẫu nhiên bị tốn thời gian nếu không gọi Bitboard clone nhanh. |
| **Tuần 3** | Tâm, Trung | Xây dựng Data Pipeline 5 bước chống rò rỉ gương, huấn luyện `Connect4PolicyValueNet` (3 ResBlocks), cài đặt `MixedMCTSAgent` (PUCT + Cache) & Saliency XAI. | `policy_net_best.pt`, `explain.py`, `test_nn_and_puct.py` | Phát hiện và sửa lỗi nhiễu Dirichlet làm bẩn Transposition Cache bằng `priors.copy()`. |
| **Tuần 4** | Trung, Tâm | Hoàn thiện Web Server (`http.server`), chạy giải đấu 3.000 ván không giới hạn thời gian + 300 ván timed + Ablation A1–A4; **Tâm test game thực tế & chuẩn bị kịch bản quay Video Demo**. | `results/logs/*.csv`, `results/figures/*.png`, `DEMO_GUIDE.md` | Giải đấu timed cần chạy tuần tự 1 luồng (`workers=1`) để không bị nhiễu bộ đếm ms do tranh chấp CPU. |
| **Tuần 5** | Trung, Tâm | Cập nhật `match.py` & các agent xử lý an toàn `timeout_policy="best_or_random"` (tránh crash khi `root.children` rỗng, fallback random nếu chưa xong bước 1); chạy **Giải đấu 6 Level giới hạn 100 ms/nước (100 ván/cặp)**; **Tâm test game & quay Video Demo hoàn chỉnh**. | `configs/tournament_levels_timed.yaml`, `results/tables/round_robin_levels_timed_summary.csv`, Video Demo | Nếu thời gian quá ngắn chưa kịp 1 mô phỏng, MCTS/PUCT dễ bị lỗi `max()` rỗng nếu không có nhánh fallback random an toàn. |
| **Tuần 6** | Tài, Thịnh, Trung | Lập **Nhật ký thí nghiệm Excel/Sheets** và đồng bộ kết quả lên **Google Drive**; chuẩn hóa repo GitHub (`CONTRIBUTING.md`, Issue/PR templates, CI); **Tài & Thịnh chỉnh sửa Báo cáo trên Google Docs, Slide PowerPoint & Kịch bản trình bày**. | Google Docs, Google Drive, Google Sheets, `BAO_CAO_DO_AN_CUOI_KY.docx`, `SLIDE_THUYET_TRINH_CONNECT_FOUR_NHOM13.pptx` | Chuẩn hóa bảng trích dẫn tài liệu tham khảo, Danh mục từ viết tắt và vẽ lại sơ đồ khối trực quan theo chuẩn báo cáo khoa học. |
| **Tuần 7** | Tâm, Trung, Tài, Thịnh | **Tâm** mở nhánh `feature/tam-ai-solo-elo` cài đặt **Hệ thống Xếp hạng Elo Bradley-Terry MLE (`compute_elo.py`)** + nâng cấp **Pygame GUI 2-Slot AI vs AI** (Start/Pause, khai cuộc 4-ply ngẫu nhiên, vector tròn, cập nhật Elo thực tế); **Trung** review code PR & sửa 4 lỗi (cờ `--games` trong `RUN_FAST.bat`, bảo vệ self-play Elo, cache Elo 60 FPS, chuẩn hóa mốc 3.000 ván), đồng bộ Báo cáo, Slide 37 trang, Excel 5 sheet (`Working_details_excel` style) và đóng gói `.zip`. | Commit `b32b327..63ade50`, `scripts/compute_elo.py`, `results/elo_ratings.json`, `elo_comparison_default_vs_100ms.png`, `NHAT_KY_THI_NGHIEM.xlsx` (5 sheets) | Đọc JSON Elo ở mỗi frame 60 FPS gây thừa I/O và self-play `p1 == p2` gây ghi đè sai dấu `-delta`; việc review chéo PR trước khi merge giúp bắt và sửa dứt điểm trước khi đưa vào báo cáo. |

---

## 4. Khung Đánh giá Dựa vào Người Yếu Nhất (Số liệu Quá trình Học tập)

Để bảo đảm mọi thành viên đều nắm được kiến thức cốt lõi của đồ án (không xảy ra tình trạng 1–2 người làm hết còn các bạn khác không hiểu bài khi giảng viên hỏi vấn đáp), nhóm áp dụng **thước đo đánh giá dựa vào năng lực của thành viên có điểm thấp nhất (Weakest-Link Evaluation)**:

1. **Bộ chỉ số quá trình học tập theo từng cá nhân (Learning Process Metrics)**:

| Tiêu chí đánh giá quá trình | Trọng số | Cách đo lường bằng số liệu | Mức sàn tối thiểu (Ngưỡng đạt cho thành viên yếu nhất) |
|---|:---:|---|---|
| **C1. Hiểu kiến trúc & Luật chơi (Bitboard / S-A-T-R / Elo)** | 25% | Trả lời đúng câu hỏi chéo trong nhóm về cấu trúc 49-bit, 6 cấp độ AI & ý nghĩa thang Elo Bradley-Terry | Giải thích được vai trò của 6 cấp độ AI, tại sao cần đổi bên Đỏ/Vàng và tại sao Mixed-MCTS giảm Elo dưới 100 ms |
| **C2. Thực hành chạy & kiểm tra kết quả (Test / Elo / Log)** | 25% | Tự mở được Web/Pygame demo qua `RUN_FAST.bat`, tự chạy mục `[5] Elo` và ghi được 1 dòng log vào Google Sheets | Tự chạy được ít nhất 1 lệnh kiểm thử (`pytest`, `compute_elo.py` hoặc `web_server`) và đọc hiểu 1 bảng kết quả CSV |
| **C3. Đóng góp tài liệu & Kiểm tra chéo (Docs / Slide)** | 25% | Số mục chỉnh sửa thực tế trên Google Docs & PPTX + độ chính xác đối chiếu số liệu | Tự sửa đúng và không sai lệch số liệu giữa Báo cáo, Slide và file log CSV gốc |
| **C4. Kỷ luật nhật ký & Tiến độ đúng hạn** | 25% | Hoàn thành đầy đủ dòng nhật ký tuần, đúng deadline chỉnh sửa tài liệu | 100% tuần có cập nhật nhật ký và tham gia tập dượt thuyết trình trước buổi bảo vệ |

2. **Bảng theo dõi điểm quá trình (Ví dụ tự đánh giá chéo trước khi bảo vệ)**:

| Thành viên | C1: Hiểu thuật toán (/10) | C2: Thực hành chạy/log (/10) | C3: Chất lượng chỉnh sửa Docs/PPT (/10) | C4: Nhật ký & Tiến độ (/10) | Điểm TB quá trình | Trạng thái |
|---|:---:|:---:|:---:|:---:|:---:|:---|
| **Bùi Minh Trung** (40%) | 9,5 | 9,5 | 9,0 | 9,5 | **9,38** | Đạt chuẩn |
| **Trần Lê Minh Tâm** (40%) | 9,0 | 9,5 | 8,5 | 9,0 | **9,00** | Đạt chuẩn |
| **Nguyễn Thành Tài** (10%) | 7,5 | 8,0 | 8,0 | 8,5 | **8,00** | Đạt chuẩn sàn (cần nắm kỹ phần giải thích Bảng 5.x khi vấn đáp) |
| **Chương Gia Thịnh** (10%) | 7,5 | 7,5 | 8,5 | 8,5 | **8,00** | Đạt chuẩn sàn (cần nắm kỹ phần Data Pipeline & giới hạn Bitboard khi vấn đáp) |
| **Ngưỡng nhóm (theo người yếu nhất)** | **7,5** | **7,5** | **8,0** | **8,5** | **8,00** | **Cả 4 thành viên đều vượt mức sàn tối thiểu (≥ 7,0)** |
