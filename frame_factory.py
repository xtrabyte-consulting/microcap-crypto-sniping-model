import pandas as pd
import sys

processed_data_path = 'tidy_data.csv'
data_variations_path = 'DataVariations/'
data_descriptions_file = 'DataSetStats.txt'

df = pd.read_csv(processed_data_path)

features_missing = ['init_market_cap', 'buy', 'max_transmit', 'honeypot']

holder_types = ['holders_qty', 'holders_amt', 'spoofed_qty', 'spoofed_pct', 'snipers_qty', 'snipers_pct', 'fresh_qty', 'fresh_pct', 'whales_qty', 'whales_pct']

std_out = sys.stdout
sys.stdout = open(data_variations_path + data_descriptions_file, 'w')

# Drop All
drop_all = df.dropna()
drop_all.to_csv(data_variations_path + 'drop_all_missing.csv')
print("Drop All Description: ")
print(drop_all.describe())

# Fill holders with median
for type in holder_types:
    df[type] = df[type].fillna(df[type].median())
    
# Zeroed
zeroed = df.fillna(0)
zeroed.to_csv(data_variations_path + 'zeroed_all_missing.csv')
print("Zeroed All Description: ")
print(zeroed.describe())

# Means
mean_frame = df
for feature in features_missing:
    mean_frame[feature] = mean_frame[feature].fillna(mean_frame[feature].mean())
mean_frame.to_csv(data_variations_path + 'mean_all_missing.csv')
print("Mean All Description: ")
print(mean_frame.describe())
    
# Medians
median_frame = df
for feature in features_missing:
    mean_frame[feature] = mean_frame[feature].fillna(mean_frame[feature].median())
median_frame.to_csv(data_variations_path + 'median_all_missing.csv')
print("Median All Description: ")
print(median_frame.describe())

# Initial Market Cap Variations

# Initial Market Cap Variations

# Max Transmit Variations

# Honey-Pot Variations

# Holders Variations

# Status Variations

sys.stdout = std_out