import pandas as pd
import re
from ekonlpy.tag import Mecab

mecab = Mecab()
df = pd.read_csv('filtered_bond_results.csv')

with open('stopwords.txt', 'r', encoding='utf-8') as f:
    file_stopwords = [line.strip() for line in f if line.strip()]

custom_stopwords = [
    '및', '이후', '명', '때', '전망', '없', '형', '들', '기록', '당', '성', '분', '올해', '이번', '더', '지난', '달러', '우', '향후', '같', '해', '일', '오', '총', '보', '인', '되', 
    '하', '등', '다', '년', '말', '따르', '나오', '중', '천억', '개', '임', '관련부서', '한', '있', '두', '적', '년물', '줄', '그림', '위', '이날', '당사', '가능성', '개월', '계', '현재', 
    '위하', '엔', '이', '시', '그', '각각', '수', '영향', '점', '주', '만', '데', '자료', '전일', '달', '화', '美', '인포맥스', '미', '억', '나타나', '내', '최근', '수준', '반면', '지표', 
    '예상', '전', '원', '후', '낮', '연', '별', '억억', '대', '대한', '하나금융투자', '것', '따라', '증', '약', '않', '조', '경우', '상황', '좌', '부', '열', '대해', '월'
]

stopwords = set(file_stopwords + custom_stopwords)

def tokenize_text(text):
    
    try:

        if not isinstance(text, str):
            return []
        
        tokens = mecab.pos(text)
        tokens = mecab.replace_synonyms(tokens)
        tokens = mecab.lemmatize(tokens)
        
        filtered_tokens = []
        for token, pos in tokens:
            
            # 숫자 제거
            if token.isdigit():
                continue
            
            # 링크 제거
            if token.startswith("www"):
                continue

            # 특수문자 제거
            clean_token = re.sub(r'[^가-힣a-zA-Z0-9]', '', token)
            if clean_token == '':
                continue
            
            # 품사 필터
            if pos[0] in ['I', 'J', 'E', 'S']:
                continue

            # 불용어 필터
            if clean_token in stopwords:
                continue

            filtered_tokens.append((clean_token, pos))

        return filtered_tokens
    
    except Exception as e:
        print(f"토큰화 중 오류 발생: {text}\n오류 메시지: {e}")
        return []

df['tagged'] = df['contents'].apply(tokenize_text)

df.to_csv('tokenized_bond_results.csv', index=False)