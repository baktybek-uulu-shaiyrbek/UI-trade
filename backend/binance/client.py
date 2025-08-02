import hmac
import hashlib
import time
import aiohttp
import json
from urllib.parse import urlencode
import backoff
from binance.exceptions import BinanceAPIException
from utils.exceptions import TradingError

class BinanceTestNetClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binance.vision/api"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    def get_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
    async def send_signed_request(self, method: str, endpoint: str, params: dict):
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        
        url = self.base_url + endpoint
        
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        async with self.session.request(method, url, params=params, headers=headers) as response:
            data = await response.json()
            
            if response.status != 200:
                raise BinanceAPIException(response.status, data)
                
            return data
            
    @backoff.on_exception(
        backoff.expo,
        (BinanceAPIException, ConnectionError),
        max_tries=5,
        max_time=300,
        jitter=backoff.full_jitter,
        giveup=lambda e: getattr(e, 'code', None) in [-2015, -1121]
    )
    async def place_order(self, symbol: str, side: str, order_type: str, **kwargs):
        endpoint = "/v3/order"
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'timestamp': int(time.time() * 1000),
            'recvWindow': 5000,
            **kwargs
        }
        
        query_string = urlencode(params, True)
        params['signature'] = self.get_signature(query_string)
        
        return await self.send_signed_request("POST", endpoint, params)