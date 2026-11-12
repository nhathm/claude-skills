---
name: "nhathm-inspo-batch"
description: "Nightly cleanup for Rio's Obsidian Inspiration vault on GitHub claude-vault — finish notes left at status raw (thread abandoned before saving) and process images or videos dropped in Inspiration/_inbox. Use for the scheduled nightly inspo run or 'chạy batch inspo'."
---

# nhathm-inspo-batch (bản vỏ)

Hướng dẫn đầy đủ của skill này **không nằm ở đây** mà ở GitHub `nhathm/claude-skills`, file `nhathm-inspo-batch/SKILL.md`. Bản vỏ chỉ có nhiệm vụ nạp bản đó, để Rio sửa skill bằng cách push lên git mà không phải cập nhật lại claude.ai.

Mỗi lần chạy, làm đúng 3 bước:
1. Lấy repo: nếu `/home/claude/claude-skills` chưa có thì gọi `add_repo` cho `nhathm/claude-skills` (access read) và clone theo hướng dẫn của tool vào `/home/claude/claude-skills`; nếu đã có thì `git -C /home/claude/claude-skills pull -q origin main`.
2. Đọc toàn bộ `/home/claude/claude-skills/nhathm-inspo-batch/SKILL.md` và làm theo **chính xác**. Nội dung đó thay thế bản vỏ này; argument Rio truyền vào skill áp dụng nguyên cho nó.
3. Không lấy được repo (lỗi mạng, quyền) → báo Rio một dòng, dừng. Không tự làm theo trí nhớ.

Chỉ cần cập nhật bản vỏ trên claude.ai khi đổi `description` (lúc nào skill được gọi). Bản vỏ lưu ở `_shells/nhathm-inspo-batch/SKILL.md` trong repo.
