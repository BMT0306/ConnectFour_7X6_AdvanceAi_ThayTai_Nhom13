# PHẦN GÕ GOOGLE DOCS: TRẦN LÊ MINH TÂM (TỶ LỆ ĐÓNG GÓP: 40% - THÀNH VIÊN)

> **Vai trò**: Trục Học sâu, PUCT, Hệ thống Elo & Trải nghiệm Game Demo.
> **Các phần phụ trách gõ lên Google Docs**:
> 1. **Chương 3**: Mục 3.2 (Nhóm tác tử Monte Carlo MCTS-UCT 4 giai đoạn) & Mục 3.3 (Tác tử Học sâu AlphaZero-lite: Dual-Head ResNet + PUCT, Transposition Cache O(1), Dirichlet noise, mã giả `MixedMCTSAgent`).
> 2. **Chương 4**: Toàn bộ Chương 4 (Data Pipeline 5 bước chống rò rỉ gương 87.725 mẫu, Huấn luyện Joint Loss, Bản đồ độ nhạy Saliency Map XAI).
> 3. **Chương 5**:
>    - Mục 5.2.3: Thí nghiệm Ablation A2 (MCTS vs Alpha-Beta độ sâu 4).
>    - Mục 5.2.4: Thí nghiệm Ablation A3 (Bóc tách vai trò Policy Prior và Value Head trong PUCT cho RQ2 & RQ3).
>    - Mục 5.2.7: Chuẩn hóa Sức mạnh Bằng Hệ thống Xếp hạng Elo Bradley-Terry MLE & FIDE Logistic.
>    - Mục 5.3: Đánh giá mối quan hệ đánh đổi: Thông lượng duyệt nút, Độ trễ suy luận và Tỷ lệ thắng.
>    - Mục 5.4: Triển khai Giao diện Ứng dụng và Minh chứng Thực tế Chạy Demo (Web App, Pygame Người vs Máy, Pygame Solo 2-Slot AI vs AI kèm chèn Hình 5.9, 5.10, 5.11).

---
## PHẦN 1: CHƯƠNG 3 (MỤC 3.2 VÀ MỤC 3.3 — MCTS, RESNET & PUCT)

### 3.2. Nhóm tác tử Monte Carlo (MCTS-UCT 4 giai đoạn)

Tác tử Cấp 4 — `MCTSAgent` (`src/c4/agents/mcts.py`) không sử dụng hàm lượng giá 69 cửa sổ mà ước lượng xác suất thắng thông qua cây tìm kiếm bất đối xứng gồm 4 giai đoạn lặp lại trong mỗi lượt mô phỏng:
1. **Selection (Chọn nhánh)**: Xuất phát từ nút gốc, khi nút hiện tại đã mở rộng hết các nước đi hợp lệ và chưa kết thúc, tác tử đi xuống nút con $a$ có chỉ số UCT lớn nhất (Kocsis & Szepesvári, 2006):
   $$\text{UCT}(s, a) = \frac{W(s, a)}{N(s, a)} + c \sqrt{\frac{\ln N(s)}{N(s, a)}}$$
   với hệ số khám phá $c = 1,4 \approx \sqrt{2}$, $N(s, a)$ là số lần đi qua nhánh $(s, a)$ và $W(s, a)$ là tổng điểm thắng tích lũy tính theo góc nhìn của người chơi vừa thực hiện nước đi $a$.
2. **Expansion (Mở rộng)**: Khi gặp một nút chưa kết thúc vẫn còn cột hợp lệ chưa từng được thử (`untried`), tác tử lấy ngẫu nhiên một cột trong danh sách đó để tạo thêm một nút con mới trong cây.
3. **Simulation / Rollout (Mô phỏng ngẫu nhiên)**: Từ trạng thái của nút vừa mở rộng, tác tử thực hiện thả quân ngẫu nhiên liên tiếp trên bản sao Bitboard cho đến khi ván đấu kết thúc để nhận kết quả thắng (`1,0`), hòa (`0,5`) hoặc thua (`0,0`).
4. **Backpropagation (Lan truyền ngược)**: Kết quả của pha mô phỏng được truyền ngược từ nút vừa mở rộng lên tới nút gốc; tại mỗi nút trên đường đi, số lượt thăm $N$ tăng thêm 1 và tổng điểm $W$ được cộng thêm theo đúng chiều người chơi tại nút đó. Khi hoàn thành đủ số lượt mô phỏng quy định, tác tử chọn cột ở gốc có số lượt thăm $N$ cao nhất (tiêu chuẩn *Robust Child*).

### 3.3. Đề xuất Tác tử Học sâu AlphaZero-lite (Dual-Head ResNet + PUCT Search Pseudocode)

#### 3.3.1. Kiến trúc mạng hai đầu `Connect4PolicyValueNet` (`src/c4/models/model.py`)
Để mạng nơ-ron vừa có thể đứng độc lập làm tác tử Cấp 5 (`NNAgent`), vừa làm hàm dẫn đường cho cây tìm kiếm ở Cấp 6 (`MixedMCTSAgent`), nhóm thiết kế kiến trúc mạng tích chập phần dư hai đầu (Dual-Head Residual Network) nhận đầu vào là tensor nhị phân kích thước $2 \times 6 \times 7$:
- **Khối tích chập đầu vào (Stem Block)**: Gồm lớp `Conv2d(in_channels=2, out_channels=64, kernel_size=3, padding=1)` theo sau bởi chuẩn hóa lô `BatchNorm2d(64)` và hàm kích hoạt `ReLU`.
- **Thân mạng gồm 3 khối phần dư (3 Residual Blocks)**: Mỗi khối gồm hai lớp tích chập `Conv2d(64, 64, kernel_size=3, padding=1) + BatchNorm2d(64)` có đường nối tắt cộng trực tiếp đầu vào của khối trước khi qua hàm `ReLU`. Cấu trúc nối tắt này giúp mạng trích xuất tốt các mẫu hình quân cờ cả cục bộ lẫn toàn bàn cờ với tổng số tham số gọn nhẹ là **278.952 tham số** (có thể chạy suy luận nhanh trên CPU).
- **Đầu ra chính sách (Policy Head)**: Đi qua lớp giảm chiều `Conv2d(64, 2, kernel_size=1) + BatchNorm2d(2) + ReLU`, trải phẳng thành vector 84 chiều rồi qua lớp tuyến tính `Linear(84, 7)` để xuất ra 7 giá trị logit tương ứng với 7 cột. Trước khi đưa qua hàm `Softmax`, các cột đã đầy trên bàn cờ bị che mặt nạ bằng giá trị $-\infty$ để xác suất rơi vào cột bất hợp lệ luôn bằng `0`.
- **Đầu ra giá trị (Value Head)**: Đi qua lớp `Conv2d(64, 1, kernel_size=1) + BatchNorm2d(1) + ReLU`, trải phẳng thành 42 chiều, qua lớp ẩn `Linear(42, 64) + ReLU` và lớp cuối `Linear(64, 1) + Tanh` để xuất ra giá trị ước lượng thế cờ $V_\theta(s) \in [-1, +1]$ theo góc nhìn của người chơi đang tới lượt.

