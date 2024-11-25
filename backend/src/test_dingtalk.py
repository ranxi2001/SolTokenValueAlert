#!/usr/bin/env python

import logging
import time
from dingtalk_notifier import DingTalkNotifier
from config import DINGTALK_ACCESS_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # 检查配置
        if not DINGTALK_ACCESS_TOKEN:
            raise ValueError("请在.env文件中配置DINGTALK_ACCESS_TOKEN")
            
        # 创建 DingTalkNotifier 实例
        notifier = DingTalkNotifier()
        
        # 构造测试数据
        test_token = {
            'symbol': 'TEST',
            'name': 'Test Token',
            'mint': '0x1234567890abcdef',
            'price': 1.23456,
            'amount': 100.0,
            'value_sol': 0.5
        }
        
        # 发送测试消息
        logger.info("发送钉钉测试消息...")
        notifier.send_price_alert(test_token, 150.0)  # 模拟150%的价格上涨
        logger.info("测试消息发送成功！")
        
    except Exception as e:
        logger.error(f"测试失败: {str(e)}")
        raise

if __name__ == "__main__":
    main() 