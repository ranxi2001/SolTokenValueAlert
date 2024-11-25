FROM python:3.8-slim

WORKDIR /app

# 安装基础依赖
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY backend/requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY backend/src/ ./src/

# 设置环境变量
ENV PYTHONPATH=/app

# 启动命令
CMD ["python", "src/scanner.py"]
