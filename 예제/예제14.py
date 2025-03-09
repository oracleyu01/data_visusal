## **예제14.** 레이더 차트 (Radar Chart)

레이더 차트(Radar Chart)는 여러 변수의 값을 다각형 형태로 표현하는 시각화 기법으로, 
다차원 데이터를 한 눈에 비교할 수 있게 해준다. 
이를 활용하면 제품 카테고리별 매출, 수익, 수량과 같은 다양한 지표를 동시에 분석할 수 있다.

### ■ 레이더 차트가 언제 필요한가?
  
- 여러 카테고리에 대해 다양한 측정값을 동시에 비교할 때 유용하다.
- 각 항목이 여러 측면에서 어떤 성능을 보이는지 파악할 때 효과적이다.
  예: 제품 카테고리별 매출/수익/수량 비교, 지역별 여러 성과 지표 분석, 고객 세그먼트별 다양한 구매 패턴 비교

### ■ 문제: 제품 대분류별 성과는 어떻게 비교되는가?

- 목적:
  - 제품 대분류별 매출, 수익, 수량, 할인율의 상대적 비교
  - 각 제품군의 강점과 약점 식별
  - 균형 잡힌 성과를 보이는 제품군과 특정 지표에서만 높은 성과를 보이는 제품군 구분

### - 데이터 로드 및 Plotly 레이더 차트 생성

```python
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")

# 제품 대분류별 지표 계산
category_metrics = df.groupby("제품 대분류").agg({
    "매출": "sum",
    "수익": "sum",
    "수량": "sum",
    "할인율": "mean"
}).reset_index()

# 정규화 함수 (0-1 스케일로 변환)
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# 각 지표 정규화
for col in ["매출", "수익", "수량", "할인율"]:
    category_metrics[f"{col}_norm"] = normalize(category_metrics[col])

# 레이더 차트 생성
categories = ["매출", "수익", "수량", "할인율"]
fig = go.Figure()

# 각 제품 대분류별로 레이더 차트에 추가
colors = ['blue', 'red', 'green', 'purple', 'orange']
for i, category in enumerate(category_metrics["제품 대분류"]):
    values = [
        category_metrics.loc[category_metrics["제품 대분류"] == category, "매출_norm"].values[0],
        category_metrics.loc[category_metrics["제품 대분류"] == category, "수익_norm"].values[0],
        category_metrics.loc[category_metrics["제품 대분류"] == category, "수량_norm"].values[0],
        category_metrics.loc[category_metrics["제품 대분류"] == category, "할인율_norm"].values[0]
    ]
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=category,
        line_color=colors[i % len(colors)]
    ))

# 레이아웃 설정
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )
    ),
    title="제품 대분류별 성과 비교 (레이더 차트)",
    width=800, 
    height=600
)

fig.show()
```

이 그래프는 레이더 차트(Radar Chart) 또는 거미줄 차트라고 불리는 형태의 시각화입니다. 
원형으로 여러 축이 중심에서 방사형으로 뻗어 있는 모양을 하고 있어요.

레이더 차트의 보는 방법은 다음과 같습니다:

1. **축(Axis)**: 그래프에는 4개의 축이 있습니다
                 - 매출, 수익, 수량, 할인율. 각 축은 중심에서 바깥쪽으로 갈수록 값이 커집니다.

2. **척도**: 각 축의 척도는 0에서 1까지 정규화되어 있습니다. 
             1(바깥쪽)은 해당 지표에서 가장 높은 값을 의미하고, 0(중심)은 가장 낮은 값을 의미합니다.

3. **색상별 선**: 각 색상은 다른 제품 대분류를 나타냅니다:
   - 파란색: 가구
   - 빨간색: 사무기기
   - 초록색: 사무용품

4. **면적**: 각 색상의 면적은 해당 제품 대분류가 4가지 지표에서 차지하는 영역을 보여줍니다. 
             면적이 클수록 전반적인 성과가 좋다고 볼 수 있습니다.

5. **형태**: 라인의 형태가 균형적이면 모든 지표에서 고른 성과를, 
            한쪽으로 치우쳐 있으면 특정 지표에서 강점을 가짐을 나타냅니다.

