## **예제17.** 이동 평균선 그래프 (Moving Average Plot)

이동 평균선 그래프(Moving Average Plot)는 시계열 데이터의 단기적 변동성을 줄이고 
장기적 추세를 파악하기 위한 시각화 기법으로,
일정 기간 동안의 데이터를 평균화하여 보다 부드러운 추세선을 생성한다.
이를 통해 매출, 주가, 수요량 등의 시계열 데이터에서 노이즈를 제거하고 실질적인 변화 추세를 식별할 수 있다.

### ■ 이동 평균선 그래프가 언제 필요한가?

- 시계열 데이터의 일시적 변동에 영향받지 않고 중장기적 추세를 파악하고자 할 때 유용하다.
- 시계열 데이터의 계절성과 주기성을 더 명확하게 식별하고자 할 때 효과적이다.
  예: 일일 판매 데이터의 주간 추세 파악, 월별 매출의 분기/반기 추세 확인, 주가 데이터의 장기 동향 분석

### ■ 문제: 일일/주간/월간 매출 추이의 실질적인 변화 패턴은 어떠한가?

- 목적:
  - 단기적 변동성을 제거하고 실질적인 매출 추세 파악
  - 다양한 주기(7일, 30일, 90일)의 이동 평균 비교를 통한 추세 변화 시점 식별
  - 매출 성장과 둔화 구간의 정확한 파악
  - 계절적 변동 패턴 확인 및 장기적 트렌드 예측

### - 데이터 로드 및 Plotly 이동 평균선 그래프 생성

```python
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 데이터 로드
df = pd.read_csv("c:\data\SUPERSTORE_2019.csv")

# 날짜 형식으로 변환
df['주문 일자'] = pd.to_datetime(df['주문 일자'])

# 일별 매출 데이터 생성
daily_sales = df.groupby(pd.Grouper(key='주문 일자', freq='D')).agg({
    '매출': 'sum'
}).reset_index()

# 누락된 날짜 처리 (매출이 0인 날짜 추가)
date_range = pd.date_range(start=daily_sales['주문 일자'].min(), 
                          end=daily_sales['주문 일자'].max(), 
                          freq='D')
daily_sales = daily_sales.set_index('주문 일자').reindex(date_range, fill_value=0).reset_index()
daily_sales = daily_sales.rename(columns={'index': '주문 일자'})

# 이동 평균 계산
daily_sales['MA7'] = daily_sales['매출'].rolling(window=7).mean()  # 7일 이동 평균
daily_sales['MA30'] = daily_sales['매출'].rolling(window=30).mean()  # 30일 이동 평균
daily_sales['MA90'] = daily_sales['매출'].rolling(window=90).mean()  # 90일 이동 평균

# 이동 평균선 그래프 생성
fig = go.Figure()

# 원본 데이터 (회색 라인으로 배경에 표시)
fig.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['매출'],
               mode='lines', name='일별 매출',
               line=dict(color='lightgray', width=1))
)

# 이동 평균선 추가
fig.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['MA7'],
               mode='lines', name='7일 이동 평균',
               line=dict(color='blue', width=2))
)

fig.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['MA30'],
               mode='lines', name='30일 이동 평균',
               line=dict(color='red', width=2))
)

fig.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['MA90'],
               mode='lines', name='90일 이동 평균',
               line=dict(color='green', width=3))
)

# 차트 레이아웃 설정
fig.update_layout(
    title='일별 매출 및 이동 평균선',
    xaxis_title='날짜',
    yaxis_title='매출',
    width=1000,
    height=600,
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.5)')
)

# 연도별 구분선 추가
for year in range(2017, 2020):
    fig.add_vline(x=f"{year}-01-01", line_dash="dash", line_color="gray", opacity=0.7)

fig.show()
```

