# 중복 정리
import pandas as pd
word_dic = pd.read_csv('파일경로로', dtype = str)

# 양쪽에 같은 단어가 있다면, 모호성이 크다고 보고 df에서 삭제해줄 것
# ex) 양족 모두 있을 법한 '금리' 라는 단어는 삭제해도 됨

# 1. 둘을 다른 데이터 프레임으로 분리한다. dovish / hawkish
df_hawkish = pd.DataFrame(word_dic['hawkish'], dtype=str)
df_dovish = pd.DataFrame(word_dic['dovish'], dtype=str)

# 2. 둘을 비교해가면서 중복으로 들어간 데이터는 두 df 모두에서 삭제 해 본다.

# 2-1. 우선 각 df 내에서 중복된 값을 지움
df_hawkish = df_hawkish.drop_duplicates()
df_dovish = df_dovish.drop_duplicates()
# 2-2. 둘을 순회하면서 서로 중복된 값을 지운다.
common_values = set(df_hawkish['hawkish']).intersection(set(df_dovish['dovish']))

# 교집합에 해당하는 값 삭제
df_hawkish = df_hawkish[~df_hawkish['hawkish'].isin(common_values)]
df_dovish = df_dovish[~df_dovish['dovish'].isin(common_values)]

# 인덱스를 0부터 재설정
df_hawkish = df_hawkish.reset_index(drop=True)
df_dovish = df_dovish.reset_index(drop=True)

# 3. 개수를 확인하고, 순서를 확인해서 구축한다.
df_hawkish.dropna(inplace=True)
df_dovish.dropna(inplace=True)