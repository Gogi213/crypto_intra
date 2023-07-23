# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19938713@localhost:3306/crypto_intra'
db = SQLAlchemy(app)

class BinanceData(db.Model):
    __tablename__ = 'binance_socket_prices'
    symbol = db.Column(db.String(50), primary_key=True)
    askprice = db.Column(db.Float)
    askqty = db.Column(db.Float)
    bidprice = db.Column(db.Float)
    bidqty = db.Column(db.Float)

@app.route('/')
def home():
    table1 = BinanceData.query.all()
    return render_template('home.html', table1=table1)

if __name__ == '__main__':
    app.run(debug=True)
