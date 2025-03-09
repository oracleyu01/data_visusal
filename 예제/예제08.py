▣ 예제8. 버블 차트 (Bubble Chart) - 지역별 매출, 수익 및 주문량 분석

1. 버블 차트가 언제 필요한가?
- 세 개 이상의 변수를 동시에 시각화할 때 유용
- X축과 Y축으로 두 개의 변수를 나타내고, 버블 크기로 세 번째 변수를 표현
- 데이터 간의 상대적인 관계를 시각적으로 비교하기에 적합
- 예: 지역별 매출, 수익 및 주문량 분석, 고객 세그먼트별 매출 및 평균 구매 금액 분석, 특정 기간별 판매 트렌드 비교

2. 문제: 지역별 매출과 수익, 주문량 간의 관계는 어떻게 되는가?

목적:
- 지역별 매출과 수익, 주문량 간의 관계를 분석하여
- 매출이 높지만 수익이 낮은 지역과 매출은 낮지만 수익이 높은 지역을 구분
- 지역별 맞춤 마케팅 및 프로모션 전략을 최적화


import pandas as pd
import plotly.express as px
from scipy.stats import f_oneway, kruskal

데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")

지역별 매출, 수익 및 주문량 집계
region_stats = df.groupby("지역").agg({"매출": "sum", "수익": "sum", "주문 번호": "count"}).reset_index()
region_stats.rename(columns={"주문 번호": "주문량"}, inplace=True)

버블 차트 생성 (Bubble Chart)
fig = px.scatter(region_stats, x="매출", y="수익", size="주문량", color="지역",
                 title="지역별 매출, 수익 및 주문량 비교",
                 labels={"매출": "총 매출액", "수익": "총 수익", "주문량": "주문 개수", "지역": "지역명"},
                 hover_name="지역", size_max=60)

fig.show()

3. 분석 결과 해석

지역별 매출, 수익 및 주문량 비교 - 버블 차트 핵심 분석

1. 주요 해석

✅ 수도권 (빨간색)
✔ 가장 높은 매출과 수익을 기록하며, 주문량도 가장 많음
✔ 고객 충성도 유지 및 프리미엄 제품 판매 전략이 효과적

✅ 영남 (초록색)
✔ 두 번째로 높은 매출과 수익을 기록하며, 고객당 평균 주문액이 높을 가능성
✔ B2B 시장 확대 및 오프라인-온라인 연계 마케팅 필요

✅ 충청 & 호남 (주황색, 하늘색)
✔ 중간 수준의 매출과 수익, 주문량이 수도권과 영남보다 적음
✔ 할인 프로모션과 지역 맞춤형 상품 제공으로 시장 점유율 확대 필요

✅ 강원 & 제주 (보라색)
✔ 매출과 수익이 가장 낮고, 주문량도 적음
✔ 물류 최적화 및 계절별 프로모션을 통한 매출 증대 전략 필요

2. 전략적 제안

🚀 수도권 - 프리미엄 제품 판매 및 VIP 고객 프로그램 운영  
🚀 영남 - B2B 영업 강화 및 대형 주문 패키지 제공  
🚀 충청 & 호남 - 할인 프로모션 및 신규 고객 유입 마케팅 강화  
🚀 강원 & 제주 - 물류 최적화 및 시즌별 특가 프로모션 진행  

지역별 맞춤 전략을 적용하면 매출 극대화 및 수익 최적화 가능


이러한 분석을 기반으로 지역별 맞춤형 마케팅과 영업 전략을 최적화하면 더욱 높은 매출과 수익을 달성할 수 있다.

5. 추가 분석 - 지역별 매출 및 수익 차이가 통계적으로 유의한가?

지역별 그룹화 (매출)
sales_groups = [df[df["지역"] == region]["매출"].dropna() for region in df["지역"].unique()]

지역별 그룹화 (수익)
profit_groups = [df[df["지역"] == region]["수익"].dropna() for region in df["지역"].unique()]

ANOVA 테스트 수행 (정규성 가정)
anova_sales_result = f_oneway(*sales_groups)
anova_profit_result = f_oneway(*profit_groups)

정규성을 가정하지 않는 Kruskal-Wallis 테스트 수행
kruskal_sales_result = kruskal(*sales_groups)
kruskal_profit_result = kruskal(*profit_groups)

결과 출력
print("ANOVA 결과 (매출):", anova_sales_result)
print("ANOVA 결과 (수익):", anova_profit_result)
print("Kruskal-Wallis 결과 (매출):", kruskal_sales_result)
print("Kruskal-Wallis 결과 (수익):", kruskal_profit_result)

6. 분석 결과 해석

✅ ANOVA 결과
- p-value가 0.05 미만이면 지역별 매출 및 수익 차이가 통계적으로 유의함을 의미
- 특정 지역이 다른 지역보다 확연히 높은 매출 또는 수익을 기록하는지 검증 가능

✅ Kruskal-Wallis 결과
- 데이터의 정규성을 가정하지 않는 경우에도 지역별 매출 및 수익 차이가 유의한지 확인 가능
- 통계적으로 유의한 차이가 있다면, 지역별 맞춤 전략을 수립하는 것이 필요

결론
🚀 수도권은 기존 고객 중심의 마케팅을 강화하고, 프리미엄 제품 전략을 도입할 필요
🚀 충청 & 영남은 수익성 개선이 필요하며, 패키지 프로모션과 B2B 영업을 강화해야 함
🚀 호남, 강원, 제주 지역은 맞춤형 광고와 배송 최적화를 통해 시장 점유율을 확대해야 함

이러한 분석을 바탕으로, 지역별 맞춤형 판매 전략을 최적화하면 더욱 높은 매출과 수익성을 확보할 수 있음
