import websocket
import threading
import time
import json
from flask_socketio import SocketIO, emit
from flask import render_template

import sys
sys.path.insert(0, '/flask')

from app import app, socketio

# List of currency pairs
# Replace these with your actual pairs
pairs1 = ['1inchbtc', '1inchbusd', '1inchusdt', 'aavebnb', 'aavebtc', 'aavebusd', 'aaveusdt', 'acabtc', 'acabusd', 'acatry', 'acausdt', 'achbtc', 'achbusd', 'achtry', 'achusdt', 'acmbusd', 'acmusdt', 'adabnb', 'adabrl', 'adabtc', 'adabusd', 'adaeth', 'adaeur', 'adatry', 'adausdt', 'adadownusdt', 'adaupusdt', 'adxusdt', 'aergousdt', 'agixbtc', 'agixbusd', 'agixtry', 'agixusdt', 'agldbtc', 'agldbusd', 'agldusdt', 'akrousdt', 'alcxusdt', 'algobtc', 'algobusd', 'algotry', 'algousdt', 'alicebusd', 'aliceusdt', 'alpacabtc', 'alpacabusd', 'alpacausdt', 'alphausdt', 'alpinebusd', 'alpinetry', 'alpineusdt', 'ambbusd', 'ambusdt', 'ampbusd', 'ampusdt', 'ankrbtc', 'ankrbusd', 'ankrtry', 'ankrusdt', 'antusdt', 'apebtc', 'apebusd', 'apetry', 'apeusdt', 'api3usdt', 'aptbtc', 'aptbusd', 'apttry', 'aptusdt', 'arbtc', 'arusdt', 'arbbtc', 'arbeth', 'arbtry', 'arbtusd', 'arbusdt', 'ardrusdt', 'arkbusd', 'arkmbnb', 'arkmbtc', 'arkmtry', 'arkmtusd', 'arkmusdt', 'arpabusd', 'arpatry', 'arpausdt', 'asrusdt', 'astbtc', 'astusdt', 'astrbtc', 'astrbusd', 'astrusdt', 'atausdt', 'atmbusd', 'atmusdt', 'atombtc', 'atombusd', 'atometh', 'atomeur', 'atomtry', 'atomusdt', 'auctionbtc', 'auctionbusd', 'auctionusdt', 'audiotry', 'audiousdt', 'avabtc', 'avausdt', 'avaxbnb', 'avaxbtc', 'avaxbusd', 'avaxeth', 'avaxeur', 'avaxtry', 'avaxusdt', 'axsbtc', 'axsbusd', 'axsusdt', 'badgerusdt', 'bakebusd', 'bakeusdt', 'balusdt', 'bandbusd', 'bandusdt', 'barbusd', 'barusdt', 'batbusd', 'batusdt', 'bchbnb', 'bchbtc', 'bchbusd', 'bcheur', 'bchtry', 'bchusdt', 'bdotdot', 'belbusd', 'beltry', 'belusdt', 'betausdt']
pairs2 = ['betheth', 'bethusdt', 'bicousdt', 'bifiusdt', 'blzbtc', 'blzusdt', 'bnbbidr', 'bnbbrl', 'bnbbtc', 'bnbbusd', 'bnbeth', 'bnbeur', 'bnbfdusd', 'bnbgbp', 'bnbtry', 'bnbtusd', 'bnbusdc', 'bnbusdt', 'bnbdownusdt', 'bnbupusdt', 'bntusdt', 'bnxusdt', 'bondbusd', 'bondusdt', 'bswbusd', 'bswtry', 'bswusdt', 'btcars', 'btcbidr', 'btcbrl', 'btcbusd', 'btcdai', 'btceur', 'btcgbp', 'btcngn', 'btcpln', 'btcrub', 'btctry', 'btctusd', 'btcusdc', 'btcusdt', 'btczar', 'btcdownusdt', 'btcupusdt', 'btsusdt', 'bttctry', 'bttcusdt', 'burgerbusd', 'burgerusdt', 'busdbidr', 'busdbrl', 'busddai', 'busdpln', 'busdrub', 'busdtry', 'busdusdt', 'busdzar', 'c98usdt', 'cakebnb', 'cakebusd', 'cakeusdt', 'celobtc', 'celobusd', 'celousdt', 'celrbusd', 'celrusdt', 'cfxbtc', 'cfxbusd', 'cfxtry', 'cfxusdt', 'chessbtc', 'chessbusd', 'chessusdt', 'chrbtc', 'chrbusd', 'chrusdt', 'chzbtc', 'chzbusd', 'chztry', 'chzusdt', 'citybusd', 'citytry', 'cityusdt', 'ckbusdt', 'clvbtc', 'clvbusd', 'clvusdt', 'combotry', 'combousdt', 'compbtc', 'compbusd', 'comptry', 'compusdt', 'cosbtc', 'costry', 'cosusdt', 'cotibusd', 'cotiusdt', 'creambusd', 'crvbtc', 'crvbusd', 'crvusdt', 'ctkusdt', 'ctsiusdt', 'ctxcbusd', 'ctxcusdt', 'cvcusdt', 'cvpbusd', 'cvpusdt', 'cvxbtc', 'cvxbusd', 'cvxusdt', 'darbusd', 'dartry', 'darusdt', 'dashbtc', 'dashusdt', 'datausdt', 'dcrusdt', 'degobtc', 'degousdt', 'dentbusd', 'denttry', 'dentusdt', 'dexeusdt', 'dfusdt', 'dgbbtc', 'dgbbusd', 'dgbusdt', 'diabtc', 'diabusd', 'diausdt', 'dockusdt', 'dodobusd', 'dodousdt', 'dogebidr', 'dogebrl', 'dogebtc', 'dogebusd', 'dogeeur', 'dogegbp', 'dogetry', 'dogetusd', 'dogeusdt', 'dotbtc', 'dotusdt']
pairs3 = [ 'dprbusd', 'dprusdt', 'duskbusd', 'duskusdt', 'duskdownusdt', 'duskupusdt', 'dvdusdt', 'dxdbusd', 'dxdusdt', 'eaaveusdt', 'edobtc', 'edobusd', 'edousdt', 'efobusd', 'egldusdt', 'ekousdt', 'elfusdt', 'elrusdt', 'elusdt', 'enjusdt', 'enousdt', 'eosbusd', 'eosusdt', 'ergusdt', 'erousdt', 'eusdcusdt', 'eurusdt', 'evxusdt', 'ezbtc', 'ezusdt', 'ezdownusdt', 'ezupusdt', 'fabusd', 'fabusdt', 'fchusdt', 'fetusdt', 'fidausdt', 'filbtc', 'filbusd', 'filtry', 'filusdt', 'fiousdt', 'flmbtc', 'flmbusd', 'flmusdt', 'flrusdt', 'flowbusd', 'flowusdt', 'flrtry', 'flrusdt', 'fltry', 'flusdt', 'fmirub', 'fmibusd', 'fmibusdt', 'fmirusdt', 'fmusdt', 'forsusdt', 'frontusdt', 'ftmusdt', 'fttbusd', 'fttusdt']

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

