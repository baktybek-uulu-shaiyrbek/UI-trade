import asyncio
import logging
from config.settings import Settings
from websocket.server import TradingWebSocketServer
from binance.client import BinanceTestNetClient
from database.connection import Database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Initialize settings
    settings = Settings()
    
    # Initialize database
    db = Database(settings.database_url)
    await db.connect()
    
    # Initialize Binance client
    binance_client = BinanceTestNetClient(
        api_key=settings.binance_api_key,
        api_secret=settings.binance_api_secret
    )
    
    # Initialize and start WebSocket server
    ws_server = TradingWebSocketServer(
        host="0.0.0.0",
        port=8765,
        binance_client=binance_client,
        database=db
    )
    
    await ws_server.start_server()

if __name__ == "__main__":
    asyncio.run(main())