# binance_api.py
import requests
import pandas as pd

def get_binance_data():
    url = 'https://api.binance.com/api/v3/ticker/bookTicker'
    response = requests.get(url)
    data = response.json()
    df_data = pd.DataFrame(data)
    df_data = df_data.rename(columns={'bidPrice': 'bidprice', 'bidQty': 'bidqty', 'askPrice': 'askprice', 'askQty': 'askqty'})
    return df_data

def get_binance_symbols():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    data = response.json()
    symbols = data['symbols']
    pairs = {f"{symbol['baseAsset']}{symbol['quoteAsset']}": f"{symbol['baseAsset']}/{symbol['quoteAsset']}" for symbol in symbols}
    return pairs

def get_binance_status():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    data = response.json()
    symbols = data['symbols']
    status = {f"{symbol['baseAsset']}{symbol['quoteAsset']}": symbol['status'] for symbol in symbols}
    return status
