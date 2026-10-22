# tests/data/positions.csv - bộ vị trí kiểm thử thủ công

File này do **TV phụ (không cần code)** bổ sung dần; test `tests/test_positions.py` sẽ TỰ ĐỘNG kiểm tra
mọi dòng. Càng nhiều vị trí đa dạng càng tốt (mục tiêu: >= 30 dòng trước mốc chấm tiến độ).

| Cột | Ý nghĩa |
|---|---|
| `id` | Tên ngắn, không trùng |
| `moves` | Chuỗi cột đã đi, đánh số **1..7**, cách nhau bằng dấu cách (X đi trước, rồi O xen kẽ). Để trống nếu bàn cờ trống |
| `side_to_move` | `X` hoặc `O`, phải khớp số nước đã đi (chẵn -> X, lẻ -> O) |
| `winning_moves` | Các cột (1..7) mà **bên đang đến lượt** thả vào là thắng ngay. Không có thì ghi `-` |
| `blocking_moves` | Các cột (1..7) mà **đối thủ** thả vào sẽ thắng ngay (bên đến lượt cần chặn). Không có thì ghi `-` |
| `note` | Giải thích bằng tiếng Việt vì sao (không dùng dấu phẩy, hoặc đặt cả ô trong dấu ngoặc kép) |

Cách thêm: vẽ bàn cờ ra giấy, tự suy ra đáp án BẰNG TAY, ghi vào CSV, rồi chạy `pytest tests/test_positions.py`.
Nếu test báo sai, hoặc bạn đã nhầm (hãy xem lại), hoặc phát hiện **lỗi engine** (báo cho nhóm trưởng qua GitHub Issue).
