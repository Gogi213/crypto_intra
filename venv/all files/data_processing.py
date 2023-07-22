# data_processing.py
import pandas as pd

def custom_format(x):
    if isinstance(x, float):
        str_x = format(x, '.15f')  # Convert number to fixed-point notation
        if '.' in str_x:
            decimal_part = str_x.split('.')[1]
            num_decimals = len(decimal_part.rstrip('0'))  # Remove trailing zeros
            return format(x, f'.{num_decimals}f')
    return x

def process_data(df):
    # Get the list of column names
    cols = list(df.columns)
    # Move 'status' column right after 'symbol'
    cols.insert(1, cols.pop(cols.index('status')))
    # Reindex the DataFrame
    df = df.reindex(columns=cols)
    # Filter out rows with 'BREAK' status or NaN status
    df = df[(df['status'] != 'BREAK') & (df['status'].notna())]
    df = df.drop(columns=['status'])
    df[['base', 'quote']] = df['symbol'].str.split('/', expand=True)
    formatted_df = df.applymap(custom_format)
    return formatted_df