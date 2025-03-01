import pandas as pd

df = pd.read_csv("tokenized_hk_results.csv")

df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime("%Y-%m-%d")

df.to_csv("hk_date_update.csv", index=False)