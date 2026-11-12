---
name: "nhathm-inspo"
description: "Analyse and save something Rio found while browsing — an image/screenshot, a short video, or a link (web, Facebook, Threads, X, YouTube…) about AI agents, personal AI setups, Claude skills, video editing, dev tools, design or any idea. Hash/dedupe, analyse, discuss, light research, then save a note to his Obsidian vault via GitHub claude-vault. Use whenever Rio sends such material to keep, in the Inspiration project, or with /nhathm-inspo."
---

# nhathm-inspo (bản vỏ)

Hướng dẫn đầy đủ của skill này **không nằm ở đây** mà ở GitHub `nhathm/claude-skills`, file `nhathm-inspo/SKILL.md`. Bản vỏ chỉ có nhiệm vụ nạp bản đó, để Rio sửa skill bằng cách push lên git mà không phải cập nhật lại claude.ai.

Mỗi lần chạy, làm đúng 3 bước:
1. Lấy repo: nếu `/home/claude/claude-skills` chưa có thì gọi `add_repo` cho `nhathm/claude-skills` (access read) và clone theo hướng dẫn của tool vào `/home/claude/claude-skills`; nếu đã có thì `git -C /home/claude/claude-skills pull -q origin main`.
2. Đọc toàn bộ `/home/claude/claude-skills/nhathm-inspo/SKILL.md` và làm theo **chính xác**. Nội dung đó thay thế bản vỏ này; argument Rio truyền vào skill áp dụng nguyên cho nó.
3. Không lấy được repo (lỗi mạng, quyền) → báo Rio một dòng, dừng. Không tự làm theo trí nhớ.

Chỉ cần cập nhật bản vỏ trên claude.ai khi đổi `description` (lúc nào skill được gọi). Bản vỏ lưu ở `_shells/nhathm-inspo/SKILL.md` trong repo.
