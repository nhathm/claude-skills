# claude-skills

Skill do Rio tự viết. Prefix `nhathm-` để phân biệt với skill tải về.

| Skill | Việc |
|---|---|
| `nhathm-inspo` | Xử lý ngay 1 ảnh inspiration vào Obsidian vault |
| `nhathm-inspo-batch` | Batch hằng đêm cho `Inspiration/_inbox` |
| `nhathm-inspo-digest` | Digest + cleanup thứ 6 |
| `nhathm-inspo-report` | Trang HTML (artifact) xem toàn bộ ý tưởng |

## Cài trên claude.ai: bản vỏ
Trên claude.ai chỉ cài **bản vỏ** trong `_shells/<skill>/SKILL.md`: nó clone repo này rồi làm theo `<skill>/SKILL.md`.
- Sửa hướng dẫn hoặc script → sửa folder skill, **push là xong**.
- Đổi `description` (lúc nào skill được gọi) → sửa cả `_shells/<skill>/SKILL.md` và cập nhật bản vỏ trên claude.ai.
- Skill mới → tạo `<skill>/` + `_shells/<skill>/`, cài bản vỏ lên claude.ai một lần.

## Kit chia sẻ (`kit/`)
Bản tổng quát cho người khác dùng, **tự chứa** (không clone repo này), không có tên/đường dẫn cá nhân:
- `kit/inspo/` (lưu ý tưởng, tự dựng vault ở lần đầu), `kit/inspo-report/` (trang xem ý tưởng).
- Vault của người nhận khai báo bằng dòng `Vault: <owner>/<repo>` trong hướng dẫn Project.
- `kit/huong-dan.html`: hướng dẫn cài (bản đang chia sẻ là artifact claude.ai).
- Đóng gói: `cd kit && zip -r inspo.zip inspo && zip -r inspo-report.zip inspo-report`.
- Sửa skill của Rio không tự sang kit; khi muốn chia sẻ bản mới, port thay đổi sang `kit/` và gửi lại zip.

