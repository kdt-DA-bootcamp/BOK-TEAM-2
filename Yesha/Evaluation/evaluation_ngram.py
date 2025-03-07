import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
#########################
# 기자회견 문서 로드
df = pd.read_csv("press_conference_sentences.csv")  # 숫자 안 지운 버전으로 다시 실행되길래 그대로 감
# n-gram 생성 함수
def generate_ngrams(text, n=5): 
    if not text.strip():  
        return []
    vectorizer = CountVectorizer(ngram_range=(1, n), token_pattern=r"(?u)\b\w+\b") # 숫자도 무시
    ngrams = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out().tolist()

# n-gram 적용
df['ngrams'] = df["tokenized_sentence"].apply(lambda x: generate_ngrams(x, n=5))
df['filtered_ngrams'] = df['filtered_tokenized_sentence'].apply(lambda x: generate_ngrams(x, n=5))

#########################
# 감성 사전 로드
# (1) ngram2vector
lexicon = pd.read_csv(r"C:/Users/iq750/bootcamp_git/BOK-TEAM-2/Yesha/nlp_ngram2vec/(dict_ver4)ngram_polarity_lexicon.csv")
hawkish_ngrams_n2v = set(lexicon['hawkish'].dropna().tolist())
dovish_ngrams_n2v = set(lexicon['dovish'].dropna().tolist())

# (2) Fast Text 모델
lexicon = pd.read_csv(r"C:/Users/iq750/bootcamp_git/대용량 파일 관리/최종lexicon/Fast-text_final.csv")
hawkish_ngrams_ft = set(lexicon['Hawkish'].dropna().tolist())
dovish_ngrams_ft = set(lexicon['Dovish'].dropna().tolist())

# (3) NBC_1 (예담)
lexicon = pd.read_csv(r"C:/Users/iq750/bootcamp_git/대용량 파일 관리/최종lexicon/word_dictionary_cleaned.csv")
hawkish_ngrams_nb1 = set(lexicon['hawkish'].dropna().tolist())
dovish_ngrams_nb1 = set(lexicon['dovish'].dropna().tolist())

# (4) NBC_2 (가희)
lexicon = pd.read_csv(r"C:/Users/iq750/bootcamp_git/대용량 파일 관리/최종lexicon/word_list.final.csv")
hawkish_ngrams_nb2 = set(lexicon['hawkish'].dropna().tolist())
dovish_ngrams_nb2 = set(lexicon['dovish'].dropna().tolist())
# (5) Kosac
hawkish_ngrams_kosac = set(pd.read_csv("filter_kosac_hawkish.csv")["filtered_ngram"].dropna().tolist())
dovish_ngrams_kosac = set(pd.read_csv("filter_kosac_dovish.csv")["filtered_ngram"].dropna().tolist())

#########################
# 감성 점수 계산 함수 (n-gram 기반)
def calculate_sentence_tone(ngrams, hawkish_ngrams, dovish_ngrams):
    hawkish_count = sum(1 for token in ngrams if token in hawkish_ngrams)
    dovish_count = sum(1 for token in ngrams if token in dovish_ngrams)
    
    if hawkish_count + dovish_count == 0:
        return 0
    
    return (hawkish_count - dovish_count) / (hawkish_count + dovish_count)

# 감성 점수 계산 적용
df["tone_s_n2v"] = df['filtered_ngrams'].apply(lambda x: calculate_sentence_tone(x, hawkish_ngrams_n2v, dovish_ngrams_n2v))
df["tone_s_ft"] = df['filtered_ngrams'].apply(lambda x: calculate_sentence_tone(x, hawkish_ngrams_ft, dovish_ngrams_ft))
df["tone_s_nb1"] = df['filtered_ngrams'].apply(lambda x: calculate_sentence_tone(x, hawkish_ngrams_nb1, dovish_ngrams_nb1))
df["tone_s_nb2"] = df['filtered_ngrams'].apply(lambda x: calculate_sentence_tone(x, hawkish_ngrams_nb2, dovish_ngrams_nb2))
df["tone_s_kosac"] = df['filtered_ngrams'].apply(lambda x: calculate_sentence_tone(x, hawkish_ngrams_kosac, dovish_ngrams_kosac))
print(df[['tone_s_n2v',"tone_s_ft",'tone_s_nb1','tone_s_nb2','tone_s_kosac']].iloc[70:88])

# 문장 polarity 저장
sentences_scores = df[['date', 'document_id', 'ngrams', 'tone_s_n2v', 'tone_s_ft', 'tone_s_nb1', 'tone_s_nb2', 'tone_s_kosac']]
sentences_scores.to_csv('filter_ngram문장단위감성점수계산.csv', encoding = 'utf-8-sig')

#####################################################

# 문서 단위 감성 점수 계산
document_scores = df.groupby("document_id")[["tone_s_n2v","tone_s_ft","tone_s_nb1","tone_s_nb2", "tone_s_kosac"]].mean().reset_index()
document_scores.rename(columns={"tone_s_n2v": "tone_i_n2v","tone_s_ft": "tone_i_ft","tone_s_nb1": "tone_i_nb1","tone_s_nb2": "tone_i_nb2", "tone_s_kosac": "tone_i_kosac"}, inplace=True)
document_scores['date'] = df.groupby('document_id')['date'].first().reset_index()['date']
document_scores = document_scores[['date', 'tone_i_n2v', 'tone_i_ft', 'tone_i_nb1', 'tone_i_nb2', 'tone_i_kosac']]
print(document_scores.iloc[0:20])
# 문서 polarity 저장
document_scores.to_csv('filter_ngram문서단위감성점수계산.csv', encoding = 'utf-8-sig')

print("모델, KOSAC 간 감성 점수 비교 완료!")