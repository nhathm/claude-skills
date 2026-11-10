---
name: nhathm-inspo
description: Analyse and save a social-media screenshot (skill, project, tool, design idea) Rio sends into a thread — hash, dedupe, discuss with Rio, light research, save a note to his Obsidian vault via GitHub claude-vault. Use whenever Rio sends an inspiration image, in the Inspiration project, or with /nhathm-inspo.
---

# nhathm-inspo — phân tích & lưu 1 ảnh inspiration

Rio lướt social, gửi ảnh vào thread kèm (hoặc không) một câu của mình. Giá trị nằm ở **phân tích + ngữ cảnh của Rio**, không phải bản thân tấm ảnh. Trả lời tiếng Việt, ngắn, có chính kiến.

## Nơi lưu: GitHub là nguồn ghi duy nhất
Mọi ghi của Claude đi vào repo private `nhathm/claude-vault` (Obsidian vault). Obsidian Git trên Mac tự pull về, iCloud đưa sang iPhone. **Không ghi trực tiếp vào vault trên Mac** — tránh xung đột với Obsidian Git.

Setup (một lần mỗi thread):
1. `add_repo` (access: push) cho `nhathm/claude-vault` và `nhathm/claude-skills`, rồi clone theo hướng dẫn của tool (vd `/home/claude/claude-vault`, `/home/claude/claude-skills`).
2. `pip install --break-system-packages -q imagehash pillow` nếu thiếu.
3. `INS=/home/claude/claude-vault/Inspiration`, `SCAN=/home/claude/claude-skills/nhathm-inspo/scripts/inspo_scan.py`.
Quy ước vault: `INS/README.md`.

## Quy trình
1. **Hash + dedupe trước khi nhìn kỹ (0 token)**: copy ảnh Rio gửi ra file, `python3 -I $SCAN "$INS" --file <ảnh>` → JSON.
   - `duplicate` có giá trị → báo "đã lưu: <id> <title> (<status>)", hỏi Rio có muốn bổ sung ghi chú/mở lại không. **Dừng**, không tạo note mới.
   - Không trùng → lấy `new_id`.
2. **Lưu tạm ngay** (để không mất nếu Rio bỏ dở): ảnh → `INS/attachments/<id>.<ext>`, note `INS/notes/<id> capture.md` với `status: raw`, hash, `captured`, mục `## Rio note` chép nguyên câu Rio gửi (nếu có). Commit + push: `inspo: <id> raw`.
3. **Nhìn ảnh đúng 1 lần**: nó là gì, nguồn/tác giả (watermark, handle), type, chủ đề.
4. **Dedupe ngữ nghĩa**: `grep -ril "<2-3 keyword>" "$INS/notes" "$INS/_archive"` (chỉ xem `title`). Cùng ý tưởng nguồn khác → `duplicate_of: "[[...]]"`, nói Rio.
5. **Research nhẹ**: tối đa 3–5 web search — repo/tool/post gốc, khả thi, thứ tương đương.
6. **Trả lời Rio**: 3–6 dòng — nó là gì, có đáng không, áp dụng vào đâu (project/skill của Rio), next action. Trả lời thẳng câu hỏi Rio đặt ra. Nếu Rio muốn trao đổi tiếp, cứ trao đổi.
7. **Chốt note** (khi Rio nói "lưu"/"ok", hoặc cuối lượt trả lời nếu Rio không phản đối): điền đủ template, `status: inbox`, đổi tên file thành `<id> <tên ngắn 2-4 từ>.md`, ghi kết luận cuộc trao đổi vào `## Rio note`. Commit + push: `inspo: <id> <title>`.

Git: `git -C /home/claude/claude-vault pull --rebase -q origin main` trước mỗi commit; sau commit `push origin main`. Push bị từ chối → pull --rebase rồi push lại 1 lần.

## Template
```markdown
---
id: INS-0003
title: "<tiêu đề rõ nghĩa>"
status: inbox            # raw khi mới lưu tạm
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

## Rio note
Câu Rio gửi kèm + kết luận sau trao đổi.

## Summary
2–3 câu: là gì, dùng khi nào.

## Research
- bullet có link

## Next action
- [ ] việc cụ thể, làm được
```

## Quy tắc token
- Ảnh chỉ nhìn 1 lần; so sánh sau đó dùng hash/frontmatter. Không mở note cũ ngoài frontmatter.
- Không lưu nội dung inspiration vào memory của Claude — vault là nguồn sự thật.
- Mỗi ảnh nên một thread mới. Quá 5 ảnh một lần → xử lý tuần tự, mỗi ảnh một commit.