### - 다양한 이동 평균선의 교차점 분석
```python
# 이동 평균선 교차점 분석을 위한 데이터 준비
# 단기(7일)와 중기(30일) 이동 평균선의 교차 신호 생성
daily_sales['Signal'] = 0
daily_sales.loc[daily_sales['MA7'] > daily_sales['MA30'], 'Signal'] = 1  # 골든 크로스 (상승 추세)
daily_sales.loc[daily_sales['MA7'] < daily_sales['MA30'], 'Signal'] = -1  # 데드 크로스 (하락 추세)

# 교차점 식별 (신호가 변경되는 지점)
daily_sales['SignalChange'] = daily_sales['Signal'].diff()
crossover_points = daily_sales[daily_sales['SignalChange'] != 0].copy()

# 골든 크로스와 데드 크로스 포인트 분리
golden_cross = crossover_points[crossover_points['SignalChange'] > 0]
death_cross = crossover_points[crossover_points['SignalChange'] < 0]

# 교차점 시각화
fig2 = go.Figure()

# 원본 데이터 (회색 라인으로 배경에 표시)
fig2.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['매출'],
               mode='lines', name='일별 매출',
               line=dict(color='lightgray', width=1), opacity=0.5)
)

# 이동 평균선 추가
fig2.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['MA7'],
               mode='lines', name='7일 이동 평균',
               line=dict(color='blue', width=2))
)

fig2.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['MA30'],
               mode='lines', name='30일 이동 평균',
               line=dict(color='red', width=2))
)

# 골든 크로스 포인트 표시
fig2.add_trace(
    go.Scatter(x=golden_cross['주문 일자'], y=golden_cross['MA7'],
               mode='markers', name='골든 크로스 (상승 신호)',
               marker=dict(color='green', size=10, symbol='triangle-up'))
)

# 데드 크로스 포인트 표시
fig2.add_trace(
    go.Scatter(x=death_cross['주문 일자'], y=death_cross['MA7'],
               mode='markers', name='데드 크로스 (하락 신호)',
               marker=dict(color='darkred', size=10, symbol='triangle-down'))
)

# 차트 레이아웃 설정
fig2.update_layout(
    title='이동 평균선 교차점 분석 (골든 크로스 및 데드 크로스)',
    xaxis_title='날짜',
    yaxis_title='매출',
    width=1000,
    height=600,
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.5)')
)

fig2.show()
```

### - 분석 결과 해석

#### ✅ 이동 평균선을 통한 추세 분석
✔ 7일 이동 평균(파란색): 단기 추세를 보여주며, 매출의 주간 변동 패턴을 반영한다.
✔ 30일 이동 평균(빨간색): 중기 추세를 보여주며, 월간 변동성을 부드럽게 처리한다.
✔ 90일 이동 평균(초록색): 장기 추세를 보여주며, 계절적 변동을 넘어선 실질적인 사업 성장 방향을 나타낸다.

#### ✅ 교차점(크로스) 분석
✔ 골든 크로스: 단기 이동 평균이 중/장기 이동 평균을 상향 돌파하는 지점으로, 매출 상승 추세의 시작을 의미한다.
✔ 데드 크로스: 단기 이동 평균이 중/장기 이동 평균을 하향 돌파하는 지점으로, 매출 하락 추세의 시작을 의미한다.
✔ 교차점 빈도: 교차점이 자주 발생하는 기간은 매출 변동성이 큰 시기로, 시장 불안정성을 나타낸다.

#### ✅ 계절적 패턴 식별
✔ 이동 평균선을 통해 연중 특정 시기(예: 연말, 분기말)에 반복되는 매출 상승 패턴을 식별할 수 있다.
✔ 장기 이동 평균선(90일)이 지속적으로 상승하는 구간은 계절적 요인을 넘어선 실질적인 사업 성장을 의미한다.
✔ 짧은 이동 평균선과 긴 이동 평균선 간의 간격이 벌어지는 시기는 추세 강도가 강화되는 시점이다.


이 그래프는 "일별 매출 및 이동 평균선"을 보여주는 시계열 차트입니다. 
2016년 초부터 2019년 말까지의 데이터를 시각화하고 있습니다.

### 그래프 요소 설명:
- **회색 막대**: 일별 매출 데이터
- **파란색 선**: 7일 이동 평균 (단기 추세)
- **빨간색 선**: 30일 이동 평균 (중기 추세)
- **초록색 선**: 90일 이동 평균 (장기 추세)

