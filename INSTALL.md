# Cài Inspiration (hướng dẫn cho Claude)

Người dùng dán link repo này và nhờ cài. Claude làm theo thứ tự, trả lời bằng ngôn ngữ người dùng, ngắn, mỗi bước một tin.

## 1. Cài skill (Claude làm)
Gọi `propose_skills` **một lần** với 2 đề xuất `kind: "new"`; `skillMd` là **nguyên văn** file trong repo, `name` và `description` lấy từ frontmatter của file đó:
- `_shells/nhathm-inspo/SKILL.md`
- `_shells/nhathm-inspo-report/SKILL.md`

Nói người dùng bấm lưu cả hai trên thẻ. Đây là bản vỏ: mỗi lần chạy tự lấy bản `stable` mới nhất từ repo, không phải cài lại khi skill cập nhật.

Không có `propose_skills` → gửi 2 file đó (đổi tên thành `SKILL.md` trong thư mục cùng tên, nén zip) và hướng dẫn tải lên ở phần cài đặt Skills của claude.ai.

Batch đêm và digest tuần (`nhathm-inspo-batch`, `nhathm-inspo-digest`) là tuỳ chọn: chỉ đề xuất khi người dùng hỏi.

## 2. Tạo kho dữ liệu (người dùng làm, Claude hướng dẫn)
1. GitHub: tạo repo **Private**, ví dụ `inspiration-vault`, tick "Add a README file". Ghi lại `<tên-github>/<repo>`.
2. Claude: kết nối GitHub ở phần Connectors, cho phép repo vừa tạo.
3. Claude: tạo Project (ví dụ "Inspiration"), dán vào hướng dẫn của Project:
   ```
   Vault: <tên-github>/<repo>
   Tôi là <tên>.
   Khi tôi gửi ảnh, video ngắn hoặc link, hoặc gõ hỏi:/xong/bỏ/để sau/tìm/thêm vào: dùng skill nhathm-inspo.
   Khi tôi muốn xem các ý tưởng: dùng skill nhathm-inspo-report.
   ```

## 3. Dùng thử
Trong Project, mở đoạn chat mới, gửi một ảnh chụp màn hình kèm một câu vì sao lưu. Lần đầu Claude tự dựng vault (`Inspiration/`, `config.md`, `categories.md`) rồi lưu.

Câu lệnh: xem `nhathm-inspo/template/README.md`. Muốn chỉnh cách phân tích: sửa `Inspiration/config.md` trong repo vault (hoặc nhờ Claude sửa).

## Tuỳ chọn: đọc bằng Obsidian
Obsidian là app ghi chú đọc thẳng các file `.md` trong vault. Cần mã truy cập GitHub (Fine-grained token, chỉ repo vault, Contents: Read and write) và plugin cộng đồng **Git**: clone `https://github.com/<tên-github>/<repo>.git`, đặt Auto pull khoảng 30 phút. Không cần Obsidian vẫn xem được mọi thứ qua lệnh `trang ý tưởng`.
