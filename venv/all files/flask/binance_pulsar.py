import asyncio
import websockets
import json
from flask_socketio import SocketIO, emit
from flask import Flask, render_template

app = Flask(__name__)
socketio = SocketIO(app)

# List of currency pairs
# Replace these with your actual pairs
pairs1 = ['1inchbtc', '1inchbusd', '1inchusdt']
pairs2 = ['betheth', 'bethusdt', 'bicousdt']
pairs3 = [ 'dprbusd', 'dprusdt', 'duskbusd']

pairs_list = [pairs1, pairs2, pairs3]

# WebSocket connections dictionary
ws_connections = {}

# Data storage
data = {pair: {} for sublist in pairs_list for pair in sublist}

@app.route('/')
def index():
    return render_template('home.html')

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

# Create a WebSocket connection for each chunk
for i, chunk in enumerate(pairs_list):
    ws_connections[f'multi{i}'] = asyncio.ensure_future(connect_to_websocket(chunk))

# Run all WebSocket connections
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*ws_connections.values()))

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)