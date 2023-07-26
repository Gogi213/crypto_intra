import websocket
import threading
import time
import json
from flask_socketio import SocketIO, emit
from flask import render_template

import sys
sys.path.insert(0, '/flask')

from app import app, socketio

# Import the Flask and SocketIO instances from app.py
from app import app, socketio

# List of currency pairs
currency_pairs = ['btcusdt', 'ethusdt', 'bnbusdt', 'ltcusdt']

# WebSocket connections dictionary
ws_connections = {}

# Data storage
data = {pair: {} for pair in currency_pairs}

@app.route('/')
def index():
    return render_template('home.html')

@socketio.on('request update')
def update():
    for pair in currency_pairs:
        emit('binance update', {'data': data[pair]})

def on_message(ws, message):
    # Parse the message
    msg = json.loads(message)

    # Update the data
    data[msg['s'].lower()] = {'symbol': msg['s'], 'askprice': msg['a'], 'askqty': msg['A'], 'bidprice': msg['b'], 'bidqty': msg['B']}

    # Send the data to the web page
    socketio.emit('binance update', {'data': data[msg['s'].lower()]})

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print('WebSocket connection closed')

def on_open(ws):
    print('WebSocket connection opened')

# Create a WebSocket connection for each currency pair
for pair in currency_pairs:
    ws = websocket.WebSocketApp(f'wss://stream.binance.com:9443/ws/{pair}@bookTicker',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws_connections[pair] = ws

# Start all WebSocket connections
for ws in ws_connections.values():
    threading.Thread(target=ws.run_forever).start()