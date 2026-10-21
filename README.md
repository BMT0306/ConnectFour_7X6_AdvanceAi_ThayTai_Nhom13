# Connect Four AI: Multi-Level Game AI System

Đề tài cuối kỳ môn **Trí tuệ Nhân tạo Nâng cao**  
Giảng viên hướng dẫn: **Thầy Tài**  
Nhóm thực hiện: **Nhóm 13**  
Chủ đề: **Xây dựng và đánh giá Game AI đa cấp độ (Connect Four 7×6)**  
Repository: [https://github.com/Kiyoshiiz178/Advance_AI_Thay_Tai_Nhom_13](https://github.com/Kiyoshiiz178/Advance_AI_Thay_Tai_Nhom_13)

---

## 1. Cấu trúc thư mục

```
Connect4/
├── .venv/                   # Môi trường ảo Python
├── requirements.txt         # Danh sách thư viện phụ thuộc
├── configs/                 # Cấu hình giải đấu, huấn luyện, tham số (YAML)
├── src/
│   └── c4/
│       ├── game/            # Engine trò chơi
│       │   ├── engine.py    # Bitboard engine (tối ưu hóa tốc độ cao)
│       │   └── reference.py # Engine mảng 2D tham chiếu (ground truth)
│       ├── agents/          # Các cấp độ AI
│       │   ├── base.py      # Abstract Base Agent
│       │   ├── random_agent.py # Cấp 1: Random baseline
│       │   ├── heuristic.py    # Cấp 2: Rule-based / Heuristic
│       │   ├── alphabeta.py    # Cấp 3: Minimax / Alpha-Beta pruning
│       │   ├── mcts.py         # Cấp 4: Monte Carlo Tree Search (UCT)
│       │   ├── nn_agent.py     # Cấp 5: Neural Network Policy (Supervised)
│       │   └── mixed_mcts.py   # Cấp 7: Mixed MCTS (MCTS + Policy Prior)
│       ├── models/
│       │   └── policy_net.py   # Mạng CNN Policy (PyTorch)
│       ├── train/
│       │   ├── gen_data.py     # Sinh dữ liệu từ Alpha-Beta (epsilon-greedy)
│       │   └── train_policy.py # Huấn luyện mô hình Supervised Learning
│       ├── eval/
│       │   ├── tournament.py   # Khung giải đấu Round-robin
│       │   ├── metrics.py      # Thống kê: Wilson CI, Bootstrap, Latency p95
│       │   └── ablation.py     # Thí nghiệm độ nhạy / Ablation study
│       └── ui/
│           └── app.py          # Giao diện Pygame (Người-Máy & Máy-Máy)
├── tests/                   # Bộ kiểm thử tự động (pytest)
│   ├── test_engine.py       # Kiểm thử tính đúng đắn của Engine & Perft
│   └── test_agents.py       # Kiểm thử logic của các Agent
├── results/                 # Nhật ký thực nghiệm & Biểu đồ
│   ├── logs/                # Log CSV thô của các trận đấu
│   ├── tables/              # Bảng ma trận đối đầu
│   └── figures/             # Biểu đồ phân tích
├── checkpoints/             # Lưu trữ trọng số mô hình đã huấn luyện (.pt)
└── notebooks/               # Phân tích số liệu và sinh đồ thị trực quan
```

---

## 2. Thiết lập môi trường

Hệ thống sử dụng Python 3.10+ (đã kiểm tra tương thích hoàn hảo trên Python 3.13) với các thư viện chính:
- `torch` (PyTorch CPU / GPU)
- `pygame` (Giao diện đồ họa)
- `numpy`, `pandas`, `scipy` (Xử lý dữ liệu & thống kê)
- `matplotlib`, `seaborn` (Trực quan hóa)
- `pytest` (Kiểm thử tự động)
- `pyyaml` (Quản lý cấu hình)

### Kích hoạt môi trường và chạy thử nghiệm
```bash
# Kích hoạt venv (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Chạy toàn bộ kiểm thử
pytest -v tests/
```
