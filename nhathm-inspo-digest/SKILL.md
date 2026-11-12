---
name: "nhathm-inspo-digest"
description: "Weekly digest and cleanup of an Inspiration vault on GitHub: summarise the week, pick the 3 ideas most worth trying, archive stale items, send a push. Use for the weekly scheduled inspo run or when the user asks for the inspo digest."
---

# nhathm-inspo-digest: tổng hợp tuần

Chạy trên cloud. Đọc **chỉ frontmatter + mục Ghi chú / Tóm tắt / Việc tiếp theo**. Không mở ảnh. Tuỳ chọn: chỉ chạy khi người dùng tự tạo scheduled task.

1. Setup như skill `nhathm-inspo` (đọc `Vault:` trong prompt của scheduled task hoặc hướng dẫn Project; clone vault; đọc `config.md` để biết bối cảnh và "Hệ thống để so sánh"). Không có `Vault:` → 1 dòng báo thiếu, dừng.
2. Thu thập bằng 1 script python (không đọc từng file qua tool): mọi `notes/*.md` → id, title, status, type, effort, related, captured, captured_by, review, Ghi chú, Tóm tắt, Việc tiếp theo.
3. **Cleanup** (tự làm, liệt kê trong digest):
   - `status: inbox` và `captured` > 30 ngày → `status: archived`, `git mv` note sang `_archive/`.
   - `status: done` hoặc `dropped` và dòng đổi trạng thái cuối trong Ghi chú > 14 ngày → `git mv` sang `_archive/` (giữ status).
   - Note trong `_archive/` đã ở đó > 90 ngày → `git rm` ảnh trong `attachments/`, giữ note (hash còn để chống trùng); thay dòng embed bằng `(ảnh đã xoá YYYY-MM-DD)`.
   - Không bao giờ xoá note.
4. **Digest** → `Inspiration/digests/YYYY-MM-DD.md`:
   - Tuần này: N mới (`[[id title]]`), N xong; các mục còn `raw`.
   - **3 việc đáng thử nhất**: ưu tiên mục người dùng đã ghi ý định trong Ghi chú, `related` tới hệ thống trong `config.md`, effort thấp, đến hạn xem lại. Mỗi việc 1 dòng: vì sao + việc tiếp theo + lệnh `xong <id>` để đánh dấu.
   - Đến hạn xem lại mà chưa đụng tới.
   - Cleanup đã làm.
5. Commit `inspo digest YYYY-MM-DD` → pull --rebase → push.
6. Kết thúc bằng 1–2 dòng (nội dung push): "Inspo tuần này: N mới. Thử: <việc #1>". Luôn gửi, kể cả tuần trống.
