▣ 예제13. 트리맵 (Treemap) - 제품 대분류별 매출 기여도 분석

트리맵(Treemap)은 계층적 데이터를 직사각형으로 표현하여, 
전체 데이터에서 각 항목이 차지하는 비율을 직관적으로 보여주는 시각화 기법이다.
이를 활용하면 제품 대분류별 매출 기여도를 효과적으로 분석할 수 있다.

■ 트리맵이 언제 필요한가?

- 전체 데이터에서 각 항목의 비중을 비교할 때 유용하다.
- 계층적 데이터(예: 제품 카테고리, 지역, 고객 세그먼트)를 시각적으로 표현할 때 효과적이다.

    예: 제품 대분류별 매출 비중 분석, 지역별 매출 기여도 비교, 고객 세그먼트별 구매 패턴 분석

■ 문제: 제품 대분류별 매출 기여도는 어떻게 되는가?

- 목적:

- 전체 매출에서 각 제품 대분류가 차지하는 비율을 분석
- 가장 높은 매출을 기록하는 제품군을 식별
- 매출 비중이 낮은 제품군에 대한 마케팅 전략 수립

- 데이터 로드 및 Plotly Treemap 생성

import pandas as pd
import plotly.express as px

df = pd.read_csv("c:\data\SUPERSTORE_2019.csv")

df_grouped = df.groupby(["제품 대분류", "제품 중분류"])["매출"].sum().reset_index()

fig = px.treemap(df_grouped,
path=["제품 대분류", "제품 중분류"],
values="매출",
title="제품 대분류별 매출 기여도 분석 (Treemap)",
color="매출",
color_continuous_scale="blues")

fig.update_layout(width=800, height=600)

fig.show()

- 분석 결과 해석

✅ 제품 대분류별 매출 차이 분석
✔ 특정 제품 대분류(예: 가구, 사무기기)가 전체 매출에서 큰 비중을 차지
✔ 일부 제품군은 상대적으로 낮은 매출을 기록

✅ 제품 중분류별 매출 비교
✔ 동일한 제품 대분류 내에서도 일부 중분류 제품이 높은 매출을 차지하는 패턴 확인 가능
✔ 매출이 낮은 제품군에 대한 개선 전략 필요

✅ 매출 집중도 분석
✔ 특정 제품군에서 높은 매출 기여도를 보이는 경우, 해당 제품군의 마케팅 강화 필요
✔ 매출이 낮은 제품군은 가격 전략 및 프로모션을 통한 판매 촉진 필요

- 추가 분석 - 제품 대분류별 매출 차이가 통계적으로 유의한가?
트리맵을 통해 시각적으로 차이를 확인할 수 있지만, 
제품 대분류별 매출 차이가 통계적으로 유의한지 검증하기 위해 가설 검정을 수행할 필요가 있다.

import pandas as pd
from scipy.stats import f_oneway, kruskal

df = pd.read_csv("c:\data\SUPERSTORE_2019.csv")

sales_groups = [df[df["제품 대분류"] == category]["매출"].dropna() for category in df["제품 대분류"].unique()]

anova_result = f_oneway(*sales_groups)
kruskal_result = kruskal(*sales_groups)

print("ANOVA 결과:", anova_result)
print("Kruskal-Wallis 결과:", kruskal_result)

- 분석 결과 해석

✅ ANOVA 결과 해석
✔ p-value < 0.05 → 제품 대분류별 매출 차이가 통계적으로 유의미함
✔ p-value >= 0.05 → 제품 대분류별 매출 차이가 유의하지 않음

✅ Kruskal-Wallis 결과 해석
✔ p-value < 0.05 → 정규성을 가정하지 않아도 제품 대분류별 매출 차이가 존재함
✔ p-value >= 0.05 → 매출 차이가 우연일 가능성이 있음

■  결론 및 실행 전략
🚀 높은 매출을 기록한 제품군을 중심으로 마케팅을 강화하고, 고객 맞춤형 프로모션을 기획
🚀 매출이 낮은 제품군은 원인을 분석하고, 가격 조정 및 신규 프로모션을 통해 매출 촉진
🚀 제품 대분류별 매출 차이가 유의미한 경우, 제품 포트폴리오를 최적화하여 수익성을 극대화

트리맵을 활용하면 제품군별 매출 기여도를 직관적으로 분석할 수 있으며, 추가적인 가설 검정을 통해 통계적으로 유의미한 차이가 있는지 확인할 수 있다. 이를 기반으로 최적의 제품 전략을 수립할 수 있다.
