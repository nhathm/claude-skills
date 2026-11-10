---
name: nhathm-inspo
description: Capture a social-media screenshot (skill, project, tool, design idea) into Rio's Obsidian Inspiration vault right now — hash, dedupe, analyse, light research, write a note. Use when Rio sends an image with "/nhathm-inspo" or "/nhathm-inspo ngay", or asks to save an inspiration image immediately.
---

# nhathm-inspo — xử lý ngay 1 ảnh

Rio lướt social, thấy ảnh hay, muốn lưu ngay thay vì chờ batch đêm. Trả lời bằng tiếng Việt, ngắn.

## Vị trí
| | Cowork (Mac liên kết) | Claude Code trên Mac |
|---|---|---|
| Vault | `$HOME/mnt/NhatHM and Claude` | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/NhatHM and Claude` |
| Script | `$HOME/mnt/ClaudeProjects/claude-skills/nhathm-inspo/scripts/inspo_scan.py` | `~/Documents/Claude Code learning/ClaudeProjects/claude-skills/nhathm-inspo/scripts/inspo_scan.py` |

| Git (`GIT`) | `git --git-dir="$HOME/mnt/ClaudeProjects/.git-dirs/claude-vault" --work-tree="$HOME/mnt/NhatHM and Claude"` | `git -C "<vault>"` |

`INS=<vault>/Inspiration`. File `.git` trong vault trỏ tới đường dẫn Mac, nên trong Cowork phải dùng dạng `--git-dir/--work-tree` ở trên (cần kết nối cả folder `ClaudeProjects`). Nếu vault chưa được kết nối, nhờ Rio "Add folder" (hoặc request folder access) rồi mới làm tiếp. Quy ước đầy đủ: `INS/README.md`.

## Quy trình
1. **Đưa ảnh vào vault**: copy ảnh Rio gửi vào `INS/_inbox/` (chat attachment → device_commit_files).
2. **Hash + dedupe (không tốn token)**: `python3 <script> "$INS"` → JSON. Nếu thiếu thư viện: `pip install --user imagehash pillow`.
   - `duplicate.reason = sha256|phash` → **không tạo note mới**. Báo Rio "đã lưu: <id> <title> (status)", xoá ảnh khỏi `_inbox`. Nếu note cũ đang `archived`, hỏi có muốn mở lại không.
3. **Nhìn ảnh đúng 1 lần**, rút ra: nó là gì, tác giả/nguồn (watermark, handle), type, chủ đề.
4. **Dedupe ngữ nghĩa** (rẻ): `grep -ril "<2-3 keyword>" "$INS/notes" "$INS/_archive"` chỉ đọc frontmatter `title`. Nếu cùng ý tưởng từ nguồn khác → vẫn tạo note nhưng điền `duplicate_of: "[[INS-xxxx ...]]"` và nói Rio.
5. **Research nhẹ**: tối đa 3–5 web search — tìm repo/tool/post gốc, tính khả thi, thứ tương đương. Không fetch trang dài nếu không cần.
6. **Liên kết với việc của Rio**: điền `related` bằng wikilink tới project/skill liên quan (vd `[[video-studio]]`). Chỉ điền khi thật sự liên quan.
7. **Ghi note** `INS/notes/<new_id> <tên ngắn 2-4 từ>.md`, chuyển ảnh sang `INS/attachments/<new_id>.<ext>`. Template:

```markdown
---
id: INS-0003
title: "<tiêu đề rõ nghĩa>"
status: inbox
type: skill|project|tool|design-pattern|idea
source: <url hoặc trống>
author: <tác giả/nguồn>
related: "[[...]]"
effort: 15-phut|1-buoi|1-tuan
tags: [..]
captured: YYYY-MM-DD
processed: YYYY-MM-DD
review: <processed + 7 ngày>
sha256: <full>
phash: <16 hex>
duplicate_of:
---
![[INS-0003.jpeg|400]]

## Summary
2–3 câu: là gì, dùng khi nào.

## Research
- bullet có link

## Next action
- [ ] việc cụ thể, làm được
```
8. **Git** (nếu vault có git): `$GIT add -A && $GIT commit -m "inspo: <id> <title>"`. Không push — Obsidian Git trên Mac lo việc push.
9. Trả lời Rio 2–3 dòng: id, title, next action, link note.

## Quy tắc token
- Ảnh chỉ nhìn 1 lần; mọi so sánh sau đó dùng hash/frontmatter.
- Không đọc lại note cũ ngoài frontmatter. Không lưu nội dung inspiration vào memory của Claude.
- Quá 10 ảnh trong 1 lần → khuyên Rio thả vào `_inbox` để batch xử lý.
