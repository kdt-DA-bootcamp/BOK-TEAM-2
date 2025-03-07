# Evaluation 활용하면서 생긴 논의, 보고할 점
# 1. 문장을 토큰화한 새로운 csv파일을 사용함
# 2. 각 문장에 대한 감성 점수 / 각 문서에 대한 감성 점수 도출 성공 (저장 X)
# + 하지만, 기존 문장은 ngram을 거치지 않음, 이를 한 번 해야 할까?  -> 시도하고 있는데 계속 오류가 생겨서 검토 필요
# 3. 4가지 모델에 대한 감성 점수 판단 (문장별/문서별) -> 취합하여 두개의 데이터 프레임을 만들고,
# 4. 절댓값이 임의값(0.05) 보다 클 경우 hawkish(1), dovish(-1)로 수정해서 데이터 프레임 제작
# 5. 실제 라벨과 concate하여 각각의 정확도와 F1 Score, 예측률과 재현율을 측정 -> 수치로 나타내기

import pandas as pd
import numpy as np
from collections import Counter

# 기자회견 문서 로드 (문장 단위로 토큰화된 데이터) -> 문장으로 나누어진 데이터 거나, 문장을 토큰화한 데이터 일 듯
df = pd.read_csv("press_conference_sentences.csv")

# 두 개의 감성 사전 로드
# (1) ngram2vec 기반 감성사전을 활용
lexicon = pd.read_csv(r"C:\Users\iq750\bootcamp_git\BOK-TEAM-2\Yesha\nlp_ngram2vec\(dict_ver4)ngram_polarity_lexicon.csv")
hawkish_ngrams_n2v = set(lexicon['hawkish'].tolist())
dovish_ngrams_n2v = set(lexicon['dovish'].tolist())

# (2) KOSAC 감성 사전
hawkish_ngrams_kosac = set(pd.read_csv("kosac_hawkish.csv")["ngram"].tolist())
dovish_ngrams_kosac = set(pd.read_csv("kosac_dovish.csv")["ngram"].tolist())

# 문장별 감성 점수 계산 함수
def calculate_sentence_tone(sentence_tokens, hawkish_ngrams, dovish_ngrams):
    hawkish_count = sum(1 for token in sentence_tokens if token in hawkish_ngrams)
    dovish_count = sum(1 for token in sentence_tokens if token in dovish_ngrams)
    
    if hawkish_count + dovish_count == 0:
        return 0  # 감성 단어가 없는 경우 0 반환
    
    tone_s = (hawkish_count - dovish_count) / (hawkish_count + dovish_count)
    return tone_s

# 문장별 감성 점수 계산 (ngram2vec 기반)
df["tone_s_n2v"] = df["tokenized_sentence"].apply(lambda x: calculate_sentence_tone(x.split(), hawkish_ngrams_n2v, dovish_ngrams_n2v))

# 문장별 감성 점수 계산 (KOSAC 기반)
df["tone_s_kosac"] = df["tokenized_sentence"].apply(lambda x: calculate_sentence_tone(x.split(), hawkish_ngrams_kosac, dovish_ngrams_kosac))

# 문서 단위 감성 점수 계산
document_scores = df.groupby("document_id")[["tone_s_n2v", "tone_s_kosac"]].mean().reset_index()
document_scores.rename(columns={"tone_s_n2v": "tone_i_n2v", "tone_s_kosac": "tone_i_kosac"}, inplace=True)
print(document_scores.iloc[55:80])
# print(df.head(10))
# 감성 점수 저장
# document_scores.to_csv("document_sentiment_comparison.csv", index=False)

print("ngram2vec 및 KOSAC 감성 점수 비교 완료!")
