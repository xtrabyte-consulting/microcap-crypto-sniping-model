from sklearn.feature_selection import mutual_info_classif
from skfeature.function.similarity_based import fisher_score
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

std_out = sys.stdout
sys.stdout = open('FeatureSelectionOnlyInfoGain.txt', 'w')

df = pd.read_csv('drop_all_no_info_gain.csv')
X = df.drop(['printed'], axis=1) 
y = df['printed']

print('Information Gains:')
depedencies = mutual_info_classif(X, y)

for i, feature in enumerate(X.columns):
    print(f"{feature}: {depedencies[i]}")

# Filter out features with 0 information gain
selected_features = X.columns[depedencies > 0]
selected_info = depedencies[depedencies > 0]

plt.bar(selected_features, selected_info)
plt.xlabel('Features')
plt.ylabel('Information Gain')
plt.title('Information Gain Scores')
#plt.show()

lasso = Lasso(alpha=0.1)  # Specify the regularization strength (alpha)
lasso.fit(X, y)

# Get the coefficients and their corresponding feature names
coefficients = lasso.coef_
feature_names = X.columns

print('LASSO: \n')
# Print the importance of each feature
for feature, coef in zip(feature_names, coefficients):
    print(f"Feature: {feature}, Coefficient: {coef:.2f}")

correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True)
print('Correlation Matrix: \n')
print(correlation_matrix)
#plt.show()