### 주요 분석:

#### ✅ 전체적인 매출 추세

✔ 2016년부터 2019년까지 전체적으로 상승하는 추세를 보입니다.
✔ 초록색으로 표시된 90일 이동 평균선이 2016년 초 약 1.5M에서 2019년 말 약 4.5M까지 상승하여, 
  약 3배의 성장이 있었음을 알 수 있습니다.
✔ 성장 추세는 완만하지만 꾸준하게 이어져 왔으며, 특히 2019년 후반에 더 가파른 상승세를 보입니다.

#### ✅ 계절적 패턴 분석
    
✔ 매년 반복되는 패턴이 관찰됩니다:
   - 연말(11-12월)과 연초(1월)에 매출이 상승하는 경향
   - 2-3월에는 매출이 다소 하락하는 패턴
   - 여름철(7-8월)에도 매출 상승이 관찰됨
✔ 이러한 계절적 패턴은 30일 이동 평균선(빨간색)에서 더 뚜렷하게 확인할 수 있습니다.

#### ✅ 단기 vs 장기 추세 비교

✔ 7일 이동 평균선(파란색)은 일별 매출의 단기적 변동성을 완화하면서도 주간 단위의 패턴을 보여줍니다.
✔ 30일 이동 평균선(빨간색)은 월간 트렌드를 보여주며, 계절적 패턴이 더 명확히 드러납니다.
✔ 90일 이동 평균선(초록색)은 단기적 변동과 계절성을 평활화하여 장기적인 사업 성장 방향을 보여줍니다.

#### ✅ 주목할 만한 시점

✔ **2018년 7-8월**: 일별 매출과 7일 이동 평균에서 높은 피크가 관찰되며, 이는 특별한 이벤트나 대형 거래가 있었을 가능성을 시사합니다.
✔ **2018-2019년**: 매출의 변동성이 이전 기간보다 커지는 경향을 보이며, 일별 매출의 최고치도 높아졌습니다.
✔ **2019년 하반기**: 모든 이동 평균선이 동시에 상승하는 추세를 보여 확실한 성장기임을 알 수 있습니다.

### 비즈니스 인사이트:

🚀 **매출 계획 수립**: 확인된 계절적 패턴(연말/연초 및 여름철 매출 상승)을 
                       고려한 연간 매출 목표 및 마케팅 계획을 수립해야 합니다.

🚀 **재고 관리 최적화**: 매출이 급증하는 시기에 앞서 적절한 재고를 확보하고, 
                        매출이 둔화되는 시기에는 재고를 줄이는 전략이 필요합니다.

🚀 **성장 전략**: 장기적인 성장 추세를 유지하기 위해 2019년 하반기에 효과적이었던 전략을 분석하고 
                  강화할 필요가 있습니다.

🚀 **변동성 관리**: 매출 변동성이 증가하는 추세에 대응하여, 리스크 관리 및 유연한 운영 체계를 구축해야 합니다.

이동 평균선 분석을 통해 일시적인 매출 변동에 과잉 반응하지 않고, 중장기적 추세에 기반한 전략적 의사결정이 가능합니다.

### - 추가 분석 - 변동성 및 추세 강도 측정

이동 평균 분석의 확장으로, 매출 변동성과 추세 강도를 측정하여 더 깊은 인사이트를 얻을 수 있다.

