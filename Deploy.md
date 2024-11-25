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


相关代码引用：

```6:14:backend/src/config.py
# 区块链配置
RPC_URL = os.getenv("RPC_URL", "https://rpc.ankr.com/solana")
JUPITER_API_BASE = "https://public.jupiterapi.com/v6"
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

# 扫描配置
SCAN_INTERVAL = 600  # 10分钟
ALERT_SCAN_INTERVAL = 180  # 3分钟
PRICE_CHANGE_THRESHOLD = 100  # 100%
```



```88:121:backend/src/scanner.py
def main():
    scanner = TokenScanner()
    
    while True:
        try:
            logger.info("开始扫描钱包代币...")
            accounts = fetch_tokens()
            
            if accounts:
                has_changes = scanner.check_price_changes(accounts)
                
                # 计算并发送总价值
                total_value_sol = sum(account['value_sol'] for account in accounts)
                total_tokens = len(accounts)
                scanner._send_scan_summary(total_value_sol, total_tokens)
                
                # 根据是否有显著变化调整扫描间隔
                if has_changes and not scanner.alert_mode:
                    logger.info("检测到显著价格变化，切换到快速扫描模式")
                    scanner.alert_mode = True
                elif not has_changes and scanner.alert_mode:
                    logger.info("价格趋于稳定，恢复常规扫描间隔")
                    scanner.alert_mode = False
                
                interval = ALERT_SCAN_INTERVAL if scanner.alert_mode else SCAN_INTERVAL
                logger.info(f"等待 {interval} 秒后进行下一次扫描...")
                time.sleep(interval)
            else:
                logger.warning("未获取到代币信息，1分钟后重试...")
                time.sleep(60)
                
        except Exception as e:
            logger.error(f"扫描出错: {str(e)}")
            time.sleep(60)  # 出错后等待1分钟再试
```


这个部署文档包含了完整的部署流程和维护指南，让用户可以轻松部署和维护服务。
