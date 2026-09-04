# Đặc tả: Cập nhật dữ liệu tuần bằng vnstock

## Bối cảnh

Ứng dụng hiện tại là báo cáo chiến lược tuần CNF chạy tĩnh bằng HTML, CSS và JavaScript. Dữ liệu trong phần tổng quan thị trường và biểu đồ mua/bán ròng khối ngoại được nhập thủ công. Thư viện `vnstock` Silver đã có sẵn trong môi trường Python của người dùng, nhưng trình duyệt không thể gọi trực tiếp thư viện Python.

## Mục tiêu

Thêm nút “Cập nhật dữ liệu” để, theo khoảng ngày trong trường “Tuần báo cáo”, tự động lấy và điền dữ liệu định lượng của tuần. Thành công được xác nhận khi dữ liệu mới được hiển thị trên Canvas và được lưu trong bản nháp cục bộ.

## Phạm vi

Trong phạm vi:

- Chạy ứng dụng qua một dịch vụ Python cục bộ sử dụng môi trường đã cài `vnstock` Silver.
- Tự động cập nhật VN-Index, VN30, HNX-Index và UPCoM-Index: điểm đóng cửa, thay đổi điểm và phần trăm trong tuần.
- Tự động cập nhật giá trị giao dịch bình quân mỗi ngày.
- Tự động cập nhật 5 phiên giá trị mua/bán ròng theo ngày của khối ngoại trên HOSE, đơn vị tỷ đồng.
- Phân tích chuỗi “Tuần báo cáo” thành khoảng ngày và trả lỗi rõ ràng nếu không hợp lệ.
- Giữ nguyên dữ liệu cũ nếu nguồn dữ liệu lỗi, thiếu dữ liệu hoặc kết quả không đúng định dạng mong đợi.
- Hiển thị trạng thái cập nhật và thời điểm/nguồn dữ liệu.

Ngoài phạm vi:

- Tự động viết nhận định thị trường, chiến lược, kịch bản hoặc tin tức.
- Cập nhật top mua/bán ròng, chỉ số độ rộng MA, ảnh biểu đồ và dữ liệu ngành.
- Backend triển khai từ xa, đăng nhập, cơ sở dữ liệu hoặc đồng bộ nhiều người dùng.
- Thay đổi bố cục Canvas 1920×1080.

## Ràng buộc

- Người dùng tự khởi động dịch vụ trong môi trường Python đã cài `vnstock` Silver.
- Giao diện phải được mở qua `http://localhost:<port>`, không phải `file://`.
- Không thêm hoặc nâng cấp dependency. Dịch vụ dùng thư viện `vnstock` đã có.
- Dữ liệu báo cáo của người dùng chỉ lưu cục bộ; truy vấn thị trường đi tới các nguồn mà `vnstock` sử dụng.
- API và schema trả về có thể khác theo phiên bản `vnstock`; cần lớp adapter/chuẩn hóa và thông báo lỗi thay vì giả định tên cột.

## Các phương án thiết kế

### A. Dịch vụ Python cục bộ với nút cập nhật — đã chọn

Python phục vụ static app và API nội bộ. Nút trên giao diện gọi API, nhận JSON đã chuẩn hóa, cập nhật state, localStorage và Canvas. Phương án này mang lại trải nghiệm một nút bấm và tách biệt Python với JavaScript.

### B. Script xuất JSON rồi người dùng nhập thủ công — không chọn

Ít thay đổi kiến trúc nhưng cần nhiều thao tác và không đáp ứng trải nghiệm cập nhật trực tiếp.

### C. Tác vụ theo lịch — không chọn

Hữu ích cho vận hành định kỳ nhưng vượt phạm vi cập nhật theo tuần báo cáo do người dùng chọn.

## Hướng đã chốt

Sử dụng phương án A. Một dịch vụ Python cục bộ sẽ nhận khoảng tuần từ báo cáo, gọi `vnstock`, chuẩn hóa dữ liệu thành các trường hiện có (`indices`, `trading_value`, `foreign_flow`) và trả JSON. Trình duyệt hiển thị tiến trình, chỉ áp dụng dữ liệu sau khi toàn bộ kiểm tra hợp lệ, sau đó lưu nháp và render lại.

Luồng dữ liệu:

```text
Trường “Tuần báo cáo”
  → nút “Cập nhật dữ liệu”
  → API Python cục bộ
  → vnstock Silver và nguồn dữ liệu thị trường
  → adapter/chuẩn hóa dữ liệu
  → JSON kiểm tra hợp lệ
  → state + localStorage + Canvas
```

## Vùng ảnh hưởng dự kiến

| Vùng | Thay đổi dự kiến |
| --- | --- |
| `index.html` | Thêm thao tác cập nhật dữ liệu và mô tả trạng thái. |
| `js/config.js` | Khai báo endpoint cục bộ, không hard-code phân tán. |
| `js/app.js` | Phân tích tuần báo cáo, gọi API, cập nhật state an toàn và báo lỗi. |
| `server.py` | Khởi động HTTP server cục bộ và phục vụ static app/API. |
| Mô-đun adapter dữ liệu mới | Cô lập việc gọi/chuẩn hóa `vnstock` và kiểm tra schema. |

`js/renderer.js` không cần sửa nếu API trả về đúng cấu trúc dữ liệu sẵn có.

## Câu hỏi mở

- Xác minh chính xác API và tên cột của phiên bản `vnstock` Silver đang cài trong môi trường Python của người dùng trước khi viết adapter.
- Xác định lệnh khởi động chính xác sau khi nhận diện interpreter/môi trường Python có `vnstock`.
