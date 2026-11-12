---
name: "inspo"
description: "Analyse and save something the user found while browsing (an image/screenshot, a short video or a link from Facebook, TikTok, Threads, X, YouTube, the web) into their Inspiration vault, an Obsidian-style folder in their own GitHub repo. Dedupe, analyse, light research, discuss, then save a note. Use whenever the user sends such material to keep, in an Inspiration project, or with /inspo."
---

# inspo: phân tích và lưu 1 ý tưởng

Người dùng lướt mạng, gửi vào chat **ảnh, video ngắn hoặc link**, thường kèm một câu. Giá trị nằm ở **phân tích + ngữ cảnh của người dùng**, không phải bản thân tài liệu. Luôn phân tích trước khi lưu. Trả lời bằng ngôn ngữ người dùng đang viết (mặc định tiếng Việt), ngắn, có chính kiến.

Đánh giá mỗi thứ theo giá trị riêng: nó mở ra việc gì cho người dùng. Đừng ép mọi thứ vào một chủ đề.

## Setup (một lần mỗi đoạn chat)
1. **Tìm vault**: trong hướng dẫn của Project có dòng `Vault: <owner>/<repo>`. Không có → hỏi người dùng tên repo GitHub, và nhắc họ thêm dòng đó vào hướng dẫn Project để lần sau khỏi hỏi.
2. `add_repo` (access: push) cho repo đó, clone theo hướng dẫn của tool vào `/home/claude/vault`. Lỗi quyền → nói rõ: cần kết nối GitHub với Claude và cho phép repo này; dừng.
3. `git -C /home/claude/vault config user.name` trống → đặt `user.name "Claude"`, `user.email "noreply@anthropic.com"`.
4. `SKILL_DIR` = thư mục của skill này (dòng "Base directory" khi skill được nạp). `INS=/home/claude/vault/Inspiration`, `SCAN=$SKILL_DIR/scripts/inspo_scan.py`.
5. **Lần đầu** (chưa có `$INS`): copy `$SKILL_DIR/template/*` vào `$INS/`, tạo `$INS/notes/.gitkeep`, `$INS/attachments/.gitkeep`, `$INS/_inbox/.gitkeep`. Commit + push `inspo: khởi tạo vault`. Chào người dùng 2 dòng: vault đã sẵn sàng, gửi ảnh/link đầu tiên đi.
6. `pip install --break-system-packages -q imagehash pillow` nếu thiếu; video cần `ffmpeg`.

## 1. Nhận diện đầu vào + chống trùng
| Đầu vào | Lệnh | "Nhìn" bằng gì |
|---|---|---|
| Ảnh | `python3 -I $SCAN "$INS" --file <ảnh>` | ảnh, 1 lần |
| Video | `python3 -I $SCAN "$INS" --file <video> [--url <link>]` → tạo `*.sheet.jpg` (6 khung) | ảnh tóm tắt, 1 lần; lời nói: dùng phụ đề trong khung hoặc hỏi người dùng |
| Link | `python3 -I $SCAN "$INS" --url <link>` | WebFetch |

- Link mạng xã hội thường bị chặn đăng nhập. Fetch 1 lần; thất bại → nói rõ, xin ảnh chụp màn hình hoặc caption, vẫn lưu tạm với URL. **Không** vòng qua bằng curl, mirror hay cache.
- `duplicate` có giá trị → báo "đã lưu rồi: <id> <title>", hỏi có muốn bổ sung không. **Dừng**, không tạo note mới.
- Không trùng → lấy `new_id`.

## 2. Lưu tạm ngay
Để không mất nếu người dùng bỏ dở: note `$INS/notes/<id> capture.md`, `status: raw`, `kind`, `source`, hash, `captured`, `## Ghi chú` chép nguyên câu người dùng gửi. Tệp đính kèm: ảnh → `attachments/<id>.<ext>`; video → **chỉ** `attachments/<id>.sheet.jpg` (không commit video); link → không có tệp. Commit + push `inspo: <id> raw`.

