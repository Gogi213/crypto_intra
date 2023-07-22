# bd.py
from sqlalchemy import create_engine
import pandas as pd
import numpy as np  # Add this line

def connect_to_db(database='crypto_intra', user='root', password='19938713', host='localhost', port='3306'):
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    return engine

def update_table(engine, df, table_name):
    # Clean up the data
    df = df.replace([np.inf, -np.inf], None)

    # Dataframe to sql table
    df.to_sql(table_name, engine, if_exists='replace', index=False)
