from pulsar import Client
import websocket
import json
import pandas as pd
import sys
sys.path.append('C:/Users/Redmi/PycharmProjects/crypto_intra/venv/all files')
from bd_case import connect_to_db, update_or_insert_trade_pairs


# Инициализация клиента Pulsar
client = Client('pulsar://localhost:6650')

# Инициализация продюсера Pulsar
producer = client.create_producer('binance')

# Определение функций обратного вызова WebSocket
trading_pairs = ['btcusdt', 'ethusdt', 'bnbusdt']  # и так далее для всех ваших торговых пар

def on_open(ws):
    print('Соединение с WebSocket открыто.')
    # Подписка на все торговые пары
    for pair in trading_pairs:
        ws.send(json.dumps({
            'method': 'SUBSCRIBE',
            'params': [f'{pair}@depth'],
            'id': 1
        }))

def on_message(ws, message):
    # Convert message to Python dictionary
    data = json.loads(message)

    # Check if the message is a depth update
    if 'e' in data and data['e'] == 'depthUpdate':
        # Check if there is enough market depth
        if not data['b'] or not data['a']:
            print(f'Not enough market depth: {data}')
            return

        # Keep only the necessary columns and rename them
        filtered_data = {
            'symbol': data['s'],
            'askprice': data['a'][0][0],
            'askqty': data['a'][0][1],
            'bidprice': data['b'][0][0],
            'bidqty': data['b'][0][1]
        }

        # Convert dictionary back to JSON string
        filtered_message = json.dumps(filtered_data)

        # Try to send the message
        try:
            # Convert message to bytes and publish to Pulsar
            producer.send(bytes(filtered_message, 'utf-8'))
        except:
            print('Pulsar producer is closed. Attempting to reconnect.')
            reconnect_pulsar()

        # Update the values in the database
        df = pd.DataFrame([filtered_data])
        print(df)  # <--- Add this line to print the dataframe
        engine = connect_to_db(database='crypto_intra')
        update_or_insert_trade_pairs(engine, df)
    else:
        print(f'Unexpected message: {data}')


def on_error(ws, error):
    print(f'Ошибка WebSocket: {error}')

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    # Закрытие продюсера и клиента Pulsar
    producer.close()
    client.close()

# Connection management functions

def reconnect_pulsar():
    global client, producer
    try:
        client.close()
    except Exception as e:
        print(f'Error closing Pulsar client: {e}')
    client = Client('pulsar://localhost:6650')
    producer = client.create_producer('binance')

# Подключение к WebSocket API Binance
ws = websocket.WebSocketApp(
    'wss://stream.binance.com:9443/ws',
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
ws.run_forever()