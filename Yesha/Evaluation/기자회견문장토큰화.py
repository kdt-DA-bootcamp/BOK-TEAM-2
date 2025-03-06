import re
from kiwipiepy import Kiwi
kiwi = Kiwi()
import glob
import os
import pandas as pd

def remove_policy_date(text):
    # "통화정책방향 (YYYY. M. D.)" 또는 "통화정책방향 (YYYY. M. D)" 패턴 제거
    pattern = r"통화정책방향\s*\(\d{4}\.\s*\d{1,2}\.\s*\d{1,2}\.?\)"
    clean_text = re.sub(pattern, "", text).strip()
    return clean_text
data_folder = r'C:/Users/iq750/bootcamp_git/대용량 파일 관리/한국은행(BOK) 총재 통화정책 결정 관련 기자회견문'
data_files = glob.glob(os.path.join(data_folder, '*.txt'))

dates = []
sentences = []

for d in data_files:
    f = open(d, encoding='utf-8')
    data = f.read()

    # 각 문서에서 날짜 뽑아내기 (형식 일정)
    date_match = re.findall(r'(\d{4}).\s*(\d{1,2}).\s*(\d{1,2})', data)

    if date_match :
        year, month, day = date_match[0]  # 첫 번째 매치만 사용
        if len(month) == 1 :
            month = '0' + month
        if len(day) == 1 :
            day = '0' + day
        date_f = f"{year}-{month}-{day}"
        print(date_f) # 정상적으로 출력되는 것 확인 가능
    else:
        date_f = "날짜 없음"
    dates.append(date_f)

    data = remove_policy_date(data)
    # 텍스트에서는 특수문자 □ 제거
    data = data.replace('□','')
    data = data.replace('\n', '')

    # 나머지는 Kiwi 이용해서 문장 토큰화시킨 담에 df 저장하기 
    sents = [s.text for s in kiwi.split_into_sents(data)]
    sentences.append(sents)

df_sentences = pd.DataFrame({'date':dates, 
                             'sentences':sentences})
# 정렬: 오름차순
df_sentences = df_sentences.sort_values('date', ignore_index=True)
# 중복값 제거 
df_sentences = df_sentences.drop_duplicates(subset=['date'], ignore_index=True)

print(df_sentences.head(10), df_sentences.tail(10))

df_sentences.to_csv(r'C:/Users/iq750/bootcamp_git/BOK-TEAM-2/Yesha/Evaluation/conferences_sentences.csv', encoding='utf-8-sig')