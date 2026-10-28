# Representative Game: AlphaBeta vs MCTS

## 1. Mục tiêu

Mô tả một ván Connect Four 7x6 tiêu biểu giữa hai tác tử AlphaBeta và MCTS, ghi lại chuỗi nước đi, bàn cờ cuối cùng và phân tích nước thắng.

## 2. Cấu hình thử nghiệm

| Tham số | Giá trị |
|---|---|
| Kích thước bàn cờ | 7 cột × 6 hàng |
| Tác tử thứ nhất | AlphaBeta |
| Độ sâu tìm kiếm AlphaBeta | 5 |
| Tác tử thứ hai | MCTS |
| Số lượt mô phỏng MCTS | 1000 mỗi nước |
| Seed | 42 |
| Chuỗi nước mở đầu | 4, 3, 4, 5 |
| Tổng số nước đi | 23 |
| Kết quả | AlphaBeta thắng |

Các cột được đánh số từ 1 đến 7, từ trái sang phải.

## 3. Chuỗi nước đi

Chuỗi nước đi của ván đấu, đánh số cột từ 1 đến 7:

`4, 3, 4, 5, 4, 4, 3, 3, 5, 3, 4, 3, 3, 1, 4, 1, 7, 1, 1, 5, 5, 2, 2`

Bốn nước đầu tiên là thế cờ mở đầu. Sau đó, hai tác tử lần lượt lựa chọn nước đi cho đến khi ván đấu kết thúc.

## 4. Bàn cờ cuối cùng

Ký hiệu:
- `A`: quân của AlphaBeta
- `M`: quân của MCTS
- `.`: ô trống

Các hàng được hiển thị từ trên xuống dưới.

```text
  1 2 3 4 5 6 7
  +-------------+
  | . . A A . . . |
  | . . M A . . . |
  | A . M M A . . |
  | M . M A M . . |
  | M A A A A . . |
  | M M M A M . A |
  +-------------+
```

## 5. Phân tích kết quả

AlphaBeta thắng ở nước đi thứ 23 khi đặt quân vào cột 2. Nước đi này tạo thành bốn quân `A` liên tiếp theo hàng ngang, tại các cột 2, 3, 4 và 5 ở hàng thứ hai tính từ dưới lên.

Ở nước thắng cuối cùng, AlphaBeta tìm kiếm ở độ sâu 5, duyệt 44 nút và trả về giá trị đánh giá 1.000.000. MCTS sử dụng 1.000 mô phỏng cho mỗi nước đi.

Đây là một ván đấu minh họa cách hai tác tử lựa chọn nước đi. Kết quả của một ván đơn lẻ không đủ để kết luận AlphaBeta luôn mạnh hơn MCTS; cần kết hợp với kết quả giải đấu trên nhiều ván để đánh giá công bằng.

## 6. Khả năng tái lập

Ván đấu được tạo bằng hàm `play_game()` trong `src/c4/eval/match.py`, sử dụng thế cờ mở đầu và cấu hình ngân sách tìm kiếm nêu trên.

Khi tái chạy, kết quả có thể phụ thuộc vào cách triển khai seed và tính ngẫu nhiên của tác tử. Vì vậy, nên đối chiếu chuỗi nước đi thực tế nếu cần xác nhận khả năng tái lập hoàn toàn.