![Hình 3.1: Sơ đồ kiến trúc mạng tích chập hai đầu Connect4PolicyValueNet (3 khối ResNet)](../results/figures/diagram_resnet_dualhead.png)

#### 3.3.2. Sự cải tiến khi tích hợp mạng học sâu vào cây tìm kiếm PUCT (`MixedMCTSAgent`)
Trong một số nghiên cứu tích hợp học máy vào MCTS trước đây (chẳng hạn như cách tiếp cận *Biased MCTS* trên cờ Othello/Reversi sử dụng mô hình thống kê Bradley-Terry), tri thức học máy thường được đưa vào bằng cách cộng thêm một đại lượng phụ thuộc xác suất mẫu cục bộ vào công thức UCB (*Biased Selection*) và dùng phân phối đó để lấy mẫu trong lúc chạy thử đến cuối ván (*Biased Simulation*).

Trong đồ án này, nhóm áp dụng cơ chế **PUCT (Predictor + UCT)** theo hướng của AlphaGo / AlphaZero (Silver et al., 2016, 2017) trong lớp `MixedMCTSAgent` (`src/c4/agents/mixed_mcts.py`). So với MCTS thuần và Biased MCTS truyền thống, thiết kế của nhóm có ba điểm khác biệt rõ rệt được tóm tắt ở Bảng 3.1:

**Bảng 3.1: So sánh cơ chế giữa MCTS-UCT thuần, Biased MCTS và MixedMCTSAgent (PUCT)**

| Tiêu chí | MCTS-UCT thuần (`MCTSAgent`) | Biased MCTS truyền thống (tham khảo KLTN) | `MixedMCTSAgent` (AlphaZero-lite của nhóm) |
|:---|:---|:---|:---|
| Nguồn tri thức định hướng | Không có (coi mọi nhánh chưa thử như nhau) | Bảng tra xác suất các mẫu hình cục bộ (Pattern Dictionary) | Mạng `Connect4PolicyValueNet` (3 khối ResNet, 278.952 tham số) nhìn toàn bộ bàn cờ $2 \times 6 \times 7$. |
| Công thức chọn nhánh (Selection) | Chỉ số UCT chuẩn với hệ số $c = 1,4$ | Cộng thêm thành phần xác suất mẫu vào UCB | Công thức **PUCT**: nhân trực tiếp xác suất tiên nghiệm $P_\theta(s,a)$ của Policy Head vào thành phần khám phá. |
| Cách đánh giá nút lá (Leaf Evaluation) | Chạy Rollout ngẫu nhiên đến cuối ván | Chạy *Biased Simulation* lấy mẫu theo xác suất | Hỗ trợ cả hai chế độ: dùng trực tiếp **Value Head $V_\theta(s)$** (bỏ hẳn bước Rollout) hoặc kết hợp **Policy Prior + Fast Rollout** để làm thí nghiệm đối chứng. |
| Cơ chế tăng tốc tra cứu $O(1)$ | Không có | Lưu từ điển mẫu ra file nhị phân | Dùng **Bảng băm trạng thái (`Transposition Cache`)** theo khóa Bitboard `key = _pos + _mask` để không phải gọi lại mạng CNN khi gặp lại cùng một thế cờ. |

Tại bước *Selection*, `MixedMCTSAgent` chọn nhánh con $a \in A(s)$ sao cho cực đại hóa công thức PUCT:

$$a^* = \arg\max_{a \in A(s)} \left( Q(s, a) + c_{\text{puct}} \cdot P_\theta(s, a) \cdot \frac{\sqrt{\max\left(1, \sum_{b \in A(s)} N(s, b)\right)}}{1 + N(s, a)} \right)$$

trong đó $Q(s, a) = \frac{W(s, a)}{N(s, a)} \in [-1, +1]$ là giá trị trung bình của nhánh $(s, a)$ (nếu $N(s, a) = 0$ thì $Q(s, a) = 0$), và hệ số mặc định $c_{\text{puct}} = 2,0$. Ở những lượt mô phỏng đầu tiên khi $N(s, a)$ còn nhỏ, thành phần thứ hai chiếm ưu thế và hướng cây tìm kiếm tập trung ngay vào 1–2 cột có xác suất $P_\theta(s, a)$ cao nhất do mạng nơ-ron gợi ý; khi số lượt thăm tăng lên, mẫu số $1 + N(s, a)$ lớn dần và thuật toán chuyển sang tin tưởng vào giá trị thực nghiệm $Q(s, a)$.

Mã giả chi tiết của thuật toán `PUCT_SEARCH` được trình bày dưới đây:

```text
Thuật toán 1: Tìm kiếm cây Monte Carlo có định hướng mạng nơ-ron (PUCT_SEARCH)
---------------------------------------------------------------------------------
Đầu vào : Trạng thái bàn cờ hiện tại s_root, mạng đã huấn luyện f_theta,
          số lượt mô phỏng M (hoặc giới hạn thời gian time_s), hệ số c_puct = 2.0,
          bộ nhớ đệm trạng thái Cache
Đầu ra  : Cột được chọn a* thuộc A(s_root)

1:  Nếu có cột a thuộc A(s_root) giúp thắng ngay trong 1 nước: trả về a
2:  Nếu đối phương có duy nhất 1 cột đe dọa thắng ngay a_block: trả về a_block
3:  Tạo nút gốc root = PUCTNode(state = s_root)
4:  MỞ_RỘNG_VÀ_ĐÁNH_GIÁ_LÁ(root, s_root, is_root = True)
5:  Lặp sim = 1 đến M (hoặc đến khi hết thời gian time_s):
6:      node = root
7:      s = s_root.clone()
8:      // Bước 1: Đi xuống cây theo công thức PUCT (Selection)
9:      Trong khi node đã mở rộng và s chưa kết thúc:
10:         N_parent = tổng N(node, b) với mọi nhánh con b của node
11:         Chọn nhánh con a có giá trị lớn nhất của:
                Q(node, a) + c_puct * P(node, a) * sqrt(max(1, N_parent)) / (1 + N(node, a))
12:         node = node.children[a]
13:         s.step(a)
14:     // Bước 2 & 3: Mở rộng nút mới và lượng giá nút lá (Expansion & Evaluation)
15:     Nếu s là trạng thái kết thúc:
16:         v_leaf = Kết_Quả_Trực_Tiếp(s)   // nhận giá trị trong {-1.0, 0.0, +1.0}
17:     Ngược lại:
18:         v_leaf = MỞ_RỘNG_VÀ_ĐÁNH_GIÁ_LÁ(node, s, is_root = False)
19:     // Bước 4: Lan truyền ngược giá trị lên gốc (Backpropagation)
20:     Trong khi node != None:
21:         node.visits += 1
22:         Nếu node.player_just_moved trùng với người thắng trong v_leaf:
23:             node.value_sum += |v_leaf|
24:         Ngược lại:
25:             node.value_sum -= |v_leaf|
26:         node = node.parent
27: Trả về nhánh a ở gốc có số lượt thăm visits lớn nhất (nếu bằng nhau thì xét Q và P)

Hàm phụ: MỞ_RỘNG_VÀ_ĐÁNH_GIÁ_LÁ(node, s, is_root)
---------------------------------------------------------------------------------
1:  key = (s.current_player, s._pos, s._mask)   // Khóa trạng thái 49-bit duy nhất
2:  Nếu key đã có trong Cache:
3:      (priors, v_net) = Cache[key]
4:  Ngược lại:
5:      (logits, v_net) = f_theta(s.encode())
6:      priors = MaskedSoftmax(logits, s.legal_actions())
7:      Cache[key] = (priors, v_net)
8:  Nếu is_root == True và có bật nhiễu khám phá Dirichlet:
9:      priors = (1 - eps) * priors.copy() + eps * Dirichlet(alpha)
10: Khởi tạo các nút con node.children[a] với xác suất P = priors[a] cho mọi a thuộc A(s)
11: Nếu use_value_head == True: trả về v_net
12: Ngược lại: trả về Fast_Bitboard_Rollout(s)
```

