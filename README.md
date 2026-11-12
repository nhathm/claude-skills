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

