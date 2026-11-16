## Tóm tắt thay đổi (Làm gì & thuộc Trục nào)
- **Loại công việc (Trục dọc)**: `[ ] Code/AI  [ ] Thực nghiệm/Log  [ ] Báo cáo Google Docs / Slide PPT  [ ] Test Game / Demo`
- **Mô tả ngắn gọn (1–3 câu)**:

## Liên quan Issue
Closes #

## Checklist Bắt Buộc Nhóm 13
- [ ] `pytest -q` xanh 100% (`59/59 passed`) trên máy trước khi push
- [ ] Đã thêm unit test tương ứng cho logic mới (đặc biệt xử lý biên/timeout `best_or_random`)
- [ ] Không tự ý phá vỡ API chuẩn ở `src/c4/game/base.py` hoặc `src/c4/agents/base.py`
- [ ] Nếu là thí nghiệm mới: có file cấu hình trong `configs/`, log thô trong `results/logs/` và cập nhật `docs/NHAT_KY_THI_NGHIEM.csv` (Google Sheets) + Google Drive
- [ ] Nếu sửa Báo cáo / Slide: đồng bộ số liệu với file CSV gốc và bản Google Docs / PPTX
