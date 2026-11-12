# claude-skills

Skill do Rio (nhathm) viết, prefix `nhathm-`. Dùng chung cho mọi người; dữ liệu của mỗi người nằm trong repo vault riêng của họ.

**Cài:** mở Claude, nhắn `Cài skill từ https://github.com/nhathm/claude-skills` (Claude làm theo [INSTALL.md](INSTALL.md)).

| Skill | Việc |
|---|---|
| `nhathm-inspo` | Lưu ảnh / video ngắn / link vào vault, kèm phân tích; lệnh `hỏi:` `xong` `bỏ` `để sau` `tìm` `thêm vào` |
| `nhathm-inspo-report` | Trang web (artifact claude.ai) xem toàn bộ ý tưởng, có lọc và nút chép lệnh |
| `nhathm-inspo-batch` | Tuỳ chọn: batch đêm, hoàn tất note dở và ảnh trong `_inbox` |
| `nhathm-inspo-digest` | Tuỳ chọn: digest tuần + dọn dẹp |

## Kiến trúc
```
Repo này (public, code)              Vault (private, dữ liệu, mỗi người một repo)
<skill>/SKILL.md + scripts/          Inspiration/
_shells/<skill>/SKILL.md  (bản vỏ)     notes/  attachments/  _inbox/  _archive/  _report/
                                       config.md      ← chủ vault, lăng kính phân tích riêng
                                       categories.md  ← danh mục riêng
```
- Hướng dẫn Project khai báo `Vault: <owner>/<repo>`, `Tôi là <tên>`, và tuỳ chọn `Channel: main|stable`.
- Mỗi Project trỏ một vault → tách được dữ liệu (cá nhân / công việc) trong cùng một tài khoản Claude.

## Kênh phát hành
- `main`: bản đang phát triển. Rio dùng (`Channel: main`).
- `stable`: mọi người khác (mặc định). Đẩy bản ổn định: `git push origin main:stable`.
- Bản vỏ lấy kênh mỗi lần chạy → sửa skill chỉ cần push. Cài lại bản vỏ trên claude.ai chỉ khi đổi `description` hoặc logic của bản vỏ.

## Phát triển
- Skill mới: tạo `<skill>/` + `_shells/<skill>/`, thêm vào INSTALL.md nếu người dùng thường cần.
- Script chạy với `python3 -I`, chỉ đọc frontmatter, không gọi mạng.
- Nâng cấp vault cũ lên định dạng v2: `python3 -I nhathm-inspo/scripts/migrate_v2.py <vault>/Inspiration --owner <tên>`.
