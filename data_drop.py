import pandas as pd

# Path to the input CSV file
input_csv_file = 'data.csv'

# Path to the output CSV file
output_csv_file = 'dropped_test.csv'

# List of field names to be dropped
fields_to_drop = ['ℹ CA (Verified ✅)', 'endDate', 'name', 'ticker', '✅ Prev', '└─ ATH', '🚩 Flags', 'date', '🍯 HP', 'sticker', '🔒 Lp']

# Read the input CSV file
df = pd.read_csv(input_csv_file)

# Drop the desired fields
df = df.drop(fields_to_drop, axis=1)

# Get the target variable column
target_variable = df['result']

# Drop the target variable column from the DataFrame
df = df.drop('result', axis=1)

# Add the target variable as the last column
df['result'] = target_variable

# Write the modified data to the output CSV file
df.to_csv(output_csv_file, index=False)
