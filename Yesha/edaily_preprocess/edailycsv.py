import pandas as pd
import numpy as np

e18 = pd.read_csv(r"C:\Users\iq750\bootcamp_git\대용량 파일 관리\2014to2018_results.csv")
e24 = pd.read_csv(r'C:\Users\iq750\bootcamp_git\대용량 파일 관리\2019to2024_results.csv')

e18 = e18.drop(['Unnamed: 0'], axis = 1)
df_edaily = pd.concat([e18, e24], ignore_index=True)
df_edaily = df_edaily.sort_values('date', ascending = True, ignore_index= True)

df_edaily = df_edaily.iloc[:104002]

print(df_edaily.tail(50))
print(df_edaily.columns)

df_edaily.to_csv(r'C:\Users\iq750\bootcamp_git\대용량 파일 관리\edaily_results.csv')
