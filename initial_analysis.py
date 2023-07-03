import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import Lasso

df = pd.read_csv('cleaned_all_num.csv')

buy_mean = df['buy'].mean()
df['buy'] = df['buy'].fillna(buy_mean)

hq_mean = df['holds_qty'].mean()
df['holds_qty'] = df['holds_qty'].fillna(hq_mean)

ha_mean = df['holds_amt'].median()
df['holds_amt'] = df['holds_amt'].fillna(ha_mean)

sq_mean = df['spoofed_qty'].mean()
df['spoofed_qty'] = df['spoofed_qty'].fillna(sq_mean)

sp_mean = df['spoofed_pct'].mean()
df['spoofed_pct'] = df['spoofed_pct'].fillna(sp_mean)

sqn_mean = df['snipers_qty'].median()
df['snipers_qty'] = df['snipers_qty'].fillna(sqn_mean)

snp_mean = df['snipers_pct'].mean()
df['snipers_pct'] = df['snipers_pct'].fillna(snp_mean)

fresh_mean = df['fresh_qty'].median()
df['fresh_qty'] = df['fresh_qty'].fillna(fresh_mean)

fresh_pct_mean = df['fresh_pct'].mean()
df['fresh_pct'] = df['fresh_pct'].fillna(fresh_pct_mean)

whq_mean = df['whales_qty'].mean()
df['whales_qty'] = df['whales_qty'].fillna(whq_mean)

whp_mean = df['whales_pct'].mean()
df['whales_pct'] = df['whales_pct'].fillna(whp_mean)

# Assuming you have a DataFrame called 'df' with numerical features and a target variable 'target'
X = df.drop('result', axis=1)  # Extract the feature matrix
y = df['result']  # Extract the target variable

# Perform Lasso regression
lasso = Lasso(alpha=0.1)  # Specify the regularization strength (alpha)
lasso.fit(X, y)

# Get the coefficients and their corresponding feature names
coefficients = lasso.coef_
feature_names = X.columns

# Print the importance of each feature
for feature, coef in zip(feature_names, coefficients):
    print(f"Feature: {feature}, Coefficient: {coef:.2f}")

# You can also access the intercept using 'lasso.intercept_'


'''
mean_values = df.mean()

median_values = df.median()

std_values = df.std()

for column_name in df.columns:
    plt.scatter(df[column_name], df['result'])
    plt.xlabel(column_name)
    plt.ylabel('Result')
    plt.title('Scatter Plot')
    plt.show()

for column in df.columns:
    plt.hist(df[column], bins=10)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of ' + column)
    plt.show()

for column in df.columns:
    plt.boxplot(df[column])
    plt.xlabel('Variable')
    plt.ylabel('Value')
    plt.title('Box Plot of ' + column)
    plt.show()

for column_name in df.columns:
    sns.kdeplot(df[column_name])
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.title('Kernel Density Plot of ' + column)
    plt.show()



result_df = pd.DataFrame({'Mean': mean_values, 'Median': median_values, 'Standard Deviation': std_values})

result_df.to_csv('basic_analysis.csv', index=True)
'''