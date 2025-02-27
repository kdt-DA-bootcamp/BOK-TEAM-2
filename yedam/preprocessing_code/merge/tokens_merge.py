import pandas as pd
from tqdm import tqdm

csv_files = [
    'tokenized_bond_results.csv', 
    'tokenized_MPB_results.csv', 
    'tokenized_edaily_results.csv', 
    'tokenized_hk_results.csv', 
    'tokenized_infomax_results.csv'
]

merged_df = pd.DataFrame()

for file in tqdm(csv_files, desc='Processing CSV files'):
    df = pd.read_csv(file)
    selected_df = df[['date', 'tagged']]
    merged_df = pd.concat([merged_df, selected_df], ignore_index=True)

grouped_df = merged_df.groupby('date').agg({'tagged':lambda x: ', '.join(x.astype(str))})

grouped_df.to_csv('merged_tokens.csv')