Một chi tiết kỹ thuật quan trọng mà nhóm đã phát hiện và xử lý trong lúc viết unit test là khi bật nhiễu khám phá Dirichlet tại nút gốc (`dirichlet_epsilon > 0`), nếu sửa trực tiếp trên mảng `priors` lấy ra từ `Cache[key]` thì vô tình làm nhiễu luôn xác suất gốc lưu trong bộ nhớ đệm. Do đó ở dòng 9 của hàm phụ, nhóm luôn tạo bản sao `priors.copy()` trước khi trộn nhiễu Dirichlet để giữ cho `Cache` luôn lưu giá trị xác suất chuẩn của mạng.



---
## PHẦN 2: CHƯƠNG 4 — QUY TRÌNH QUẢN TRỊ DỮ LIỆU VÀ MINH BẠCH HÓA AI (XAI)

## CHƯƠNG 4: QUY TRÌNH QUẢN TRỊ DỮ LIỆU VÀ MINH BẠCH HÓA AI (XAI)

### 4.1. Data Pipeline: Mã hóa Tensor, Symmetry Augmentation và Game-level Splitting

Khác với một số trò chơi như cờ vua hay cờ Othello có sẵn các kho biên bản thi đấu quốc tế để tải về huấn luyện, nhóm quyết định tự xây dựng toàn bộ quy trình sinh dữ liệu từ tác tử chuyên gia `AlphaBetaAgent(depth = 4)` thông qua kịch bản `src/c4/train/gen_data.py`. Khi thiết kế quy trình này, nhóm đặc biệt chú ý tránh ba lỗi thường gặp khiến mô hình bị đánh giá ảo: (1) lưu cả các nước đi thăm dò ngẫu nhiên làm nhãn huấn luyện, (2) trộn lẫn các nước đi của cùng một ván vào cả tập Train và tập Test, và (3) để lọt trạng thái đối xứng gương của tập Train sang tập Test.

Quy trình quản trị và tiền xử lý dữ liệu của nhóm gồm 5 bước tuần tự như sau:

1. **Bước 1 — Tự đấu sinh ván cờ có pha khám phá (`2.500` ván, `seed = 42`)**:
   Để tránh việc hai tác tử `AlphaBetaAgent(depth = 4)` tất định chỉ đánh đi đánh lại một kịch bản duy nhất, ở 4 đến 6 nước đi đầu tiên của mỗi ván, chương trình chọn cột ngẫu nhiên (nhưng có kiểm tra để không đi vào nước thua ngay lập tức). Từ sau giai đoạn khai cuộc đến nước thứ 18, với xác suất $\epsilon = 0,14$, bàn cờ sẽ rẽ sang một nhánh ngẫu nhiên để mở rộng độ đa dạng của các thế cờ thu thập được; từ nước thứ 19 trở đi, hai bên đánh hoàn toàn bằng `AlphaBetaAgent(depth = 4)` ($\epsilon = 0$) cho tới khi kết thúc ván để kết quả thắng/hòa/thua cuối ván phản ánh đúng chất lượng thế cờ.
2. **Bước 2 — Gán nhãn chuyên gia sạch (Clean Expert Labels) và mã hóa Tensor $2 \times 6 \times 7$**:
   Tại mỗi trạng thái trong ván đấu, **trước khi** quyết định có tung đồng xu $\epsilon = 0,14$ để đi ngẫu nhiên hay không, chương trình luôn hỏi `AlphaBetaAgent(depth = 4)` xem nước đi tối ưu nhất tại thế cờ đó là cột nào và lưu cột đó làm nhãn chính sách `y_policy`. Nhờ vậy, dù ván cờ có rẽ nhánh để khám phá thế cờ mới, nhãn dạy cho mạng nơ-ron vẫn luôn là nước đi chuẩn của chuyên gia chứ không bị lẫn nước đi ngẫu nhiên. Mỗi trạng thái được mã hóa thành tensor nhị phân $X \in \{0, 1\}^{2 \times 6 \times 7}$ theo góc nhìn của người đang tới lượt: kênh 0 đánh dấu `1` tại các ô có quân của mình, kênh 1 đánh dấu `1` tại các ô có quân của đối phương. Nhãn giá trị `y_value` nhận giá trị $+1,0$ nếu người đang tới lượt tại trạng thái đó thắng vào cuối ván, $-1,0$ nếu thua và $0,0$ nếu hòa.
3. **Bước 3 — Phân chia tập dữ liệu theo đơn vị ván đấu (Game-level Splitting 70/15/15)**:
   Toàn bộ `2.500` ván đấu được chia nguyên ván theo tỷ lệ 70% / 15% / 15%, tương ứng với **1.750 ván cho tập Train**, **375 ván cho tập Validation** và **375 ván cho tập Test**. Việc chia theo ván giúp đảm bảo các trạng thái liên tiếp nhau trong cùng một trận đấu không bao giờ vừa nằm ở tập huấn luyện vừa nằm ở tập kiểm tra.
