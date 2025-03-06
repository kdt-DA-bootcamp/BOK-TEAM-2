import pandas as pd
import numpy as np
from collections import Counter

# 기자회견 문서 로드 (문장 단위로 토큰화된 데이터)
df = pd.read_csv("Evaluation/conferences_sentences.csv")  # 문장 데이터 파일

# 두 개의 감성 사전 로드
# (1) ngram2vec 기반 감성사전을 활용
lexicon = pd.read_csv('nlp_ngram2vec\(dict_ver4)ngram_polarity_lexicon.csv')
hawkish_ngrams_nb = set(lexicon['hawkish'].tolist())
dovish_ngrams_nb = set(lexicon['dovish'].tolist())

# (2) KOSAC 감성 사전
hawkish_ngrams_kosac = set(pd.read_csv("kosac_hawkish.csv")["feature"].tolist())
dovish_ngrams_kosac = set(pd.read_csv("kosac_dovish.csv")["feature"].tolist())

# 문장별 감성 점수 계산 함수
def calculate_sentence_tone(sentence_tokens, hawkish_ngrams, dovish_ngrams):
    hawkish_count = sum(1 for token in sentence_tokens if token in hawkish_ngrams)
    dovish_count = sum(1 for token in sentence_tokens if token in dovish_ngrams)
    
    if hawkish_count + dovish_count == 0:
        return 0  # 감성 단어가 없는 경우 0 반환
    
    tone_s = (hawkish_count - dovish_count) / (hawkish_count + dovish_count)
    return tone_s

# 문장별 감성 점수 계산 (나이브 베이즈 기반)
df["tone_s_nb"] = df["tokenized_sentence"].apply(lambda x: calculate_sentence_tone(eval(x), hawkish_ngrams_nb, dovish_ngrams_nb))

# 문장별 감성 점수 계산 (KOSAC 기반)
df["tone_s_kosac"] = df["tokenized_sentence"].apply(lambda x: calculate_sentence_tone(eval(x), hawkish_ngrams_kosac, dovish_ngrams_kosac))

# 문서 단위 감성 점수 계산
document_scores = df.groupby("document_id")[["tone_s_nb", "tone_s_kosac"]].mean().reset_index()
document_scores.rename(columns={"tone_s_nb": "tone_i_nb", "tone_s_kosac": "tone_i_kosac"}, inplace=True)

# 감성 점수 저장
document_scores.to_csv("document_sentiment_comparison.csv", index=False)

print("나이브 베이즈 및 KOSAC 감성 점수 비교 완료!")
