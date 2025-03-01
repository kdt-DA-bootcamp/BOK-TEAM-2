import pandas as pd

df = pd.read_csv('tokenized_economy_results.csv')

df_selected = df[['date', 'tagged']]

df_selected.to_csv('economy_docs.csv', index=False)