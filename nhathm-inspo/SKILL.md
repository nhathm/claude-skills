---
name: "nhathm-inspo"
description: "Analyse and save something the user found while browsing (an image/screenshot, a short video, or a link from Facebook, TikTok, Threads, X, YouTube, the web) into their Inspiration vault, an Obsidian folder in their own GitHub repo; also handle the vault commands hỏi:, xong, bỏ, để sau, tìm, thêm vào. Use whenever the user sends such material, in an Inspiration project, or with /nhathm-inspo."
---

# nhathm-inspo: phân tích, lưu và quản lý ý tưởng

Người dùng lướt mạng, gửi vào chat **ảnh, video ngắn hoặc link**, thường kèm một câu. Giá trị nằm ở **phân tích + ngữ cảnh của người dùng**, không phải bản thân tài liệu. Luôn phân tích trước khi lưu. Trả lời bằng ngôn ngữ người dùng đang viết (mặc định tiếng Việt), ngắn, có chính kiến.

Code skill dùng chung cho mọi người; phần riêng của từng người nằm trong vault của họ (`config.md`, `categories.md`).

## Setup (một lần mỗi đoạn chat)
1. **Đọc khai báo** trong hướng dẫn Project (hoặc trong tin nhắn / prompt của scheduled task):
   - `Vault: <owner>/<repo>`: bắt buộc. Không có → hỏi tên repo GitHub, nhắc thêm dòng này vào hướng dẫn Project.
   - `Tôi là <tên>`: người lưu (`captured_by`). Không có → `owner` trong `config.md`.
2. `add_repo` (access: push) cho repo vault, clone theo hướng dẫn của tool vào `/home/claude/<repo>` (đã có thì `git pull -q`). Lỗi quyền → nói rõ: cần kết nối GitHub với Claude và cho phép repo này; dừng.
3. Git identity trống → `user.name "Claude"`, `user.email "noreply@anthropic.com"`.
4. Biến: `SK=/home/claude/claude-skills/nhathm-inspo`, `INS=/home/claude/<repo>/Inspiration`, `SCAN=$SK/scripts/inspo_scan.py`, `CMD=$SK/scripts/inspo_cmd.py`.
5. **Lần đầu** (chưa có `$INS`): copy `$SK/template/*` vào `$INS/`, điền `owner:` trong `config.md` bằng tên ở bước 1 (chưa có tên → hỏi), tạo `notes/.gitkeep`, `attachments/.gitkeep`, `_inbox/.gitkeep`. Commit + push `inspo: khởi tạo vault`. Chào 2 dòng: vault sẵn sàng, gửi ý tưởng đầu tiên đi.
   - Có `$INS` nhưng thiếu `config.md` → copy từ template, điền `owner`, commit cùng thay đổi kế tiếp.
6. **Đọc `$INS/config.md`** (bối cảnh, lăng kính, hệ thống để so sánh) và bảng `$INS/categories.md`. Đây là cách phân tích riêng của vault này.
7. `pip install --break-system-packages -q imagehash pillow` nếu thiếu; video cần `ffmpeg`.

## Nhận lệnh
| Tin nhắn | Làm |
|---|---|
| ảnh / video / link (kèm hoặc không kèm câu) | luồng **Lưu** bên dưới |
| bắt đầu bằng `hỏi:` | bước 1 + 3 + 4 của luồng Lưu, **không** lưu tạm, không commit. Cuối câu trả lời: "Muốn lưu thì nhắn `lưu`." |
| `xong` / `bỏ` / `để sau` + mã hoặc từ khoá | `python3 -I $CMD "$INS" status <id> done\|dropped\|later` |
| `tìm <từ khoá>` | `python3 -I $CMD "$INS" find "<từ khoá>"` → liệt kê `id · title · status`, tối đa 5. Không mở note |
| `thêm vào <mã>: <nội dung>` | `python3 -I $CMD "$INS" append <id> "<nội dung>"` |
| `trang ý tưởng` / mở / cập nhật trang | dùng skill `nhathm-inspo-report` |

- Lệnh nhận **mã** (`INS-…`, hoặc phần đuôi như `0012`) hoặc **từ khoá**. Từ khoá → chạy `find` trước: đúng 1 kết quả thì làm luôn; nhiều kết quả thì liệt kê và hỏi chọn, **không tự đoán**.
- Script trả `error: ambiguous` → liệt kê `candidates` và hỏi.
- Lệnh sửa note: commit + push `inspo: <id> <lệnh>`, trả lời 1 dòng.

## Luồng Lưu

