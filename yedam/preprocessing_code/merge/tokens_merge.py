import pandas as pd
import ast
from tqdm import tqdm

csv_files = [
    'tokenized_bond_results.csv', 
    'tokenized_MPB_results.csv', 
    'tokenized_edaily_results.csv', 
    'tokenized_hk_results.csv', 
    'tokenized_infomax_results.csv'
]

merged_df = pd.DataFrame()

# 일별 토큰 수 계산 함수
def count_tokens(tagged_str):
    try:
        tokens = ast.literal_eval(tagged_str)
        return len(tokens)
    except Exception as e:
        return 0

for file in tqdm(csv_files, desc='Processing CSV files'):
    df = pd.read_csv(file)
    df['token_count'] = df['tagged'].apply(count_tokens)
    selected_df = df[['date', 'tagged', 'token_count']]
    merged_df = pd.concat([merged_df, selected_df], ignore_index=True)

grouped_df = merged_df.groupby('date').agg({
    'tagged': lambda x: ', '.join(x.astype(str)),
    'token_count': 'sum'
}).reset_index()

grouped_df.to_csv('merged_tokens.csv')