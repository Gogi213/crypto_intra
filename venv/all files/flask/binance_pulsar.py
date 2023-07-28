import yappi
import asyncio
import websockets
import json
import threading
from flask_socketio import emit
from app import socketio
import aiohttp

# Вставьте свой API ключ здесь
API_KEY = 'jByRuDyDvM3bQl71hLgadWt932jodjvpJRqvXsQRIWHfpSZwxYBR7BWFBOXO7o6b'

pairs1 = ['1inchbtc', '1inchbusd', '1inchusdt', 'aavebnb', 'aavebtc', 'aavebusd', 'aaveusdt', 'acabtc', 'acabusd', 'acatry', 'acausdt', 'achbtc', 'achbusd', 'achtry', 'achusdt', 'acmbusd', 'acmusdt', 'adabnb', 'adabrl', 'adabtc', 'adabusd', 'adaeth', 'adaeur', 'adatry', 'adausdt', 'adadownusdt']
pairs2 = ['alpineusdt', 'ambbusd', 'ambusdt', 'ampbusd', 'ampusdt', 'ankrbtc', 'ankrbusd', 'ankrtry', 'ankrusdt', 'antusdt', 'apebtc', 'apebusd', 'apetry', 'apeusdt', 'api3usdt', 'aptbtc', 'aptbusd', 'apttry', 'aptusdt', 'arbtc', 'arusdt', 'arbbtc', 'arbeth', 'arbtry', 'arbtusd', 'arbusdt']
pairs3 = ['atomusdt', 'auctionbtc', 'auctionbusd', 'auctionusdt', 'audiotry', 'audiousdt', 'avabtc', 'avausdt', 'avaxbnb', 'avaxbtc', 'avaxbusd', 'avaxeth', 'avaxeur', 'avaxtry', 'avaxusdt', 'axsbtc', 'axsbusd', 'axsusdt', 'badgerusdt', 'bakebusd', 'bakeusdt', 'balusdt', 'bandbusd']

pairs_list = [pairs1, pairs2, pairs3]

data = {pair: {} for sublist in pairs_list for pair in sublist}

@socketio.on('request update')
def update():
    for pair in data.keys():
        emit('binance update', {'data': data[pair]})

async def connect_to_websocket(chunk):
    uri = 'wss://stream.binance.com:9443/stream'
    async with websockets.connect(uri, extra_headers={'X-MBX-APIKEY': API_KEY}) as ws:
        params = {
            'method': 'SUBSCRIBE',
            'params': [f'{pair}@bookTicker' for pair in chunk],
            'id': 1
        }
        await ws.send(json.dumps(params))

        while True:
            message = await ws.recv()
            print(f'Raw message: {message}')

            msg = json.loads(message)

            if 'data' in msg and 's' in msg['data']:
                data[msg['data']['s'].lower()] = {'symbol': msg['data']['s'], 'askprice': msg['data']['a'], 'askqty': msg['data']['A'], 'bidprice': msg['data']['b'], 'bidqty': msg['data']['B']}
                socketio.emit('binance update', {'data': data[msg['data']['s'].lower()]})
