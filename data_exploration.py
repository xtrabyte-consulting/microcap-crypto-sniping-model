import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import sklearn.decomposition
import numpy as np


df = pd.read_csv('drop_all_no_info_gain2.csv')

#Histograms
sns.pairplot(data=df, hue='printed', kind='kde')
#Pair Plot

plt.savefig('MicroCapPairplotNoGainDropped.pdf')

#PCA Projection
