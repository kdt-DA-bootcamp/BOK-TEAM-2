# eKoNPLy and Article review
# https://blog.naver.com/jjys9047/221599162443
from datetime import datetime
import csv
import pandas as pd
import numpy as np
from ekonlpy import Mecab
import re
mecab = Mecab()
start = datetime.now() 
edaily = pd.read_csv(r"C:\Users/iq750/bootcamp_git/대용량 파일 관리/edaily_results.csv")

# column ['title', 'contents', 'date']

# 금융과 관련 없는 부분
# [기자이름, 신년사] (영어 이니셜이나 설명)

# Pre-processing texts
# 1. Tokenization
def cleaned_(text:str):
    pattern1 = r'\[[^\]]*\]' 
    pattern2 = r'\([^)]*\)' 
    text = re.sub(pattern1, '', text)
    text = re.sub(pattern2, '', text) # 대괄호 및 소괄호 내 내용 삭제제
    return text.strip()
# fiftynine = cleaned_(edaily['contents'][100])
# lemfn = mecab.lemmatize(fiftynine)
# print(lemfn)

contents_tagged = []
for idx, content in enumerate(edaily['contents']):
    print(idx)
    content = cleaned_(content)
    fin_lem = mecab.lemmatize(content) # 품사 태깅, lemmatize
    temp = []
    for tag in fin_lem :
        if tag[1] in ['NNP' , 'NNG' , 'VV' , 'VA' ] : # 명사, 동사, 형용사만 남김
            temp.append(tag)   
        else :
            continue
    contents_tagged.append(temp)
print(contents_tagged[:3])
end = datetime.now()
print(f"소요 시간: {end - start}")
edaily['tagged'] = contents_tagged

edaily.to_csv(r"C:\Users/iq750/bootcamp_git/대용량 파일 관리/edaily_results.csv", encoding = 'utf-8', index = False)
# 2. Norlmalization
#   - removing stop words, stemming and lemmatization
# stopwords: NNP, NNG, VV, VA (실질적 의미가 있는 명사/동사/형용사만)
# lemmatization으로 동사 형용사 통일시키기 : 

# 3. Morphological analysis of the Korean Language -> eKoNLKPy
#   - spacing, terminology and foreign words