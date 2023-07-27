import asyncio
import websockets
import json
from flask_socketio import emit

# Импортируем socketio из app.py
from app import socketio

# List of currency pairs
# Replace these with your actual pairs
pairs1 = ['1inchbtc','1inchbusd','1inchusdt','aavebnb','aavebtc']
pairs2 = ['alpineusdt','ambbusd','ambusdt','ampbusd','ampusdt']
pairs3 = ['atomusdt','auctionbtc','auctionbusd','auctionusdt','audiotry']
pairs4 = ['bnbeur','bnbfdusd','bnbgbp','bnbtry','bnbtusd']
pairs5 = ['celobtc','celobusd','celousdt','celrbusd','celrusdt']

pairs_list = [pairs1, pairs2, pairs3, pairs4, pairs5]

# Data storage
data = {pair: {} for sublist in pairs_list for pair in sublist}

@socketio.on('request update')
def update():
    for pair in data.keys():
        emit('binance update', {'data': data[pair]})

async def connect_to_websocket(chunk):
    uri = 'wss://stream.binance.com:9443/stream'
    async with websockets.connect(uri) as ws:
        params = {
            'method': 'SUBSCRIBE',
            'params': [f'{pair}@bookTicker' for pair in chunk],
            'id': 1
        }
        await ws.send(json.dumps(params))

        while True:
            message = await ws.recv()
            print(f'Raw message: {message}')

            # Parse the message
            msg = json.loads(message)

            # Check if 'data' is in the message
            if 'data' in msg and 's' in msg['data']:
                # Update the data
                data[msg['data']['s'].lower()] = {'symbol': msg['data']['s'], 'askprice': msg['data']['a'], 'askqty': msg['data']['A'], 'bidprice': msg['data']['b'], 'bidqty': msg['data']['B']}

                # Send the data to the web page
                socketio.emit('binance update', {'data': data[msg['data']['s'].lower()]})
