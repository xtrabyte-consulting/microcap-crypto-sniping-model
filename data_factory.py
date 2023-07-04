from sklearn.feature_selection import mutual_info_classif
from skfeature.function.similarity_based import fisher_score
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

df = pd.read_csv('drop_all.csv')
features_no_info_gain = ['buy', 'sell', 'funding_time', 'airdrops', 'amount', 'ape_score', 'sell_tax', 'owner_quant', 
                 'owner_type_INDIVIDUAL', 'owner_type_RENOUNCED', 'source_01121994.eth', 'source_Binance', 'source_Bitget', 'source_Bybit', 
                 'source_FixedFloat', 'source_Gate.io', 'source_Kraken', 'source_INDIVIDUAL', 'source_SideShift', 'source_Kucoin', 'source_Mexc', 'source_cemedeul.eth', 
                 'source_tsunamitreasury.eth', 'spoofed_pct', 'snipers_pct', 'fresh_qty', 'fresh_pct', 'whales_qty', 'safu_score_qty']

info_gain_df = df.drop(features_no_info_gain, axis=1)
info_gain_df.to_csv('drop_all_no_info_gain2.csv')