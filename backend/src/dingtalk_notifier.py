import logging
import requests
from config import DINGTALK_ACCESS_TOKEN

logger = logging.getLogger(__name__)

class DingTalkNotifier:
    def __init__(self):
        if not DINGTALK_ACCESS_TOKEN:
            logger.error("钉钉配置缺失")
            raise ValueError("请在.env文件中配置DINGTALK_ACCESS_TOKEN")
            
        self.access_token = DINGTALK_ACCESS_TOKEN
        self.base_url = "https://oapi.dingtalk.com/robot/send"

    def send_price_alert(self, token_info: dict, price_change: float):
        """发送价格异动提醒"""
        if price_change < 100:  # 只在涨幅超过100%时发送钉钉通知
            return
            
        title = f"重要提醒：代币 {token_info['symbol']} 价格大幅上涨 {price_change:.2f}%"
        text = (f"## {title}\n\n"
                f"- 代币符号：{token_info['symbol']}\n"
                f"- 代币名称：{token_info['name']}\n"
                f"- 涨幅：**{price_change:.2f}%**\n"
                f"- 当前价格：${token_info['price']:.6f}\n"
                f"- 持有数量：{token_info['amount']:.6f}\n"
                f"- 当前价值：{token_info['value_sol']:.6f} SOL\n")
        
        self._send_message(title, text)

    def _send_message(self, title: str, text: str):
        """发送钉钉消息"""
        try:
            url = f"{self.base_url}?access_token={self.access_token}"
            
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": text
                }
            }
            
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('errcode') != 0:
                logger.error(f"钉钉API返回错误: {result.get('errmsg')}")
                raise Exception(result.get('errmsg'))
                
            logger.info("钉钉消息发送成功")
            
        except Exception as e:
            logger.error(f"发送钉钉消息时出错: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"错误详情: {e.response.text}") 