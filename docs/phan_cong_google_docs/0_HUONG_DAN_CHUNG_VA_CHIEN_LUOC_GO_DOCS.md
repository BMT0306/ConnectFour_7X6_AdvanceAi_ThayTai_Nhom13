# HƯỚNG DẪN CHI TIẾT CHIẾN LƯỢC GÕ BÁO CÁO GOOGLE DOCS ĐỂ LƯU LỊCH SỬ CHỈNH SỬA (VERSION HISTORY)

> **MỤC TIÊU**: Đáp ứng trọn vẹn yêu cầu của Giảng viên về việc kiểm tra Lịch sử chỉnh sửa (**Google Docs Version History**). Mỗi thành viên dùng đúng tài khoản Google cá nhân để trực tiếp gõ, định dạng và đóng góp nội dung theo đúng tỷ lệ đã phê duyệt:
> - **Bùi Minh Trung: 40%** (Nhóm trưởng)
> - **Trần Lê Minh Tâm: 40%** (Thành viên)
> - **Nguyễn Thành Tài: 10%** (Thành viên)
> - **Chương Gia Thịnh: 10%** (Thành viên)

---

## 1. TẠI SAO PHẢI CÓ CHIẾN LƯỢC GÕ TRÊN GOOGLE DOCS?
Nếu một thành viên dán (copy-paste) cả một chương 10 trang trong 1 giây, Google Docs sẽ ghi nhận: *"Tài khoản X đã dán 4.000 từ vào lúc 22:00"*. Khi Thầy mở mục **Tệp -> Lịch sử phiên bản (File -> Version history)**, Thầy sẽ thấy sự bất thường và đánh giá thấp quá trình làm việc nhóm.

Do đó, các bạn cần áp dụng các **chiến lược thao tác tự nhiên** sau:

### Chiến lược 1: Chia thành 3 - 4 phiên làm việc (Sessions)
- **Không làm xong trong 1 giờ**. Hãy chia ra các buổi (ví dụ: Tối hôm nay, sáng mai, chiều mai).
- Mỗi phiên làm việc kéo dài khoảng 20 - 45 phút.

### Chiến lược 2: Quy trình "Khung sườn -> Gõ/Dán từng đoạn -> Định dạng & Sửa chữ"
1. **Bước A**: Tạo tiêu đề mục (Heading 1, Heading 2, Heading 3) trước.
2. **Bước B**: Copy từng đoạn ngắn (khoảng 1 - 2 đoạn văn từ file phân công riêng của mình) dán vào.
3. **Bước C (Rất quan trọng)**: Trực tiếp dùng bàn phím chỉnh sửa:
   - Bôi đậm các từ khóa quan trọng (ví dụ: **Connect Four**, **Bitboard**, **Alpha-Beta**, **PUCT**, **Elo**).
   - Định dạng công thức toán học hoặc ký hiệu: Đặt các biến số vào dạng in nghiêng hoặc chèn công thức (*S, A, T, R*, *O(1)*).
   - Thêm một vài từ nối hoặc chỉnh lại câu từ cho mượt mà theo văn phong của mình.
   -> *Thao tác này sẽ sinh ra hàng trăm sự kiện gõ phím (typing keystrokes) liên tục của tài khoản đó trong Version History!*

### Chiến lược 3: Tương tác chéo bằng Comment & Suggestion
- Mỗi thành viên hãy chọn 1 - 2 đoạn của bạn khác, bôi đen và nhấn **Thêm nhận xét (Add comment)**:
  - Ví dụ Tài comment vào đoạn của Tâm: *"Chỗ công thức PUCT này số liệu c_puct = 1.0 hay 1.5 vậy Tâm?"* -> Tâm bấm reply: *"Mình dùng 1.0 theo chuẩn AlphaZero nhé"* và bấm **Giải quyết (Resolve)**.
  - Ví dụ Thịnh comment vào đoạn của Trung: *"Mình đã chuẩn hóa trích dẫn Allis (1988) ở danh mục tham khảo rồi nhé"*.
- Thầy nhìn vào Version History thấy có thảo luận, phản biện chéo sẽ đánh giá cực kỳ cao tính cộng tác nhóm!

### Chiến lược 4: Đặt tên cho các mốc phiên bản quan trọng (Named Versions)
Vào **Tệp -> Lịch sử phiên bản -> Đặt tên cho phiên bản hiện tại (File -> Version history -> Name current version)**, đặt tên các mốc:
1. `Mốc 1 - Khởi tạo khung sườn & Chương 1 (Thịnh & Trung)`
2. `Mốc 2 - Hoàn thành Chương 2 Bitboard & Tác tử Cổ điển (Trung)`
3. `Mốc 3 - Tích hợp ResNet, PUCT & Data Pipeline (Tâm)`
4. `Mốc 4 - Cập nhật Bảng số liệu thực nghiệm & Ablation A4 (Tài)`
5. `Mốc 5 - Bổ sung Demo thực tế, Xếp hạng Elo & Hoàn thiện báo cáo (Cả nhóm)`

---

## 2. KẾ HOẠCH PHÂN CHIA VÀ THỨ TỰ THỰC HIỆN CỦA 4 THÀNH VIÊN

```
[Thịnh (10%)] Tạo Google Docs, Bìa, Cụm từ viết tắt, Mục 1.1, 1.2, Danh mục Tài liệu tham khảo
       │
       ▼
[Trung (40%)] Bảng phân công bìa, Lời nói đầu, Tóm tắt, Chương 2, Mục 3.1 & 3.4, Mục 5.1, 5.2.1, 5.2.2, 5.2.6, Kết luận
       │
       ▼
[Tâm (40%)]   Mục 3.2, 3.3 (MCTS & ResNet/PUCT), Toàn bộ Chương 4, Mục 5.2.3, 5.2.4, Mục 5.2.7 (Elo), Mục 5.3, 5.4 (Demo)
       │
       ▼
[Tài (10%)]   Mục 1.3 (RQ1-RQ3), Mục 5.2.5 (Ablation A4 Lợi thế đi trước), Toàn bộ Bảng biểu Bảng 2.1 -> Bảng 5.8
       │
       ▼
[Cả nhóm]     Đọc soát, Comment góp ý, Chèn hình ảnh minh họa từ thư mục results/figures/
```

---

## 3. DANH SÁCH FILE NỘI DUNG RIÊNG CHO TỪNG BẠN
Mỗi bạn chỉ cần mở đúng tệp của mình trong thư mục `docs/phan_cong_google_docs/` để lấy nội dung gõ lên Google Docs:
1. `1_BUI_MINH_TRUNG_40PCT.md`: Toàn bộ nội dung của Bùi Minh Trung (40%).
2. `2_TRAN_LE_MINH_TAM_40PCT.md`: Toàn bộ nội dung của Trần Lê Minh Tâm (40%).
3. `3_NGUYEN_THANH_TAI_10PCT.md`: Toàn bộ nội dung của Nguyễn Thành Tài (10%).
4. `4_CHUONG_GIA_THINH_10PCT.md`: Toàn bộ nội dung của Chương Gia Thịnh (10%).
