---
name: nhathm-inspo-batch
description: Nightly cleanup for Rio's Obsidian Inspiration vault on GitHub claude-vault — finish notes left at status raw (thread abandoned before saving) and process images dropped in Inspiration/_inbox. Use for the scheduled nightly inspo run or "chạy batch inspo".
---

# nhathm-inspo-batch — dọn dẹp ban đêm

Chạy không có người xem, trên cloud. Không hỏi lại; quyết định hợp lý và ghi lý do vào note.

1. Setup như skill `nhathm-inspo` (add_repo + clone `claude-vault`, `claude-skills`; cài imagehash). Đọc `claude-skills/nhathm-inspo/SKILL.md` để lấy template và quy trình.
2. Tìm việc (0 token):
   - Note dang dở: `grep -l "^status: raw" "$INS"/notes/*.md`
   - Ảnh sót: `python3 -I $SCAN "$INS"` → plan cho `_inbox/`.
   - Không có gì → **dừng ngay**, không thông báo, không commit.
3. Note `raw` (tối đa 10): nhìn ảnh trong `attachments/` 1 lần, làm bước 3–5 và 7 của `nhathm-inspo`. Giữ nguyên `## Rio note`; thêm dòng "(hoàn tất bởi batch YYYY-MM-DD — thread không chốt)".
4. Ảnh `_inbox` (tối đa 10): trùng → xoá khỏi `_inbox`. Không trùng → như `nhathm-inspo` bước 2–5, 7. Có sidecar `.md/.txt` cùng tên → làm `source`/`Rio note`, rồi xoá sidecar.
5. Không xử lý được (ảnh lỗi, không hiểu) → để `status: raw`, ghi lý do trong Summary, không thử lại quá 3 đêm (đếm bằng dòng ghi chú).
6. Một commit: `inspo batch YYYY-MM-DD: N hoàn tất, M từ inbox, K trùng` → pull --rebase → push.
7. Kết thúc bằng 1 dòng (nội dung push) **chỉ khi có ≥1 note hoàn tất**: "Inspo: đã hoàn tất N mục — <title nổi bật>".
