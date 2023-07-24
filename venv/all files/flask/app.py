# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from threading import Thread
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19938713@localhost:3306/crypto_intra'
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class BinanceData(db.Model):
    __tablename__ = 'binance_socket_prices'
    symbol = db.Column(db.String(50), primary_key=True)
    askprice = db.Column(db.Float)
    askqty = db.Column(db.Float)
    bidprice = db.Column(db.Float)
    bidqty = db.Column(db.Float)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route('/')
def home():
    table1 = BinanceData.query.all()
    return render_template('home.html', table1=table1)

@socketio.on('connect')
def test_connect():
    emit('binance update', {'data': 'Connected'})

@socketio.on('request update')
def update():
    table1 = [row.to_dict() for row in BinanceData.query.all()]
    emit('binance update', {'data': table1})

def background_thread():
    with app.app_context():
        while True:
            socketio.sleep(100)
            table1 = [row.to_dict() for row in BinanceData.query.all()]
            socketio.emit('binance update', {'data': table1})

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.cache_control.proxy_revalidate = True
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    socketio.start_background_task(background_thread)
    socketio.run(app)