def on_message(ws, message):
    # Print the raw message
    print(f'Raw message: {message}')

    # Parse the message
    msg = json.loads(message)

    # Check if 'data' is in the message
    if 'data' in msg and 's' in msg['data']:
        # Update the data
        data[msg['data']['s'].lower()] = {'symbol': msg['data']['s'], 'askprice': msg['data']['a'], 'askqty': msg['data']['A'], 'bidprice': msg['data']['b'], 'bidqty': msg['data']['B']}

        # Send the data to the web page
        socketio.emit('binance update', {'data': data[msg['data']['s'].lower()]})
    else:
        print(f"Message without 'data' or 's': {msg}")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print('WebSocket connection closed')

def create_on_open(pairs):
    def on_open(ws):
        print('WebSocket connection opened')
        params = {
            'method': 'SUBSCRIBE',
            'params': [f'{pair}@bookTicker' for pair in pairs],
            'id': 1
        }
        ws.send(json.dumps(params))
    return on_open

# Create a WebSocket connection for each chunk
for i, pairs in enumerate(pairs_list):
    ws = websocket.WebSocketApp('wss://stream.binance.com:9443/stream',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = create_on_open(pairs)
    ws_connections[f'multi{i}'] = ws

# Start all WebSocket connections
for ws in ws_connections.values():
    if not ws.sock or not ws.sock.connected:
        threading.Thread(target=ws.run_forever).start()