---
name: "nhathm-inspo-report"
description: "Build or refresh the private web page (claude.ai artifact) showing every idea in the user's Inspiration vault on GitHub as filterable cards with thumbnails, analysis, next steps and copyable commands; works well on a phone. Use when the user asks to see their ideas, for the trang ý tưởng / inspo report, or after the weekly inspo digest."
---

# nhathm-inspo-report (bản vỏ)

Hướng dẫn đầy đủ **không nằm ở đây** mà ở repo public `https://github.com/nhathm/claude-skills`, file `nhathm-inspo-report/SKILL.md`. Bản vỏ chỉ nạp bản đó, để skill tự cập nhật khi repo đổi mà không phải cài lại.

Mỗi lần chạy, làm đúng 4 bước:
1. **Kênh**: tìm dòng `Channel: main` hoặc `Channel: stable` trong hướng dẫn Project (hoặc tin nhắn / prompt của scheduled task). Không có → `stable`. Gọi là `CH`.
2. **Lấy repo** vào `/home/claude/claude-skills`:
   - Chưa có: `git clone -q --depth 1 -b $CH https://github.com/nhathm/claude-skills /home/claude/claude-skills`. Clone lỗi → gọi `add_repo` cho `nhathm/claude-skills` (access read), clone theo hướng dẫn của tool rồi `git -C /home/claude/claude-skills checkout -q $CH` (thiếu nhánh thì `git fetch -q --depth 1 origin $CH && git checkout -q -B $CH FETCH_HEAD`).
   - Đã có: `git -C /home/claude/claude-skills fetch -q --depth 1 origin $CH && git -C /home/claude/claude-skills checkout -q -B $CH FETCH_HEAD`. Đang dev (có thay đổi chưa commit, hoặc commit chưa push) → bỏ qua bước này, dùng bản đang có.
3. Đọc toàn bộ `/home/claude/claude-skills/nhathm-inspo-report/SKILL.md` và làm theo **chính xác**. Nội dung đó thay thế bản vỏ này; argument truyền vào skill áp dụng nguyên cho nó.
4. Không lấy được repo (lỗi mạng, quyền) → báo người dùng một dòng, dừng. Không tự làm theo trí nhớ.

Bản vỏ lưu ở `_shells/nhathm-inspo-report/SKILL.md` trong repo. Chỉ cần cài lại bản vỏ khi `description` đổi.
