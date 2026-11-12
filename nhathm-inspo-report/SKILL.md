---
name: "nhathm-inspo-report"
description: "Build or refresh the private web page (claude.ai artifact) showing every idea in the user's Inspiration vault on GitHub as filterable cards with thumbnails, analysis, next steps and copyable commands; works well on a phone. Use when the user asks to see their ideas, for the trang ý tưởng / inspo report, or after the weekly inspo digest."
---

# nhathm-inspo-report: trang xem toàn bộ ý tưởng

Sinh một trang HTML tự chứa từ `Inspiration/` trong vault GitHub (frontmatter + các mục của note + ảnh đầu tiên thu nhỏ), publish lên **cùng một artifact claude.ai** mỗi lần (một link cố định, mở được trên điện thoại), và lưu bản sao vào vault. Script làm hết, không đọc từng note.

Trang có: lọc theo category, chủ đề, loại, trạng thái, người lưu, thời gian lưu; ý tưởng xong/bỏ/lưu trữ ẩn mặc định; mỗi ý tưởng có nút chép lệnh (`xong …`, `để sau …`, `bỏ …`, `thêm vào …:`) để dán vào chat.

## Setup
1. **Vault**: dòng `Vault: <owner>/<repo>` trong hướng dẫn Project (hoặc tin nhắn / prompt của scheduled task); không có thì hỏi. `add_repo` (push) rồi clone vào `/home/claude/<repo>` (đã có thì `git pull -q`). Chưa có `Inspiration/` → báo người dùng gửi ý tưởng đầu tiên trước (skill `nhathm-inspo` sẽ khởi tạo), dừng.
2. `SK=/home/claude/claude-skills/nhathm-inspo-report`, `INS=/home/claude/<repo>/Inspiration`. `python3 -c "import PIL"` || `pip install --break-system-packages -q pillow`.
3. Git identity trống → `user.name "Claude"`, `user.email "noreply@anthropic.com"`.

## Chạy
1. `python3 -I $SK/scripts/build_report.py "$INS" --out "$INS/_report/index.html" --source <owner>/<repo>` → in JSON `items`, `bytes`, `due`.
2. Publish artifact:
   - Có `$INS/_report/artifact.txt` (URL) → `Artifact action:"read"` URL đó trước (bắt buộc với artifact từ đoạn chat khác), rồi `Artifact publish` với `url` + `file_path` = file index.html. Không truyền `icon`.
   - Chưa có → publish mới với `icon: "lightbulb"`, ghi URL trả về vào `artifact.txt`.
   - Đã có URL thì **không** tạo artifact mới: người dùng cần một link cố định.
3. Commit + push vault `inspo: report YYYY-MM-DD` (gồm `_report/index.html`, `artifact.txt` nếu mới). Pull --rebase trước; bị từ chối thì pull --rebase, push lại 1 lần.
4. Trả lời 1–2 dòng: số ý tưởng, số đến hạn xem lại. Không dán URL (thẻ artifact đã có link). Lần đầu thêm 1 dòng: ghim trang hoặc lưu link để mở nhanh trên điện thoại.
