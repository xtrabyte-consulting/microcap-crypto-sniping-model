import pandas as pd
import re


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
output_csv_file = 'cleaned.csv'

df = pd.read_csv(input_csv_file)

df['buy'] = df['buy'].str.extract(r'\((\d+)\)')
df['sell'] = df['sell'].str.extract(r'\((\d+)\)')
df[['buy_tax', 'sell_tax']] = df['tax'].str.split('/', expand=True)
df['scams'] = df['scams'].apply(parse_scammed)
df[['owner_type', 'owner_quant']] = df['owner'].str.split(r'\s+', n = 1, expand=True)
df['owner_quant'] = df['owner_quant'].str.extract(r'\((\d+)\)')
df['owner_type'] = df['owner_type'].apply(parse_individuals)
df['worth'] = pd.to_numeric(df['worth'].str.replace(r'[\$,]', '', regex=True))
df['contract_age'] = df['contract_age'].apply(parse_time_entry)
df['pair_age'] = df['pair_age'].apply(parse_time_entry)
df['funding_time'] = df['funding_time'].apply(parse_time_entry)
df['source'] = df['source'].apply(parse_individuals)
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
df['fresh_pct'].f

drop_fields = ['tax', 'owner', 'holds', 'spoofed', 'snipers', 'fresh', 'whales', 'result', 'wallet_id']

df.drop(drop_fields, axis=0)

# Write the modified data to the output CSV file
df.to_csv(output_csv_file, index=False)