4. **Bước 4 — Khử trùng lặp theo khóa Bitboard và lọc chéo đối xứng gương**:
   Trong mỗi tập, các trạng thái trùng nhau (xác định bằng khóa `key = _pos + _mask`) được gộp lại thành một mẫu duy nhất: nhãn `y_policy` lấy theo cột xuất hiện nhiều nhất (biểu quyết đa số) và nhãn `y_value` lấy trung bình cộng. Tiếp theo, nhóm lập tập hợp tất cả các khóa trạng thái của tập `Train` cùng với khóa của **bản lật gương ngang** của chúng, rồi quét qua hai tập `Validation` và `Test` để xóa bỏ mọi mẫu trùng lặp (`2.917` mẫu bị lọc khỏi tập `Val` và `3.468` mẫu bị lọc khỏi tập `Test`). Bước này đảm bảo tập `Test` hoàn toàn độc lập, không có bất kỳ thế cờ nào trùng hoặc đối xứng gương với tập `Train`.
5. **Bước 5 — Tăng cường dữ liệu đối xứng lật ngang (Horizontal Flip Symmetry) trên tập Train**:
   Vì bàn cờ Connect Four có tính đối xứng trái – phải qua cột giữa ($c = 3$), một thế cờ có nước đi tốt nhất ở cột $c$ khi lật ngược theo chiều ngang sẽ có nước đi tốt nhất ở cột $6 - c$ và giữ nguyên giá trị thắng thua $z$. Nhóm áp dụng phép lật ngang này trên `37.518` trạng thái gốc của tập `Train` để nhân đôi thành **75.036 mẫu huấn luyện**, trong khi giữ nguyên **6.396 mẫu Validation** và **6.293 mẫu Test** (tổng cộng bộ dữ liệu trong thư mục `data/` gồm **87.725 mẫu sạch**).

### 4.2. Quá trình huấn luyện Joint Loss và trực quan hóa bản đồ độ nhạy Saliency Map

#### 4.2.1. Kiểm định toán học quá trình huấn luyện đa mục tiêu (Joint Loss Validation)

Mạng `Connect4PolicyValueNet` được huấn luyện trong kịch bản `src/c4/train/train_policy.py` bằng cách tối thiểu hóa đồng thời hàm mất mát kết hợp (Joint Loss) của cả hai đầu ra:

$$\mathcal{L}(\theta) = -\sum_{a=0}^{6} \tilde{\pi}_a \log P_\theta(a \mid s) + \lambda_v \left( z - V_\theta(s) \right)^2 + c \|\theta\|_2^2$$

Trong đó, thành phần thứ nhất là hàm mất mát Cross-Entropy giữa phân phối nhãn mục tiêu $\tilde{\pi}$ (đã áp dụng làm mượt nhãn *Label Smoothing* với $\alpha_{\text{ls}} = 0,05$ trên các cột hợp lệ để tránh mạng quá tự tin gây quá khớp) và xác suất dự đoán $P_\theta(a \mid s)$; thành phần thứ hai là sai số bình phương trung bình (MSE) giữa kết cục ván đấu $z \in \{-1, 0, +1\}$ và đầu ra Value Head $V_\theta(s)$ với trọng số cân bằng $\lambda_v = 0,5$; thành phần thứ ba là điều chuẩn trọng số $L_2$ (`weight_decay` $c = 10^{-3}$). Nhóm sử dụng bộ tối ưu `Adam` với tốc độ học ban đầu `lr = 0,0015`, giảm dần theo lịch `CosineAnnealingLR` trong 10 epochs với kích thước lô `batch_size = 256`.

![Hình 4.1: Diễn biến hàm mất mát và độ chính xác trên tập Train và Validation qua 10 epochs](../results/figures/nn_learning_curves.png)

Bảng 4.1 ghi lại chi tiết các chỉ số mất mát và độ chính xác qua từng epoch (trích từ tệp `checkpoints/training_history.json`).

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

Quan sát Hình 4.1 và Bảng 4.1, cả hai đường mất mát Policy Cross-Entropy và Value MSE trên tập Validation đều giảm ổn định từ Epoch 1 đến Epoch 6 và đi ngang ở mức ~1,134 từ Epoch 6 đến Epoch 10 chứ không bị vọt ngược lên, cho thấy việc lọc sạch nhãn và thêm điều chuẩn `weight_decay` + `label_smoothing` đã kiểm soát tốt hiện tượng quá khớp (overfitting).

Khi lấy trọng số tốt nhất tại Epoch 6 (`checkpoints/policy_net_best.pt`) đem đánh giá một lần duy nhất trên **tập Test độc lập (`6.293` mẫu)**:
- **Độ chính xác dự đoán đúng nước đi của chuyên gia (`Test Top-1 Accuracy`)**: đạt **71,68%** (cao gấp khoảng 5 lần so với xác suất đoán ngẫu nhiên 1/7 $\approx$ 14,29%).
- **Độ chính xác trong 2 lựa chọn hàng đầu (`Test Top-2 Accuracy`)**: đạt **89,07%**. Con số gần 90% này rất có ý nghĩa khi ghép vào cây tìm kiếm PUCT, bởi vì nó cho thấy trong 9/10 thế cờ bất kỳ, nước đi tốt nhất của `Alpha-Beta (depth = 4)` đều nằm trong 2 nhánh đầu tiên được mạng nơ-ron ưu tiên mở rộng.
- **Sai số đầu ra giá trị (`Test Value MSE / MAE`)**: đạt `MSE = 0,7884` và `MAE = 0,6360` trên miền $[-1, +1]$; thời gian suy luận trung bình cho một trạng thái trên CPU là `1,909 ms` (`p95 = 2,475 ms`).

#### 4.2.2. Trực quan hóa quyết định của mạng bằng bản đồ độ nhạy Saliency Map (XAI)

Mạng nơ-ron tích chập thường bị xem là "hộp đen" vì khó biết mạng dựa vào ô cờ nào để chọn nước đi. Để làm rõ cơ chế bên trong của `Connect4PolicyValueNet`, nhóm cài đặt hàm `compute_saliency_map` trong tệp `src/c4/models/explain.py` theo phương pháp đạo hàm bậc nhất của Simonyan et al. (2014). Cụ thể, sau khi truyền thẳng tensor trạng thái $X \in \mathbb{R}^{2 \times 6 \times 7}$ để tìm ra cột có xác suất cao nhất $a^* = \arg\max_a z_a(X)$, chương trình tính đạo hàm ngược của logit $z_{a^*}$ theo từng phần tử đầu vào $X_{k, r, c}$ và cộng trị tuyệt đối trên hai kênh quân cờ:

$$S_{r, c} = \sum_{k \in \{0, 1\}} \left| \frac{\partial z_{a^*}(X)}{\partial X_{k, r, c}} \right|, \qquad \hat{S}_{r, c} = \frac{S_{r, c}}{\max_{r', c'} S_{r', c'} + 10^{-8}} \in [0, 1]$$

Giá trị $\hat{S}_{r, c}$ càng gần `1,00` (màu tím/đỏ đậm trên bản đồ nhiệt) chứng tỏ ô cờ $(r, c)$ đó có ảnh hưởng càng quyết định đến việc mạng chọn cột $a^*$. Hình 4.2 minh họa kết quả trích xuất trên hai thế cờ chiến thuật cụ thể.