이 차트를 통해 각 제품 대분류의 성과를 여러 지표에서 한눈에 비교할 수 있으며, 
어떤 제품군이 어떤 지표에서 강점을 보이는지 쉽게 파악할 수 있습니다.

### - 분석 결과 해석

#### ✅ 제품 대분류별 종합 성과 분석
✔ 어떤 제품 대분류가 매출과 수익에서 균형 잡힌 성과를 보이는지 확인 가능
✔ 할인율이 높은 제품군과 낮은 제품군 식별 가능
✔ 단위 수량 대비 매출/수익이 높은 고부가가치 제품군 파악 가능

#### ✅ 강점/약점 분석
✔ 특정 제품군이 매출은 높지만 수익성이 낮은 경우 원가 구조 검토 필요
✔ 수량은 많이 팔리지만 매출 기여도가 낮은 제품군은 가격 전략 재검토 필요
✔ 할인율이 높은데도 판매량이 적은 제품군은 고객 선호도 분석 필요

#### ✅ 제품 포트폴리오 최적화
✔ 모든 지표에서 고른 성과를 보이는 제품군은 투자 확대 검토
✔ 특정 지표에서만 강점을 보이는 제품군은 약점 보완을 위한 전략 수립
✔ 대부분의 지표에서 저조한 성과를 보이는 제품군은 포트폴리오 조정 고려

이 레이더 차트는 "제품 대분류별 성과 비교"를 보여주고 있습니다. 
세 가지 제품 대분류(가구, 사무기기, 사무용품)의 성과를 매출, 수익, 수량, 할인율 네 가지 지표를 기준으로 비교하고 있습니다.
  
■ 주요 해석:

- 사무기기(빨간색):

매출과 수익 측면에서 가장 높은 성과를 보이고 있습니다.
특히 매출에서는 최대치(1.0)에 도달했습니다.
그러나 수량은 상대적으로 낮은 편입니다.


- 사무용품(초록색):

수량과 할인율 측면에서 가장 높은 수치를 보입니다.
이는 많은 수량이 판매되지만 할인율도 높다는 것을 의미합니다.
매출은 세 카테고리 중 가장 낮습니다.


- 가구(파란색):

모든 지표에서 비교적 균형 잡힌 성과를 보입니다.
다른 카테고리에 비해 특별히 두드러지는 지표는 없습니다.
매출은 중간 수준이지만, 수익과 수량은 상대적으로 낮은 편입니다.


- 비즈니스 인사이트:

사무기기는 고가 제품으로 보입니다. 많이 팔리지는 않지만 매출과 수익이 높습니다.
사무용품은 저가 대량판매 모델로 보입니다. 많은 수량이 팔리지만 할인율이 높아 수익성은 낮을 수 있습니다.
가구는 중간 가격대로, 전반적으로 안정적인 성과를 보이고 있습니다.

- 전략적 제안:

사무기기: 이미 높은 매출과 수익을 올리고 있으므로, 판매량을 늘리는 전략이 효과적일 수 있습니다.
사무용품: 할인율을 줄여 수익성을 개선하는 방안을 고려해볼 수 있습니다.
가구: 특별한 강점이 없으므로, 제품 차별화나 타겟 마케팅을 통해 경쟁력을 강화할 필요가 있습니다.

이 차트는 제품 카테고리별 성과를 다각도로 비교할 수 있게 해주어, 
각 제품군의 강점과 약점을 명확히 파악하는 데 도움이 됩니다.

### - 추가 분석 - 제품 대분류별 성과 지표 간 상관관계 분석

레이더 차트를 통해 각 제품군의 성과를 시각적으로 비교할 수 있지만, 
성과 지표 간의 상관관계를 분석하여 더 깊은 인사이트를 얻을 수 있다.

