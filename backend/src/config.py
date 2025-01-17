import os
from dotenv import load_dotenv

load_dotenv()

# 区块链配置
RPC_URL = os.getenv("RPC_URL", "https://rpc.ankr.com/solana")
JUPITER_API_BASE = "https://public.jupiterapi.com/v6"
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

# 扫描配置
SCAN_INTERVAL = 600  # 10分钟
ALERT_SCAN_INTERVAL = 180  # 3分钟
PRICE_CHANGE_THRESHOLD = 100  # 100%

# Telegram配置
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 邮件配置
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")

# 飞书配置
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")

# Solscan API 配置
SOLSCAN_API_KEY = os.getenv("SOLSCAN_API_KEY")

# Raydium API 配置
RAYDIUM_API_BASE = "https://api-v3.raydium.io"

# 钉钉配置
DINGTALK_CLIENT_ID = os.getenv("DINGTALK_CLIENT_ID")
DINGTALK_CLIENT_SECRET = os.getenv("DINGTALK_CLIENT_SECRET")
# 从环境变量中获取钉钉访问令牌
DINGTALK_ACCESS_TOKEN = os.getenv('DINGTALK_ACCESS_TOKEN')