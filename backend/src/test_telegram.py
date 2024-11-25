import logging
import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            logger.error("Telegram配置缺失")
            raise ValueError("请在.env文件中配置TELEGRAM_BOT_TOKEN和TELEGRAM_CHAT_ID")
            
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, message: str):
        """发送Telegram消息"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            if not response.json().get('ok'):
                error_msg = response.json().get('description', '未知错误')
                logger.error(f"Telegram API返回错误: {error_msg}")
                raise Exception(error_msg)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"发送Telegram消息时出错: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"错误详情: {e.response.text}")

def main():
    try:
        # 创建 TelegramNotifier 实例
        notifier = TelegramNotifier()
        
        # 发送测试消息
        test_message = (
            "<b>Telegram Bot 测试消息</b>\n\n"
            "如果您收到这条消息，说明配置正确！\n"
            "当前时间: <code>" + time.strftime("%Y-%m-%d %H:%M:%S") + "</code>"
        )
        
        logger.info("发送测试消息...")
        notifier.send_message(test_message)
        logger.info("测试消息发送成功！")
        
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")

if __name__ == "__main__":
    main() 