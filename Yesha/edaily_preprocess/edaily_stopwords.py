import pandas as pd
import numpy as np
import re
import ast
edaily = pd.read_csv(r"C:/Users/iq750/bootcamp_git/대용량 파일 관리/edaily_results.csv")
edaily= edaily.drop(['Unnamed: 0'], axis = 1)

tagged = []
for text in edaily['tagged'] :
    parsed_data = ast.literal_eval(text)
    tagged.append(parsed_data)
print(tagged[1])

# stopword
stopword_kor = r"C:/Users/iq750/bootcamp_git/BOK-TEAM-2/Yesha/stopwords-ko.txt"
with open(stopword_kor, 'r',encoding='UTF-8') as file:
    stopword_ko = []
    for l in file:
        stopword_ko.append(l.strip())
stopword_ko +=  ["있", "되", "한", "것", "원", "등", "년", "보", "억", "인", "수" , "만", "적", "해", "중", "조", "다", "전", "대", "이날", "그", "낮", "내", "및", "경우", "개월", "개", "이번", "명", '점', '시', '데', '달', '화', '두', '미', '각각', '열', '연', '오', '엔', '성', '분', '총', '당', '후', '반면', '형', '계', '위', '약', '美']

for tags in tagged :
    for tag in tags:
        if tag[0] in stopword_ko :
            tags.remove(tag)
            print("delete", tag[0])
print(tagged[1])