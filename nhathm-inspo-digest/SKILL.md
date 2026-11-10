---
name: nhathm-inspo-digest
description: Weekly digest and cleanup of Rio's Obsidian Inspiration vault on GitHub claude-vault — summarise the week, pick the 3 ideas most worth trying, archive stale items, send a push. Use for the Friday scheduled run or when Rio asks for the inspo digest.
---

# nhathm-inspo-digest — tổng hợp thứ 6

Chạy trên cloud. Đọc **chỉ frontmatter + mục Rio note / Summary / Next action**. Không mở ảnh.

1. Setup như skill `nhathm-inspo` (add_repo + clone `claude-vault`). `INS=/home/claude/claude-vault/Inspiration`.
2. Thu thập bằng 1 script python (không đọc từng file qua tool): mọi `notes/*.md` → id, title, status, type, effort, related, captured, review, Rio note, Summary, Next action.
3. **Cleanup** (tự làm, liệt kê trong digest):
   - `status: inbox` và `captured` > 30 ngày → `status: archived`, `git mv` note sang `_archive/`.
   - Note trong `_archive/` đã archive > 90 ngày → `git rm` ảnh trong `attachments/`, giữ note (hash còn để chống trùng); thay dòng embed bằng `(ảnh đã xoá YYYY-MM-DD)`.
   - Không bao giờ xoá note.
4. **Digest** → `Inspiration/digests/YYYY-MM-DD.md`:
   - Tuần này: N mới (`[[id title]]`); các mục còn `raw`.
   - **3 việc đáng thử nhất**: ưu tiên mục Rio đã ghi ý định trong Rio note, `related` tới project Rio đang làm, effort thấp, review đến hạn. Mỗi việc 1 dòng: vì sao + next action.
   - Đến hạn review mà chưa đụng tới.
   - Cleanup đã làm.
5. Commit `inspo digest YYYY-MM-DD` → pull --rebase → push.
6. Kết thúc bằng 1–2 dòng (nội dung push): "Inspo tuần này: N mới. Thử: <việc #1>". Luôn gửi, kể cả tuần trống.
