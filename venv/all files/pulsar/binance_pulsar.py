import websocket
import threading
import time
import json
import pandas as pd
from bd_case import connect_to_db, update_or_insert_trade_pairs
from pulsar import Client

# List of currency pairs
currency_pairs = ['btcusdt', 'qtumeth', 'eoseth', 'snteth', 'bnteth', 'bnbeth', 'lrceth', 'funeth', 'neoeth', 'iotaeth', 'linketh', 'xvgeth', 'mtleth', 'etceth', 'zeceth', 'dasheth', 'trxeth', 'powreth', 'xrpeth', 'enjeth', 'xmreth', 'bateth', 'neobnb', 'lsketh', 'manaeth', 'iotabnb', 'adxeth', 'adaeth', 'xlmeth', 'xlmbnb', 'ltceth', 'ltcbnb', 'waveseth', 'elfeth', 'rlceth', 'iosteth', 'steemeth', 'zileth', 'zilbnb', 'waneth', 'adabnb', 'ethtusd', 'zeneth', 'eosbnb', 'thetaeth', 'thetabnb', 'xrpbnb', 'iotxeth', 'qkceth', 'trxbnb', 'etcbnb', 'sceth', 'denteth', 'hoteth', 'veteth', 'vetbnb', 'bnbtusd', 'xrptusd', 'bnbusdc', 'ethusdc', 'adatusd', 'trxxrp', 'ltctusd', 'fetbnb', 'xmrbnb', 'celrbnb', 'maticbnb', 'atombnb', 'onebnb', 'ftmbnb', 'algobnb', 'ankrbnb', 'winbnb', 'cosbnb', 'wintrx', 'chzbnb', 'bnbbusd', 'hbarbnb', 'xrpbusd', 'ethbusd', 'ltcbusd', 'linkbusd', 'etcbusd', 'stxbnb', 'kavabnb', 'arpabnb', 'trxbusd', 'eosbusd', 'xlmbusd', 'adabusd', 'bchbnb', 'bchtusd', 'bchbusd', 'ethrub', 'xrprub', 'bnbrub', 'busdrub', 'qtumbusd', 'vetbusd']  # Add more pairs as needed

# WebSocket connections dictionary
ws_connections = {}

# Data storage
data = {pair: {} for pair in currency_pairs}

# Pulsar client
client = Client('pulsar://localhost:6650')
producer = client.create_producer('binance')

def on_message(ws, message):
    # Parse the message
    msg = json.loads(message)

    # Update the data
    global data
    data[msg['s'].lower()] = {'symbol': msg['s'], 'askprice': msg['a'], 'askqty': msg['A'], 'bidprice': msg['b'], 'bidqty': msg['B']}

    # Update the values in the database
    df = pd.DataFrame([data[msg['s'].lower()]])
    print(df)
    engine = connect_to_db(database='crypto_intra')
    update_or_insert_trade_pairs(engine, df)

    # Send the data to Pulsar
    producer.send(bytes(json.dumps(data[msg['s'].lower()]), 'utf-8'))

def on_error(ws, error):
    print(error)

def on_close(ws):
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