```python
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 일별 매출 데이터 사용 (앞서 생성한 daily_sales 데이터프레임)

# 1. 볼린저 밴드 계산 (20일 이동 평균 기준)
window = 20
daily_sales['MA20'] = daily_sales['매출'].rolling(window=window).mean()
daily_sales['STD20'] = daily_sales['매출'].rolling(window=window).std()
daily_sales['UpperBand'] = daily_sales['MA20'] + (daily_sales['STD20'] * 2)
daily_sales['LowerBand'] = daily_sales['MA20'] - (daily_sales['STD20'] * 2)

# 2. 변동성 지표 계산 - 상대적 변동폭
daily_sales['Volatility'] = (daily_sales['STD20'] / daily_sales['MA20']) * 100  # 백분율로 표현

# 3. 추세 강도 지표 계산 - MACD 기반
daily_sales['EMA12'] = daily_sales['매출'].ewm(span=12, adjust=False).mean()  # 12일 지수 이동 평균
daily_sales['EMA26'] = daily_sales['매출'].ewm(span=26, adjust=False).mean()  # 26일 지수 이동 평균
daily_sales['MACD'] = daily_sales['EMA12'] - daily_sales['EMA26']  # MACD 라인
daily_sales['Signal'] = daily_sales['MACD'].ewm(span=9, adjust=False).mean()  # 신호선
daily_sales['Histogram'] = daily_sales['MACD'] - daily_sales['Signal']  # 히스토그램

# 볼린저 밴드 및 변동성 시각화
fig3 = make_subplots(rows=2, cols=1, 
                    shared_xaxes=True, 
                    vertical_spacing=0.1, 
                    row_heights=[0.7, 0.3],
                    subplot_titles=('볼린저 밴드 (매출 변동성)', '상대 변동성 (%)'))

# 메인 차트 - 볼린저 밴드
fig3.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['매출'],
              mode='lines', name='일별 매출',
              line=dict(color='gray', width=1)),
    row=1, col=1
)

fig3.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['MA20'],
              mode='lines', name='20일 이동 평균',
              line=dict(color='blue', width=2)),
    row=1, col=1
)

fig3.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['UpperBand'],
              mode='lines', name='상단 밴드 (+2σ)',
              line=dict(color='rgba(0, 128, 0, 0.3)', width=1)),
    row=1, col=1
)

fig3.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['LowerBand'],
              mode='lines', name='하단 밴드 (-2σ)',
              line=dict(color='rgba(255, 0, 0, 0.3)', width=1),
              fill='tonexty', fillcolor='rgba(200, 200, 200, 0.2)'),
    row=1, col=1
)

# 하단 차트 - 변동성 지표
fig3.add_trace(
    go.Scatter(x=daily_sales['주문 일자'], y=daily_sales['Volatility'],
              mode='lines', name='상대 변동성',
              line=dict(color='orange', width=2)),
    row=2, col=1
)

# 차트 레이아웃 설정
fig3.update_layout(
    title='매출 변동성 분석 (볼린저 밴드)',
    xaxis_title='날짜',
    width=1000,
    height=800,
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.5)')
)

fig3.update_yaxes(title_text='매출', row=1, col=1)
fig3.update_yaxes(title_text='변동성 (%)', row=2, col=1)

fig3.show()
```

### - 분석 결과 해석

#### ✅ 볼린저 밴드 분석
✔ 밴드 폭 확대: 밴드가 넓어지는 구간은 매출 변동성이 커지는 시기로, 시장 불확실성이 증가함을 의미한다.
✔ 밴드 폭 축소: 밴드가 좁아지는 구간은 매출 변동성이 줄어드는 시기로, 안정적인 매출 패턴을 나타낸다.
✔ 밴드 돌파: 매출이 상단/하단 밴드를 돌파하는 경우는 비정상적인 매출 변화로, 특별한 이벤트나 시장 변화를 시사한다.

#### ✅ 변동성 지표 분석
✔ 변동성 증가 구간: 시장 불안정성이 커지는 시기로, 리스크 관리가 필요하다.
✔ 변동성 감소 구간: 매출 예측 정확도가 높아지는 시기로, 안정적인 계획 수립이 용이하다.
✔ 변동성 패턴: 특정 시기(예: 홀리데이 시즌)에 반복되는 변동성 패턴은 계절적 요인에 의한 것으로 볼 수 있다.

#### ✅ MACD 분석을 통한 추세 강도 파악
✔ MACD 상향 추세: 상승 모멘텀이 강화되는 시기로, 매출 성장 가속화를 의미한다.
✔ MACD 하향 추세: 하락 모멘텀이 강화되는 시기로, 매출 성장 둔화 또는 감소를 나타낸다.
✔ 히스토그램 폭: 히스토그램 폭이 넓어질수록 현재 추세의 강도가 강함을 의미한다.

