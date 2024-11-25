import logging
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_PROXIES

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        self.session = requests.Session()
        self.session.proxies.update(TELEGRAM_PROXIES)
        self.session.verify = False
    
    def send_message(self, message: str) -> bool:
        """发送Telegram消息"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = self.session.post(url, data=data)
            response.raise_for_status()
            
            if response.status_code == 200:
                logger.info("Telegram消息发送成功")
                return True
            else:
                logger.error(f"Telegram消息发送失败: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"发送Telegram消息时出错: {str(e)}")
            return False 