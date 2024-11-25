import requests
import logging
from config import PROXIES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_token_price(mint_address: str) -> float:
    """获取代币价格"""
    try:
        session = requests.Session()
        session.proxies.update(PROXIES)
        session.verify = False
        
        url = "https://quote-api.jup.ag/v6/quote"
        params = {
            "inputMint": mint_address,
            "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
            "amount": "1000000",  # 1 token
            "slippageBps": 50
        }
        headers = {
            'Accept': 'application/json'
        }
        
        logger.info(f"获取代币价格: {mint_address}")
        response = session.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"价格响应: {data}")
        
        if 'outAmount' in data:
            # 1 token = outAmount/1000000 USDC
            price = float(data['outAmount']) / 1000000
            logger.info(f"代币价格: ${price}")
            return price
        return 0
    except Exception as e:
        logger.error(f"获取价格失败: {str(e)}")
        return 0

def main():
    mint_address = "wUtwjNmjCP9TTTtoc5Xn5h5sZ2cYJm5w2w44b79yr2o"
    price = get_token_price(mint_address)
    
    if price > 0:
        print(f"\nWIF 代币当前价格: ${price:.6f}")
    else:
        print("\n无法获取 WIF 代币价格")

if __name__ == "__main__":
    main() 