![Hình 4.2: Bản đồ độ nhạy Saliency Map giải thích quyết định của mạng trên hai thế cờ chiến thuật](../results/figures/xai_saliency_double_threat.png)

1. **Tình huống 1 (Hàng trên của Hình 4.2 — Phát hiện và chặn sớm đòn bẫy hai đầu ở hàng đáy)**:
   - Sau 3 nước đi đầu tiên `moves = [3, 0, 4]`, Quân Đỏ (`X`) đã có 2 quân nằm cạnh nhau ở hàng đáy tại `(Hàng 1, Cột 4)` và `(Hàng 1, Cột 5)` (tính theo nhãn hiển thị từ 1 đến 7), đồng thời hai ô sát bên ở Cột 3 và Cột 6 đều đang trống.
   - Nếu đến lượt Quân Vàng (`O`) mà dùng `HeuristicAgent` (Level 2), do lúc này trên bàn cờ `X` mới chỉ có 2 quân liên tiếp chứ chưa thành chuỗi 3 quân, luật chặn thua của `HeuristicAgent` chưa kích hoạt và nó sẽ đánh vào cột giữa (Cột 4, Hàng 2). Ngay lượt sau, `X` sẽ đánh vào Cột 3 để tạo chuỗi 3 quân mở cả hai đầu tại Cột 2 và Cột 6, khiến `O` chắc chắn thua.
   - Ngược lại, mạng `Connect4PolicyValueNet` dự đoán nước đi cần đánh ngay là **Cột 3** với xác suất cao nhất `54,2%` (và phương án chặn đầu bên kia ở Cột 6 đạt `14,9%`), đồng thời Value Head đánh giá thế cờ của bên đi sau đang hơi bất lợi (`Value = -0,188`). Khi nhìn sang bản đồ nhiệt Saliency ở giữa, ô có độ nhạy cao nhất đạt mức cực đại `1,00` nằm chính xác tại ô trống `(Hàng 1, Cột 3)` và `0,62` tại `(Hàng 1, Cột 2)`, cùng với `0,43` tại quân `X` ở `(Hàng 1, Cột 4)`. Điều này cho thấy mạng đã học được mối liên hệ không gian của thế cờ đe dọa hai đầu mở ở hàng đáy.
2. **Tình huống 2 (Hàng dưới của Hình 4.2 — Nhận diện nước thắng đường chéo bị khuyết ở giữa)**:
   - Ở thế cờ trung cuộc `moves = [0, 1, 1, 2, 3, 2, 3, 3, 3, 6]`, Quân Đỏ (`X`) đã có 3 quân nằm trên đường chéo chính tại `(Hàng 1, Cột 1)`, `(Hàng 2, Cột 2)` và `(Hàng 4, Cột 4)`, chỉ còn thiếu đúng ô ở giữa là `(Hàng 3, Cột 3)`.
   - Mạng nơ-ron tập trung gần như toàn bộ xác suất **98,9% vào Cột 3** kèm ước lượng điểm thắng cao (`Value = +0,601`), và bản đồ độ nhạy cũng làm nổi bật rõ dải ô dọc theo Cột 3, Cột 4 và đường chéo chiến thắng.

---



---
## PHẦN 3: CHƯƠNG 5 (MỤC 5.2.3, 5.2.4, 5.2.7, 5.3 VÀ 5.4 — ABLATION A2/A3, ELO & DEMO GAME)

#### 5.2.3. Thí nghiệm Ablation A2: Tìm điểm giao thoa của MCTS trước Alpha-Beta cố định độ sâu 4

Để trả lời vế thứ hai của **RQ1**, nhóm giữ cố định đối thủ là `AlphaBetaAgent(depth = 4)` và tăng dần ngân sách mô phỏng của `MCTSAgent` qua 5 mốc: `100`, `500`, `1.000`, `2.000` và `5.000` mô phỏng/nước (mỗi mốc đấu 100 ván đối xứng, lưu tại `results/tables/ablation_a2_results.csv`).

**Bảng 5.4: Kết quả Ablation A2 — Tỷ lệ điểm của MCTS-UCT khi tăng số mô phỏng trước Alpha-Beta (depth = 4)**

| Số mô phỏng của MCTS (`Sims`) | Số ván | `MCTS` Thắng | Hòa | `Alpha-Beta (d=4)` Thắng | Điểm của `MCTS` | Khoảng tin cậy Bootstrap 95% | Độ trễ `p95 MCTS` (ms) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| 100 sims | 100 | 5 | 3 | 92 | 0,0650 | `[0,0250; 0,1150]` | 4,62 |
| 500 sims | 100 | 29 | 3 | 68 | 0,3050 | `[0,2200; 0,3950]` | 28,20 |
| 1.000 sims | 100 | 42 | 0 | 58 | 0,4200 | `[0,3200; 0,5200]` | 71,40 |
| **2.000 sims** | **100** | **51** | **6** | **43** | **0,5400** | **`[0,4450; 0,6350]`** | **118,43** |
| **5.000 sims** | **100** | **57** | **3** | **40** | **0,5850** | **`[0,4900; 0,6800]`** | **287,94** |

![Hình 5.4: Đường cong tăng trưởng điểm số của MCTS-UCT theo số lượng mô phỏng trước Alpha-Beta depth 4](../results/figures/ablation_a2_scaling.png)

Từ Hình 5.4, điểm số của `MCTS-UCT` tăng đều đặn khi được cấp thêm số lượt mô phỏng và vượt qua mốc cân bằng `0,50` tại khoảng **1.500 đến 2.000 mô phỏng/nước** (đạt `0,540` ở 2.000 sims và `0,585` ở 5.000 sims).

#### 5.2.4. Thí nghiệm Ablation A3: Bóc tách vai trò của Policy Prior và Value Head trong PUCT (Trả lời RQ2 và RQ3)

Nhằm kiểm tra xem sự cải thiện của `MixedMCTSAgent` đến từ đầu ra xác suất nước đi (Policy Prior) hay đầu ra ước lượng giá trị (Value Head), nhóm thiết lập 4 biến thể và cho mỗi biến thể đấu 100 ván đối xứng với hai mốc chuẩn là `MCTS-UCT (500 sims)` và tác tử thầy `Alpha-Beta (depth = 4)`:
1. `NN_Policy_Only (0 sims)`: Chỉ dùng Policy Head của mạng nơ-ron chọn ngay cột có xác suất cao nhất, không duyệt cây.
2. `MCTS_UCT_Rollout (200 sims)`: MCTS thuần dùng công thức UCT và chạy Rollout ngẫu nhiên với 200 mô phỏng.
3. `PUCT_Prior_Rollout (200 sims)`: Dùng Policy Head $P_\theta(s,a)$ dẫn đường trong công thức PUCT, nhưng tại nút lá dùng Rollout nhanh trên Bitboard.
4. `PUCT_Prior_ValueHead (200 sims)`: Dùng cả Policy Head $P_\theta(s,a)$ trong công thức PUCT lẫn Value Head $V_\theta(s)$ tại nút lá (không chạy Rollout).

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

