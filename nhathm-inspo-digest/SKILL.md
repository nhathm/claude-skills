---
name: nhathm-inspo-digest
description: Weekly digest and cleanup of Rio's Obsidian Inspiration vault — summarise the week, pick the 3 ideas most worth trying, archive stale items, send a push. Use for the Friday 20:00 scheduled run or when Rio asks for the inspo digest.
---

# nhathm-inspo-digest — tổng hợp thứ 6

Đọc **chỉ frontmatter + mục Summary/Next action**. Không mở ảnh.

1. Tìm vault như skill `nhathm-inspo`. `INS=<vault>/Inspiration`.
2. Thu thập (1 lệnh python/grep, không đọc từng file qua tool): với mọi `notes/*.md` lấy id, title, status, type, effort, related, captured, review, Summary, Next action.
3. **Cleanup** (tự làm, liệt kê trong digest):
   - `status: inbox` và `captured` > 30 ngày → `status: archived`, chuyển note sang `_archive/`.
   - Note trong `_archive/` có ngày archive > 90 ngày → xoá ảnh trong `attachments/`, giữ note (hash còn để chống trùng); sửa dòng embed thành `(ảnh đã xoá YYYY-MM-DD)`.
   - Không bao giờ xoá note.
4. **Digest** → ghi `Inspiration/digests/YYYY-MM-DD.md`:
   - Tuần này: N mới (liệt kê `[[id title]]`).
   - **3 việc đáng thử nhất**: ưu tiên `related` tới project Rio đang làm, effort thấp, review đã đến hạn. Mỗi việc 1 dòng: vì sao + next action.
   - Đến hạn review chưa đụng tới.
   - Cleanup đã làm.
5. Commit bằng `$GIT` (xem skill `nhathm-inspo`): `inspo digest YYYY-MM-DD`.
6. Push notification 1–2 dòng: "Inspo tuần này: N mới. Thử: <việc #1>". Luôn gửi (kể cả tuần trống: "Tuần này chưa có gì mới").
