# Thiết kế UI: CNF Strategic Weekly Report Engine

## 1. Brief

- Nền tảng: Web tĩnh, chạy offline, tiếng Việt, không backend.
- Người dùng: chuyên viên CNF lập báo cáo chiến lược hằng tuần trên máy tính; mobile chỉ dùng để xem/chỉnh nhanh.
- Màn hình chính: form Accordion bên trái và preview Canvas báo cáo bên phải.
- Mục tiêu UX: nhập nhanh, phát hiện lỗi trước render, xuất PNG 1920×1080 đúng mẫu demo.

## 2. Điều hướng và luồng chính

Không dùng routing. Một màn hình có hai vùng:

1. Người dùng mở một nhóm Accordion, nhập hoặc chỉnh dữ liệu.
2. Ứng dụng lưu nháp cục bộ sau thay đổi hợp lệ về cấu trúc.
3. Người dùng chọn `Render báo cáo`; lỗi hiển thị ngay tại trường và ở vùng trạng thái.
4. Preview cập nhật khi validation PASS.
5. Người dùng chọn `Xuất PNG`; file ảnh được tải từ canvas.

Thanh tác vụ cố định của sidebar gồm: Render báo cáo, Xuất PNG, Nhập JSON, Tải JSON và Khôi phục dữ liệu mẫu.

## 3. Tokens

### Màu primitive

| Token | Giá trị | Mục đích |
| --- | --- | --- |
| `--cnf-navy-950` | `#03101E` | nền sâu/sidebar field |
| `--cnf-navy-900` | `#07152B` | sidebar, đầu/cuối báo cáo |
| `--cnf-navy-700` | `#0D2D49` | nút phụ |
| `--cnf-green-600` | `#5BA524` | hành động chính |
| `--cnf-green-500` | `#68B828` | nhấn mạnh tích cực |
| `--cnf-lime-400` | `#8BD234` | brand accent |
| `--semantic-danger` | `#C81E1E` | lỗi/giảm giá |
| `--semantic-warning` | `#9A6700` | cảnh báo |
| `--surface-page` | `#E9EEF3` | nền ứng dụng |
| `--surface-card` | `#FFFFFF` | card/preview |
| `--text-primary` | `#111827` | nội dung chính |
| `--text-inverse` | `#FFFFFF` | nội dung trên navy |
| `--border-subtle` | `#8EA0B5` | đường viền |

Semantic colors phải được dùng thay vì raw hex trong component CSS.

### Typography và spacing

- Font: `Arial, "Segoe UI", Roboto, sans-serif`; dùng hoàn toàn cục bộ, hỗ trợ tiếng Việt.
- Base text: 16px / 1.5; label: 13px / 1.5; heading: 18–24px / 1.3.
- Chuỗi kiểm tra dấu tiếng Việt: `Nguyễn Tiến Dũng — Báo cáo chiến lược tuần mới`.
- Spacing scale: 4, 8, 12, 16, 24, 32px.
- Radius: 6px (field), 8px (card), 10px (panel).
- Focus ring: 3px `--cnf-lime-400` với offset 2px.
- Motion: 180ms ease-out cho Accordion và hover; `prefers-reduced-motion` vô hiệu transition.

## 4. Layout responsive

| Thiết bị | Layout |
| --- | --- |
| ≥ 1280px | Grid 360px sidebar + preview co giãn; sidebar sticky, preview cuộn độc lập. |
| 640–1279px | Sidebar nằm trên preview; Accordion hai cột khi đủ rộng; canvas cuộn ngang trong khung. |
| 320–639px | Một cột; action bar sticky cuối màn hình; Accordion full-width; preview thu nhỏ bằng CSS nhưng PNG vẫn 1920×1080. |

Không thay đổi tỷ lệ output canvas trên mọi breakpoint. Không có horizontal scroll ở form; vùng preview có scroll riêng khi cần.

## 5. Component specification

### Accordion section

- Header gồm số thứ tự, tiêu đề, trạng thái lỗi và chevron.
- Vùng click tối thiểu 44px cao; hỗ trợ Enter/Space; `aria-expanded` và `aria-controls`.
- Một section mở mặc định; nhiều section có thể mở đồng thời để đối chiếu dữ liệu.
- Error state: badge số lỗi + viền danger; success state: dấu xác nhận bằng text/icon, không chỉ dùng màu.

