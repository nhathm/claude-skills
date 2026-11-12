---
name: "nhathm-inspo"
description: "Analyse and save something the user found while browsing (an image/screenshot, a short video, or a link from Facebook, TikTok, Threads, X, YouTube, the web) into their Inspiration vault, an Obsidian folder in their own GitHub repo; also handle the vault commands hỏi:, xong, bỏ, để sau, tìm, thêm vào. Use whenever the user sends such material, in an Inspiration project, or with /nhathm-inspo."
---

# nhathm-inspo (bản vỏ)

Hướng dẫn đầy đủ **không nằm ở đây** mà ở repo public `https://github.com/nhathm/claude-skills`, file `nhathm-inspo/SKILL.md`. Bản vỏ chỉ nạp bản đó, để skill tự cập nhật khi repo đổi mà không phải cài lại.

Mỗi lần chạy, làm đúng 4 bước:
1. **Kênh**: tìm dòng `Channel: main` hoặc `Channel: stable` trong hướng dẫn Project (hoặc tin nhắn / prompt của scheduled task). Không có → `stable`. Gọi là `CH`.
2. **Lấy repo** vào `/home/claude/claude-skills`:
   - Chưa có: `git clone -q --depth 1 -b $CH https://github.com/nhathm/claude-skills /home/claude/claude-skills`. Clone lỗi → gọi `add_repo` cho `nhathm/claude-skills` (access read), clone theo hướng dẫn của tool rồi `git -C /home/claude/claude-skills checkout -q $CH` (thiếu nhánh thì `git fetch -q --depth 1 origin $CH && git checkout -q -B $CH FETCH_HEAD`).
   - Đã có: `git -C /home/claude/claude-skills fetch -q --depth 1 origin $CH && git -C /home/claude/claude-skills checkout -q -B $CH FETCH_HEAD`. Đang dev (có thay đổi chưa commit, hoặc commit chưa push) → bỏ qua bước này, dùng bản đang có.
3. Đọc toàn bộ `/home/claude/claude-skills/nhathm-inspo/SKILL.md` và làm theo **chính xác**. Nội dung đó thay thế bản vỏ này; argument truyền vào skill áp dụng nguyên cho nó.
4. Không lấy được repo (lỗi mạng, quyền) → báo người dùng một dòng, dừng. Không tự làm theo trí nhớ.

Bản vỏ lưu ở `_shells/nhathm-inspo/SKILL.md` trong repo. Chỉ cần cài lại bản vỏ khi `description` đổi.