![Hình 5.5: Kết quả Ablation A3 bóc tách đóng góp của Policy Prior và Value Head ở mức 200 mô phỏng](../results/figures/ablation_a3_puct_value.png)

Từ Bảng 5.5 và Hình 5.5, nhóm rút ra hai nhận xét quan trọng:
- Thứ nhất, khi chỉ có 200 mô phỏng, `MCTS_UCT_Rollout` thuần chỉ đạt `0,325` trước `mcts_500` và `0,145` trước `alphabeta_d4` vì 200 mô phỏng chia đều cho 7 cột là quá ít để tìm ra nước đi tốt. Thậm chí chỉ dùng mạng `NN_Policy_Only` không duyệt cây (`2,99 ms/nước`) đã đạt `0,440` trước `mcts_500` và `0,395` trước `alphabeta_d4`. Khi kết hợp xác suất tiên nghiệm của Policy Head vào cây tìm kiếm 200 mô phỏng (`PUCT_Prior_Rollout` và `PUCT_Prior_ValueHead`), điểm số trước `mcts_500` tăng vọt từ `0,325` lên **0,695 và 0,685** (tăng thêm khoảng 36–37 điểm phần trăm). Đặc biệt, khi đấu với chính tác tử thầy `alphabeta_d4`, cả hai biến thể PUCT đều vượt mốc 0,50 (đạt **0,625** và **0,510**).
- Thứ hai, khi so sánh giữa hai cách đánh giá nút lá trong PUCT, biến thể `PUCT_Prior_Rollout` chạy nhanh hơn gần 3 lần (`151 ms` so với `425 ms`) và đạt điểm cao hơn trước `alphabeta_d4` (`0,625` so với `0,510`). Lý do là ở biến thể `PUCT_Prior_Rollout`, mạng CNN chỉ cần gọi tại các nút trong khi mở rộng để lấy phân phối `priors`, còn tại nút lá mới tạo thì chạy Rollout trên Bitboard rất nhẹ và kiểm tra được trực tiếp điều kiện thắng thua cuối ván; trong khi đó đầu ra `Value Head` của nhóm được huấn luyện có giám sát trên tập dữ liệu 2.500 ván (`Test Value MSE = 0,7884`) nên đôi khi ước lượng chưa thật sát ở các thế cờ chiến thuật phức tạp. Kết quả thực nghiệm này cũng rất khớp với ghi nhận trong bài báo AlphaGo gốc (Silver et al., 2016) khi kết hợp mạng Policy học có giám sát với Rollout nhanh.



#### 5.2.7. Chuẩn hóa Sức mạnh Bằng Hệ thống Xếp hạng Elo (Bradley-Terry MLE & FIDE Logistic)

Chỉ số tỷ lệ điểm trung bình (`Overall Score %`) dù trực quan nhưng có hai hạn chế khoa học: (i) không mang tính tuyến tính trên thang xác suất khi chênh lệch trình độ rất lớn (ví dụ sự cách biệt giữa `0,40%` và `38,50%` lớn hơn rất nhiều so với giữa `60,95%` và `75,00%`), và (ii) khó dự đoán xác suất thắng trực tiếp khi so sánh hai tác tử bất kỳ hoặc cập nhật dần khi đấu thêm ván lẻ. Để khắc phục, nhóm triển khai hệ thống định lượng **Elo Rating** trong kịch bản `scripts/compute_elo.py` (lưu bền vững tại `results/elo_ratings.json` và tích hợp trực tiếp vào chế độ Solo 2-Slot trên giao diện Pygame `src/c4/ui/gui.py`):

1. **Ước lượng toàn cục bằng mô hình Bradley-Terry MLE (Hunter, 2004)**:
   Với ma trận tổng điểm $W_{ij} = \text{Wins}_{ij} + 0,5 \cdot \text{Draws}_{ij}$ và tổng số ván $N_{ij}$ giữa tác tử $i$ và $j$, xác suất $i$ thắng $j$ được mô hình hóa theo tham số thực lực dương $\gamma_i > 0$:
   $$P(i \text{ thắng } j) = \frac{\gamma_i}{\gamma_i + \gamma_j}$$
   Nghiệm hợp lý cực đại (MLE) được tìm bằng thuật toán lặp tối ưu hóa MM (Minorization-Maximization) hội tụ sau 2.000 vòng lặp chuẩn hóa trung bình hình học:
   $$\gamma_i^{(t+1)} = \frac{\sum_{j \ne i} W_{ij}}{\sum_{j \ne i} \frac{N_{ij}}{\gamma_i^{(t)} + \gamma_j^{(t)}}}, \qquad R_i = 400 \cdot \log_{10}(\gamma_i) + C$$
   trong đó hằng số dịch $C$ được chọn để cố định mốc cơ sở **Random Baseline** tại $R_{\text{random}} = 1000,0\text{ Elo}$.
2. **Cập nhật Elo trực tuyến theo chuẩn FIDE Logistic (Elo, 1978)** cho chế độ đấu Solo 2 máy (CLI `--solo` & Pygame GUI 2-Slot có khai cuộc 4-ply ngẫu nhiên):
   $$E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}, \qquad \Delta R_A = K \cdot (S_A - E_A) \quad (K = 32)$$
   Nhóm cũng cài đặt bộ bảo vệ `self-play guard` (khi cho hai tác tử cùng cấp độ tự đấu nhau `p1 == p2` thì giữ nguyên Elo thay vì ghi đè sai dấu `-delta`) và lưu đệm `self.elo_dict` trong RAM trên giao diện Pygame để giữ vững 60 FPS mà không đọc file JSON lặp lại mỗi khung hình.

**Bảng 5.8: Đối chiếu điểm xếp hạng Bradley-Terry MLE Elo giữa Giải Mặc định (3.000 ván) và Giải 100 ms/nước (1.500 ván)**

