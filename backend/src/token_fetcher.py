import os
import requests
import json
import logging
from solana.rpc.api import Client
from base58 import b58decode
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Optional
from config import RPC_URL, WALLET_ADDRESS, JUPITER_API_BASE, SOLSCAN_API_KEY
import urllib3
import time

# 设置日志级别为 INFO，增加输出
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class TokenFetcher:
    def __init__(self):
        self.token_info_cache = {}  # 添加缓存字典
        try:
            self.client = Client(RPC_URL, timeout=30)
            self.session = requests.Session()
        except Exception as e:
            logger.error(f"初始化失败: {str(e)}")
            raise
        
    def _make_request_with_retry(self, url, headers=None, params=None, max_retries=3):
        """发送请求并支持重试"""
        # 所有请求都使用代理，但对不同域名采用不同的SSL验证策略
        domains_no_verify = [
            'api.telegram.org'  # Telegram API 需要代理且不验证SSL
        ]
        
        verify_ssl = not any(domain in url for domain in domains_no_verify)
        
        for attempt in range(max_retries):
            try:
                session = requests.Session()
                
                if params:
                    response = session.get(
                        url, 
                        headers=headers, 
                        params=params, 
                        timeout=10,
                        verify=verify_ssl
                    )
                else:
                    response = session.get(
                        url, 
                        headers=headers, 
                        timeout=10,
                        verify=verify_ssl
                    )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求异常 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    raise
                
            time.sleep(1)
        
        return None

    def get_sol_price(self) -> float:
        """获取 SOL 价格"""
        try:
            logger.info("获取 SOL 价格...")
            url = "https://quote-api.jup.ag/v6/quote"
            params = {
                "inputMint": "So11111111111111111111111111111111111111112",  # SOL
                "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
                "amount": "1000000000",  # 1 SOL = 1,000,000,000 lamports
                "slippageBps": 50
            }
            headers = {
                'Accept': 'application/json'
            }
            
            response_data = self._make_request_with_retry(url, headers=headers, params=params)
            if response_data and 'outAmount' in response_data:
                # 1 SOL = outAmount/1000000 USDC (USDC有6位小数)
                price = float(response_data['outAmount']) / 1000000
                logger.info(f"SOL 价格: ${price}")
                return price
                
            raise Exception("无效的响应数据")
                
        except Exception as e:
            logger.error(f"获取 SOL 价格失败: {str(e)}")
            return 0

    def get_token_price(self, mint_address: str) -> Optional[float]:
        """获取代币价格"""
        try:
            url = "https://api-v3.raydium.io/mint/price"
            params = {
                "mints": mint_address
            }
            headers = {
                'Accept': 'application/json'
            }
            
            logger.info(f"获取代币价格: {mint_address}")
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success') and 'data' in data:
                price_data = data['data']
                if mint_address in price_data and price_data[mint_address] is not None:
                    price = float(price_data[mint_address])
                    logger.info(f"代币价格: ${price}")
                    return price
            return None
            
        except Exception as e:
            logger.error(f"获取价格失败: {str(e)}")
            return None

    def get_token_info(self, mint_address: str) -> Dict:
        """获取代币信息"""
        # 检查缓存
        if mint_address in self.token_info_cache:
            return self.token_info_cache[mint_address]
        
        try:
            headers = {
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            }
            
            # 使用 Raydium API 获取代币信息
            url = f"https://api-v3.raydium.io/mint/ids"
            params = {
                "mints": mint_address
            }
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success') and 'data' in data and len(data['data']) > 0:
                token_data = data['data'][0]
                result = {
                    'symbol': token_data.get('symbol', ''),
                    'name': token_data.get('name', ''),
                    'mint': mint_address
                }
                self.token_info_cache[mint_address] = result
                return result
            
            # 如果找不到代币信息，返回简化的地址
            logger.warning(f"无法从Raydium获取代币信息: {mint_address}")
            return {
                'symbol': mint_address[:8],
                'name': mint_address[:12],
                'mint': mint_address
            }
            
        except Exception as e:
            logger.warning(f"获取代币信息异常: {str(e)}")
            return {
                'symbol': mint_address[:8],
                'name': mint_address[:12],
                'mint': mint_address
            }

    def get_token_accounts(self, min_value_sol=0.01):
        try:
            if not WALLET_ADDRESS:
                logger.error("未设置钱包地址")
                return []
            
            logger.info(f"正在查询钱包地址: {WALLET_ADDRESS}")
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenAccountsByOwner",
                "params": [
                    WALLET_ADDRESS,
                    {
                        "programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
                    },
                    {
                        "encoding": "jsonParsed"
                    }
                ]
            }
            
            headers = {"Content-Type": "application/json"}
            logger.info("发送RPC请求...")
            response = requests.post(
                RPC_URL, 
                json=payload, 
                headers=headers,
                timeout=30
            )
            response_data = response.json()
            logger.info(f"RPC响应: {json.dumps(response_data, indent=2)}")
            
            if "result" not in response_data:
                return []
                
            accounts = response_data["result"]["value"]
            
            # 获取 SOL 价格
            sol_price = self.get_sol_price()
            if sol_price <= 0:
                logger.error("无法获取 SOL 价格")
                return []
            logger.info(f"当前 SOL 价格: ${sol_price}")
            
            # 批量处理代币，每批10个
            BATCH_SIZE = 10
            DELAY_SECONDS = 0.01  # 每批之间延迟2秒
            
            parsed_accounts = []
            account_batches = []
            current_batch = []
            
            for account in accounts:
                try:
                    parsed_data = account["account"]["data"]["parsed"]["info"]
                    if float(parsed_data["tokenAmount"]["uiAmount"] or 0) > 0:
                        current_batch.append({
                            'mint': parsed_data["mint"],
                            'amount': float(parsed_data["tokenAmount"]["uiAmount"]),
                            'decimals': parsed_data["tokenAmount"]["decimals"]
                        })
                        
                        if len(current_batch) >= BATCH_SIZE:
                            account_batches.append(current_batch)
                            current_batch = []
                except Exception:
                    continue
                    
            if current_batch:
                account_batches.append(current_batch)
                
            # 分批处理代币价格查询
            for batch in account_batches:
                # 收集当前批次的所有代币地址
                mint_addresses = [account['mint'] for account in batch]
                
                # 批量获取价格
                prices = self.get_batch_token_prices(mint_addresses)
                
                # 处理结果
                for account_info in batch:
                    if account_info['mint'] in prices:
                        price = prices[account_info['mint']]
                        value_sol = (account_info['amount'] * price) / sol_price
                        if value_sol >= min_value_sol:
                            token_info = self.get_token_info(account_info['mint'])
                            account_info.update({
                                'price': price,
                                'value_sol': value_sol,
                                'symbol': token_info['symbol'],
                                'name': token_info['name']
                            })
                            parsed_accounts.append(account_info)
                
                time.sleep(DELAY_SECONDS)
            return sorted(parsed_accounts, key=lambda x: x['value_sol'], reverse=True)
            
        except Exception as e:
            logger.error(f"获取代币账户时发生错误: {str(e)}")
            return []

    def get_batch_token_prices(self, mint_addresses: list) -> Dict[str, float]:
        """批量获取代币价格"""
        try:
            prices = {}
            raydium_url = "https://api-v3.raydium.io/mint/price"
            params = {
                "mints": ",".join(mint_addresses)
            }
            headers = {
                'Accept': 'application/json'
            }
            
            try:
                response = self.session.get(raydium_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get('success') and 'data' in data:
                    price_data = data['data']
                    for mint_address in mint_addresses:
                        if mint_address in price_data and price_data[mint_address] is not None:
                            try:
                                price = float(price_data[mint_address])
                                prices[mint_address] = price
                                logger.info(f"代币 {mint_address} 价格: ${price}")
                            except (ValueError, TypeError):
                                logger.warning(f"代币 {mint_address} 价格格式无效")
                        else:
                            logger.info(f"代币 {mint_address} 在Raydium上没有价���数据")
                
                return prices
                
            except Exception as e:
                logger.error(f"从Raydium获取价格败: {str(e)}")
                return {}
                
        except Exception as e:
            logger.error(f"批量获取价格失败: {str(e)}")
            return {}

def main():
    try:
        fetcher = TokenFetcher()
        accounts = fetcher.get_token_accounts()
        
        print("\n钱包代币持仓汇总 (价值 > 0.01 SOL):")
        print("-" * 120)
        print(f"{'代币符号':15} {'代币名称':30} {'合约地址':45} {'持有数量':>15} {'价格(USD)':>12} {'总价值(SOL)':>12}")
        print("-" * 120)
        
        total_value_sol = 0
        for account in accounts:
            name = account['name'][:28] + '..' if len(account['name']) > 30 else account['name']
            print(f"{account['symbol']:15} {name:30} {account['mint']:45} "
                  f"{account['amount']:15.6f} {account['price']:12.6f} "
                  f"{account['value_sol']:12.6f}")
            total_value_sol += account['value_sol']
        
        print("-" * 120)
        print(f"总计: {len(accounts)} 个代币, 总价值: {total_value_sol:.6f} SOL")
        
        return accounts  # 返回账户信息供其他能使用
            
    except Exception as e:
        logger.error(f"主程序执行失败: {str(e)}")
        return []

if __name__ == "__main__":
    main() 