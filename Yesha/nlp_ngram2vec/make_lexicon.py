import pandas as pd
import numpy as np

df = pd.read_csv("nlp_ngram2vec/ngram_polarity_separated.csv")
"""
h_list = []
d_list = []
for idx in range(len(df)) :
    if df['dovish'][idx] > df['hawkish'][idx]:
        h_list.append('O')
        d_list.append(np.nan)
    else:
        d_list.append('O')
        h_list.append(np.nan)

df['매파'] = h_list
df[df['매파']=='O'] # 7857개
df['비둘기파'] = d_list
df[df['비둘기파']=='O'] # 8014개
"""
# 해당 데이터를 바탕으로 lexicon 만들기
### ---------------------------------------------------------------------- ###
# 데이터 로드
df = pd.read_csv("nlp_ngram2vec/(dict_ver4)ngram_polarity_separated.csv")

# 매파/비둘기파 lexicon을 저장할 리스트
hawkish_list = []
dovish_list = []

# hawkish / dovish 구분하여 리스트에 저장
for idx in range(len(df)):
    ngram = df.loc[idx, 'ngram']
    dovish_score = df.loc[idx, 'dovish']
    hawkish_score = df.loc[idx, 'hawkish']

    if dovish_score > hawkish_score:
        dovish_list.append((ngram, dovish_score))
    elif dovish_score < hawkish_score:
        hawkish_list.append((ngram, hawkish_score))

# 리스트를 DataFrame으로 변환
df_hawkish = pd.DataFrame(hawkish_list, columns=['ngram', 'count'])
df_dovish = pd.DataFrame(dovish_list, columns=['ngram', 'count'])

# 각각 빈도수 높은 순으로 정렬
df_hawkish = df_hawkish.sort_values('count', ascending=False)
df_dovish = df_dovish.sort_values('count', ascending=False)

# 결과 출력
print(df_hawkish.head(15))
print(df_dovish.head(15))

# hawkish, dovish 각각 ngram 리스트 추출
hawkish_list = df_hawkish['ngram'].tolist()
dovish_list = df_dovish['ngram'].tolist()

# 두 리스트 길이를 맞추기 (짧은 쪽에 NaN 추가)
max_len = max(len(hawkish_list), len(dovish_list))
hawkish_list.extend([None] * (max_len - len(hawkish_list)))
dovish_list.extend([None] * (max_len - len(dovish_list)))

# DataFrame 생성
df_lexicon = pd.DataFrame({'hawkish': hawkish_list, 'dovish': dovish_list})

# 결과 확인
print(df_lexicon.head(40))

# CSV 파일 저장
df_lexicon.to_csv("nlp_ngram2vec/(dict_ver4)ngram_polarity_lexicon.csv", index=False)