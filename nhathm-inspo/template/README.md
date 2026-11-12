# Inspiration

Ảnh, video ngắn, link bắt gặp khi lướt mạng. Claude phân tích trước khi lưu. Skill: `nhathm-inspo` (lưu), `nhathm-inspo-report` (trang xem).

## Câu lệnh (trong Project có dòng `Vault:`)
| Gõ | Việc |
|---|---|
| gửi ảnh / video ngắn / link (+ 1 câu vì sao) | phân tích, bàn, lưu |
| `hỏi:` + ảnh / link | chỉ phân tích, không lưu |
| `xong` / `bỏ` / `để sau` + mã hoặc từ khoá | đổi trạng thái |
| `tìm` + từ khoá | liệt kê tối đa 5 ý tưởng khớp |
| `thêm vào <mã>: …` | ghi thêm vào phần Ghi chú |
| `trang ý tưởng` | dựng lại và mở trang xem |

## Quy ước
- ID: `INS-YYYYMMDD-HHMM-<người lưu>`. Note: `notes/<ID> <tên ngắn>.md`; ảnh: `attachments/<ID>.<ext>`; video: chỉ lưu ảnh tóm tắt `attachments/<ID>.sheet.jpg`.
- `config.md`: chủ vault, lăng kính phân tích riêng. `categories.md`: danh mục (tự thêm được).
- `status`: raw (lưu tạm) · inbox · later (để sau) · done (xong) · dropped (bỏ) · archived (lưu trữ)
- `type`: skill · project · tool · design-pattern · idea · setup · `effort`: 15-phut · 1-buoi · 1-tuan
- `captured_by`: người lưu · `source_author`: tác giả của nguồn
- Mục trong note: Ghi chú · Tóm tắt · Phân tích · Nguồn · Việc tiếp theo
- Chống trùng: cùng file, cùng link, hoặc ảnh gần như giống hệt.

Có Obsidian: mở `Inspiration.base` để xem dạng bảng.
