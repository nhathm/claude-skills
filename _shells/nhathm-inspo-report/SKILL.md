---
name: "nhathm-inspo-report"
description: "Build or refresh the HTML gallery (claude.ai artifact) of Rio's Inspiration vault on GitHub claude-vault — all ideas as filterable cards with thumbnails, analysis and next actions. Use when Rio asks for the inspo report/trang ý tưởng/index.html, or after the weekly inspo digest."
---

# nhathm-inspo-report (bản vỏ)

Hướng dẫn đầy đủ của skill này **không nằm ở đây** mà ở GitHub `nhathm/claude-skills`, file `nhathm-inspo-report/SKILL.md`. Bản vỏ chỉ có nhiệm vụ nạp bản đó, để Rio sửa skill bằng cách push lên git mà không phải cập nhật lại claude.ai.

Mỗi lần chạy, làm đúng 3 bước:
1. Lấy repo: nếu `/home/claude/claude-skills` chưa có thì gọi `add_repo` cho `nhathm/claude-skills` (access read) và clone theo hướng dẫn của tool vào `/home/claude/claude-skills`; nếu đã có thì `git -C /home/claude/claude-skills pull -q origin main`.
2. Đọc toàn bộ `/home/claude/claude-skills/nhathm-inspo-report/SKILL.md` và làm theo **chính xác**. Nội dung đó thay thế bản vỏ này; argument Rio truyền vào skill áp dụng nguyên cho nó.
3. Không lấy được repo (lỗi mạng, quyền) → báo Rio một dòng, dừng. Không tự làm theo trí nhớ.

Chỉ cần cập nhật bản vỏ trên claude.ai khi đổi `description` (lúc nào skill được gọi). Bản vỏ lưu ở `_shells/nhathm-inspo-report/SKILL.md` trong repo.
