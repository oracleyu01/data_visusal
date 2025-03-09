## **예제19.** 인터랙티브 그래프 만들기 (Hover, Zoom)

인터랙티브 그래프는 사용자가 마우스 움직임, 클릭, 드래그 등을 통해 데이터와 상호작용할 수 있는 시각화 기법으로,
정적 그래프보다 더 많은 정보를 탐색하고 다양한 관점에서 데이터를 분석할 수 있게 해준다.
이를 활용하면 복잡한 데이터셋을 직관적으로 탐색하고 심층적인 인사이트를 얻을 수 있다.

### ■ 인터랙티브 그래프가 언제 필요한가?

- 다차원 데이터를 다양한 관점에서 탐색해야 할 때 유용하다.
- 사용자가 데이터를 자유롭게 탐색하고 필터링해야 할 때 효과적이다.
  예: 다양한 지표 간 관계 분석, 시계열 데이터의 특정 구간 확대, 세부 정보 확인, 이상치 탐색

### ■ 문제: 어떻게 하면 사용자가 데이터를 더욱 효과적으로 탐색할 수 있을까?

- 목적:
  - 마우스 호버를 통한 데이터 포인트의 상세 정보 제공
  - 확대/축소(Zoom) 기능으로 특정 구간에 집중한 분석 지원
  - 다중 축, 애니메이션 등 고급 인터랙션 구현
  - 필터링과 하이라이팅을 통한 데이터 탐색 촉진

### - 예제 1: 호버 정보가 포함된 산점도

이 예제에서는 제품 대분류 및 중분류별 매출과 수익의 관계를 산점도로 표현하고, 마우스 호버 기능을 통해 상세 정보를 제공합니다.

```python
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")

# 데이터 전처리 및 제품 중분류별 집계
grouped_df = df.groupby(["제품 대분류", "제품 중분류"]).agg({
    "매출": "sum",
    "수익": "sum",
    "수량": "sum"
}).reset_index()

# 수익률 미리 계산
grouped_df["수익률"] = (grouped_df["수익"] / grouped_df["매출"]) * 100

# 호버 정보가 포함된 산점도 생성
scatter_fig = px.scatter(
    grouped_df,
    x="매출",
    y="수익",
    size="수량",
    color="제품 대분류",
    hover_name="제품 중분류",
    hover_data={
        "매출": ":,.0f",  # 천 단위 구분 기호와 소수점 없음
        "수익": ":,.0f",
        "수량": True,
        "수익률": ":.2f"  # 미리 계산된 수익률 사용
    },
    title="제품 대분류/중분류별 매출-수익 관계 (호버로 세부 정보 확인)",
    labels={"매출": "총 매출 (원)", "수익": "총 수익 (원)", "수량": "판매 수량", "수익률": "수익률 (%)"}
)

# 호버 템플릿 사용자 정의
scatter_fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>" + 
                "매출: %{customdata[0]}<br>" +
                "수익: %{customdata[1]}<br>" +
                "수량: %{customdata[2]}<br>" +
                "수익률: %{customdata[3]}%<extra></extra>"
)

# 레이아웃 설정
scatter_fig.update_layout(
    width=900, 
    height=600,
    hovermode="closest",  # 가장 가까운 점의 정보 표시
    xaxis_title="총 매출 (원)",
    yaxis_title="총 수익 (원)",
    legend_title="제품 대분류"
)

scatter_fig.show()
```

#### ✅ 산점도 호버 기능 분석 결과

✔ 각 점이 제품 중분류를 나타내며, 마우스를 가져가면 상세 정보가 표시됩니다.
✔ 점 크기는 판매 수량에 비례하며, 색상은 제품 대분류를 구분합니다.
✔ 수익률 정보를 호버에 추가하여 수익성 분석이 용이합니다.
✔ 이상치나 성과가 특히 좋은 제품군을 빠르게 식별할 수 있습니다.

### - 예제 2: 확대/축소 기능이 있는 시계열 그래프

이 예제에서는 시간에 따른 매출 추이를 시각화하고, 확대/축소 기능을 통해 특정 기간을 자세히 분석할 수 있습니다.

