FROM python:3.11-slim

WORKDIR /app

# Cài đặt các công cụ cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy toàn bộ mã nguồn
COPY . .

# Mở port 5000 cho Web App
EXPOSE 5000

# Khởi chạy Web Server
CMD ["python", "scripts/run_web.py", "--host", "0.0.0.0", "--port", "5000", "--no-browser"]
