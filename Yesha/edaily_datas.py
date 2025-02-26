import pandas as pd
import os
import csv
folders = os.listdir(r'C:\Users\iq750\bootcamp_git\BOK_project\Yesha\edaily2014')
folders.remove('edaily2014')
folders.remove('scrapy.cfg')
print(folders)
df_1418 = pd.DataFrame()
for file in folders:
    df = pd.read_csv( 'C:/Users/iq750/bootcamp_git/BOK_project/Yesha/edaily2014/'+ file, encoding = 'utf-8')
    df_1418 = pd.concat([df_1418, df], ignore_index=True)

df_1418 = df_1418.sort_values('date')
print(df_1418)
df_1418.to_csv('edaily_20142018.csv', encoding= 'utf-8')
