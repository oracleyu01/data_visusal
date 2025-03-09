### **예제 5. 박스 플롯 (Box Plot)**

### **1. 박스 플롯이 언제 필요한가?**
# ✅ 데이터의 분포와 이상치(outlier)를 동시에 파악할 때 유용함.
# ✅ 여러 그룹 간의 데이터 분포를 비교할 때 효과적임.
# ✅ 예: 지역별 매출 분포, 제품 카테고리별 수익 분포, 고객 세그먼트별 할인율 분포 등.

# 코드

# 1. 어떤 제품 카테고리가 가장 큰 매출 변동성을 보이는가?
df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv')

# 제품 대분류별 매출 박스 플롯 생성
fig = px.box(df, x='제품 대분류', y='매출', 
            title='제품 대분류별 매출 분포',
            labels={'제품 대분류': '제품 카테고리', '매출': '매출액'})

fig.update_layout(xaxis_title='제품 카테고리', yaxis_title='매출액')
fig.show()


🔹 가구 제품이 가장 큰 매출 변동성을 보이며, 일부 거래에서 매우 높은 매출이 발생
🔹 사무용품과 사무기기는 매출 변동성이 적어, 안정적인 수익 모델 구축이 가능
🔹 VIP 고객, 법인 고객 타겟 마케팅 및 구독 모델 도입으로 매출을 최적화할 전략 필요

📌 결론적으로, 가구는 "고가 주문 최적화", 사무용품과 사무기기는 "안정적인 반복 구매" 전략이 필요함! 🚀

문제. 배송 방법별 배송 소요일 분포에 차이가 있는지 분석하세요.

# 4. 배송 방법별 배송 소요일 분포에 차이가 있는지 분석하세요.
# 배송 일자와 주문 일자를 datetime으로 변환
df['주문 일자'] = pd.to_datetime(df['주문 일자'])
df['배송 일자'] = pd.to_datetime(df['배송 일자'])

# 배송 소요일 계산
df['배송 소요일'] = (df['배송 일자'] - df['주문 일자']).dt.days

# 배송 방법별 배송 소요일 박스 플롯
fig = px.box(df, x='배송 방법', y='배송 소요일',
            title='배송 방법별 배송 소요일 분포',
            labels={'배송 방법': '배송 방법', '배송 소요일': '배송 소요일(일)'})
fig.update_layout(xaxis_title='배송 방법', yaxis_title='배송 소요일(일)')
fig.show()

분석 결과 요약:

1.표준 배송: 평균적으로 가장 긴 배송 시간이 소요되며, 대략 4~6일 정도가 일반적입니다.
           일부 사례에서는 8일 이상의 배송 시간이 소요된 경우도 있습니다.
2.당일 배송: 대부분의 배송이 당일 완료되는 것으로 보이며, 일부 예외적인 경우(1일 초과)가 있지만 거의 0일에 집중되어 있습니다.
3.빠른 배송: 평균적으로 2~4일 정도 소요되며, 일부 경우 6일 이상 걸린 경우도 있습니다.
4.특급 배송: 대부분 1~2일 내에 배송이 완료되며, 일부 예외적으로 5일 이상 걸린 경우도 보입니다.

박스플롯만으로는 배송 방법 간의 차이가 유의한지를 정확히 판단하기 어려우므로,
ANOVA(분산 분석) 또는 Kruskal-Wallis 테스트를 통해 통계적으로 유의한 차이가 있는지 검정합니다.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, kruskal

# 데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")

# 날짜 형식 변환
df["주문 일자"] = pd.to_datetime(df["주문 일자"])
df["배송 일자"] = pd.to_datetime(df["배송 일자"])

# 배송 소요일 계산
df["배송 소요일"] = (df["배송 일자"] - df["주문 일자"]).dt.days

# 배송 방법 목록 가져오기
shipping_methods = df["배송 방법"].unique()

# 각 배송 방법별로 데이터 그룹화
groups = []
for method in shipping_methods:
    # 해당 배송 방법의 배송 소요일 데이터 추출
    delivery_days = df[df["배송 방법"] == method]["배송 소요일"]
    # 결측값 제거
    delivery_days = delivery_days.dropna()
    # 그룹에 추가
    groups.append(delivery_days)

# ANOVA 테스트 수행 (정규성 가정)
anova_result = f_oneway(*groups)

# 정규성을 가정하지 않는 Kruskal-Wallis 테스트 수행
kruskal_result = kruskal(*groups)

# 결과 출력
print("ANOVA 결과:", anova_result)
print("Kruskal-Wallis 결과:", kruskal_result)
