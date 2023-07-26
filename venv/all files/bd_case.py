# bd_case.py
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
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
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}',
                           poolclass=QueuePool,
                           pool_size=10,  # Adjust as needed
                           max_overflow=20  # Adjust as needed
                           )
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
            session.add(trade_pair)
        # Update the trade pair with the new data
        session.query(TradePair).filter_by(symbol=row['symbol']).update({
            'askprice': row['askprice'],
            'askqty': row['askqty'],
            'bidprice': row['bidprice'],
            'bidqty': row['bidqty']
        })

    session.commit()

