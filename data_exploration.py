import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.decomposition
import sklearn.preprocessing
import sklearn.metrics
import sklearn.svm
import sklearn.tree
import sklearn.neighbors
import numpy as np


df = pd.read_csv('drop_all_no_info_gain2.csv')

#Histograms
#sns.pairplot(data=df, hue='printed', kind='kde')
#Pair Plot

#plt.savefig('MicroCapPairplotNoGainDropped.pdf')

#PCA Projection
X = df.drop('printed', axis=1)
y = df['printed']

# Initialize a PCA object and specify that we want the transformed data to be 2D
pca = sklearn.decomposition.PCA(n_components=2)

# Perform the PCA transformation
X_2D = pca.fit_transform(X)

# Plot a scatterplot of the result
sns.scatterplot(x=X_2D[:,0], y=X_2D[:,1], hue=y)

plt.savefig('MicroCapPCADroppedNoInfoGain.pdf')

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.20)

# standardize data
scaler = sklearn.preprocessing.StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# create classifiers
dtree = sklearn.tree.DecisionTreeClassifier()
svc = sklearn.svm.SVC()
knn = sklearn.neighbors.KNeighborsClassifier(n_neighbors=5)

# train classifiers
dtree.fit(X_train, y_train)
svc.fit(X_train, y_train)
knn.fit(X_train, y_train)

fig, ax = plt.subplots() 
sklearn.metrics.plot_roc_curve(dtree, X_test, y_test, ax=ax)
sklearn.metrics.plot_roc_curve(svc, X_test, y_test, ax=ax)
sklearn.metrics.plot_roc_curve(knn, X_test, y_test, ax=ax)

plt.savefig('ROCCurvesDroppedNoInfoGain.pdf')

sklearn.metrics.plot_confusion_matrix(svc, X_test, y_test)
plt.savefig('ConfusionMatrixSVC.pdf')

sklearn.metrics.plot_confusion_matrix(dtree, X_test, y_test)
plt.savefig('ConfusionMatrixDTree.pdf')

sklearn.metrics.plot_confusion_matrix(knn, X_test, y_test)
plt.savefig('ConfusionMatrixKNN.pdf')