```python
## **예제14.** 레이더 차트 (Radar Chart)

레이더 차트(Radar Chart)는 여러 변수의 값을 다각형 형태로 표현하는 시각화 기법으로, 
다차원 데이터를 한 눈에 비교할 수 있게 해준다. 
이를 활용하면 제품 카테고리별 매출, 수익, 수량과 같은 다양한 지표를 동시에 분석할 수 있다.

### ■ 레이더 차트가 언제 필요한가?
- 여러 카테고리에 대해 다양한 측정값을 동시에 비교할 때 유용하다.
- 각 항목이 여러 측면에서 어떤 성능을 보이는지 파악할 때 효과적이다.
  예: 제품 카테고리별 매출/수익/수량 비교, 지역별 여러 성과 지표 분석, 고객 세그먼트별 다양한 구매 패턴 비교

### ■ 문제: 제품 대분류별 성과는 어떻게 비교되는가?
- 목적:
  - 제품 대분류별 매출, 수익, 수량, 할인율의 상대적 비교
  - 각 제품군의 강점과 약점 식별
  - 균형 잡힌 성과를 보이는 제품군과 특정 지표에서만 높은 성과를 보이는 제품군 구분

### - 데이터 로드 및 Plotly 레이더 차트 생성
```python
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 데이터 로드
df = pd.read_csv("c:\data\SUPERSTORE_2019.csv")

# 제품 대분류별 지표 계산
category_metrics = df.groupby("제품 대분류").agg({
    "매출": "sum",
    "수익": "sum",
    "수량": "sum",
    "할인율": "mean"
}).reset_index()

# 정규화 함수 (0-1 스케일로 변환)
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# 각 지표 정규화
for col in ["매출", "수익", "수량", "할인율"]:
    category_metrics[f"{col}_norm"] = normalize(category_metrics[col])

# 레이더 차트 생성
categories = ["매출", "수익", "수량", "할인율"]
fig = go.Figure()

# 각 제품 대분류별로 레이더 차트에 추가
colors = ['blue', 'red', 'green', 'purple', 'orange']
for i, category in enumerate(category_metrics["제품 대분류"]):
    values = [
        category_metrics.loc[category_metrics["제품 대분류"] == category, "매출_norm"].values[0],
        category_metrics.loc[category_metrics["제품 대분류"] == category, "수익_norm"].values[0],
        category_metrics.loc[category_metrics["제품 대분류"] == category, "수량_norm"].values[0],
        category_metrics.loc[category_metrics["제품 대분류"] == category, "할인율_norm"].values[0]
    ]
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=category,
        line_color=colors[i % len(colors)]
    ))

# 레이아웃 설정
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )
    ),
    title="제품 대분류별 성과 비교 (레이더 차트)",
    width=800, 
    height=600
)

fig.show()
```

### - 분석 결과 해석

#### ✅ 제품 대분류별 종합 성과 분석
✔ 어떤 제품 대분류가 매출과 수익에서 균형 잡힌 성과를 보이는지 확인 가능
✔ 할인율이 높은 제품군과 낮은 제품군 식별 가능
✔ 단위 수량 대비 매출/수익이 높은 고부가가치 제품군 파악 가능

#### ✅ 강점/약점 분석
✔ 특정 제품군이 매출은 높지만 수익성이 낮은 경우 원가 구조 검토 필요
✔ 수량은 많이 팔리지만 매출 기여도가 낮은 제품군은 가격 전략 재검토 필요
✔ 할인율이 높은데도 판매량이 적은 제품군은 고객 선호도 분석 필요

#### ✅ 제품 포트폴리오 최적화
✔ 모든 지표에서 고른 성과를 보이는 제품군은 투자 확대 검토
✔ 특정 지표에서만 강점을 보이는 제품군은 약점 보완을 위한 전략 수립
✔ 대부분의 지표에서 저조한 성과를 보이는 제품군은 포트폴리오 조정 고려

### - 추가 분석 - 제품 대분류별 성과 지표 간 통계적 분석

레이더 차트를 통해 각 제품군의 성과를 시각적으로 비교할 수 있지만, 
성과 지표 간의 통계적 관계를 분석하여 더 깊은 인사이트를 얻을 수 있다.

```python
import pandas as pd
from scipy.stats import pearsonr, f_oneway, kruskal
import numpy as np

# 데이터 로드
df = pd.read_csv("c:\data\SUPERSTORE_2019.csv")

