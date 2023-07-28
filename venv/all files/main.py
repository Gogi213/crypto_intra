# main.py
import sys
from flask import Flask
from flask_socketio import SocketIO
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import asyncio
import threading

# Add the path to the folder containing app.py to the system path
app_path = r'C:\\Users\\Redmi\\PycharmProjects\\crypto_intra\\venv\\all files\\flask'
sys.path.append(app_path)

# Now we can import app and socketio from app.py and the function connect_to_websocket from binance_pulsar.py
from app import app
from binance_pulsar import connect_to_websocket, pairs_list

def start_websockets():
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Create a WebSocket connection for each chunk
    ws_connections = {}
    for i, chunk in enumerate(pairs_list):
        ws_connections[f'multi{i}'] = asyncio.ensure_future(connect_to_websocket(chunk))

    # Start all WebSocket connections
    loop.run_until_complete(asyncio.gather(*ws_connections.values()))

if __name__ == "__main__":
    # Start the websockets in a separate thread
    ws_thread = threading.Thread(target=start_websockets)
    ws_thread.start()

    # Start the Flask application
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()


# from calculate_profit import calculate_triple_exchanges
# output_path = r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\debug_df_data.csv'
# triple_exchanges = calculate_triple_exchanges(output_path)
# print("Triple exchanges saved to CSV:", output_path)
