import time
import logging
from typing import Dict, List
from token_fetcher import TokenFetcher, main as fetch_tokens
from config import SCAN_INTERVAL, ALERT_SCAN_INTERVAL, PRICE_CHANGE_THRESHOLD
from notification import TelegramNotifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TokenScanner:
    def __init__(self):
        self.fetcher = TokenFetcher()
        self.last_prices: Dict[str, float] = {}
        self.last_total_value_sol: float = 0
        self.alert_mode = False
        self.telegram = TelegramNotifier()
        
    def check_price_changes(self, accounts: List[dict]) -> bool:
        """检查价格变化并返回是否有显著变化"""
        has_significant_change = False
        
        # 计算当前总价值
        current_total_value_sol = sum(account['value_sol'] for account in accounts)
        
        # 检查总价值变化
        if self.last_total_value_sol > 0:
            value_change_sol = current_total_value_sol - self.last_total_value_sol
            if value_change_sol >= 0.3:  # 总价值增加超过0.3 SOL
                has_significant_change = True
                self._send_total_value_alert(current_total_value_sol, value_change_sol)
        
        # 检查单个代币价格变化
        for account in accounts:
            mint = account['mint']
            current_price = account['price']
            
            if mint in self.last_prices:
                price_change = ((current_price - self.last_prices[mint]) 
                              / self.last_prices[mint] * 100)
                
                if abs(price_change) >= PRICE_CHANGE_THRESHOLD:
                    has_significant_change = True
                    self._send_price_alert(account, price_change)
            
            self.last_prices[mint] = current_price
        
        self.last_total_value_sol = current_total_value_sol
        return has_significant_change
    
    def _send_price_alert(self, account: dict, price_change: float):
        """发送价格变动提醒"""
        change_direction = "上涨" if price_change > 0 else "下跌"
        message = (
            f"<b>代币价格{change_direction}提醒!</b>\n\n"
            f"代币符号: <code>{account['symbol']}</code>\n"
            f"代币名称: <code>{account['name']}</code>\n"
            f"合约地址: <code>{account['mint']}</code>\n"
            f"{change_direction}幅度: <b>{abs(price_change):.2f}%</b>\n"
            f"当前价格: <code>${account['price']:.6f}</code>\n"
            f"持有数量: <code>{account['amount']:.6f}</code>\n"
            f"当前价值: <code>{account['value_sol']:.6f} SOL</code>"
        )
        logger.info("\n" + message)
        self.telegram.send_message(message)
    
    def _send_total_value_alert(self, current_value: float, value_change: float):
        """发送总价值变动提醒"""
        message = (
            f"<b>钱包总价值增长提醒!</b>\n\n"
            f"当前总价值: <code>{current_value:.6f} SOL</code>\n"
            f"增长数量: <code>{value_change:.6f} SOL</code>\n"
            f"增长比例: <b>{(value_change / (current_value - value_change)) * 100:.2f}%</b>"
        )
        logger.info("\n" + message)
        self.telegram.send_message(message)
    
    def _send_scan_summary(self, total_value_sol: float, total_tokens: int):
        """发送扫描摘要信息"""
        message = (
            f"<b>钱包扫描摘要</b>\n\n"            
            f"总价值: <code>{total_value_sol:.6f}</code> SOL\n"
            f"扫描时间: <code>{time.strftime('%Y-%m-%d %H:%M:%S')}</code>"
        )
        logger.info("\n" + message)
        self.telegram.send_message(message)

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

if __name__ == "__main__":
    main() 