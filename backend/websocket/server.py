import asyncio
import json
import logging
from websockets.server import serve
from typing import Dict, Set
from .handlers import TradingEndpoints

class TradingWebSocketServer:
    def __init__(self, host: str, port: int, binance_client):
        self.host = host
        self.port = port
        self.clients: Set = set()
        self.authenticated_clients: Dict = {}
        self.binance_client = binance_client
        # self.authenticator = JWTAuthenticator()
        self.endpoints = TradingEndpoints(binance_client, self)
        
    async def register_client(self, websocket):
        self.clients.add(websocket)
        logging.info(f"Client {websocket.remote_address} connected")
        
    async def authenticate_client(self, auth_message: str, websocket):
        return await self.authenticator.authenticate_websocket(auth_message)
        
    async def handle_client(self, websocket):
        await self.register_client(websocket)
        try:
            # First message must be authentication
            auth_message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            user = await self.authenticate_client(auth_message, websocket)
            
            if not user:
                await websocket.close(code=1008, reason="Authentication failed")
                return
                
            self.authenticated_clients[websocket] = user
            
            # Handle authenticated messages
            async for message in websocket:
                await self.endpoints.handle_message(json.loads(message), websocket)
                
        except Exception as e:
            logging.error(f"Client error: {e}")
        finally:
            self.clients.discard(websocket)
            self.authenticated_clients.pop(websocket, None)
            
    async def start_server(self):
        async with serve(self.handle_client, self.host, self.port):
            logging.info(f"Trading WebSocket server started on {self.host}:{self.port}")
            await asyncio.Future()  # run forever
            
    async def broadcast_to_user(self, user_id: str, message: dict):
        """Broadcast message to all connections of a specific user"""
        for ws, user in self.authenticated_clients.items():
            if user['user_id'] == user_id:
                await ws.send(json.dumps(message))