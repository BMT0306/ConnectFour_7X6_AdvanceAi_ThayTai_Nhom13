# Connect Four Game AI (7x6)

Đồ án cuối kỳ môn **Trí tuệ nhân tạo nâng cao**: xây dựng và đánh giá Game AI đa cấp độ
(Random → Heuristic → Alpha-Beta → MCTS → Neural Network) trên Connect Four, kèm giải đấu round-robin
có khoảng tin cậy và ablation.

> Trạng thái: **v0.2 - engine + 4 agent (Random, Heuristic, Alpha-Beta, MCTS) + khung giải đấu + test.** Còn lại: sinh dữ liệu/huấn luyện NN, giao diện, giải đấu chính, ablation (xem `docs/ROADMAP.md`).

## Cài đặt (Python 3.10+)
```bash
git clone <link-repo> && cd connect4-ai
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
pytest -q                         # tất cả phải xanh
```

## Chạy thử
```bash
python -m c4.play --opponent random                       # chơi Người vs Máy trong terminal
python -m c4.eval.cli --a random --b random --openings 100 --seed 0 \
       --out results/logs/random_vs_random.csv            # trận đấu 200 ván, có log thô + thống kê
python -m c4.eval.cli --a alphabeta --b mcts --time-a 0.1 --time-b 0.1 --openings 20   # cùng 100 ms/nước
python -m c4.eval.cli --a alphabeta --b mcts --depth-a 5 --sims-b 1000 --openings 20   # cấu hình mặc định
```

## Cấu trúc
```
src/c4/game/     engine.py (bitboard), reference.py (bản chậm để đối chiếu), base.py (API + quy ước)
src/c4/agents/   base.py (Agent, Budget), random_agent.py, heuristic.py, alphabeta.py, mcts.py, __init__.py (đăng ký)
src/c4/eval/     match.py (ván/trận, khai cuộc, đổi bên), metrics.py (Wilson, bootstrap, p95), cli.py
src/c4/play.py   chơi trong terminal
tests/           unit test; tests/data/positions.csv = bộ vị trí kiểm thử viết tay
configs/ results/ checkpoints/ notebooks/ docs/
```

## API engine (tóm tắt)
```python
from c4.game import Connect4
g = Connect4()
g.legal_actions()      # [0..6]
g.step(3); g.undo()    # thả quân / hoàn tác
g.clone()              # bản sao độc lập
g.is_terminal(); g.winner; g.result(player)   # +1 / 0 / -1 theo góc nhìn player
g.winning_moves(player)                        # cột thắng ngay của player (dùng cho Heuristic)
g.to_array(); g.encode(); g.key(); print(g.render())
```
Quy ước chi tiết: xem `CONTRIBUTING.md`. Cách viết agent mới: kế thừa `c4.agents.base.Agent`, đăng ký vào `AGENTS`.

## Tái lập thí nghiệm
Mọi thí nghiệm có seed và cấu hình ghi trong `configs/`; log thô nằm ở `results/logs/`.
Mã nguồn/ý tưởng kế thừa ghi tại `THIRD_PARTY.md`.

## Danh sách thành viên (Nhóm 13 - CONNECT FOUR 7x6)
**GVHD: Thầy Đỗ Như Tài**

| STT | Họ và tên | MSSV | Vai trò | Nhiệm vụ chính | Tỷ lệ đóng góp |
|---|---|---|---|---|:---:|
| 1 | **Bùi Minh Trung** | 3124720074 | Nhóm Trưởng | Engine (bitboard + reference), kiểm thử, Heuristic, Alpha-Beta, khung giải đấu và thống kê | **32%** |
| 2 | **Trần Lê Minh Tâm** | 3124720064 | Thành viên | Random, MCTS-UCT, sinh dữ liệu & huấn luyện Neural Network, giao diện pygame | **32%** |
| 3 | **Chương Gia Thịnh** | 3124720067 | Thành viên | Chạy thực nghiệm, lưu log CSV, kiểm thử thủ công (`positions.csv`), phân tích ván, video demo | **18%** |
| 4 | **Nguyễn Thành Tài** | 3124720062 | Thành viên | Báo cáo 5 chương, slide thuyết trình, poster A0, tài liệu tham khảo, README, in ấn | **18%** |
| | **TỔNG CỘNG** | | | | **100%** |

## Quy định nộp đề tài cuối kỳ
- File nộp dạng ZIP: `Nhom13_GameAI_Connect4_BuiMinhTrung_3124720074.zip`
- Lệnh tự động đóng gói đúng chuẩn: `python scripts/package_submission.py`
- Bộ sản phẩm bao gồm:
  1. Mã nguồn Python, cấu hình YAML, requirements.txt, bộ test tự động (`pytest`).
  2. Báo cáo hoàn chỉnh (5 chương), slide thuyết trình, poster giới thiệu đề tài (`docs/`).
  3. Log thực nghiệm đối kháng thô CSV, bảng biểu ma trận và biểu đồ trực quan hóa (`results/`).
  4. Script đóng gói, chạy giải đấu và video demo (`scripts/`, `docs/demo/`).
