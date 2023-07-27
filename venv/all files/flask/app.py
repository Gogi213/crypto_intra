from flask import Flask, render_template
from flask_socketio import SocketIO

# Создаем Flask-приложение
app = Flask(__name__, template_folder=r'C:\\Users\\Redmi\\PycharmProjects\\crypto_intra\\venv\\all files\\flask\\templates')

# Создаем SocketIO-приложение
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('home.html')

# Импортируем binance_pulsar
import binance_pulsar
