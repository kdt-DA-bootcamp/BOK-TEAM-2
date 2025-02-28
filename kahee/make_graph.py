import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1. 인포맥스
df = pd.read_csv(r'C:\Users\bona_\infomax_crawler\infomax_processed.csv', encoding = 'utf-8-sig')
df['date'] = pd.to_datetime(df['date'])

infomax_counts = df.groupby(df['date'].dt.to_period('M')).size()
infomax_counts= infomax_counts.loc["2014-01":"2024-11"]




# 2. 한국경제
df = pd.read_csv(r'C:\Users\bona_\infomax_crawler\2010to2025_results.csv', encoding = 'utf-8-sig')

#날짜 형식 통일
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime("%Y-%m-%d")
df.to_csv("hk_date_update.csv", index=False)
df = pd.read_csv(r'C:\Users\bona_\infomax_crawler\hk_date_update.csv', encoding = 'utf-8-sig')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

hk_counts = df.groupby(df['date'].dt.to_period('M')).size()
hk_counts= hk_counts.loc["2014-01":"2024-11"]
#print(hk_counts)
#print(sum(hk_counts))

hk_counts_only = hk_counts.tolist()
print(hk_counts_only)




# 3. 이데일리
df = pd.read_csv(r'C:\Users\bona_\infomax_crawler\edaily_results.csv', encoding = 'utf-8-sig', on_bad_lines='skip')
df['date'] = pd.to_datetime(df['date'])
edaily_counts = df.groupby(df['date'].dt.to_period('M')).size()

# 데이터 없는 기간 0으로 채우기
periods = pd.period_range(start="2014-01", end="2024-11", freq="M")
edaily_counts = edaily_counts.reindex(periods, fill_value=0)

# print(edaily_counts)
# print(sum(edaily_counts))

counts_only = edaily_counts.tolist()
print(counts_only)



# 그래프 그리기

# 데이터 정리
df = pd.DataFrame(list(infomax_counts.items()), columns=["date", "Infomax"])
df['Hankyung'] = [281, 261, 250, 235, 238, 258, 332, 329, 324, 383, 309, 386, 363, 296, 608, 435, 406, 428, 364, 458, 518, 438, 424, 481, 378, 383, 356, 320, 354, 392, 284, 369, 370, 356, 393, 406, 292, 246, 295, 196, 183, 213, 228, 163, 223, 186, 215, 221, 258, 280, 253, 243, 254, 244, 256, 219, 180, 278, 237, 263, 304, 129, 193, 212, 185, 184, 258, 260, 258, 282, 217, 232, 164, 203, 430, 249, 141, 221, 207, 228, 238, 187, 252, 249, 267, 254, 310, 262, 248, 287, 279, 125, 189, 305, 279, 290, 415, 361, 395, 460, 530, 592, 700, 632, 728, 752, 614, 583, 586, 533, 512, 556, 527, 472, 397, 436, 412, 546, 557, 542, 690, 509, 531, 630, 484, 445, 568, 583, 477, 466, 414]
df['Edaily'] = [600, 590, 656, 541, 502, 587, 841, 790, 809, 925, 813, 872, 970, 789, 1375, 969, 1016, 1140, 905, 957, 1097, 1007, 1180, 1420, 976, 843, 921, 709, 752, 908, 749, 756, 870, 786, 797, 960, 810, 658, 917, 658, 542, 664, 536, 523, 521, 581, 591, 555, 546, 644, 567, 477, 497, 547, 491, 482, 476, 725, 540, 585, 551, 296, 411, 352, 356, 480, 593, 448, 0, 0, 1, 0, 0, 0, 812, 465, 342, 415, 407, 400, 413, 336, 338, 330, 528, 496, 780, 571, 509, 664, 668, 606, 586, 609, 708, 691, 0, 0, 0, 0, 923, 1205, 1425, 1161, 1299, 1372, 1356, 1256, 0, 0, 0, 694, 979, 1045, 918, 1224, 1032, 1387, 1413, 1308, 0, 0, 978, 2706, 2424, 2218, 2726, 2532, 2272, 2148, 1996]

# 'monthly_sum' 열 추가 (세 개 언론사의 합)
df["monthly_sum"] = df[["Infomax", "Hankyung", "Edaily"]].sum(axis=1)


# 새로운 csv파일로 저장
df.to_csv(r'C:\Users\bona_\infomax_crawler\for_graph.csv', index=False, encoding="utf-8-sig")




#월별 총 기사수(꺾은선)
df = pd.read_csv(r'C:\Users\bona_\infomax_crawler\for_graph.csv', encoding="utf-8-sig")

# if "date" in df.columns:
#     df["date"] = pd.to_datetime(df["date"])

plt.figure(figsize=(12, 6))
plt.plot(df["date"], df["monthly_sum"], linestyle="-")

plt.xlabel("Month")
plt.ylabel("Number of News")
plt.title("Number of news for each month")
plt.legend()

plt.show()


#연도별, 언론사별 기사 수 (히스토그램)
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
yearly_counts = df.groupby("year")[["Infomax", "Hankyung", "Edaily"]].sum()

plt.figure(figsize=(12, 6))
yearly_counts.plot(kind="bar", stacked=True, figsize=(12, 6))

plt.title("Total number of News per agency over time")
plt.xticks(rotation=90)
plt.legend(title="News Source")
# plt.grid(axis="y", linestyle="--", alpha=0.7)
# 그리드 없는 게 더 깔끔해보여서 우선은 지웠습니다

plt.show()