제시된 두 그래프는 매출 변동성 분석에 관한 시각화입니다.

### 그래프 1: 매출 변동성 분석 (볼린저 밴드)

이 그래프는 볼린저 밴드를 활용한 매출 변동성 분석을 보여줍니다.

#### 주요 구성요소:
- **회색 막대**: 일별 매출 데이터
- **파란색 선**: 20일 이동 평균선 (추세 파악)
- **초록색 선**: 상단 밴드 (+2σ, 표준편차의 2배 상승)
- **빨간색 선**: 하단 밴드 (-2σ, 표준편차의 2배 하락)
- **주황색 선**: 상대 변동성 (범례에는 없지만 첫 번째 그래프에는 보이지 않음)

#### 분석:

1. **변동폭 확대**: 시간이 지남에 따라 볼린저 밴드의 폭이 확대되는 추세를 보이며,
                   특히 2019년 후반부에 가장 넓어졌습니다. 이는 매출 변동성이 최근으로 올수록 증가했음을 의미합니다.

2. **상단 밴드 돌파**: 여러 시점에서 매출이 상단 밴드를 돌파했는데, 특히 2019년 후반에 더 자주 발생했습니다. 
                      이는 예상보다 높은 비정상적 매출 증가가 있었음을 나타냅니다.

3. **추세 상승**: 20일 이동 평균선(파란색)이 전반적으로 상승 추세를 보이며, 
                 특히 2019년 후반에 더 가파른 상승세를 보입니다.

4. **주기적 패턴**: 매출 데이터에서 규칙적인 주기성이 관찰되며, 
                    이는 계절적 요인이나 사업 주기에 영향을 받는 것으로 보입니다.

### 그래프 2: 상대 변동성 (%)

이 그래프는 시간에 따른 매출의 상대적 변동성을 백분율로 보여줍니다.

#### 분석:
                      
1. **변동성 감소 추세**: 2016년 초 약 250%의 매우 높은 변동성에서 시작하여 시간이 지남에 따라 전반적으로 감소하는 추세를 보입니다. 2019년 말에는 약 70% 수준으로 안정화되었습니다.

2. **주요 변동성 피크**: 
   - 2016년 초: 가장 높은 250%의 변동성
   - 2017년 중반: 약 200%로 다시 급증
   - 2018년 중반: 150% 수준의 변동성 피크
   - 2019년 중반: 약 50%까지 떨어진 후 다시 반등

3. **안정화 패턴**: 2018년 이후로 변동성의 진폭이 작아지고 있어, 비즈니스가 점차 안정화되고 있음을 시사합니다.

### ■ 결론 및 실행 전략

🚀 이동 평균선 분석을 통해 단기 노이즈를 제거하고 실질적인 매출 추세를 파악하여 중장기 전략 수립이 가능하다.
🚀 다양한 주기의 이동 평균선 교차점을 모니터링하여 매출 추세 전환 시점을 조기에 감지하고 대응할 수 있다.
🚀 볼린저 밴드와 변동성 지표를 활용하여 매출의 안정성과 예측 가능성을 평가하고, 이에 맞는 재고 및 인력 계획을 수립한다.
🚀 계절적 패턴과 장기적 추세를 구분하여 일시적인 매출 변동에 과잉 대응하지 않고 장기적인 사업 방향성에 집중한다.
🚀 추세 강도 지표를 활용하여 매출 성장 가속화 시기에 마케팅 및 확장을 강화하고, 둔화 시기에는 비용 효율화에 집중한다.

이동 평균선 그래프는 시계열 데이터의 노이즈를 제거하고 실질적인 추세를 파악하는 강력한 도구로,
단기적 변동에 좌우되지 않고 데이터에 기반한 전략적 의사결정을 가능하게 한다.
다양한 주기의 이동 평균과 파생 지표를 함께 활용하면 더욱 정교한 시장 분석과 예측이 가능하다.
