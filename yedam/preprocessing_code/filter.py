# 표만 들어있는 항목 제외
import pandas as pd

df = pd.read_csv('debenture_results.csv')

df_filtered = df[~df['title'].str.contains('Daily', na=False)]
df_filtered.to_csv('filtered_bond.csv', index=False)