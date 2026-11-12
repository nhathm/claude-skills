---
name: "nhathm-inspo-digest"
description: "Weekly digest and cleanup of an Inspiration vault on GitHub: summarise the week, pick the 3 ideas most worth trying, archive stale items, send a push. Use for the weekly scheduled inspo run or when the user asks for the inspo digest."
---

# nhathm-inspo-digest (bản vỏ)

Hướng dẫn đầy đủ **không nằm ở đây** mà ở repo public `https://github.com/nhathm/claude-skills`, file `nhathm-inspo-digest/SKILL.md`. Bản vỏ chỉ nạp bản đó, để skill tự cập nhật khi repo đổi mà không phải cài lại.

Mỗi lần chạy, làm đúng 4 bước:
1. **Kênh**: tìm dòng `Channel: main` hoặc `Channel: stable` trong hướng dẫn Project (hoặc tin nhắn / prompt của scheduled task). Không có → `stable`. Gọi là `CH`.
2. **Lấy repo** vào `/home/claude/claude-skills`:
   - Chưa có: `git clone -q --depth 1 -b $CH https://github.com/nhathm/claude-skills /home/claude/claude-skills`. Clone lỗi → gọi `add_repo` cho `nhathm/claude-skills` (access read), clone theo hướng dẫn của tool rồi `git -C /home/claude/claude-skills checkout -q $CH` (thiếu nhánh thì `git fetch -q --depth 1 origin $CH && git checkout -q -B $CH FETCH_HEAD`).
   - Đã có: `git -C /home/claude/claude-skills fetch -q --depth 1 origin $CH && git -C /home/claude/claude-skills checkout -q -B $CH FETCH_HEAD`. Đang dev (có thay đổi chưa commit, hoặc commit chưa push) → bỏ qua bước này, dùng bản đang có.
3. Đọc toàn bộ `/home/claude/claude-skills/nhathm-inspo-digest/SKILL.md` và làm theo **chính xác**. Nội dung đó thay thế bản vỏ này; argument truyền vào skill áp dụng nguyên cho nó.
4. Không lấy được repo (lỗi mạng, quyền) → báo người dùng một dòng, dừng. Không tự làm theo trí nhớ.

Bản vỏ lưu ở `_shells/nhathm-inspo-digest/SKILL.md` trong repo. Chỉ cần cài lại bản vỏ khi `description` đổi.