### 1. Nhận diện đầu vào + chống trùng
| Đầu vào | Lệnh | "Nhìn" bằng gì |
|---|---|---|
| Ảnh | `python3 -I $SCAN "$INS" --file <ảnh> --by "<tên>"` | ảnh, 1 lần |
| Video | `python3 -I $SCAN "$INS" --file <video> [--url <link>] --by "<tên>"` → tạo `*.sheet.jpg` (6 khung) | ảnh tóm tắt, 1 lần; lời nói: dùng phụ đề trong khung hoặc hỏi |
| Link | `python3 -I $SCAN "$INS" --url <link> --by "<tên>"` | WebFetch |

- Link mạng xã hội thường bị chặn đăng nhập. Fetch 1 lần; thất bại → nói rõ, xin ảnh chụp màn hình hoặc caption, vẫn lưu tạm với URL. **Không** vòng qua bằng curl, mirror hay cache.
- `duplicate` có giá trị → báo "đã lưu rồi: <id> <title> (<status>)", hỏi có muốn bổ sung không (bổ sung = lệnh `thêm vào`). **Dừng**, không tạo note mới.
- Không trùng → lấy `new_id`.

### 2. Lưu tạm ngay
Để không mất nếu người dùng bỏ dở: note `$INS/notes/<id> capture.md`, `status: raw`, `kind`, `source`, hash, `captured`, `captured_by`, `## Ghi chú` chép nguyên câu người dùng gửi. Tệp đính kèm: ảnh → `attachments/<id>.<ext>`; video → **chỉ** `attachments/<id>.sheet.jpg` (không commit video, ghi `duration`); link → không có tệp. Commit + push `inspo: <id> raw`.

### 3. Phân tích
- Theo **lăng kính trong `config.md`** (chọn 1–2, đừng ép). So với "Hệ thống để so sánh" chỉ khi thật sự liên quan; không liên quan thì để `related` trống.
- **Category**: chọn 1 hoặc nhiều slug trong `categories.md`. Không vừa cái nào → đề xuất category mới (slug, tên, mô tả 1 dòng) và hỏi; đồng ý thì thêm dòng vào `categories.md` trong cùng commit. Không hỏi được (batch) → `khac`.
- **Trùng ý**: `python3 -I $CMD "$INS" find "<2-3 từ khoá>"`. Cùng ý tưởng nguồn khác → `duplicate_of: "[[<id> …]]"`, báo người dùng.
- **Tìm hiểu nhẹ**: 3–5 web search: nguồn gốc (repo, tác giả, bài gốc), độ tin cậy, thứ tương đương.

### 4. Trả lời
3–8 dòng: category · nó là gì · có đáng không (có chính kiến) · áp dụng vào đâu · việc nhỏ nhất nên làm tiếp. Trả lời thẳng câu người dùng hỏi; họ muốn bàn tiếp thì bàn.

### 5. Chốt note
Khi người dùng nói "lưu"/"ok", hoặc cuối lượt trả lời nếu họ không phản đối: điền đủ template, `status: inbox`, đổi tên file thành `<id> <tên ngắn 2-4 từ>.md`, ghi kết luận trao đổi vào `## Ghi chú`. Commit + push `inspo: <id> <title>`.

Git: `git -C <vault> pull --rebase -q origin HEAD` trước mỗi commit, rồi push. Bị từ chối → pull --rebase, push lại 1 lần.

## Template
```markdown
---
id: INS-20261112-2119-rio
title: "<tiêu đề rõ nghĩa>"
status: inbox            # raw · inbox · later · done · dropped · archived
kind: image|video|link
type: skill|project|tool|design-pattern|idea|setup
topic: ai-agent|personal-ai|claude-skill|video|dev|ios|design|other
category: [khac]         # slug trong categories.md, được nhiều
source: <url hoặc trống>
source_author: <tác giả của nguồn>
captured_by: <người lưu>
related: ""              # thứ trong "Hệ thống để so sánh" thật sự liên quan, hoặc trống
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
![[INS-20261112-2119-rio.jpeg|400]]   # video: ![[<id>.sheet.jpg|500]]; link: bỏ dòng này

## Ghi chú
Câu người dùng gửi kèm + kết luận sau trao đổi. Lệnh xong/bỏ/thêm vào ghi thêm dòng có ngày ở cuối mục này.

## Tóm tắt
2–3 câu: là gì, dùng khi nào.

## Phân tích
Theo lăng kính (gạch đầu dòng ngắn).

## Nguồn
- gạch đầu dòng có link

## Việc tiếp theo
- [ ] việc cụ thể, làm được
```

## Quy tắc tiết kiệm
- Mỗi tài liệu chỉ "nhìn" 1 lần (ảnh, ảnh tóm tắt, hoặc 1 lần fetch). Sau đó chỉ dùng hash/frontmatter.
- Không mở note cũ ngoài frontmatter; lệnh dùng script, không sửa note bằng tay.
- Vault là nguồn sự thật; không lưu nội dung ý tưởng vào memory của Claude.
- Nhiều tài liệu một lần → xử lý lần lượt, mỗi cái một commit.
