# Deciphering Monetary Policy Board Minutes with Text Mining: The Case of South Korea* 

## 데이터와 방법론

### Sentimental Analysis
1. 문서 크롤링
2. 전처리
3. N-gram? tagging
4. Classification
5. 
```
 (i) preparation of the 
corpus of interests, (ii) pre-processing of texts, (iii) feature selection, (iv) polarity or sentiment classification of features, and (v) measurement of sentiments of sentences and documents
```
---

## Data And Methology

### 데이터 수집
1. 어떤 데이터 얼마나 수집할 것인가? (뉴스기사 + 채권 보고서 + 한국은행 의사록)
2. 기준 금리
- scrapy / multi threding
3. 의사록 (사용할 section과 시기)
4. 뉴스: 포함된 단어 / 주제 등 + 중복된 기사 수집 막기 위한 방법 고안 (top3 news 배급사)
5. 채권 분석 보고서 

- Topic Modeling을 통한 주제 추출(LDA)
- 각 토픽 별로 글을 나누고 (topic 어떻게 정할 것인가?)

### 데이터 전처리 (Data Cleansing)
1. typical: Tokenization, Normalization(punctuation removal, stop word removal, conversion of numbers to their word equivalents, stemming, lemmatization, and case folding, 한국어processing 고민)
2. eKonlpy: Mecab 활용, 관련 자료 조금 더 찾아볼 수 있음
3. 만약 사전에 없는 외래어 등 나올 시 사전 추가 작업도 필요
4. Normalization은 표제어 추출로 

### Future Selection
1. n-gram (몇 개 단어까지 묶을 것인가?, 어떤 단어를 사용할 것인가?)
2. 1 to 5 gram -> n-grams polarity
3. Polarity Classification: 언어적 접근 or Machine Learning 사용? + n-gram polarity 구분 방법

### Polarity  Classification
1. Lexical Approach: 직관적으로 자주 같이 나옴 == polarity 같음 (SO-PMI 사용 가능)
- ngram embedding, SentProp frameword
- ngram2vec (공부 필요)
2. NBC : Market Approach : 나이브베이즈 분류 (data 확보, 학습 데이터 9:1, 5gram으로 각 문장 구분하여 사용, accuracy 확인)
-> 극성 어휘를 뽑아내는 방법 (문장에서 뽑아낸 n-gram 바탕으로 긍/부정 labeling, 이를 교육 시켜서 정리)

## 평가()
- Accuracy, Precision, Recall, F1 score 등 활용

### lexicon 형성에 사용되지 않은 문서로 평가
1. 특정 문서 라벨을 수동으로 지정하고
2. 우리가 사용한 모델을 바탕으로 train 후 test score 확인
3. NBC -> 반복
4. vs KOSAC

---

## Empirical Analysis

### 실증적 분석_ RQ
1. Can our lexicon-based indicators ( mkt tone and lex tone ) explain the BOK’s current and future monetary policy decisions? In particular, do these indicators have additional information that are unavailable in the existing macroeconomic data? 
2. Is it important to use a field-specific dictionary? 
3. Is it important to use the original Korean text, not Korean-to-English text?

### Measures of MP Sentiment
- market approach
- lexical approach 
-> 2개의 indicators 만듦

-> RE: evaluation ~ comparsion