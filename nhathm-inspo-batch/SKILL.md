---
name: nhathm-inspo-batch
description: Nightly batch that processes every image waiting in Rio's Obsidian Inspiration vault _inbox — hash, dedupe, analyse, light research, write notes. Use for the scheduled nightly inspo run or when Rio says "chạy batch inspo".
---

# nhathm-inspo-batch — xử lý `_inbox` hằng đêm

Chạy không có người xem. Không hỏi lại; quyết định hợp lý và ghi chú lý do vào note.

1. Tìm vault và script như trong skill `nhathm-inspo` (bảng "Vị trí"). Đọc `nhathm-inspo/SKILL.md` để lấy template note và quy trình từng item.
2. `python3 <script> "$INS"` → plan JSON cho mọi ảnh trong `_inbox/`.
   - `inbox: 0` → **dừng ngay**, không gửi thông báo.
3. Với mỗi item (tối đa 15 mỗi đêm; còn lại để đêm sau):
   - `duplicate` có giá trị → xoá ảnh khỏi `_inbox`, ghi vào log "bỏ qua: trùng <id>".
   - Ngược lại làm bước 3–7 của `nhathm-inspo`. Nếu có `sidecar` (.md/.txt cùng tên) → đọc lấy URL/ghi chú làm `source`, rồi xoá sidecar.
   - Nếu không xử lý được (ảnh lỗi, không hiểu) → tạo note `status: raw`, summary ghi lý do, chuyển ảnh vào attachments như thường.
4. Commit 1 lần: `$GIT add -A && $GIT commit -m "inspo batch YYYY-MM-DD: N mới, M trùng"`.
5. Kết quả ngắn: số mới / trùng / lỗi + danh sách id–title. **Chỉ gửi push khi có ≥1 note mới**, nội dung 1 dòng: "Inspo: đã xử lý N ảnh mới — <title nổi bật nhất>".