| Cấp độ Tác tử | Giải Mặc định (3.000 ván) | Elo Mặc định (`Tier`) | Giải 100 ms/nước (1.500 ván) | Elo 100 ms (`Tier`) | Biến động $\Delta\text{Elo}$ |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Level 6: `MixedMCTSAgent` (PUCT)** | `75,00%` (`705-90-205`) | **2114,8** (*Grandmaster*) | `61,10%` (`282-47-171`) | **1988,1** (*Expert*) | **-126,7** |
| **Level 3: `AlphaBetaAgent`** | `74,80%` (`716-64-220`) | **2113,1** (*Grandmaster*) | `78,80%` (`372-44-84`) | **2125,8** (*Grandmaster*) | **+12,7** |
| **Level 4: `MCTSAgent` (UCT)** | `60,95%` (`596-27-377`) | **2004,3** (*Master*) | `63,00%` (`310-10-180`) | **2002,2** (*Master*) | `-2,1` |
| **Level 5: `NNAgent` (0-search)** | `50,35%` (`460-87-453`) | **1922,3** (*Expert*) | `53,20%` (`239-54-207`) | **1929,6** (*Expert*) | `+7,3` |
| **Level 2: `HeuristicAgent`** | `38,50%` (`350-70-580`) | **1822,2** (*Club*) | `43,50%` (`191-53-256`) | **1854,3** (*Club*) | `+32,1` |
| **Level 1: `RandomAgent` (Anchor)** | `0,40%` (`4-0-996`) | **1000,0** (*Novice*) | `0,40%` (`2-0-498`) | **1000,0** (*Novice*) | `0,0` |

![Hình 5.8: So sánh điểm xếp hạng Bradley-Terry MLE Elo và biến động Δ Elo giữa giải Mặc định (3.000 ván) và giới hạn 100 ms/nước (1.500 ván)](../results/figures/elo_comparison_default_vs_100ms.png)

Phân tích thang đo Elo trên Bảng 5.8 và Hình 5.8 mang lại ba hàm ý định lượng sâu sắc hơn tỷ lệ thắng thô:
- **Khoảng cách năng lực dạng bước nhảy logarit**: Việc bổ sung 4 luật phản xạ 1-ply ở `HeuristicAgent` tạo ra bước nhảy khổng lồ **`+822,2 Elo`** so với `RandomAgent` (tương ứng xác suất thắng kỳ vọng $> 99,1\%$). Từ đó, mỗi bước nâng cấp kiến trúc AI tạo ra một nấc thang rõ rệt: mạng học sâu `NNAgent` 0-search vượt `Heuristic` **`+100,1 Elo`** (`1922,3`), tìm kiếm cây `MCTS-1000` cộng thêm **`+82,0 Elo`** (`2004,3`), và nhóm *Grandmaster* (`Alpha-Beta d=5` và `Mixed-MCTS 200 sims`) bứt phá thêm **`+108,8` đến `+110,5 Elo`** (`2113,1` – `2114,8`).
- **Định lượng chính xác "chi phí độ trễ CNN trên CPU"**: Dưới ràng buộc cứng `100 ms/nước`, `MixedMCTSAgent` sụt đúng **`-126,7 Elo`** (rơi từ hạng *Grandmaster* xuống *Expert*, thấp hơn `Alpha-Beta` tới `137,7 Elo`), trong khi `AlphaBetaAgent` tăng thêm **`+12,7 Elo`** lên `2125,8 Elo` nhờ thông lượng Bitboard 49-bit.
- **Khả năng trình diễn & kiểm chứng trực tiếp**: Người dùng có thể mở `RUN_FAST.bat` chọn mục `[5]` để xem bảng Elo hoặc chạy `python scripts/compute_elo.py --solo alphabeta mixed_mcts --games 4 --time 0.1 --watch`, cũng như chọn chế độ *Máy vs Máy* trên Pygame GUI để quan sát biến động Elo sau từng ván đấu thực tế.

### 5.3. Đánh giá mối quan hệ đánh đổi: Thông lượng duyệt nút, Độ trễ suy luận và Tỷ lệ thắng

Để nhìn nhận tổng thể quá trình phát triển tăng dần qua 6 phiên bản tác tử của nhóm (từ `v1` đến `v6`), Bảng 5.9 tổng hợp số nút/mô phỏng trung bình mỗi nước, độ trễ suy luận trung bình (`Mean Latency`), độ trễ phân vị thứ 95 (`p95 Latency`), điểm tổng hợp cùng điểm xếp hạng **Bradley-Terry Elo** ở cả hai kịch bản mặc định và `100 ms/nước`.

**Bảng 5.9: Bảng tổng hợp tiến hóa 6 phiên bản tác tử AI và sự đánh đổi giữa độ trễ suy luận, tỷ lệ thắng và điểm Elo**

| Phiên bản tác tử | Cơ chế suy luận chính | Số nút / mô phỏng TB | Độ trễ TB / `p95` (`ms`) | Điểm Mặc định (`1.000` ván) | Elo Mặc định | Elo `100 ms` ($\Delta$ Elo) | Điểm đối đầu vs `MCTS-1000` | Điểm đối đầu vs `AlphaBeta d=5` |
|:---|:---|---:|---:|:---:|:---:|:---:|:---:|:---:|
| **v1: `RandomAgent`** (L1) | Chọn ngẫu nhiên cột hợp lệ | 1 | `0,006 / 0,012` | `0,40%` | `1000,0` | `1000,0` (`0,0`) | 0,00% | 0,00% |
| **v2: `HeuristicAgent`** (L2) | Luật 4 tầng 1 bước + lọc tự sát | ~14 | `0,121 / 0,248` | `38,50%` | `1822,2` | `1854,3` (`+32,1`) | 23,25% | 16,75% |
| **v3: `NNAgent`** (L5, `0-search`) | Truyền thẳng mạng ResNet 2 đầu | 1 CNN | `2,910 / 3,864` | `50,35%` | `1922,3` | `1929,6` (`+7,3`) | 41,00% | 23,50% |
| **v4: `MCTSAgent`** (L4, `1.000`) | Cây MCTS 4 bước + Rollout | 1.000 | `83,42 / 148,85` | `60,95%` | `2004,3` | `2002,2` (`-2,1`) | *Mốc chuẩn* | 31,50% |
| **v5: `AlphaBetaAgent`** (L3, `d=5`) | Negamax + $\alpha$-$\beta$ + Center-First | ~339 nút | `21,86 / 61,48` | `74,80%` | `2113,1` | **`2125,8` (`+12,7`)** | **68,50%** | *Mốc chuẩn* |
| **v6: `MixedMCTSAgent`** (L6, `200`) | **ResNet 2 đầu + PUCT + Cache $O(1)$** | **200** | **`348,1 / 709,1`** | **`75,00%`** | **`2114,8`** | `1988,1` (`-126,7`) | **62,50%** | **54,25%** |

