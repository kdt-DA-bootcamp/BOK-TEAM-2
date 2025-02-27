import pandas as pd
import re
from ekonlpy.tag import Mecab

mecab = Mecab()
df = pd.read_csv('MPB.csv')

def tokenize_text(text):
    
    try:

        if not isinstance(text, str):
            return []
        
        tokens = mecab.pos(text)
        tokens = mecab.replace_synonyms(tokens)
        tokens = mecab.lemmatize(tokens)

        allowed_tags = {'NNP', 'NNG', 'VV', 'VA'}
        
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
            if pos not in allowed_tags:
                continue

            filtered_tokens.append((clean_token, pos))

        return filtered_tokens
    
    except Exception as e:
        print(f"토큰화 중 오류 발생: {text}\n오류 메시지: {e}")
        return []

df['tagged'] = df['contents'].apply(tokenize_text)

df.to_csv('tokenized_MPB_results.csv', index=False)