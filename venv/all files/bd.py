from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import numpy as np

Base = declarative_base()

class TradePair(Base):
    __tablename__ = 'binance_socket_prices'
    symbol = Column(String, primary_key=True)
    askprice = Column(Float)
    askqty = Column(Float)
    bidprice = Column(Float)
    bidqty = Column(Float)

def connect_to_db(database='crypto_intra', user='root', password='19938713', host='localhost', port='3306'):
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    return engine

def update_table(engine, df, table_name):
    # Clean up the data
    df = df.replace([np.inf, -np.inf], None)

    # Dataframe to sql table
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def update_or_insert_trade_pairs(engine, df):
    Session = sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():
        trade_pair = session.query(TradePair).filter_by(symbol=row['symbol']).first()
        if trade_pair is None:
            # If the trade pair does not exist in the table, create a new one
            trade_pair = TradePair(symbol=row['symbol'])
        # Update the trade pair with the new data
        trade_pair.ask_price = row['askprice']
        trade_pair.ask_quantity = row['askqty']
        trade_pair.bid_price = row['bidprice']
        trade_pair.bid_quantity = row['bidqty']
        session.merge(trade_pair)

    session.commit()