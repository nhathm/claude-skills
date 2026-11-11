---
name: "nhathm-inspo"
description: "Analyse and save something Rio found while browsing — an image/screenshot, a short video, or a link (web, Facebook, Threads, X, YouTube…) about AI agents, personal AI setups, Claude skills, video editing, dev tools, design or any idea. Hash/dedupe, analyse, discuss, light research, then save a note to his Obsidian vault via GitHub claude-vault. Use whenever Rio sends such material to keep, in the Inspiration project, or with /nhathm-inspo."
---

# nhathm-inspo — phân tích & lưu 1 inspiration

Rio lướt social, gửi vào thread **ảnh, video ngắn hoặc link**, thường kèm một câu của mình. Giá trị nằm ở **phân tích + ngữ cảnh của Rio**, không phải bản thân tài liệu. Luôn phân tích trước khi lưu. Trả lời tiếng Việt, ngắn, có chính kiến.

**Inspiration là kho ý tưởng cho mọi công việc của Rio** — không chỉ video, và video không chỉ talking-head. Đánh giá mỗi thứ theo giá trị riêng: nó mở ra việc gì, loại nội dung/sản phẩm gì cho Rio. Chỉ so với hệ thống hay skill Rio đang có khi thật sự liên quan (bổ sung một bước, thay một công cụ); không ép mọi thứ vào dự án đang làm, và để `related` trống nếu không liên quan.

## Nơi lưu: GitHub là nguồn ghi duy nhất
Mọi ghi của Claude đi vào repo private `nhathm/claude-vault` (Obsidian vault). Obsidian Git trên Mac pull về, iCloud đưa sang iPhone. **Không ghi trực tiếp vào vault trên Mac.**

Setup (một lần mỗi thread):
1. `add_repo` (access: push) cho `nhathm/claude-vault` và `nhathm/claude-skills`, clone theo hướng dẫn của tool (vd `/home/claude/claude-vault`, `/home/claude/claude-skills`).
2. `pip install --break-system-packages -q imagehash pillow` nếu thiếu; video cần `ffmpeg`.
3. `INS=/home/claude/claude-vault/Inspiration`, `SCAN=/home/claude/claude-skills/nhathm-inspo/scripts/inspo_scan.py`. Quy ước vault: `INS/README.md`.

## 1. Nhận diện đầu vào + dedupe (0 token)
| Đầu vào | Lệnh | "Nhìn" bằng gì |
|---|---|---|
| Ảnh | `python3 -I $SCAN "$INS" --file <ảnh>` | ảnh, 1 lần |
| Video | `python3 -I $SCAN "$INS" --file <video> [--url <link post>]` → tạo `*.sheet.jpg` (6 khung, lưới 3×2) | contact sheet, 1 lần; lời thoại: dùng caption/phụ đề trong khung, hoặc hỏi Rio nếu nội dung nằm ở lời nói |
| Link | `python3 -I $SCAN "$INS" --url <link>` | WebFetch |

- Link mạng xã hội (Facebook, Instagram, Threads, X, TikTok) thường bị chặn đăng nhập. Fetch 1 lần; thất bại → nói rõ, xin Rio screenshot/caption, vẫn lưu tạm với URL. **Không** vòng qua bằng curl, mirror hay cache.
- `duplicate` có giá trị (`sha256` / `url` / `phash`) → báo "đã lưu: <id> <title> (<status>)", hỏi Rio có muốn bổ sung không. **Dừng**, không tạo note mới.
- Không trùng → lấy `new_id`.

## 2. Lưu tạm ngay
Để không mất nếu Rio bỏ dở: note `INS/notes/<id> capture.md`, `status: raw`, `kind`, `source`, hash, `captured`, `## Rio note` chép nguyên câu Rio gửi. Tệp đính kèm:
- ảnh → `attachments/<id>.<ext>`
- video → **chỉ** contact sheet `attachments/<id>.sheet.jpg` (không commit video; ghi `duration` và `source`)
- link → không có tệp.
Commit + push: `inspo: <id> raw`.

## 3. Phân tích theo lăng kính của chủ đề
Xác định chủ đề trước, rồi trả lời các câu hỏi tương ứng (chọn 1–2 lăng kính, đừng ép):

