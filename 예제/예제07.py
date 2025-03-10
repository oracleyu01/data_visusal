▣ 예제 7. 파이 차트 (Pie Chart) & 도넛 차트 (Donut Chart) - 제품 카테고리별 매출 비중 분석

1. 파이 차트 & 도넛 차트가 언제 필요한가?

- 전체 데이터에서 각 항목이 차지하는 비율을 비교할 때 유용
- 한눈에 데이터의 구성 비율을 쉽게 파악할 수 있음
- 예: 제품 카테고리별 매출 비율, 지역별 주문량 비율, 고객 세그먼트별 매출 기여도 분석

2. 문제: 제품 대분류별 매출 비중은 어떻게 다른가?

목적:
- 전체 매출에서 각 제품 카테고리가 차지하는 비율을 분석하여
- 어떤 제품군이 가장 높은 매출을 발생시키는지 파악하고
- 낮은 비중의 제품군에 대한 마케팅 전략을 수립

코드:

import pandas as pd
import plotly.express as px
from scipy.stats import f_oneway, kruskal

데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")

제품 대분류별 매출 집계
category_sales = df.groupby("제품 대분류")["매출"].sum().reset_index()

파이 차트 생성 (Pie Chart)
fig = px.pie(category_sales, names="제품 대분류", values="매출",
             title="제품 대분류별 매출 비중", hole=0.0,  # hole=0.0이면 일반 파이 차트
             labels={"제품 대분류": "제품 카테고리", "매출": "매출액"},
             color_discrete_sequence=px.colors.qualitative.Set2)

fig.show()

도넛 차트 생성 (Donut Chart)
fig = px.pie(category_sales, names="제품 대분류", values="매출",
             title="제품 대분류별 매출 비중 (도넛 차트)", hole=0.4,  # hole 값을 0.4로 설정하면 도넛 차트
             labels={"제품 대분류": "제품 카테고리", "매출": "매출액"},
             color_discrete_sequence=px.colors.qualitative.Set2)

fig.show()

3. 분석 결과 해석

제품 대분류별 매출 비중 분석

1. 그래프 해석
- 이 파이 차트는 제품 대분류별 매출 비중을 나타냄
- 세 가지 제품 카테고리(사무기기, 가구, 사무용품)의 매출 비율을 비교하여 각 제품군의 기여도를 확인 가능
- 각 섹션의 크기는 전체 매출에서 해당 제품 카테고리가 차지하는 비율을 나타냄

2. 주요 분석 결과
✅ 사무기기 (37.9%)
✔ 전체 매출에서 가장 높은 비중을 차지
✔ 기업(B2B) 고객 대상 대형 주문이 많아 매출 기여도가 높음
✔ 수익성이 높은 제품군으로 추가적인 마케팅 및 프로모션 강화 가능

✅ 가구 (37.5%)
✔ 사무기기와 거의 비슷한 매출 비중을 차지
✔ 고가 제품군이 포함되어 있어 단일 거래당 매출 기여도가 높음
✔ 하지만 수익률 변동성이 크므로 손실이 발생하는 제품 분석 필요

✅ 사무용품 (24.7%)
✔ 가장 낮은 매출 비중을 기록
✔ 개별 제품 가격이 낮고, 반복 구매가 많음
✔ 안정적인 매출 흐름을 유지하지만 추가적인 수익 창출 기회가 필요

3. 인사이트 및 전략 제안
💡 사무기기
✔ 높은 매출 비중을 유지하면서 고객 충성도를 높이기 위해 B2B 고객 대상 맞춤형 할인 제공
✔ 대량 구매 고객을 위한 특가 패키지 및 멤버십 프로그램 도입 검토
✔ 사후 서비스(A/S) 및 추가 제품 업셀링 전략 추진

💡 가구
✔ 고가 제품의 마진을 최적화하여 손실을 줄이고 매출 대비 수익성을 높이는 전략 필요
✔ 인테리어 및 사무공간 최적화 패키지 제안으로 매출 증가 기회 발굴
✔ 계절별 할인 및 신규 고객 대상 혜택 제공을 통해 판매 촉진

💡 사무용품
✔ 정기 구매 고객을 대상으로 구독 모델 도입하여 안정적인 매출 구조 구축
✔ 번들 패키지 판매를 확대하여 단가를 높이고 고객당 평균 매출 증가 유도
✔ 온라인 및 오프라인 판촉 활동을 강화하여 신규 고객 유입 촉진

4. 결론
- 사무기기와 가구가 전체 매출에서 가장 큰 비중을 차지하고 있으며, 수익성을 높이기 위한 추가 최적화가 필요함
- 사무용품은 반복 구매가 많은 제품군이므로, 고객 충성도를 높이고 평균 주문 금액을 증가시키는 전략이 필요함
- 제품별 매출 비중을 고려한 맞춤형 마케팅 및 가격 전략을 수립하여 수익 극대화 가능

4. 추가 분석 - 제품 카테고리별 매출 비중 차이가 통계적으로 유의한가?

# 파이 차트는 비율을 시각적으로 보여주지만, 카테고리별 매출 차이가 통계적으로 유의한지 확인하려면 
# ANOVA 또는 Kruskal-Wallis 테스트를 수행해야 함.

# 제품 카테고리별 그룹화
product_categories = df["제품 대분류"].unique()

groups = []
for category in product_categories:
   # 해당 제품 카테고리의 매출 데이터 추출
   sales_data = df[df["제품 대분류"] == category]["매출"]
   # 결측값 제거
   sales_data = sales_data.dropna()
   # 그룹에 추가
   groups.append(sales_data)

# ANOVA 테스트 수행 (정규성 가정)
anova_result = f_oneway(*groups)

# 정규성을 가정하지 않는 Kruskal-Wallis 테스트 수행
kruskal_result = kruskal(*groups)

# 결과 출력
print("ANOVA 결과:", anova_result)
print("Kruskal-Wallis 결과:", kruskal_result)

5. 분석 결과 해석

✅ ANOVA 결과:

- p-value가 0.05 미만이면 제품 카테고리별 매출 차이가 통계적으로 유의함을 의미
- 특정 제품 카테고리가 전체 매출에서 확연히 높은 비중을 차지하는지 검증 가능

✅ Kruskal-Wallis 결과:

- 데이터의 정규성을 가정하지 않는 경우에도 제품별 매출 차이가 유의한지 확인 가능
- 매출 차이가 유의하다면, 카테고리별 맞춤 전략을 수립하는 것이 필요

결론:

🚀 가구는 주요 매출원이지만 변동성이 크므로 손실 제품을 최적화하고 프리미엄 전략 도입
🚀 사무용품은 안정적인 매출을 유지하므로, 구독 모델을 통해 추가 매출 기회 탐색
🚀 사무기기는 기업(B2B) 고객을 대상으로 대량 주문 프로모션 강화 필요

이러한 분석을 바탕으로, 각 제품군별 맞춤형 마케팅 및 가격 정책을 구축하면 더 높은 매출과 수익성을 확보할 수 있음
