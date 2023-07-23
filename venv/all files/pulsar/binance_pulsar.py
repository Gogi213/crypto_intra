from pulsar import Client
import websocket
import json
import pandas as pd
from bd import connect_to_db, update_or_insert_trade_pairs  # Add update_or_insert_trade_pairs to the import statement



# Инициализация клиента Pulsar
client = Client('pulsar://localhost:6650')

# Инициализация продюсера Pulsar
producer = client.create_producer('binance')

# Определение функций обратного вызова WebSocket

def on_open(ws):
    print('Соединение с WebSocket открыто.')
    # Подписка на все торговые пары
    ws.send(json.dumps({
        'method': 'SUBSCRIBE',
        'params': ['!ticker@arr'],
        'id': 1
    }))

def on_message(ws, message):
    # Convert message to list of Python dictionaries
    data_list = json.loads(message)

    for data in data_list:
        if isinstance(data, dict):
            # Keep only the necessary columns and rename them
            filtered_data = {
                'symbol': data['s'],
                'askprice': data['a'],
                'askqty': data['A'],
                'bidprice': data['b'],
                'bidqty': data['B']
            }

            # Print filtered data to console
            print(filtered_data)

            # Convert dictionary back to JSON string
            filtered_message = json.dumps(filtered_data)

            # Convert message to bytes and publish to Pulsar
            producer.send(bytes(filtered_message, 'utf-8'))

            # Update the values in the database
            df = pd.DataFrame([filtered_data])
            engine = connect_to_db(database='crypto_intra')
            update_or_insert_trade_pairs(engine, df)  # Replace update_table with update_or_insert_trade_pairs





def on_error(ws, error):
    print(f'Ошибка WebSocket: {error}')

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    # Закрытие продюсера и клиента Pulsar
    producer.close()
    client.close()

# Подключение к WebSocket API Binance
ws = websocket.WebSocketApp(
    'wss://stream.binance.com:9443/ws',
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
ws.run_forever()