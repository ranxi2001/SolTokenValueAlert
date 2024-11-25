# VPS 环境搭建文档

## 1. 安装 Python 3.8

在 CentOS 系统上安装 Python 3.8：

```bash
# 安装 Python 3.8 及开发工具
sudo yum install python38 python38-devel
```

## 2. 创建项目目录

```bash
# 创建并进入项目目录
mkdir SolTokenValueAlert
cd SolTokenValueAlert
```

## 3. 配置虚拟环境

```bash
# 创建虚拟环境
python3.8 -m venv alert

# 激活虚拟环境
source alert/bin/activate
```

## 4. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

## 5. 配置项目

```bash
# 创建项目结构
mkdir -p backend/src
touch backend/src/__init__.py

# 创建环境变量文件
```

参考 Deploy.md 中的环境变量配置：

````12:23:Deploy.md
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
````


## 6. 验证安装

```bash
# 确认 Python 版本
python3.8 --version

# 验证依赖安装
pip list
```

## 注意事项

1. 确保系统时间准确
2. 如果使用代理，需要正确配置代理环境变量
3. 建议使用稳定的网络环境
4. 定期检查日志确保服务正常运行

## 故障排查

1. 如果出现权限问题，使用 `sudo` 执行相关命令
2. 如果依赖安装失败，可以尝试使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
3. 确保环境变量文件 `.env` 配置正确
4. 检查网络连接是否正常
