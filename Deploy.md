# 部署指南

## 1. 环境要求
- Docker
- Docker Compose

## 2. 配置文件准备

### 2.1 创建环境变量文件
在 `backend` 目录下创建 `.env` 文件：
```env
# 区块链配置
RPC_URL=https://rpc.ankr.com/solana
WALLET_ADDRESS=你的钱包地址

# Telegram配置
TELEGRAM_BOT_TOKEN=你的Telegram机器人token
TELEGRAM_CHAT_ID=你的Telegram聊天ID

# 钉钉配置（可选）
DINGTALK_ACCESS_TOKEN=你的钉钉机器人访问令牌

# 代理配置（如果需要）
PROXY_HOST=127.0.0.1
PROXY_PORT=7890
```

## 3. 部署步骤

### 3.1 克隆代码
```bash
git clone <repository_url>
cd SolTokenValueAlert
```

### 3.2 构建和启动服务
```bash
docker-compose up -d
```

### 3.3 查看运行状态
```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

## 4. 维护命令

### 4.1 停止服务
```bash
docker-compose down
```

### 4.2 重启服务
```bash
docker-compose restart
```

### 4.3 更新代码后重新部署
```bash
# 停止服务
docker-compose down

# 重新构建
docker-compose build

# 启动服务
docker-compose up -d
```

## 5. 验证部署

服务启动后，你应该能在配置的 Telegram 机器人中收到类似这样的消息：
```
钱包扫描摘要

总价值: 123.456789 SOL
扫描时间: 2024-01-01 12:00:00
```

## 6. 故障排查

如果遇到问题：

1. 检查日志
```bash
docker-compose logs -f
```

2. 确认环境变量是否正确配置
3. 确认网络连接是否正常
4. 如果使用代理，确认代理配置是否正确

## 7. 注意事项

1. 确保服务器时间准确
2. 建议使用稳定的网络环境
3. 定期检查日志确保服务正常运行
4. 建议设置服务器监控


要删除其他容器，可以使用以下命令：

```bash
# 查看所有容器（包括已停止的）
docker ps -a

# 删除指定容器（替换 CONTAINER_ID 为实际容器ID）
docker rm CONTAINER_ID

# 或者使用容器名称删除
docker rm 容器名称
```


如果要强制删除正在运行的容器，可以添加 `-f` 参数：

```bash
docker rm -f CONTAINER_ID
```


在我们的项目中，根据 `docker-compose.yml` 配置：


```3:8:docker-compose.yml
services:
  scanner:
    build: .
      context: .
      dockerfile: Dockerfile
    container_name: sol_token_scanner
```


我们只定义了一个名为 `sol_token_scanner` 的容器。如果有其他容器，可以直接删除：

```bash
# 删除其他容器，保留 sol_token_scanner
docker rm -f $(docker ps -a | grep -v "sol_token_scanner" | awk 'NR>1 {print $1}')
```


删除后可以使用 `docker ps -a` 确认是否只剩下 `sol_token_scanner` 容器。


这个部署文档包含了完整的部署流程和维护指南，让用户可以轻松部署和维护服务。
