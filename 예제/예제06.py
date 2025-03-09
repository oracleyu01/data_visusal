
▣ 예제 6. 바이올린 플롯 (Violin Plot) - 수익률 분석

1. 바이올린 플롯이 언제 필요한가?

- 데이터의 분포와 밀도를 시각적으로 확인할 때 유용
- 극단값(outlier)과 데이터가 몰려 있는 부분을 동시에 확인 가능
- 평균값과 분포를 비교하면서 차이를 해석할 때 효과적
- 예: 지역별 수익률 분포, 제품 카테고리별 마진율, 고객 세그먼트별 할인율 비교

2. 문제: 제품 카테고리별 수익률(매출 대비 수익) 분포는 어떻게 다른가?

목적:
- 제품 카테고리별 수익률을 비교하여,
- 어떤 카테고리가 높은 마진을 갖고 있으며,
- 수익률이 낮은 제품군을 최적화할 방법을 모색

# 데이터 로드

import pandas as pd
import plotly.express as px
from scipy.stats import f_oneway, kruskal

df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")

# 수익률 계산 (수익 / 매출 * 100)
df["수익률"] = (df["수익"] / df["매출"]) * 100

# 제품 대분류별 수익률 바이올린 플롯 생성
fig = px.violin(df, x="제품 대분류", y="수익률", box=True, points="all",
                title="제품 대분류별 수익률 분포",
                labels={"제품 대분류": "제품 카테고리", "수익률": "수익률 (%)"},
                color="제품 대분류")

fig.update_layout(xaxis_title="제품 카테고리", yaxis_title="수익률 (%)")
fig.show()

3. 분석 결과 해석

💡 사무용품
✔ 수익률이 안정적인 제품군 → 유지하면서 신규 고객 확대 전략 필요
✔ 할인율을 낮추고, 꾸준한 반복 구매를 유도하는 구독 모델 도입 고려

💡 가구
✔ 수익률 변동성이 매우 크므로, 손실이 발생하는 제품을 분석할 필요가 있음
✔ 마진율이 낮거나 손실이 많은 제품의 가격 정책 및 원가 절감 전략 필요
✔ 손실 발생 원인을 파악하여 비효율적인 제품을 단종하거나 리브랜딩 고려

💡 사무기기
✔ 수익률이 일정하지만, 일부 손실이 발생하는 제품을 분석하여 최적화 필요
✔ 기업 대상의 B2B 프로모션을 강화하여 안정적인 매출 확보
✔ 고객 맞춤형 할인 정책을 도입하여 수익률을 조정

4. 추가 분석 - 수익률 차이가 통계적으로 유의한가?
바이올린 플롯만으로는 차이를 확실히 판단하기 어려우므로, ANOVA(분산 분석) 또는 Kruskal-Wallis 테스트를 수행하여 유의성을 검증

# 제품 카테고리별 그룹화
shipping_methods = df["제품 대분류"].unique()

groups = []
for category in shipping_methods:
   # 해당 제품 카테고리의 수익률 데이터 추출
   profit_ratio = df[df["제품 대분류"] == category]["수익률"]
   # 결측값 제거
   profit_ratio = profit_ratio.dropna()
   # 그룹에 추가
   groups.append(profit_ratio)

# ANOVA 테스트 수행 (정규성 가정)
anova_result = f_oneway(*groups)

# 정규성을 가정하지 않는 Kruskal-Wallis 테스트 수행
kruskal_result = kruskal(*groups)

# 결과 출력
print("ANOVA 결과:", anova_result)
print("Kruskal-Wallis 결과:", kruskal_result)

5. 분석 결과 해석

- ANOVA 결과: p-value가 0.05 미만이면 제품 카테고리별 수익률 차이가 통계적으로 유의함을 의미
- Kruskal-Wallis 결과: 데이터의 정규성을 가정하지 않더라도 제품별 수익률 차이가 유의한지 검정

결론:
- 제품별 수익률 차이가 유의하다면, 고수익 제품을 중심으로 마케팅 및 가격 정책을 최적화해야 함
- 가구는 마진율 개선, 사무용품은 고객 확대, 사무기기는 손실 제품 분석이 필요
