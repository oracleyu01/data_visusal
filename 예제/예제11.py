▣ 예제11. 히트맵 (Heatmap) - 지역별 고객 세그먼트 매출 분석

히트맵(Heatmap)은 데이터를 색상으로 표현하여 변수 간의 관계를 시각적으로 확인할 수 있는 그래프이다. 이를 활용하면 지역별 고객 세그먼트 매출 차이를 한눈에 비교할 수 있다.

■ 히트맵이 언제 필요한가?

- 데이터의 패턴 및 경향성을 직관적으로 분석할 때 유용하다.
- 다변량 데이터 간의 관계를 시각적으로 비교할 수 있다.
예: 지역별 고객 세그먼트 매출, 제품 카테고리별 수익성, 시간대별 주문량 비교

■ 문제: 고객 세그먼트별 지역별 매출 차이는 어떻게 되는가?

- 목적:

- 지역별 매출 규모가 어떻게 다른지 분석
- 고객 세그먼트별 매출 비율이 지역에 따라 어떻게 변화하는지 확인
- 매출이 낮은 지역과 고객 세그먼트에 대한 전략적 접근 필요

- 데이터 로드 및 Plotly 히트맵 생성

import pandas as pd
import plotly.express as px

df = pd.read_csv("c:\data\SUPERSTORE_2019.csv")

df_grouped = df.groupby(["고객 세그먼트", "지역"])["매출"].sum().reset_index()

fig = px.imshow(df_grouped.pivot(index="고객 세그먼트", columns="지역", values="매출"),
labels=dict(x="지역", y="고객 세그먼트", color="매출"),
title="고객 세그먼트별 지역별 매출 분포 (Heatmap)",
color_continuous_scale="blues")

fig.update_layout(width=800, height=600)

fig.show()

■ 분석 결과 해석
✅ 지역별 매출 차이 분석
✔ 수도권과 영남 지역에서 가장 높은 매출을 기록
✔ 강원, 제주 지역에서는 상대적으로 매출이 낮음

✅ 고객 세그먼트별 매출 차이 분석
✔ 기업 고객이 대부분의 지역에서 높은 매출을 차지
✔ 소비자와 홈 오피스 고객 매출은 지역에 따라 차이가 있음

✅ 매출 집중도 분석
✔ 특정 지역에서 특정 고객 세그먼트가 강한 매출을 보이는 패턴 확인 가능
✔ 매출이 낮은 지역에서는 마케팅 강화가 필요

추가 분석 - 지역별 매출 차이가 통계적으로 유의한가?
히트맵을 통해 시각적으로 차이를 확인할 수 있지만, 지역별 매출 차이가 통계적으로 유의한지 검증하기 위해 가설 검정을 수행할 필요가 있다.

import pandas as pd
from scipy.stats import f_oneway, kruskal

df = pd.read_csv("c:\data\SUPERSTORE_2019.csv")

sales_groups = [df[df["지역"] == region]["매출"].dropna() for region in df["지역"].unique()]

anova_result = f_oneway(*sales_groups)
kruskal_result = kruskal(*sales_groups)

print("ANOVA 결과:", anova_result)
print("Kruskal-Wallis 결과:", kruskal_result)

■ 분석 결과 해석
✅ ANOVA 결과 해석
✔ p-value < 0.05 → 지역별 매출 차이가 통계적으로 유의미함
✔ p-value >= 0.05 → 지역별 매출 차이가 유의하지 않음

✅ Kruskal-Wallis 결과 해석
✔ p-value < 0.05 → 정규성을 가정하지 않아도 지역별 매출 차이가 존재함
✔ p-value >= 0.05 → 매출 차이가 우연일 가능성이 있음

■ 결론 및 실행 전략
🚀 수도권과 영남 지역에서 기업 고객을 대상으로 프리미엄 서비스를 제공하여 매출 극대화 필요
🚀 충청, 호남 지역에서는 소비자 및 홈 오피스 고객을 타겟으로 신규 고객 확보 전략 강화
🚀 매출이 낮은 강원, 제주 지역에서는 지역 특성을 반영한 프로모션 전략 적용

히트맵을 활용하여 지역별 고객 세그먼트 매출을 분석한 후, 가설 검정을 통해 차이가 통계적으로 유의한지 확인하면 더욱 정밀한 데이터 기반 전략을 수립할 수 있다.