| Chủ đề | Câu hỏi cần trả lời |
|---|---|
| **AI agent / bộ AI cá nhân** | Kiến trúc: trigger, memory/lưu trữ, tool/MCP, model, chạy ở đâu (local/cloud), chi phí. So với hệ của Rio (Obsidian vault + GitHub, skill `nhathm-*`, scheduled task, Claude app/Code): họ làm gì tốt hơn, cái gì nên lấy về, cái gì Rio đã có rồi. |
| **Claude skill / MCP / plugin** | Làm gì, nguồn cài (repo, marketplace), trùng skill nào Rio đang có, đáng cài/tự viết `nhathm-*` không. |
| **Video / motion / content** | Kỹ thuật, template hay cách làm nội dung gì (talking-head, faceless, explainer, motion graphics, 3D…); mở ra loại nội dung nào cho Rio; làm bằng công cụ gì, công sức bao nhiêu. Liên hệ video-studio chỉ khi nó bổ sung một bước trong luồng edit (brief, cắt, âm thanh, màu, hiệu ứng, xuất). |
| **Dev / iOS / tooling** | Giải quyết vấn đề gì, mức trưởng thành, áp dụng cho dự án cá nhân hay công việc. |
| **Design / UI** | Pattern gì, dùng ở đâu. |
| **Khác** | Là gì, vì sao đáng chú ý, bước thử nhỏ nhất. |

Rồi:
- **Category** (mảng việc của Rio, khác `topic`): đọc bảng trong `$INS/categories.md`, chọn 1 hoặc nhiều slug. Không vừa cái nào → đề xuất category mới (slug + tên + mô tả 1 dòng), hỏi Rio; Rio đồng ý thì thêm dòng vào `categories.md` trong cùng commit. Chưa hỏi được (batch/không có Rio) → `khac`.
- **Dedupe ngữ nghĩa**: `grep -ril "<2-3 keyword>" "$INS/notes" "$INS/_archive"` (chỉ xem `title`). Cùng ý tưởng nguồn khác → `duplicate_of: "[[...]]"`, nói Rio.
- **Research nhẹ**: 3–5 web search — nguồn gốc (repo, tác giả, bài gốc), độ khả thi, thứ tương đương.

## 4. Trả lời Rio
3–8 dòng: category · nó là gì · đáng không (có chính kiến) · áp dụng vào đâu cho Rio · next action nhỏ nhất. Trả lời thẳng câu Rio hỏi. Rio muốn bàn tiếp thì bàn.

## 5. Chốt note
Khi Rio nói "lưu"/"ok", hoặc cuối lượt trả lời nếu Rio không phản đối: điền đủ template, `status: inbox`, đổi tên file thành `<id> <tên ngắn 2-4 từ>.md`, ghi kết luận trao đổi vào `## Rio note`. Commit + push: `inspo: <id> <title>`.

Git: `git -C /home/claude/claude-vault pull --rebase -q origin main` trước mỗi commit, sau đó `push origin main`. Bị từ chối → pull --rebase, push lại 1 lần.

## Template
```markdown
---
id: INS-0003
title: "<tiêu đề rõ nghĩa>"
status: inbox            # raw khi mới lưu tạm
kind: image|video|link
type: skill|project|tool|design-pattern|idea|setup
topic: ai-agent|personal-ai|claude-skill|video|dev|ios|design|other
category: [video-editor]   # slug trong categories.md, được nhiều
source: <url hoặc trống>
author: <tác giả/nguồn>
related: "[[...]]"       # project/skill của Rio thật sự liên quan, hoặc trống
effort: 15-phut|1-buoi|1-tuan
tags: [..]
captured: YYYY-MM-DD
processed: YYYY-MM-DD
review: <processed + 7 ngày>
sha256: <file, nếu có>
phash: <ảnh hoặc contact sheet, nếu có>
duration:                # giây, chỉ với video
duplicate_of:
---
![[INS-0003.jpeg|400]]   # video: ![[INS-0003.sheet.jpg|500]]; link: bỏ dòng này

## Rio note
Câu Rio gửi kèm + kết luận sau trao đổi.

## Summary
2–3 câu: là gì, dùng khi nào.

## Analysis
Theo lăng kính ở bước 3 (bullet ngắn).

## Research
- bullet có link

## Next action
- [ ] việc cụ thể, làm được
```

## Quy tắc token
- Mỗi tài liệu chỉ "nhìn" 1 lần (ảnh, contact sheet, hoặc 1 lần fetch). Sau đó chỉ dùng hash/frontmatter.
- Không mở note cũ ngoài frontmatter. Không lưu nội dung inspiration vào memory của Claude — vault là nguồn sự thật.
- Mỗi tài liệu một thread mới là tốt nhất. Nhiều tài liệu một lần → xử lý tuần tự, mỗi cái một commit.