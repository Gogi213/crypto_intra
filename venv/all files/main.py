import sys
from flask import Flask
from flask_socketio import SocketIO
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import asyncio
import threading

# Добавляем путь к папке, содержащей app.py, в системный путь
app_path = r'C:\\Users\\Redmi\\PycharmProjects\\crypto_intra\\venv\\all files\\flask'
sys.path.append(app_path)

# Теперь можно импортировать app и socketio из app.py и функцию connect_to_websocket из binance_pulsar.py
from app import app, socketio
from binance_pulsar import connect_to_websocket, pairs_list

def start_websockets():
    # Создаем новый цикл событий для этого потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Создаем WebSocket-соединение для каждого chunk
    ws_connections = {}
    for i, chunk in enumerate(pairs_list):
        ws_connections[f'multi{i}'] = asyncio.ensure_future(connect_to_websocket(chunk))

    # Запускаем все WebSocket-соединения
    loop.run_until_complete(asyncio.gather(*ws_connections.values()))

if __name__ == "__main__":
    # Запускаем вебсокеты в отдельном потоке
    ws_thread = threading.Thread(target=start_websockets)
    ws_thread.start()

    # Запускаем Flask-приложение
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()







# from calculate_profit import calculate_triple_exchanges
# output_path = r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\debug_df_data.csv'
# triple_exchanges = calculate_triple_exchanges(output_path)
# print("Triple exchanges saved to CSV:", output_path)
