import json
import asyncio
from fastapi import FastAPI, WebSocket
from binance.client import Client
import websockets

app = FastAPI()
clients = set()


BINANCE_API_KEY = "57795ea630735102707074edf67fe1eb2c18886204cfb2e1b30354399be254ed"
BINANCE_API_SECRET = "405fdcbc82754009a6fb8ba804e6587311163ec2289620750578bbaa16cf25e1"
SYMBOL = "BTCUSDT"

async def send_open_orders(websocket: WebSocket):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
    open_orders = client.futures_get_open_orders(symbol=SYMBOL)
    await websocket.send_text(json.dumps({
        "type": "open_orders",
        "orders": open_orders
    }))
    print(f"[SEND] Отправлены открытые ордера: {len(open_orders)} шт.")

async def push_order_updates(websocket: WebSocket):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
    listen_key = client.futures_stream_get_listen_key()
    ws_url = f"wss://fstream.binancefuture.com/ws/{listen_key}"
    print("[Binance] Слушаю ws:", ws_url)
    async with websockets.connect(ws_url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get('e') == 'ORDER_TRADE_UPDATE':
                await websocket.send_text(json.dumps({
                    "type": "order_update",
                    "data": data
                }))
                print("[PUSH]", data['o']['i'], data['o']['X'])

@app.websocket("/ws")
async def ws_orders(websocket: WebSocket):
    await websocket.accept()
    print("[Client] ws подключен")
    try:
        await send_open_orders(websocket)
        await push_order_updates(websocket)
    except Exception as e:
        print("[ERROR]", e)
    finally:    
        print("[Client] ws отключён")

@app.websocket("/ws-pnl")
async def ws_pnl(websocket: WebSocket):
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
    symbol = "BTCUSDT"
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            positions = client.futures_position_information(symbol=symbol)
            unrealized_pnl = None
            for pos in positions:
                if pos['symbol'] == symbol:
                    unrealized_pnl = pos['unRealizedProfit']
                    break
            if unrealized_pnl is not None:
                await websocket.send_text(json.dumps({
                    "symbol": symbol,
                    "unrealized_pnl": unrealized_pnl
                }))
            await asyncio.sleep(2)  # Пушим каждые 2 секунды (можно реже)
    except Exception as e:
        print("WS error:", e)
    finally:
        clients.discard(websocket)

