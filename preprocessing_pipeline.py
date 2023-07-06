import json
import csv
import pandas as pd
import sys
from sklearn.preprocessing import OneHotEncoder


def minute_coversion(value: int, unit):
    if unit == 'days':
        value *= 24 * 60
    elif unit == 'hours':
        value *= 60
    return value

def parse_time_entry(entry: str):
    time_vals = entry.split(' ')
    unit = time_vals.pop()
    if unit == 'ago':
        unit = time_vals.pop()
    value = time_vals.pop()
    minutes = minute_coversion(int(value), unit)
    if len(time_vals) == 0:
        return minutes
    unit = time_vals.pop()
    value = time_vals.pop()
    minutes2 = minute_coversion(int(value), unit)
    return minutes + minutes2

def parse_individuals(entry: str):
    if entry[:2] == '0x':
        entry = 'INDIVIDUAL' 
    return entry

def parse_scammed(entry: str) -> float:
    if entry == '0 out of 0 Unique':
        return 0.0
    scammed, total = entry.split(' out of ')
    if scammed[-1] == 'k':
        scammed = float(scammed[:-1]) * 1000
    if total[-1] == 'k':
        total = float(total[:-1]) * 1000
    return int(scammed) / int(total)

def parse_status(entry: str) -> str:
    if "100K" in entry:
        return '100K'
    elif '50K' in entry:
        return '50K'
    elif '10K' in entry:
        return '10K'
    else:
        return 'Above'

# Path to the JSON file
json_file_path = 'data.json'

# Raw CSV path
raw_csv_file = 'raw_data.csv'

# Final CSV Path
clean_csv_file = 'tidy_data.csv'

key_mapping = {
    '👯‍♂️ Pair Age': 'pair_age',
    '🎯 Initial Mcap': 'init_market_cap',
    '└─ Scams': 'scams',
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
# TODO: Lock days might be worth processing
fields_to_drop = ['verified', 'end_date', 'name', 'lock', 'previous', 'ticker', 'ath', 'sticker'] 
df = df.drop(fields_to_drop, axis=1)

# Make some data
df['buy'] = df['buy'].str.extract(r'\((\d+)\)').astype(float)
df['sell'] = df['sell'].str.extract(r'\((\d+)\)').astype(float)
df[['buy_tax', 'sell_tax']] = df['tax'].str.split('/', expand=True)
df['scams'] = df['scams'].apply(parse_scammed)
df[['owner_type', 'owner_quant']] = df['owner'].str.split(r'\s+', n = 1, expand=True)
df['owner_quant'] = df['owner_quant'].str.extract(r'\((\d+)\)')
df['owner_type'] = df['owner_type'].apply(parse_individuals)
one_hot = OneHotEncoder(sparse=False)
encoded_sources = one_hot.fit_transform(df[['owner_type']])
encoded_df = pd.DataFrame(encoded_sources, columns=one_hot.get_feature_names_out(['owner_type']))
df = pd.concat([df, encoded_df], axis=1)
df['worth'] = pd.to_numeric(df['worth'].str.replace(r'[\$,]', '', regex=True))
df['contract_age'] = df['contract_age'].apply(parse_time_entry)
df['pair_age'] = df['pair_age'].apply(parse_time_entry)
df['funding_time'] = df['funding_time'].apply(parse_time_entry)
df['source'] = df['source'].apply(parse_individuals)
encoded_sources = one_hot.fit_transform(df[['source']])
encoded_df = pd.DataFrame(encoded_sources, columns=one_hot.get_feature_names_out(['source']))
df = pd.concat([df, encoded_df], axis=1)
df[['holders_qty', 'holders_amt', 'eth_unit']] = df['holders'].str.split(' ', expand=True)
df['holders_qty'] = pd.to_numeric(df['holders_qty'])
df['holders_amt'] = df['holders_amt'].str.replace('(', '', regex=False).astype(float)
df[['spoofed_qty', 'spoofed_pct']] = df['spoofed'].str.split(' own ', expand=True)
df['spoofed_qty'] = pd.to_numeric(df['spoofed_qty'])
df['spoofed_pct'] = df['spoofed_pct'].str.replace('%', '', regex=False).astype(float)
df[['snipers_qty', 'snipers_pct']] = df['snipers'].str.split(' own ', expand=True)
df['snipers_qty'] = pd.to_numeric(df['snipers_qty'])
df['snipers_pct'] = df['snipers_pct'].str.replace('%', '', regex=False).astype(float)
df[['fresh_qty', 'fresh_pct']] = df['fresh'].str.split(' own ', expand=True)
df['fresh_qty'] = pd.to_numeric(df['fresh_qty'])
df['fresh_pct'] = df['fresh_pct'].str.replace('%', '', regex=False).astype(float)
df[['whales_qty', 'whales_pct']] = df['whales'].str.split(' own ', expand=True)
df['whales_qty'] = pd.to_numeric(df['whales_qty'])
df['whales_pct'] = df['whales_pct'].str.replace('%', '', regex=False).astype(float)
df['airdrops'] = pd.to_numeric(df['airdrops'].fillna(0))
df['amount'] = pd.to_numeric(df['amount'].str.replace(r'[\$,]', '', regex=True))
df[['wallet_id', 'wallet']] = df['wallet'].str.split(' ', expand=True)
df['wallet'] = pd.to_numeric(df['wallet'].str.replace(r'[\(\$,\)]', '', regex=True))
df['ape_score'] = df['ape_score'].str.extract(r'\b(-?\d+)%')
df[['safu_score', 'safu_score_qty']] = df['safu_score'].str.split('% out of ', expand=True)
df['safu_score'] = pd.to_numeric(df['safu_score'])
df['safu_score_qty'] = pd.to_numeric(df['safu_score_qty'])
df[['init_market_cap', 'init_mcap_qty']] = df['init_market_cap'].str.split(' \\| ', expand=True)
df['init_market_cap'] = pd.to_numeric(df['init_market_cap'].str.replace(r'[\$,]', '', regex=True))
df['status'] = df['status'].fillna('Above')
df['status'] = df['status'].apply(parse_status)
encoded_sources = one_hot.fit_transform(df[['status']])
encoded_df = pd.DataFrame(encoded_sources, columns=one_hot.get_feature_names_out(['status']))
df = pd.concat([df, encoded_df], axis=1)
df['time_of_day'] = pd.to_timedelta(df['time_of_day']).dt.total_seconds()
df[['transmit_pct', 'max_transmit']] = df['max_transmit'].str.split(' \\| ', expand=True)
df['max_transmit'] = df['max_transmit'].str.replace(' eth', '', regex=False).astype(float)
df['honeypot'] = df['honeypot'].str.extract(r'\b(\d+)/')
df['printed'] = df['result'] > 0

# Drop Red Flags
df = df[pd.isnull(df['red_flags'])]

# Drop Processed
drop_fields = ['transmit_pct', 'status', 'init_mcap_qty', 'red_flags', 'tax', 'owner', 'owner_type', 'source', 'holders', 'spoofed', 'snipers', 'fresh', 'whales', 'result', 'eth_unit', 'wallet_id']
df = df.drop(drop_fields, axis=1)

df.to_csv(clean_csv_file)