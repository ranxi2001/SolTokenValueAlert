# SOL 代币价格异动监测服务

## 项目介绍

一个基于 Python 的自动化监控服务，用于监测 Solana 钱包中代币的价格变动。当代币价格发生显著变化时，通过 Telegram 机器人发送提醒通知。

## 主要功能

- 自动扫描指定钱包地址的所有代币
- 实时监控代币价格变动
- 价格异动自动提醒（支持 Telegram、钉钉）
- 定期发送钱包代币总览报告
- 支持代理配置

## 监测规则

- 基础扫描间隔：10分钟
- 异动扫描间隔：3分钟（检测到价格变动时）
- 价格变动阈值：100%（可配置）
- 最小代币价值：0.01 SOL（过滤dust）

## 技术架构

- 后端：Python 3.8
- 容器化：Docker & Docker Compose
- API：Jupiter API、Raydium API
- 通知：Telegram Bot API

## 快速开始

1. 克隆项目并进入目录
```bash
git clone <repository_url>
cd SolTokenValueAlert
```

2. 配置环境变量（在 backend 目录下创建 .env 文件）
```env
# 必需配置
RPC_URL=https://rpc.ankr.com/solana
WALLET_ADDRESS=你的钱包地址
TELEGRAM_BOT_TOKEN=你的Telegram机器人token
TELEGRAM_CHAT_ID=你的Telegram聊天ID

# 可选配置（如需代理）
PROXY_HOST=127.0.0.1
PROXY_PORT=7890
```

3. 使用 Docker 部署
```bash
docker-compose up -d
```

## 项目结构
```
SolTokenValueAlert/
├── backend/
│   ├── src/
│   │   ├── scanner.py    # 主扫描程序
│   │   ├── token_fetcher.py  # 代币数据获取
│   │   ├── notification.py   # 通知服务
│   │   └── config.py    # 配置管理
│   └── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

## 部署文档

详细的部署和配置说明请参考：
- [部署指南](Deploy.md)
- [VPS环境搭建](VPSREADME.md)

## 注意事项

1. 确保 Telegram Bot 已正确配置并已启动
2. 建议使用稳定的 RPC 节点
3. 如果使用代理，需要正确配置代理环境变量
4. 定期检查日志确保服务正常运行

## 许可证

MIT License


## 更新信息 24/11/25：

1. 更准确地反映了当前项目的实际功能
2. 添加了详细的配置说明
3. 更新了项目结构以匹配实际代码
4. 添加了快速开始指南
5. 移除了尚未实现的功能（如邮件和飞书通知）
