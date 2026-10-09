# Hướng dẫn mở CNF Strategic Weekly Report

## Cách 1: Chạy trực tiếp trong PowerShell

Mở PowerShell và chạy:

```powershell
cd "C:\Users\long.DESKTOP-DCLSBL3\Documents\workspace\BCCL"
& "C:\Users\long.DESKTOP-DCLSBL3\.venv\Scripts\python.exe" server.py
```

Giữ cửa sổ PowerShell đang chạy. Sau đó mở trình duyệt và truy cập:

```text
http://127.0.0.1:8000
```

## Cách 2: Chạy nền và tự mở trình duyệt

Chạy một lệnh PowerShell duy nhất:

```powershell
Start-Process -WindowStyle Hidden -FilePath "C:\Users\long.DESKTOP-DCLSBL3\.venv\Scripts\python.exe" -ArgumentList "server.py" -WorkingDirectory "C:\Users\long.DESKTOP-DCLSBL3\Documents\workspace\BCCL"; Start-Process "http://127.0.0.1:8000"
```

## Lưu ý

- Luôn mở web qua `http://127.0.0.1:8000`.
- Không mở trực tiếp file `index.html` bằng `file://`.
- Không dùng `python -m http.server 8000`, vì lệnh này không cung cấp API cập nhật dữ liệu Vnstock.
- Nếu cổng `8000` đang được sử dụng, hãy đóng server cũ hoặc khởi động lại PowerShell.