## 3. Phân tích
Xác định loại nội dung, trả lời các câu hỏi hợp (chọn 1–2, đừng ép):

| Loại | Câu hỏi |
|---|---|
| Công cụ / app / AI | Làm gì, miễn phí hay trả phí, dùng thử thế nào, có gì tương tự |
| Nội dung / video / bài viết | Cách làm hay template gì, áp dụng được vào nội dung nào, công sức |
| Mẹo / kiến thức | Điều cốt lõi là gì, có đúng không (kiểm tra nhanh), áp dụng ra sao |
| Sản phẩm / địa điểm / món | Là gì, giá, ở đâu, đáng không |
| Khác | Là gì, vì sao đáng chú ý, bước thử nhỏ nhất |

Rồi:
- **Category**: đọc bảng trong `$INS/categories.md`, chọn 1 hoặc nhiều slug. Không vừa cái nào → đề xuất category mới (slug, tên, mô tả 1 dòng) và hỏi; đồng ý thì thêm dòng vào `categories.md` trong cùng commit.
- **Trùng ý**: `grep -ril "<2-3 từ khoá>" "$INS/notes"` (chỉ xem `title`). Cùng ý tưởng nguồn khác → `duplicate_of: "[[...]]"`, báo người dùng.
- **Tìm hiểu nhẹ**: 3–5 web search: nguồn gốc, độ tin cậy, thứ tương đương.

## 4. Trả lời
3–8 dòng: category · nó là gì · có đáng không (có chính kiến) · áp dụng vào đâu · việc nhỏ nhất nên làm tiếp. Trả lời thẳng câu người dùng hỏi; họ muốn bàn tiếp thì bàn.

## 5. Chốt note
Khi người dùng nói "lưu"/"ok", hoặc cuối lượt trả lời nếu họ không phản đối: điền đủ template, `status: inbox`, đổi tên file thành `<id> <tên ngắn 2-4 từ>.md`, ghi kết luận vào `## Ghi chú`. Commit + push `inspo: <id> <title>`.

Git: `git -C /home/claude/vault pull --rebase -q origin HEAD` trước mỗi commit, rồi push. Bị từ chối → pull --rebase, push lại 1 lần.

## Template
```markdown
---
id: INS-0001
title: "<tiêu đề rõ nghĩa>"
status: inbox            # raw khi mới lưu tạm
kind: image|video|link
type: skill|project|tool|design-pattern|idea|setup
category: [khac]         # slug trong categories.md, được nhiều
source: <url hoặc trống>
author: <tác giả/nguồn>
effort: 15-phut|1-buoi|1-tuan
tags: [..]
captured: YYYY-MM-DD
processed: YYYY-MM-DD
review: <processed + 7 ngày>
sha256: <nếu có file>
phash: <ảnh hoặc ảnh tóm tắt, nếu có>
duration:                # giây, chỉ với video
duplicate_of:
---
![[INS-0001.jpeg|400]]   # video: ![[INS-0001.sheet.jpg|500]]; link: bỏ dòng này

## Ghi chú
Câu người dùng gửi kèm + kết luận sau trao đổi.

## Tóm tắt
2–3 câu: là gì, dùng khi nào.

## Phân tích
Theo bước 3 (gạch đầu dòng ngắn).

## Nguồn
- gạch đầu dòng có link

## Việc tiếp theo
- [ ] việc cụ thể, làm được
```

## Quy tắc tiết kiệm
- Mỗi tài liệu chỉ "nhìn" 1 lần. Sau đó chỉ dùng hash/frontmatter.
- Không mở note cũ ngoài frontmatter. Vault là nguồn sự thật; không lưu nội dung ý tưởng vào memory của Claude.
- Nhiều tài liệu một lần → xử lý lần lượt, mỗi cái một commit.
