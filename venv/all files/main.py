import sys
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask
from flask_socketio import SocketIO

# Добавляем путь к папке, содержащей binance_pulsar.py, в системный путь
binance_pulsar_path = r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\flask'
sys.path.append(binance_pulsar_path)

# Теперь можно импортировать app из binance_pulsar
from binance_pulsar import app


# from calculate_profit import calculate_triple_exchanges
#
# output_path = r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\debug_df_data.csv'

# triple_exchanges = calculate_triple_exchanges(output_path)

# print("Triple exchanges saved to CSV:", output_path)

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
