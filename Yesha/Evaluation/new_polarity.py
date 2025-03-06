# polarity.csv를 가공하여 넣어야 함
# kosac을 바탕으로 사용할 수 있는 lexicon 만들기
import pandas as pd
import re

polarity = pd.read_csv("C:/Users/iq750/bootcamp_git/대용량 파일 관리/lexicon/polarity.csv")

# 데이터 분석
print(polarity.head(10))
ngrams = polarity['ngram'].tolist() # 가공해야 함
# ';'와 한글 제외 모두 삭제 -> ';'을 공백으로 전환
pattern = r'[^가-힣;]'
new_ngram = []
for ngram in ngrams :
    ngram = re.sub(pattern,'', ngram)
    ngram = ngram.replace(';', ' ')
    new_ngram.append(ngram)
print(new_ngram)
# 얘는 조사가 있는데 그냥 사용해도 괜찮은가? 
# or 우리 모델은 이미 품사를 필터링했는데 어떻게 하지?

# polarity['max.value']
# POS = hawkish
# NEUT = 0
# NEG = dovish
# 해서 new_list 생성

# lexicon_kosac = pd.DataFrame({'hawkish': hawkish_list, 'dovish': dovish_list})