# 제품 대분류별 지표 계산
metrics_by_category = df.groupby("제품 대분류").agg({
    "매출": "sum",
    "수익": "sum",
    "수량": "sum",
    "할인율": "mean"
}).reset_index()

# 제품 대분류별 수익률 계산
metrics_by_category["수익률"] = metrics_by_category["수익"] / metrics_by_category["매출"] * 100

# 1. 상관관계 분석 - 피어슨 상관계수 및 p-value 계산

print("===== 지표 간 상관관계 분석 =====")
metrics = ["매출", "수익", "수량", "할인율"]
correlation_results = {}

for i in range(len(metrics)):
    for j in range(i+1, len(metrics)):
        metric1, metric2 = metrics[i], metrics[j]
        corr, p_value = pearsonr(metrics_by_category[metric1], metrics_by_category[metric2])
        correlation_results[(metric1, metric2)] = (corr, p_value)
        print(f"{metric1}와(과) {metric2} 간의 상관계수: {corr:.4f}, p-value: {p_value:.4f}")
        if p_value < 0.05:
            print(f"  → 통계적으로 유의미한 {corr > 0 and '양' or '음'}의 상관관계가 있습니다.")
        else:
            print(f"  → 통계적으로 유의미한 상관관계가 없습니다.")

# 2. 제품 대분류별 수익률 통계 분석

print("\n===== 제품 대분류별 수익률 통계 =====")
print(metrics_by_category[["제품 대분류", "수익률"]].to_string(index=False))
avg_profit_margin = metrics_by_category["수익률"].mean()
print(f"\n평균 수익률: {avg_profit_margin:.2f}%")
print(f"최대 수익률: {metrics_by_category['수익률'].max():.2f}% ({metrics_by_category.loc[metrics_by_category['수익률'].idxmax(), '제품 대분류']})")
print(f"최소 수익률: {metrics_by_category['수익률'].min():.2f}% ({metrics_by_category.loc[metrics_by_category['수익률'].idxmin(), '제품 대분류']})")
print(f"수익률 표준편차: {metrics_by_category['수익률'].std():.2f}%")

# 3. 제품 대분류별 매출/수익/수량 차이에 대한 가설 검정

print("\n===== 제품 대분류별 매출 차이 가설 검정 =====")
sales_by_category = [df[df["제품 대분류"] == category]["매출"] for category in df["제품 대분류"].unique()]
try:
    # 정규성 가정을 따르는 ANOVA 검정
    anova_result = f_oneway(*sales_by_category)
    print(f"ANOVA 결과: F-statistic = {anova_result.statistic:.4f}, p-value = {anova_result.pvalue:.4f}")
    if anova_result.pvalue < 0.05:
        print("  → 제품 대분류별 매출 차이가 통계적으로 유의미합니다.")
    else:
        print("  → 제품 대분류별 매출 차이가 통계적으로 유의미하지 않습니다.")
    
    # 비모수적 검정 (정규성 가정이 필요 없음)
    kruskal_result = kruskal(*sales_by_category)
    print(f"Kruskal-Wallis 검정 결과: H-statistic = {kruskal_result.statistic:.4f}, p-value = {kruskal_result.pvalue:.4f}")
    if kruskal_result.pvalue < 0.05:
        print("  → 비모수 검정에서도 제품 대분류별 매출 차이가 통계적으로 유의미합니다.")
    else:
        print("  → 비모수 검정에서는 제품 대분류별 매출 차이가 통계적으로 유의미하지 않습니다.")
except:
    print("가설 검정 수행 중 오류가 발생했습니다. 데이터를 확인해주세요.")

# 4. 할인율과 수익률 간의 관계 분석

print("\n===== 할인율과 수익률 간의 관계 분석 =====")
discount_profit_corr, discount_profit_p = pearsonr(metrics_by_category["할인율"], metrics_by_category["수익률"])
print(f"할인율과 수익률 간의 상관계수: {discount_profit_corr:.4f}, p-value: {discount_profit_p:.4f}")
if discount_profit_p < 0.05:
    relation = "양의" if discount_profit_corr > 0 else "음의"
    print(f"  → 할인율과 수익률 간에 통계적으로 유의미한 {relation} 상관관계가 있습니다.")
    if discount_profit_corr < 0:
        print("  → 할인율이 높을수록 수익률이 감소하는 경향이 있습니다.")
    else:
        print("  → 할인율이 높을수록 수익률이 증가하는 경향이 있습니다.")
