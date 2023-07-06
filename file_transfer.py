import json
import csv
import pandas as pd

# Path to the JSON file
json_file_path = 'data.json'

# Raw CSV path
raw_csv_file = 'raw_data.csv'

# Final CSV Path
clean_csv_file = 'tidy_data.csv'

key_mapping = {
    '👯‍♂️ Pair Age': 'pair_age',
    '🎯 Initial Mcap': 'initial_market_cap',
    '🏦 Funding': 'funding_time',
    '🚫 Owner': 'owner',
    '└─ Source': 'source',
    'status': 'status',
    'ℹ CA (Verified ✅)': 'verified',
    'endDate': 'end_date',
    'name': 'name',
    '👥 Hds': 'holders',
    '🔖 Tax': 'tax',
    'ticker': 'ticker',
    '🦍 ApeScore': 'ape_score',
    '└─ Spoofed': 'spoofed',
    'liquidity': 'liquidity',
    '🔒 Lp': 'lock',
    'mcap': 'market_cap',
    '✅ Prev': 'previous',
    '⌚ Contract Age': 'contract_age',
    '📉 Sell': 'sell',
    '└─ Airdrops': 'airdrops',
    'result': 'result',
    '└─ ATH': 'ath',
    '└─ Whales': 'whales',
    '🚩 Flags': 'red_flags',
    'date': 'time_of_day',
    '└─ Worth': 'worth',
    '└─ Snipers': 'snipers',
    '📈 Buy': 'buy',
    '└─ Fresh': 'fresh',
    '⬆️ Max Tx': 'max_transmit',
    '🍯 HP': 'honeypot',
    '🛡 SafuScore': 'safu_score',
    '🐋 Wallet': 'wallet',
    'sticker': 'sticker',
    '🤑 Amount': 'amount'
}

# Load JSON data
with open(json_file_path) as json_file:
    data = json.load(json_file)

# Create CSV
with open(raw_csv_file, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=key_mapping.values())
    writer.writeheader()

    for entry in data:
        mapped_entry = {key_mapping.get(key, key): value for key, value in entry.items()}
        writer.writerow(mapped_entry)

# Create the DataFrame
df = pd.read_csv(raw_csv_file)

# Drop some garbage before preprocessing
fields_to_drop = ['verified', 'end_date', 'name', 'ticker', 'ath', 'sticker'] 
df = df.drop(fields_to_drop, axis=1)




# Get the target variable column
target_variable = df['result']

# Drop the target variable column from the DataFrame
df = df.drop('result', axis=1)

# Add the target variable as the last column
df['result'] = target_variable