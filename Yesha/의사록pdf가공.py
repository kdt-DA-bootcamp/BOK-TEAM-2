from pdfminer.high_level import extract_text
import re
import os
import glob
import pandas as pd
import numpy as np
# PDF 파일이 있는 폴더 경로 설정
pdf_folder = r'C:\Users\iq750\bootcamp_git\BOK_project\Yesha\금통위의사록'

# 폴더 내 모든 PDF 파일 리스트 가져오기
pdf_files = glob.glob(os.path.join(pdf_folder, '*.pdf'))
# print(pdf_files)

data_date = []
data_text = []
for pdf in pdf_files:
    text = extract_text(pdf)

    # 날짜 추출 및 변환 (형식: YYYY-MM-DD)
    date_match = re.findall(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', text)

    if date_match:
        year, month, day = date_match[0]  # 첫 번째 매치만 사용
        date_f = f"{year}-{month}-{day}"
    else:
        date_f = "날짜 없음"
    data_date.append(date_f)
    # 6. 회의경과 part 텍스트 뽑기

    text = text.replace('\n', '')
    pattern = r'회의경과(.*)'
    match = re.search(pattern, text, re.DOTALL)
    article = match.group(1) if match else ""

    # 페이지 번호 제거 (예: '- 1 -' 같은 형식)
    article = re.sub(r'-\s*\d+\s*-\s', '', article)

    # 해당 텍스트 정제 (띄어쓰기 다시, 특수문자 및 숫자, 제거)
    def text_clean(text):
        # 한글 문자만 남기고 나머지는 제거
        result = re.sub(r'[^가-힣\s.,]', '', text)
        return result

    cleaned_article = text_clean(article)
    # 불필요한 단어 제거
    def remove_stopwords(text):
        stopwords = ['의안', '제호', '심의결과원안대로 가결', '의결사항', '제조제항제호', '붙임', '년', '월', '개월', '일', '분기']
        for word in stopwords:
            text = text.replace(word, '')
        return text

    article_f = remove_stopwords(cleaned_article)
    data_text.append(article_f)
print('Extracted Date:', data_date[:2])
print('Final Article:', data_text[:2])
df_MPB = pd.DataFrame({'date':data_date,
                        'article':data_text})
print(df_MPB)
import csv
df_MPB.to_csv('MPB.csv', encoding = 'utf-8')
# 텍스트가 완벽하게 뽑히진 않았으나, 줄바꿈 있던 단어들을 모두 전환
# 문장 분리에는 문제가 없을 것 같은데, 그대로 만들지 아닐지 문의

