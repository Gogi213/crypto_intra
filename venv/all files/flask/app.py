# app.py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19938713@localhost:3306/crypto_intra'
db = SQLAlchemy(app)

class BinanceData(db.Model):
    __tablename__ = 'binance_bundles'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50))
    base = db.Column(db.String(50))
    quote = db.Column(db.String(50))
    swap = db.Column(db.String(50))
    symbol2 = db.Column(db.String(50))
    base2 = db.Column(db.String(50))
    quote2 = db.Column(db.String(50))
    swap2 = db.Column(db.String(50))
    symbol3 = db.Column(db.String(50))
    base3 = db.Column(db.String(50))
    quote3 = db.Column(db.String(50))
    swap3 = db.Column(db.String(50))

@app.route('/')
def home():
    table1 = BinanceData.query.all()
    return render_template('home.html', table1=table1)

if __name__ == '__main__':
    app.run(debug=True)
