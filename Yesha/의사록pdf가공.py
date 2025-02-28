from pdfminer.high_level import extract_text
import re
import os
import glob
import pandas as pd
import numpy as np
# PDF 파일이 있는 폴더 경로 설정
pdf_folder = r"C:\Users\iq750\bootcamp_git\BOK-TEAM-2\Yesha\pdf_금통위의사록"

# 폴더 내 모F든 PDF 파일 리스트 가져오기
pdf_files = glob.glob(os.path.join(pdf_folder, '*.pdf'))
# print(pdf_files)
# 해당 텍스트 정제 (한글, 숫자, 공백, 쉼표, 온점만 남김.)
def text_clean(text):
    result = re.sub(r'[^가-힣0-9\s.,]', '', text)
    return result

data_date = []
data_text = []
for pdf in pdf_files:
    text = extract_text(pdf)

    # 날짜 추출 및 변환 (형식: YYYY-MM-DD)
    date_match = re.findall(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', text)

    if date_match:
        year, month, day = date_match[0]  # 첫 번째 매치만 사용
        if len(month) == 1 :
            month = '0' + month
        if len(day) == 1 :
            day = '0' + day
        date_f = f"{year}-{month}-{day}"
        print(date_f) # 정상적으로 출력되는 것 확인 가능
    else:
        date_f = "날짜 없음"
    data_date.append(date_f)

    # 페이지 번호 제거 (예: '- 1 -' 같은 형식)
    article = re.sub(r'-\s*\d+\s*-\s', '', text)

    # 텍스트 뽑기 (위원 토의내용/의결사항)
    # 위원 토의내용 ~ 심의결과 까지
    all_article = ""
    discuss = re.findall(r"위원 토의내용(.*?)심의결과", article, re.DOTALL)
    for i, text in enumerate(discuss, 1):
        # print(f"{i}: {text.strip()}")
        all_article += text

    # 의결사항 ~ < 나 (
    decision = re.findall(r"의결사항(.*?)(?:붙임|별첨|<)", article, re.DOTALL)
    for i, text in enumerate(decision, 1):
        print(f"{i}: {text.strip()}")
        all_article += text
    break
    all_article = all_article.replace('\n', '')
    all_article = " ".join(all_article.split())
    # 불필요한 단어 제거
    article_f = text_clean(all_article)
    data_text.append(article_f)
print('Extracted Date:', data_date[:2])
print('Final Article:', data_text[:2])
df_MPB = pd.DataFrame({'date':data_date,
                        'article':data_text})
print(df_MPB)
df_MPB.to_csv('C:/Users/iq750/bootcamp_git/대용량 파일 관리/MPB.csv', encoding = 'utf-8')
# 텍스트가 완벽하게 뽑히진 않았으나, 줄바꿈 있던 단어들을 모두 전환
# 문장 분리에는 문제가 없을 것 같은데, 그대로 만들지 아닐지 문의

