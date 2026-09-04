# Đặc tả: CNF Strategic Weekly Report Engine

## Bối cảnh

Workspace chưa có mã nguồn. File demo Canvas được cung cấp ngoài workspace là nguồn tham chiếu bắt buộc cho bố cục báo cáo 1920×1080.

## Mục tiêu

Tạo công cụ web chạy offline để người dùng nhập dữ liệu báo cáo tuần CNF qua form Accordion, xem trước bằng Canvas và xuất PNG chính xác 1920×1080.

## Phạm vi

- Form tiếng Việt gồm: thông tin báo cáo, tổng quan thị trường, dòng tiền ngoại, chiến lược tuần mới và tin tức.
- Validation dữ liệu, danh sách động, upload hai ảnh biểu đồ, lưu nháp localStorage, nhập/xuất JSON và xuất PNG.
- Canvas giữ nguyên bố cục, màu sắc và cấu trúc đầu ra từ demo.

Ngoài phạm vi: backend, đăng nhập, database, API thị trường, đồng bộ nhiều người dùng và thay đổi thiết kế ảnh báo cáo.

## Ràng buộc

- Chạy hoàn toàn cục bộ trong trình duyệt, không CDN hoặc request mạng.
- HTML, CSS và JavaScript ES modules; không thêm dependency nếu không cần thiết.
- Canvas xuất ảnh gốc 1920×1080; export PNG dùng `canvas.toBlob()`.
- Không sửa file demo gốc trong Downloads.

## Các phương án thiết kế

- A — Accordion: chia form theo nhóm báo cáo, giảm cuộn và giúp rà soát; đã chọn.
- B — Một form dài: xem được toàn bộ nhưng khó điều hướng; không chọn.
- C — Wizard theo bước: ít quá tải nhưng chậm khi cần sửa; không chọn.

## Hướng đã chốt

Giao diện có sidebar Accordion và vùng preview Canvas. State là nguồn dữ liệu duy nhất; validation chuẩn hóa state trước render. Renderer chỉ chịu trách nhiệm vẽ canvas; storage, import/export và upload được tách thành module riêng.

## Câu hỏi mở

- Dùng logo nhúng của demo nếu có thể tái sử dụng trực tiếp; nếu không giữ vùng logo với placeholder ổn định.
- Không có câu hỏi nào chặn bước thiết kế UI hoặc lập kế hoạch.
