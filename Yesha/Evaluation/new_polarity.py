# polarity.csv를 가공하여 넣어야 함
# kosac을 바탕으로 사용할 수 있는 lexicon 만들기
import pandas as pd
import re

polarity = pd.read_csv("C:/Users/iq750/bootcamp_git/대용량 파일 관리/lexicon/polarity.csv")
# 품사 구분해서 한 번 다시 해 보자고 (25.03.07)
# print(polarity['ngram'][120:150])
# 데이터 분석
# print(polarity.head(45))
ngrams = polarity['ngram'].tolist() # 가공해야 함

# ';'로 구분하여 분리 .split(";") -> 리스트가 생김
# 각각의 리스트에 대하여, ALLOWED_TAGS에 포함된 품사만 필터링
ALLOWED_TAGS = {'NNG', 'VA', 'VAX', 'MAG', 'negations'}
# 다시 공백을 포함한 문자열로 변환
filtered_ngrams = []
for ngram in ngrams:
    ngram_list = ngram.split(';')
    filtered_ngram = []  # 여기에서 리스트로 선언해야 함

    for token in ngram_list:
        word, tag = token.split('/')
        if tag in ALLOWED_TAGS:
            filtered_ngram.append(word)  # 리스트에 단어 추가

    # 빈 리스트 처리 (필터링된 n-gram이 없으면 None 추가)
    if filtered_ngram:
        filtered_ngrams.append(" ".join(filtered_ngram))  # 공백으로 이어붙인 후 추가
    else:
        filtered_ngrams.append(None)  # 필터링된 n-gram이 없으면 None 추가
print(filtered_ngrams)

# 결과를 polarity 데이터프레임에 추가
polarity['filtered_ngram'] = filtered_ngrams
print(polarity)
"""
# ';'와 한글 제외 모두 삭제 -> ';'을 공백으로 전환 
pattern = r'[^가-힣;]'
new_ngram = []
for ngram in ngrams :
    ngram = re.sub(pattern,'', ngram)
    ngram = ngram.replace(';', ' ')
    new_ngram.append(ngram)
polarity['ngram'] = new_ngram
# 얘는 조사가 있는데 그냥 사용해도 괜찮은가? 
# or 우리 모델은 이미 품사를 필터링했는데 어떻게 하지?

# 우선은 그냥 이용 -> 안 되면 다음으로 넘기기
"""
# polarity['max.value']
# POS = hawkish
# NEUT = 0
# NEG = dovish
# 해서 new_list 생성
hawkish_list = []
dovish_list = []
for idx, value in enumerate(polarity['max.value']):
    if value == 'POS':
        hawkish_list.append(polarity['filtered_ngram'][idx])
    elif value == 'NEG':
        dovish_list.append(polarity['filtered_ngram'][idx])
kosac_hawkish = pd.DataFrame({'filtered_ngram': hawkish_list}).dropna()
kosac_dovish = pd.DataFrame({'filtered_ngram':dovish_list}).dropna()
# 문제가 생기는 것을 막기 위해 해야 할 일
# None값 지운다 (dropna)

# 데이터 프레임 내 중복값 지운다
kosac_hawkish = kosac_hawkish.drop_duplicates(subset=['filtered_ngram'], ignore_index=True)
kosac_dovish = kosac_dovish.drop_duplicates(subset=['filtered_ngram'], ignore_index=True)

# hawkish와 dovish에 모두 있는 단어를 제거
common_ngrams = set(kosac_hawkish['filtered_ngram']).intersection(set(kosac_dovish['filtered_ngram']))

# 두 리스트에서 공통된 n-gram을 제거
kosac_hawkish = kosac_hawkish[~kosac_hawkish['filtered_ngram'].isin(common_ngrams)].reset_index(drop=True)
kosac_dovish = kosac_dovish[~kosac_dovish['filtered_ngram'].isin(common_ngrams)].reset_index(drop=True)
for ngram in kosac_dovish:
    ngram = ngram.replace('*',"")
for ngram in kosac_hawkish:
    ngram = ngram.replace('*','')

print(kosac_hawkish[100:130])
print(kosac_dovish[100:130])

kosac_hawkish.to_csv(r'filter_kosac_hawkish.csv', encoding = 'utf-8-sig')
kosac_dovish.to_csv(r'filter_kosac_dovish.csv', encoding = 'utf-8-sig')
# lexicon_kosac = pd.DataFrame({'hawkish': hawkish_list, 'dovish': dovish_list})"""