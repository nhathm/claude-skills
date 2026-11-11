---
name: "nhathm-inspo-report"
description: "Build or refresh the HTML gallery (claude.ai artifact) of Rio's Inspiration vault on GitHub claude-vault — all ideas as filterable cards with thumbnails, analysis and next actions. Use when Rio asks for the inspo report/trang ý tưởng/index.html, or after the weekly inspo digest."
---

# nhathm-inspo-report — trang HTML xem toàn bộ ý tưởng

Sinh một trang HTML tự chứa từ `claude-vault/Inspiration` (frontmatter + các mục của note + ảnh đầu tiên thu nhỏ), publish lên **cùng một artifact claude.ai**, và lưu bản sao vào vault. Script làm hết, không cần đọc từng note → gần như không tốn token.

| Thứ | Ở đâu | Vai trò |
|---|---|---|
| Note, ảnh | `claude-vault/Inspiration/notes`, `attachments` | nguồn sự thật |
| Script | `claude-skills/nhathm-inspo-report/scripts/build_report.py` | công thức |
| Trang | artifact claude.ai (URL trong `Inspiration/_report/artifact.txt`) | chỉ để xem |
| Bản sao | `claude-vault/Inspiration/_report/index.html` | backup, mở offline bằng trình duyệt |

## Setup (một lần mỗi thread)
1. `add_repo` `nhathm/claude-vault` (push) và `nhathm/claude-skills` (read); clone theo hướng dẫn của tool vào `/home/claude/claude-vault`, `/home/claude/claude-skills`. Đã có thì `git pull`.
2. `python3 -c "import PIL"` || `pip install --break-system-packages -q pillow`.

## Chạy
1. `git -C /home/claude/claude-vault pull --rebase -q origin main`
2. `python3 -I /home/claude/claude-skills/nhathm-inspo-report/scripts/build_report.py /home/claude/claude-vault/Inspiration --out /home/claude/claude-vault/Inspiration/_report/index.html` → in JSON `items`, `bytes`, `due`.
3. Publish artifact:
   - Đọc URL trong `Inspiration/_report/artifact.txt`.
   - Có URL: `Artifact action:"read"` URL đó trước (bắt buộc với artifact từ thread khác), rồi `Artifact publish` với `url` + `file_path` = file index.html. Không truyền `icon`.
   - Chưa có: publish mới với `icon: "lightbulb"`, ghi URL trả về vào `artifact.txt`.
   - Không tạo artifact mới khi đã có URL — Rio cần một link cố định.
4. Commit + push vault: `inspo: report YYYY-MM-DD` (gồm `_report/index.html`, `artifact.txt` nếu mới). Pull --rebase trước; bị từ chối thì pull --rebase, push lại 1 lần.
5. Trả lời Rio 1–2 dòng: số ý tưởng, số đến hạn review. Không dán URL (card artifact đã có link).

## Lưu ý
- Trang chỉ để xem; sửa ý tưởng trong Obsidian hoặc qua `nhathm-inspo`.
- Không sửa giao diện trong file HTML — sửa `TEMPLATE` trong script rồi commit `claude-skills`, để lần chạy sau giữ thay đổi.
- Trang > 15MB → giảm `THUMB_W` trong script.
- `_report/` không phải note: `inspo_scan.py` chỉ quét `notes/` và `_archive/`, nên không ảnh hưởng dedupe.
