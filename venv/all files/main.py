# main.py
import sys
sys.path.append('C:/Users/Redmi/PycharmProjects/crypto_intra/venv/all files/pulsar')
from binance_pulsar import ws
from calculate_profit import calculate_triple_exchanges

# Start the Binance subscription and Pulsar publication process
# ws.run_forever()

output_path = r'C:\Users\Redmi\PycharmProjects\crypto_intra\venv\all files\debug_df_data.csv'

# triple_exchanges = calculate_triple_exchanges(output_path)

print("Triple exchanges saved to CSV:", output_path)