else:
    print("  → 할인율과 수익률 간에 통계적으로 유의미한 상관관계가 없습니다.")
```

### - 분석 결과 해석

#### ✅ 지표 간 상관관계 분석
✔ 매출과 수익 간의 높은 양의 상관관계 → 대부분의 제품군에서 매출 증가가 수익 증가로 이어짐
✔ 할인율과 수익 간의 부정적 상관관계 → 할인이 수익성을 저하시킬 수 있음
✔ 수량과 매출 간의 상관관계 정도 → 단가가 높은 제품군과 낮은 제품군 식별 가능

#### ✅ 수익률 분석
✔ 평균 수익률보다 높은 제품군 → 고수익 제품군으로 투자 확대 고려
✔ 평균 수익률보다 낮은 제품군 → 원가 구조 및 가격 전략 재검토 필요
✔ 매출은 높지만 수익률이 낮은 제품군 → 판매 전략 최적화 필요

### ■ 결론 및 실행 전략

🚀 레이더 차트를 통해 각 제품 대분류의 종합적인 성과를 한눈에 파악하고, 강점과 약점을 식별할 수 있다.
🚀 균형 잡힌 성과를 보이는 제품군은 투자를 확대하고, 특정 지표에서만 강점을 보이는 제품군은 약점 보완을 위한 전략을 수립한다.
🚀 수익률이 높은 제품군은 마케팅을 강화하고, 수익률이 낮은 제품군은 원가 구조 및 가격 전략을 재검토한다.
🚀 할인율과 수익성 간의 관계를 고려하여 할인 정책을 최적화하고, 고객 가치를 높이는 방향으로 제품 포트폴리오를 조정한다.

레이더 차트를 활용하면 제품 대분류별 다차원 성과를 직관적으로 비교할 수 있으며,
상관관계 분석과 수익률 비교를 통해 더 깊은 인사이트를 얻을 수 있다. 
이를 기반으로 데이터 기반의 최적화된 제품 전략을 수립할 수 있다.
```

### - 분석 결과 해석

#### ✅ 지표 간 상관관계 분석
✔ 매출과 수익 간의 높은 양의 상관관계 → 대부분의 제품군에서 매출 증가가 수익 증가로 이어짐
✔ 할인율과 수익 간의 부정적 상관관계 → 할인이 수익성을 저하시킬 수 있음
✔ 수량과 매출 간의 상관관계 정도 → 단가가 높은 제품군과 낮은 제품군 식별 가능

#### ✅ 수익률 분석
✔ 평균 수익률보다 높은 제품군 → 고수익 제품군으로 투자 확대 고려
✔ 평균 수익률보다 낮은 제품군 → 원가 구조 및 가격 전략 재검토 필요
✔ 매출은 높지만 수익률이 낮은 제품군 → 판매 전략 최적화 필요

### ■ 결론 및 실행 전략

🚀 레이더 차트를 통해 각 제품 대분류의 종합적인 성과를 한눈에 파악하고, 강점과 약점을 식별할 수 있다.
🚀 균형 잡힌 성과를 보이는 제품군은 투자를 확대하고, 특정 지표에서만 강점을 보이는 제품군은 약점 보완을 위한 전략을 수립한다.
🚀 수익률이 높은 제품군은 마케팅을 강화하고, 수익률이 낮은 제품군은 원가 구조 및 가격 전략을 재검토한다.
🚀 할인율과 수익성 간의 관계를 고려하여 할인 정책을 최적화하고, 고객 가치를 높이는 방향으로 제품 포트폴리오를 조정한다.

레이더 차트를 활용하면 제품 대분류별 다차원 성과를 직관적으로 비교할 수 있으며, 
상관관계 분석과 수익률 비교를 통해 더 깊은 인사이트를 얻을 수 있다. 
이를 기반으로 데이터 기반의 최적화된 제품 전략을 수립할 수 있다.