```python
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")
df['주문 일자'] = pd.to_datetime(df['주문 일자'])

# 월별 제품 대분류별 매출 집계
time_series = df.groupby([pd.Grouper(key='주문 일자', freq='M'), '제품 대분류']).agg({
    '매출': 'sum'
}).reset_index()

# 확대/축소 기능이 있는 시계열 그래프 생성
time_fig = px.line(
    time_series,
    x='주문 일자',
    y='매출',
    color='제품 대분류',
    title='월별 제품 대분류별 매출 추이 (드래그로 구간 확대)',
    labels={'주문 일자': '날짜', '매출': '매출액', '제품 대분류': '제품 카테고리'}
)

# 확대/축소 기능 및 호버 모드 설정
time_fig.update_layout(
    width=900,
    height=600,
    hovermode="x unified",  # x축 기준으로 모든 라인의 값 표시
    xaxis=dict(
        rangeslider=dict(visible=True),  # 하단에 범위 슬라이더 추가
        type='date'
    ),
    xaxis_title="날짜",
    yaxis_title="매출액 (원)",
    legend_title="제품 대분류"
)

time_fig.show()
```

#### ✅ 시계열 확대/축소 분석 결과

✔ 시간 범위 슬라이더를 통해 전체 추세를 유지하면서 특정 기간 확대 가능합니다.
✔ 드래그하여 특정 구간을 선택하면 자동으로 확대되어 세부 패턴을 분석할 수 있습니다.
✔ 범례 클릭으로 특정 제품군만 선택적으로 표시하여 비교 분석이 가능합니다.
✔ x축 기준 통합 호버 모드로 특정 시점의 모든 제품군 매출을 동시에 비교할 수 있습니다.

### - 예제 3: 다중 축과 인터랙션 기능을 갖춘 복합 그래프
이 예제에서는 서로 다른 단위를 가진 여러 지표(매출, 수익, 할인율)를 하나의 그래프에 표시하고, 다양한 인터랙션 기능을 제공합니다.

```python
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")
df['주문 일자'] = pd.to_datetime(df['주문 일자'])

# 월별 지표 집계
monthly_metrics = df.groupby(pd.Grouper(key='주문 일자', freq='M')).agg({
    '매출': 'sum',
    '수익': 'sum',
    '할인율': 'mean'
}).reset_index()

# 다중 축 그래프 생성
multi_fig = make_subplots(specs=[[{"secondary_y": True}]])

# 매출 데이터 추가 (좌측 y축)
multi_fig.add_trace(
    go.Scatter(
        x=monthly_metrics['주문 일자'],
        y=monthly_metrics['매출'],
        name="매출",
        line=dict(color='blue', width=2),
        hovertemplate="날짜: %{x}<br>매출: %{y:,.0f}원<extra></extra>"
    ),
    secondary_y=False
)

# 수익 데이터 추가 (좌측 y축)
multi_fig.add_trace(
    go.Scatter(
        x=monthly_metrics['주문 일자'],
        y=monthly_metrics['수익'],
        name="수익",
        line=dict(color='green', width=2),
        hovertemplate="날짜: %{x}<br>수익: %{y:,.0f}원<extra></extra>"
    ),
    secondary_y=False
)

# 할인율 데이터 추가 (우측 y축)
multi_fig.add_trace(
    go.Scatter(
        x=monthly_metrics['주문 일자'],
        y=monthly_metrics['할인율'] * 100,  # 퍼센트로 변환
        name="평균 할인율",
        line=dict(color='red', width=2, dash='dot'),
        hovertemplate="날짜: %{x}<br>할인율: %{y:.2f}%<extra></extra>"
    ),
    secondary_y=True
)

# 축 제목 설정
multi_fig.update_xaxes(title_text="날짜")
multi_fig.update_yaxes(title_text="금액 (원)", secondary_y=False)
multi_fig.update_yaxes(title_text="할인율 (%)", secondary_y=True)

# 레이아웃 설정
multi_fig.update_layout(
    title="월별 매출, 수익, 할인율 추이 (다중 축)",
    width=900,
    height=600,
    hovermode="x unified",  # x축 기준으로 모든 라인의 값 표시
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

multi_fig.show()
```

#### ✅ 다중 축 그래프 분석 결과

✔ 단위가 다른 매출/수익(원)과 할인율(%)을 하나의 그래프로 효과적으로 비교할 수 있습니다.
✔ x축 기준 통합 호버는 특정 시점의 모든 지표 값을 동시에 확인할 수 있게 합니다.
✔ 매출과 수익의 추세를 할인율 변화와 함께 분석하여 할인 전략의 효과를 평가할 수 있습니다.
✔ 수평 배치된 범례를 통해 그래프 영역을 최대화하면서도 쉽게 지표를 선택할 수 있습니다.

