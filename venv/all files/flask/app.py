from flask import Flask, render_template
from flask_socketio import SocketIO
import sys

# Create Flask application
app = Flask(__name__, template_folder=r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\flask\templates')

# Create SocketIO application
socketio = SocketIO(app)

# Import the routes module
import binance_pulsar

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
