
▣ 예제1. 선 그래프 (Line Plot)

■ 1. line 그래프가 언제 필요한지?

   - 시간에 따른 변화(trend)를 분석할 때 사용
   - 주가, 기온, 판매량 등 시계열 데이터 표현에 적합
   - 연속적인 데이터 포인트를 연결하여 패턴을 쉽게 파악할 수 있음

■ 2. plotly 로 선 그래프 그리는 파이썬 예제

import pandas as pd
import plotly.graph_objects as go

# 데이터 로드
df = pd.read_csv('d:\\data\\SUPERSTORE_2019.csv')

# 월별 매출 계산
df['주문 일자'] = pd.to_datetime(df['주문 일자'])
df['월'] = df['주문 일자'].dt.strftime('%Y-%m')
월별매출 = df.groupby('월')['매출'].sum().reset_index()

# 라인 그래프 생성
fig = go.Figure(data=[go.Scatter(x=월별매출['월'], y=월별매출['매출'])])

# 레이아웃 설정
fig.update_layout(title='월별 매출 추이',
                  xaxis_title='월',
                  yaxis_title='매출')

# 그래프 표시
fig.show()

■ 3. 문제를 풀면서 예제 익히기


문제1: 2019년 월별 총 매출 추이는 어떻게 되나요?

목적: 전체 매출의 시간적 패턴을 파악하여 성수기와 비수기를 식별하고, 
      매출이 증가하거나 감소하는 트렌드를 발견할 수 있습니다. 
      이를 통해 계절적 변동성을 분석하고 향후 영업 계획 수립에 활용할 수 있습니다.

답:
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# 데이터 로드
df = pd.read_csv('d:\\data\\SUPERSTORE_2019.csv', encoding='utf-8')

# 날짜 컬럼 변환
df['주문 일자'] = pd.to_datetime(df['주문 일자'])
df['배송 일자'] = pd.to_datetime(df['배송 일자'])

# 년, 월, 분기 컬럼 추가
df['월'] = df['주문 일자'].dt.month
df['분기'] = df['주문 일자'].dt.quarter
df['연월'] = df['주문 일자'].dt.strftime('%Y-%m')

# 월별 총 매출 집계
monthly_sales = df.groupby('월')['매출'].sum().reset_index()

# 라인 그래프 생성
fig = px.line(monthly_sales, x='월', y='매출', 
              title='2019년 월별 총 매출 추이',
              labels={'월': '월', '매출': '총 매출액'},
              markers=True)

fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
fig.show()


2019년 월별 총 매출 추이 그래프를 해석해 드리겠습니다:

이 그래프는 2019년 1월부터 12월까지의 월별 총 매출을 보여주고 있습니다. 
Y축은 매출액을 나타내며 단위는 백만(M)이고, X축은 1월부터 12월까지의 월을 나타냅니다.

주요 트렌드 및 패턴:

**종합 분석**:
   
- 전반적으로 2019년은 상반기보다 하반기 매출이 더 높은 경향을 보였습니다.
- 큰 폭의 변동이 있으며, 특히 7월의 급격한 하락이 주목됩니다.
- 연중 최저 매출은 4월, 최고 매출은 10월에 기록되었습니다.
- 연말(10-12월)은 매출이 높고 안정적인 패턴을 보였습니다.
- 4, 7월은 다른 달에 비해 매출이 크게 감소한 시기로, 계절적 요인이나 특별한 이벤트가 있었을 수 있습니다.

이러한 패턴은 비즈니스의 계절성, 프로모션 기간, 또는 다른 외부 요인들에 의해 영향받았을 가능성이 있습니다.

문제2: 제품 대분류별 월간 매출 추이를 비교해 볼 수 있을까요?

목적: 여러 제품 카테고리 간의 매출 성과를 비교하여 어떤 카테고리가 특정 시기에 더 잘 팔리는지 파악할 수 있습니다.
      이를 통해 인벤토리 관리와 마케팅 전략을 카테고리별로 최적화할 수 있습니다.

#답:

# 제품 대분류별, 월별 매출 집계
category_monthly_sales = df.groupby(['제품 대분류', '월'])['매출'].sum().reset_index()

# 라인 그래프 생성
fig = px.line(category_monthly_sales, x='월', y='매출', color='제품 대분류',
              title='2019년 제품 대분류별 월간 매출 추이',
              labels={'월': '월', '매출': '매출액', '제품 대분류': '제품 대분류'},
              markers=True)

fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
fig.show()


전체적인 패턴:

모든 카테고리가 7월에 뚜렷한 하락을 보이는데, 이는 계절적 요인이나 특정 이벤트로 인한 것일 수 있습니다.
5월부터 상승 추세가 시작되어 6월에 첫 번째 피크를 보입니다.
8월부터 10월까지 다시 상승세를 보입니다.
가구와 사무기기는 유사한 패턴을 보이는 반면, 사무용품은 더 완만하고 꾸준한 성장 패턴을 보입니다.
이 그래프는 각 제품 대분류의 계절적 패턴을 보여주며, 특히 가구와 사무기기가 유사한 고객 수요 패턴을 가지고 있음을 시사합니다.
반면 사무용품은 보다 일관된 수요를 가지고 있어 연말로 갈수록 꾸준히 성장하는 모습을 보입니다.




