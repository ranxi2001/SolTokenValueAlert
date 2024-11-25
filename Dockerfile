FROM python:3.8-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY backend /app/backend

# 设置工作目录
WORKDIR /app/backend

# 启动扫描程序
CMD ["python", "src/scanner.py"]
