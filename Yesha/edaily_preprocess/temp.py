# eKoNPLy and Article review
# https://blog.naver.com/jjys9047/221599162443
from datetime import datetime
import csv
import pandas as pd
import numpy as np
from ekonlpy import Mecab
import re

mecab = Mecab()
start = datetime.now() 
edaily = pd.read_csv(r"C:/Users/iq750/bootcamp_git/대용량 파일 관리/edaily_results.csv")


# [표]로 시작하는 행 모두 지우기
edaily = edaily[~edaily['contents'].str.contains(r'^\[표\]', regex=True, na=False)]

print(len(edaily))

edaily.to_csv(r"C:/Users/iq750/bootcamp_git/대용량 파일 관리/edaily_results.csv", encoding = 'utf-8', index = False)