### Field và dynamic list

- Label luôn hiển thị phía trên input; helper text ở dưới khi cần.
- Number input có đơn vị rõ: `%`, `tỷ đồng`, `điểm`.
- Error text sát field, dùng `aria-describedby`.
- Dynamic list dùng card hàng; nút `Thêm` và `Xóa` có nhãn đầy đủ, confirm không cần thiết cho thao tác xóa một hàng chưa lưu vì local undo không có trong scope.
- Giới hạn 6 ngành phải hiển thị rõ khi đạt giới hạn.

### Upload biểu đồ

- Drop zone + nút `Chọn ảnh`; nhận PNG/JPEG/WebP.
- Sau upload: thumbnail, tên file và nút thay ảnh/xóa ảnh.
- Empty: minh họa placeholder trong preview Canvas.
- Error: định dạng không hỗ trợ hoặc ảnh không đọc được.

### Action bar và status

- Một CTA chính: `Render báo cáo`.
- Nút phụ `Cập nhật dữ liệu` nằm trước `Render báo cáo`, chỉ tải lại dữ liệu định lượng theo trường `Tuần báo cáo`; không thay đổi các trường nhận định hoặc chiến lược.
- Trạng thái nút: mặc định có nhãn đầy đủ; loading đổi thành `Đang cập nhật dữ liệu…` và disabled; success/error trả qua vùng status bằng text, không chỉ dùng màu.
- Khi server cục bộ chưa chạy hoặc khoảng tuần sai, status nêu rõ lý do và cách khôi phục; focus giữ ở nút để người dùng có thể sửa và thử lại bằng bàn phím.
- `Xuất PNG` disabled đến khi render thành công.
- Trạng thái dùng live region: đang lưu, validation lỗi, render thành công, export thành công/thất bại.
- Phím tắt: `Ctrl/Cmd + Enter` render; không chặn shortcut trình duyệt khác.

## 6. Accessibility

- `lang="vi"`, HTML semantic (`aside`, `main`, `form`, `fieldset`, `legend`).
- Tab order theo thứ tự nhập liệu; focus không bị che bởi action bar sticky.
- Text/ nền đạt WCAG AA: navy/white, white/navy, primary text/white; green chỉ dùng cho text lớn hoặc có nền tương phản phù hợp.
- Error không truyền đạt bằng màu đơn lẻ: có icon/badge và thông điệp.
- Canvas preview có vùng text thay thế tóm tắt trạng thái báo cáo; ảnh upload có alt bằng tên loại biểu đồ.
- Tôn trọng `prefers-reduced-motion`.

## 7. Hướng dẫn triển khai

- Khai báo token bằng CSS custom properties trong stylesheet chung.
- Form UI chỉ phát state events; validation, storage, render và export là các module riêng.
- Renderer giữ tọa độ Canvas trong config, không đọc trực tiếp DOM form.
- Preview canvas có `aria-label`; trạng thái render cập nhật qua live region.
- Không tải font, icon hoặc asset từ mạng. Biểu tượng Accordion dùng CSS hoặc SVG nội tuyến tối giản.

## 8. Tiêu chí nghiệm thu UI

- Form desktop hiển thị sidebar Accordion 360px và preview rõ ràng ở màn hình ≥1280px.
- Mọi trường có label tiếng Việt, trạng thái focus/error/success và hỗ trợ bàn phím.
- Mobile không vỡ layout; preview không làm thay đổi độ phân giải xuất ảnh.
- Render/Export có phản hồi trạng thái dễ hiểu.
- Cập nhật dữ liệu có đủ state mặc định/loading/success/error, không cho response cũ ghi đè lượt cập nhật mới hơn.
- Màu, spacing và typography chỉ tham chiếu token.
- Output Canvas giữ nguyên layout demo.

## 9. Câu hỏi còn lại

Không có câu hỏi nào chặn lập kế hoạch. Logo sẽ được xử lý ở implementation theo khả năng tái sử dụng asset của demo.
