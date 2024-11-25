from web3 import Web3
from typing import List, Dict
import time
from .config import RPC_URL, SCAN_INTERVAL, PRICE_CHANGE_THRESHOLD
from .price_fetcher import PriceFetcher

class WalletScanner:
    def __init__(self, wallet_address: str):
        self.web3 = Web3(Web3.HTTPProvider(RPC_URL))
        self.wallet_address = Web3.to_checksum_address(wallet_address)
        self.price_fetcher = PriceFetcher()
        self.last_prices: Dict[str, float] = {}
        
    def get_token_holdings(self) -> List[str]:
        """获取钱包中的代币合约地址列表"""
        # 这里需要根据具体链来实现获取代币列表的逻辑
        # 以下是示例代码
        token_list = []
        # TODO: 实现获取代币列表的逻辑
        return token_list
        
    def check_price_changes(self):
        """检查代币价格变化"""
        tokens = self.get_token_holdings()
        
        for token_address in tokens:
            current_price = self.price_fetcher.get_token_price(token_address)
            
            if current_price is None:
                continue
                
            if token_address in self.last_prices:
                price_change = ((current_price - self.last_prices[token_address]) 
                              / self.last_prices[token_address] * 100)
                
                if price_change >= PRICE_CHANGE_THRESHOLD:
                    self._send_alert(token_address, price_change, current_price)
            
            self.last_prices[token_address] = current_price
    
    def _send_alert(self, token_address: str, price_change: float, current_price: float):
        """发送价格变动提醒"""
        message = (f"代币 {token_address} 价格发生显著变化!\n"
                  f"涨幅: {price_change:.2f}%\n"
                  f"当前价格: ${current_price:.6f}")
        print(message)  # 临时使用打印,后续替换为实际的提醒方式

def main():
    wallet_address = "YOUR_WALLET_ADDRESS"  # 替换为要监控的钱包地址
    scanner = WalletScanner(wallet_address)
    
    while True:
        try:
            scanner.check_price_changes()
            time.sleep(SCAN_INTERVAL)
        except Exception as e:
            print(f"扫描出错: {str(e)}")
            time.sleep(60)  # 出错后等待1分钟再试

if __name__ == "__main__":
    main() 