Từ Bảng 5.9 (cùng phân tích Elo ở Bảng 5.8 và giải `100 ms` ở Bảng 5.6), nhóm rút ra ba nhận xét tổng kết về sự đánh đổi giữa chi phí tính toán và hiệu quả chiến thuật:
1. **Duyệt ít mô phỏng hơn nhưng chất lượng nước đi cao hơn (`v6` so với `v4`)**: Phiên bản `MCTSAgent` thuần (`v4`) phải thực hiện `1.000` lượt mô phỏng mỗi nước nhưng chỉ đạt `60,95%` (`2004,3 Elo`). Trong khi đó, `MixedMCTSAgent` (`v6`) nhờ xác suất tiên nghiệm từ mạng `Connect4PolicyValueNet` dẫn đường chỉ cần chạy **200 lượt mô phỏng/nước** (giảm 5 lần) nhưng đạt **75,00%** (**2114,8 Elo**, tăng **`+110,5 Elo`**) và thắng trực tiếp `v4` với điểm số **62,50%**.
2. **Vai trò bổ trợ giữa mạng nơ-ron và tìm kiếm cây (`v6` so với `v3` và `v5`)**: Khi chỉ dùng mạng nơ-ron độc lập không duyệt cây (`v3`), thời gian phản hồi rất nhanh (`~2,91 ms/nước`, đạt `1922,3 Elo`) và thắng tốt `HeuristicAgent` (`64,25%`), nhưng vẫn kém nhóm duyệt cây sâu khoảng `190 Elo`. Khi đặt mạng nơ-ron đó vào vòng lặp tìm kiếm cây PUCT 200 mô phỏng (`v6`), sức mạnh nhảy vọt thêm **`+192,5 Elo`** lên `2114,8 Elo`, vượt qua cả tác tử thầy `Alpha-Beta` ở độ sâu 4 (`62,50%`) và nhỉnh hơn `Alpha-Beta` ở độ sâu 5 (`54,25%`).
3. **Đánh đổi về độ trễ thực thi trên CPU**: Do mỗi lần mở rộng nút mới chưa có trong `Transposition Cache`, `MixedMCTSAgent` phải chạy 1 lượt ResNet trên CPU (`~1,9 ms`/lần), nên độ trễ trung bình khi chạy đủ 200 sims là `348 ms/nước` (hoặc `151 ms/nước` với biến thể `PUCT_Prior_Rollout`). Khi bị giới hạn cứng `100 ms/nước` trên CPU (Bảng 5.6 & 5.8), `AlphaBetaAgent` là lựa chọn vượt trội nhất (**2125,8 Elo**, `78,80%`), còn ở chế độ tương tác người chơi cho phép chờ 0,3–0,7 giây thì `MixedMCTSAgent` đạt sức mạnh cao nhất (**2114,8 Elo**, `75,00%`).

### 5.4. Triển khai Giao diện Ứng dụng và Minh chứng Thực tế Chạy Demo

Để kiểm chứng toàn bộ hệ thống không chỉ chạy ở mức dòng lệnh thí nghiệm mà còn hoạt động ổn định trong môi trường tương tác trực tiếp với người dùng, nhóm đóng gói 3 giao diện khởi chạy một chạm thông qua tệp `RUN_FAST.bat`: **Web App RESTful** (`http.server` cổng `5000`), **Desktop Pygame 60 FPS** (`src/c4/ui/gui.py`) và **Terminal CLI / Elo Solo** (`c4.play`, `scripts/compute_elo.py`).

1. **Giao diện Web App (`python -m c4.ui.web_server --port 5000`)**:
   - Xây dựng hoàn toàn bằng thư viện chuẩn `http.server` của Python kết hợp HTML/CSS/JS thuần (không phụ thuộc framework nặng), cung cấp các API `/api/state`, `/api/move`, `/api/ai_move`, `/api/undo`, `/api/reset`.
   - Hình 5.9 ghi lại phiên chạy thực tế trên trình duyệt khi người chơi (Quân Đỏ) đối kháng với `MixedMCTSAgent` (Quân Vàng, `200` mô phỏng): hệ thống hiển thị trực tiếp thông số suy luận theo từng nước (`659,69 ms`, `200 sims · WR 77.8% · Cache 9`), hỗ trợ chọn đầy đủ 6 cấp độ AI, đổi bên đi trước/đi sau, hoàn tác (`Đi Lại`) và gợi ý `Máy Đi Hộ Lượt Này`.

![Hình 5.9: Giao diện Web App (localhost:5000) chạy thực tế chế độ Người vs Máy gặp Mixed-MCTS (200 sims, Cache 9)](../results/figures/demo_web_app_ui.png)

2. **Giao diện Desktop Pygame 60 FPS — Chế độ Người vs Máy (`H_VS_AI`)**:
   - Giao diện Pygame mô phỏng vật lý thả quân có trọng lực và độ nảy (`FallingPiece`), hiệu ứng bóng 3D và xem trước cột thả quân (hover preview).
   - Hình 5.10 minh họa ván đấu thực tế giữa Người chơi (Quân Đỏ) và `Cấp 6: Mixed-MCTS (2114,8 Elo)` ở nước thứ `10 / 42`: tác tử tự động thiết lập cột trung tâm 3 quân liên tiếp gây áp lực chiến thuật chỉ trong `558,6 ms` (`sims=200 cache=9`), đồng thời bảng điều khiển bên phải hiển thị điểm Elo chuẩn Bradley-Terry của cả 6 cấp độ.

![Hình 5.10: Giao diện Desktop Pygame 60 FPS chạy thực tế chế độ Người vs Máy gặp Cấp 6 Mixed-MCTS (2114,8 Elo)](../results/figures/demo_pygame_human_vs_ai.png)

3. **Giao diện Desktop Pygame — Chế độ Solo Máy vs Máy 2-Slot & Cập nhật Elo Thời gian Thực (`AI_VS_AI`)**:
   - Phiên bản nâng cấp hỗ trợ 2 tab độc lập `M1` (Quân Đỏ) và `M2` (Quân Vàng) cho phép ghép cặp tự do mọi cấp độ AI, bật/tắt **Khai cuộc 4 nước ngẫu nhiên (phím `O`)** để tránh các cặp đấu tất định bị lặp kịch bản, điều khiển **Bắt đầu / Tạm dừng (phím `Space`/`P`)**, và tự động đánh dấu vòng hào quang xanh ngọc quanh 4 quân chiến thắng.
   - Hình 5.11 ghi lại trận đấu thực tế giữa `M1: Alpha-Beta` và `M2: Mixed-MCTS`: sau 42 lượt giằng co kín bàn cờ (`42 / 42`), `Mixed-MCTS` hoàn tất đường chéo 4 quân chiến thắng ở nước cuối cùng, hệ thống lập tức tính và hiển thị biến động Elo FIDE thực tế (`Elo: alphabeta (-15.9) | mixed_mcts (+15.9)`). Bên cạnh đó, chế độ dòng lệnh `python -m c4.play --opponent alphabeta --depth 4` và mục `[5]` `scripts/compute_elo.py` cũng đã được chạy kiểm chứng hoàn toàn không lỗi runtime.

![Hình 5.11: Chế độ Solo Máy vs Máy 2-Slot trên Pygame giữa Alpha-Beta và Mixed-MCTS kết thúc nước 42/42 kèm cập nhật Elo thời gian thực](../results/figures/demo_pygame_ai_vs_ai_elo.png)

---

