# Sử dụng một base image Python chính thức, gọn nhẹ
FROM python:3.11-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Sao chép file requirements.txt vào trước để tận dụng cache của Docker
COPY requirements.txt .

# Cài đặt các thư viện đã định nghĩa
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của ứng dụng vào container
COPY . .

# Lệnh để chạy ứng dụng khi container khởi động
# Cloud Run sẽ tự động cung cấp biến PORT, nhưng chúng ta mặc định là 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]