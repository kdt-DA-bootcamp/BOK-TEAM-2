# eKoNPLy and Article review
# https://blog.naver.com/jjys9047/221599162443
import pandas as pd
import numpy as np
import re
edaily = pd.read_csv(r"C:/Users/iq750/bootcamp_git/대용량 파일 관리/edaily_results.csv")
edaily= edaily.drop(['Unnamed: 0'], axis = 1)
# word 뽑아내기
edaily_tokens = pd.Series(edaily['tagged'])
words_list = []
total_words = []
cnt = 1
for string in edaily_tokens:
    # 정규식 패턴: 튜플 내부의 첫 번째 요소(단어)만 추출
    words = re.findall(r"\('(.+?)',\s*'.+?'\)", string)
    print(cnt)
    words_list.append(words)
    total_words += words
    cnt += 1
print(len(total_words))
df_total = pd.DataFrame(total_words, index = ['Word'])
print(df_total.head(10))
print(df_total.value_counts())