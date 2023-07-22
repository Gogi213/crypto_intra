from pulsar import Client
import websocket
import json

# Initialize Pulsar client
client = Client('pulsar://localhost:6650')

# Initialize Pulsar producer
producer = client.create_producer('binance')

# Define WebSocket callback functions

def on_open(ws):
    print('WebSocket connection opened.')
    # Subscribe to all trading pairs
    ws.send(json.dumps({
        'method': 'SUBSCRIBE',
        'params': ['!ticker@arr'],
        'id': 1
    }))

def on_message(ws, message):
    # Convert message to bytes and publish to Pulsar
    producer.send(bytes(message, 'utf-8'))

def on_error(ws, error):
    print(f'WebSocket error: {error}')

def on_close(ws):
    print('WebSocket connection closed.')
    # Close Pulsar producer and client
    producer.close()
    client.close()

# Connect to Binance WebSocket API
ws = websocket.WebSocketApp(
    'wss://stream.binance.com:9443/ws',
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
ws.run_forever()
