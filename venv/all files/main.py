# main.py
from calculate_profit import calculate_triple_exchanges

output_path = r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\debug_df_data.csv'

triple_exchanges = calculate_triple_exchanges(output_path)

print("Triple exchanges saved to CSV:", output_path)