### - 예제 4: 애니메이션과 드롭다운 필터가 있는 바 차트

이 예제에서는 시간에 따른 지역별 매출 변화를 애니메이션으로 표현하고, 드롭다운 필터를 통해 데이터를 선택적으로 표시합니다.

```python
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")
df['주문 일자'] = pd.to_datetime(df['주문 일자'])

# 분기별 데이터 추가
df['분기'] = pd.PeriodIndex(df['주문 일자'], freq='Q').astype(str)
df['연도'] = df['주문 일자'].dt.year

# 지역별, 분기별 매출 집계
region_sales = df.groupby(['지역', '분기']).agg({
    '매출': 'sum'
}).reset_index()

# 애니메이션이 있는 바 차트 생성
animation_fig = px.bar(
    region_sales,
    x='지역', 
    y='매출',
    color='지역',
    animation_frame='분기',  # 애니메이션 프레임으로 분기 설정
    animation_group='지역',
    range_y=[0, region_sales['매출'].max() * 1.1],
    title='분기별 지역 매출 추이 (애니메이션)',
    labels={'매출': '매출액 (원)', '지역': '지역명', '분기': '분기'},
    color_discrete_sequence=px.colors.qualitative.Bold  # 색상 팔레트 설정
)

# 애니메이션 및 레이아웃 설정
animation_fig.update_layout(
    width=900,
    height=600,
    xaxis_title="지역",
    yaxis_title="매출액 (원)",
    # 애니메이션 컨트롤 설정
    updatemenus=[
        dict(
            type="buttons",
            buttons=[
                dict(label="재생",
                     method="animate",
                     args=[None, {"frame": {"duration": 800, "redraw": True}, "fromcurrent": True}]),
                dict(label="일시정지",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}])
            ],
            direction="left",
            pad={"r": 10, "t": 10},
            showactive=False,
            x=0.1,
            xanchor="right",
            y=0,
            yanchor="top"
        )
    ]
)

# 호버 템플릿 사용자 정의
animation_fig.update_traces(
    hovertemplate="지역: %{x}<br>매출액: %{y:,.0f}원<br>분기: %{customdata[0]}<extra></extra>",
    customdata=region_sales[['분기']]
)

animation_fig.show()
```

#### ✅ 애니메이션 바 차트 분석 결과

✔ 분기별 지역 매출 변화를 애니메이션으로 직관적으로 파악할 수 있습니다.
✔ 재생/일시정지 버튼으로 애니메이션을 제어할 수 있습니다.
✔ 특정 분기에서 매출이 급증하거나 감소하는 지역을 시각적으로 빠르게 식별할 수 있습니다.
✔ 사용자 정의 호버 템플릿으로 각 막대에 대한 상세 정보를 제공합니다.

### ■ 결론 및 실행 전략

🚀 **데이터 탐색 효율화**: 인터랙티브 그래프를 통해 데이터 탐색 과정의 효율성을 높이고, 다양한 각도에서 신속하게 인사이트를 발견한다.

🚀 **사용자 경험 개선**: 호버, 확대/축소, 애니메이션 등의 인터랙션 요소를 통해 사용자 친화적인 데이터 분석 환경을 구축한다.

🚀 **다차원 데이터 분석**: 다중 축, 복합 그래프를 활용하여 여러 변수 간의 관계를 동시에 분석하고 포괄적인 인사이트를 얻는다.

🚀 **시간적 패턴 파악**: 애니메이션과 시계열 확대/축소 기능을 통해 시간에 따른 변화 패턴을 효과적으로 분석한다.

🚀 **이상치 및 특이점 발견**: 호버 정보와 상세 데이터 탐색을 통해 일반적인 패턴에서 벗어난 데이터 포인트를 신속하게 발견하고 원인을 분석한다.

인터랙티브 그래프는 정적 시각화의 한계를 넘어, 사용자가 데이터와 능동적으로 상호작용할 수 있는 환경을 제공한다.
Plotly와 같은 현대적인 시각화 라이브러리를 활용하면 웹 기반의 인터랙티브 요소를 손쉽게 구현할 수 있어, 
더 풍부하고 직관적인 데이터 탐색 경험을 제공할 수 있다.
특히 복잡한 비즈니스 데이터를 분석할 때 인터랙티브 그래프의 활용은 숨겨진 패턴과 인사이트를 발견하는 데 큰 도움이 된다.
