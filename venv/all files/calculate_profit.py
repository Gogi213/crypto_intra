# calculate_profi.py
import binance_api
import data_processing
import itertools
import pandas as pd
from bd import connect_to_db, update_table

def calculate_triple_exchanges(output_path):
    data = binance_api.get_binance_data()
    data = data.drop(columns=['bidprice', 'askprice', 'bidqty', 'askqty'])
    symbols = binance_api.get_binance_symbols()
    status = binance_api.get_binance_status()
    data['status'] = data['symbol'].map(status)
    data = data[data['status'] != 'BREAK']
    data['symbol'] = data['symbol'].map(symbols)
    data = data_processing.process_data(data)

    new_data_rows = []
    for index, row in data.iterrows():
        base = row['base']
        quote = row['quote']
        symbol = row['symbol']

        # Scenario 1: base
        # Stage 1
        swap = base

        # Stage 2
        symbol2_data = data[(data['base'] == base) & (data['quote'] != quote)]
        if len(symbol2_data) > 0:
            for _, row2 in symbol2_data.iterrows():
                symbol2 = row2['symbol']
                base2 = row2['base']
                quote2 = row2['quote']
                if base == base2:
                    swap2 = quote2
                else:
                    swap2 = base2

                # Stage 3
                symbol3_data = data[(data['base'] == base2) & (data['quote'] != quote2)]
                if len(symbol3_data) > 0:
                    for _, row3 in symbol3_data.iterrows():
                        symbol3 = row3['symbol']
                        base3 = row3['base']
                        quote3 = row3['quote']
                        if base2 == base3:
                            swap3 = quote3
                        else:
                            swap3 = base3

                        if swap3 == base or swap3 == quote:
                            new_data_rows.append([symbol, base, quote, swap, symbol2, base2, quote2, swap2, symbol3, base3, quote3, swap3])

    new_data = pd.DataFrame(new_data_rows, columns=['symbol', 'base', 'quote', 'swap', 'symbol2', 'base2', 'quote2', 'swap2', 'symbol3', 'base3', 'quote3', 'swap3'])

    # Reset the index and add an 'id' column
    new_data.reset_index(inplace=True)
    new_data.rename(columns={'index': 'id'}, inplace=True)

    new_data.to_csv(output_path, index=False)
    print(new_data.head())

    engine = connect_to_db()
    update_table(engine, new_data, 'binance_bundles')
    return new_data
