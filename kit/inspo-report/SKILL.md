---
name: "inspo-report"
description: "Build or refresh a private web page (claude.ai artifact) showing every idea in the user's Inspiration vault on GitHub as filterable cards with thumbnails, analysis and next steps; works well on a phone. Use when the user asks to see their ideas, open the idea page, or update it."
---

# inspo-report: trang xem toàn bộ ý tưởng

Sinh một trang HTML từ `Inspiration/` trong vault GitHub của người dùng, publish lên **cùng một artifact claude.ai** mỗi lần (một link cố định, mở được trên điện thoại), và lưu bản sao vào vault. Script làm hết, không đọc từng note.

## Setup
1. **Vault**: dòng `Vault: <owner>/<repo>` trong hướng dẫn Project; không có thì hỏi. `add_repo` (push) rồi clone vào `/home/claude/vault` (đã có thì `git pull`). Chưa có `Inspiration/` → báo người dùng gửi ý tưởng đầu tiên trước (skill `inspo` sẽ khởi tạo), dừng.
2. `SKILL_DIR` = thư mục skill này (dòng "Base directory" khi nạp). `python3 -c "import PIL"` || `pip install --break-system-packages -q pillow`.
3. Git identity trống → `user.name "Claude"`, `user.email "noreply@anthropic.com"`.

## Chạy
1. `python3 -I $SKILL_DIR/scripts/build_report.py /home/claude/vault/Inspiration --out /home/claude/vault/Inspiration/_report/index.html` → in `items`, `bytes`, `due`.
2. Publish artifact:
   - Có `Inspiration/_report/artifact.txt` (URL) → `Artifact action:"read"` URL đó trước, rồi `Artifact publish` với `url` + `file_path` là file index.html. Không truyền `icon`.
   - Chưa có → publish mới với `icon: "lightbulb"`, ghi URL vào `artifact.txt`.
   - Đã có URL thì **không** tạo artifact mới: người dùng cần một link cố định.
3. Commit + push vault `inspo: report YYYY-MM-DD` (pull --rebase trước).
4. Trả lời 1–2 dòng: số ý tưởng, số đến hạn xem lại. Không dán URL (thẻ artifact đã có link). Lần đầu thêm 1 dòng: ghim trang lên thanh bên hoặc lưu link để mở nhanh trên điện thoại.
