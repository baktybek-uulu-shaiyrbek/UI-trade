import logging
import asyncio
import json
import websockets

class OrderStatusManager:
    def __init__(self, binance_client, websocket_server):
        self.binance_client = binance_client
        self.websocket_server = websocket_server
        self.active_orders = {}
        
    async def start_user_data_stream(self):
        # Create listen key
        response = await self.binance_client.create_listen_key()
        listen_key = response['listenKey']
        
        # Connect to user data stream
        url = f"wss://stream.binance.com:9443/ws/{listen_key}"
        async with websockets.connect(url) as websocket:
            async for message in websocket:
                await self.handle_user_update(json.loads(message))
                
    async def handle_user_update(self, message):
        if message.get('e') == 'executionReport':
            # Order update
            order_id = message['c']
            status = message['X']
            
            # Update local state
            self.active_orders[order_id] = message
            
            # Broadcast to relevant clients
            await self.websocket_server.broadcast_order_update({
                "type": "order_status_update",
                "orderId": order_id,
                "status": status,
                "side": message['S'],
                "symbol": message['s'],
                "price": message['p'],
                "quantity": message['q'],
                "executedQty": message['z'],
                "timestamp": message['E']
            })