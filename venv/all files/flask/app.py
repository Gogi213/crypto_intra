from flask import Flask
from flask_socketio import SocketIO
import os

# Create Flask application
app = Flask(__name__, template_folder=r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\flask\templates')


# Create SocketIO application
socketio = SocketIO(app)

# Import the routes module
import binance_pulsar
