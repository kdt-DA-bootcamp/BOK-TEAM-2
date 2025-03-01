import pandas as pd

df = pd.read_csv('edaily_tokens.csv')

df_selected = df[['date', 'tagged']]

df_selected.to_csv('edaily_docs.csv', index=False)