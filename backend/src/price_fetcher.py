import requests
from typing import Dict, Optional
from .config import JUPITER_API_BASE

class PriceFetcher:
    def __init__(self):
        self.session = requests.Session()
        
    def get_token_price(self, token_address: str) -> Optional[float]:
        """获取代币当前价格"""
        try:
            url = f"{JUPITER_API_BASE}/price?ids={token_address}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            if token_address in data['data']:
                return float(data['data'][token_address]['price'])
            return None
            
        except Exception as e:
            print(f"获取价格失败: {str(e)}")
            return None 