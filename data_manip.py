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

def parse_scammed(entry) -> float:
    if entry == '0 out of 0 Unique':
        return 0.0
    scammed, total = entry.split(' out of ')
    if scammed[-1] == 'k':
        scammed = float(scammed[:-1]) * 1000
    if total[-1] == 'k':
        total = float(total[:-1]) * 1000
    return int(scammed) / int(total)
    
input_csv_file = 'dropped.csv'

# Path to the output CSV file
output_csv_file = 'clean.csv'

df = pd.read_csv(input_csv_file)

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
one_hot = OneHotEncoder(sparse=False)
encoded_sources = one_hot.fit_transform(df[['source']])
encoded_df = pd.DataFrame(encoded_sources, columns=one_hot.get_feature_names_out(['source']))
df = pd.concat([df, encoded_df], axis=1)
df[['holds_qty', 'holds_amt', 'eth_unit']] = df['holds'].str.split(' ', expand=True)
df['holds_qty'] = pd.to_numeric(df['holds_qty'])
df['holds_amt'] = df['holds_amt'].str.replace('(', '', regex=False).astype(float)
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
df['printed'] = df['result'] > 0

drop_fields = ['tax', 'owner', 'owner_type', 'source', 'holds', 'spoofed', 'snipers', 'fresh', 'whales', 'result', 'eth_unit', 'wallet_id']

fill_mean = df.drop(drop_fields, axis=1)
fill_median = df.drop(drop_fields, axis=1)
drop_rows = df.drop(drop_fields, axis=1)

std_out = sys.stdout
sys.stdout = open('statistics.txt', 'w')
#print("Raw Description: ")
#print(fill_mean.describe())

fill_mean['buy'] = fill_mean['buy'].fillna(fill_mean['buy'].mean())
fill_mean['holds_qty'] = fill_mean['holds_qty'].fillna(fill_mean['holds_qty'].mean())
fill_mean['holds_amt'] = fill_mean['holds_amt'].fillna(fill_mean['holds_amt'].mean())
fill_mean['spoofed_qty'] = fill_mean['spoofed_qty'].fillna(fill_mean['spoofed_qty'].mean())
fill_mean['spoofed_pct'] = fill_mean['spoofed_pct'].fillna(fill_mean['spoofed_pct'].mean())
fill_mean['snipers_qty'] = fill_mean['snipers_qty'].fillna(fill_mean['snipers_qty'].mean())
fill_mean['snipers_pct'] = fill_mean['snipers_pct'].fillna(fill_mean['snipers_pct'].mean())
fill_mean['fresh_qty'] = fill_mean['fresh_qty'].fillna(fill_mean['fresh_qty'].mean())
fill_mean['fresh_pct'] = fill_mean['fresh_pct'].fillna(fill_mean['fresh_pct'].mean())
fill_mean['whales_qty'] = fill_mean['whales_qty'].fillna(fill_mean['whales_qty'].mean())
fill_mean['whales_pct'] = fill_mean['whales_pct'].fillna(fill_mean['whales_pct'].mean())
#print("Filled Mean: \n")
#print(fill_mean.describe())

fill_median['buy'] = fill_median['buy'].fillna(fill_median['buy'].mean())
fill_median['holds_qty'] = fill_median['holds_qty'].fillna(fill_median['holds_qty'].median())
fill_median['holds_amt'] = fill_median['holds_amt'].fillna(fill_median['holds_amt'].median())
fill_median['spoofed_qty'] = fill_median['spoofed_qty'].fillna(fill_median['spoofed_qty'].median())
fill_median['spoofed_pct'] = fill_median['spoofed_pct'].fillna(fill_median['spoofed_pct'].median())
fill_median['snipers_qty'] = fill_median['snipers_qty'].fillna(fill_median['snipers_qty'].median())
fill_median['snipers_pct'] = fill_median['snipers_pct'].fillna(fill_median['snipers_pct'].median())
fill_median['fresh_qty'] = fill_median['fresh_qty'].fillna(fill_median['fresh_qty'].median())
fill_median['fresh_pct'] = fill_median['fresh_pct'].fillna(fill_median['fresh_pct'].median())
fill_median['whales_qty'] = fill_median['whales_qty'].fillna(fill_median['whales_qty'].median())
fill_median['whales_pct'] = fill_median['whales_pct'].fillna(fill_median['whales_pct'].median())
#print("Filled Median: \n")
#print(fill_median.describe())

drop_buy = drop_rows.dropna(subset=['buy']) #fill_median['buy'].fillna(fill_median['buy'].mean())
#print("Dropped Buys: \n")
#print(drop_buy.describe())

drop_hold_types = drop_rows.dropna(subset=['holds_qty'])
#print("Dropped Hold Types: \n")
#print(drop_hold_types.describe())

drop_rows.dropna(subset=['buy', 'holds_qty'], inplace=True)
#print("Dropped All: \n")
#print(drop_rows.describe())


# Write the modified data to the output CSV file
fill_mean.to_csv('fill_mean.csv', index=False)
fill_median.to_csv('fill_median.csv', index=False)
drop_buy.to_csv('drop_buy.csv', index=False)
drop_hold_types.to_csv('drop_holders.csv', index=False)
drop_rows.to_csv('drop_all.csv', index=False)