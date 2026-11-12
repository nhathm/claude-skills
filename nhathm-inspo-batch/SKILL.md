---
name: "nhathm-inspo-batch"
description: "Nightly cleanup for an Inspiration vault on GitHub: finish notes left at status raw (chat abandoned before saving) and process images or videos dropped in Inspiration/_inbox. Use for the scheduled nightly inspo run or 'chạy batch inspo'."
---

# nhathm-inspo-batch: dọn dẹp ban đêm

Chạy không có người xem, trên cloud. Không hỏi lại; quyết định hợp lý và ghi lý do vào note. Tuỳ chọn: chỉ chạy khi người dùng tự tạo scheduled task.

1. Setup như skill `nhathm-inspo` (đọc `Vault:` / `Tôi là` trong prompt của scheduled task hoặc hướng dẫn Project; clone vault; cài imagehash; đọc `config.md`, `categories.md`). Đọc `/home/claude/claude-skills/nhathm-inspo/SKILL.md` để lấy template và quy trình. Prompt không có `Vault:` → kết thúc bằng 1 dòng báo thiếu, dừng.
2. Tìm việc (0 token):
   - Note dang dở: `grep -l "^status: raw" "$INS"/notes/*.md`
   - Ảnh/video sót: `python3 -I $SCAN "$INS"` → plan cho `_inbox/`.
   - Không có gì → **dừng ngay**, không thông báo, không commit.
3. Note `raw` (tối đa 10): "nhìn" 1 lần theo `kind`: ảnh hoặc ảnh tóm tắt trong `attachments/`, hoặc fetch `source` nếu là link (bị chặn đăng nhập → giữ `raw`, ghi lý do). Làm bước 3 và 5 của luồng Lưu. Giữ nguyên `## Ghi chú`; thêm dòng "(hoàn tất bởi batch YYYY-MM-DD, đoạn chat không chốt)".
4. Ảnh/video `_inbox` (tối đa 10): trùng → xoá khỏi `_inbox`. Không trùng → bước 2, 3, 5 của luồng Lưu (video: chỉ commit ảnh tóm tắt, xoá video gốc khỏi `_inbox`). Có file `.md/.txt` cùng tên → làm `source` / `## Ghi chú`, rồi xoá file đó.
5. Không xử lý được (ảnh lỗi, không hiểu) → để `status: raw`, ghi lý do trong `## Tóm tắt`, không thử lại quá 3 đêm (đếm bằng dòng ghi chú).
6. Một commit: `inspo batch YYYY-MM-DD: N hoàn tất, M từ inbox, K trùng` → pull --rebase → push.
7. Kết thúc bằng 1 dòng (nội dung push) **chỉ khi có ≥1 note hoàn tất**: "Inspo: đã hoàn tất N mục: <title nổi bật>".
