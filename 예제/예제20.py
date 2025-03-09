## **예제20.** Dash를 활용한 웹 대시보드

Dash는 Python으로 웹 기반 대시보드를 구축할 수 있는 프레임워크로,
Plotly 그래프와 HTML 컴포넌트를 조합하여 인터랙티브한 데이터 시각화 애플리케이션을 만들 수 있다.
이를 활용하면 데이터 분석 결과를 웹 기반으로 공유하고 사용자가 직접 데이터를 탐색할 수 있는 환경을 제공할 수 있다.

### ■ Dash 대시보드가 언제 필요한가?

- 여러 이해관계자에게 데이터 분석 결과를 공유해야 할 때 유용하다.
- 사용자가 직접 데이터를 필터링하고 다양한 관점에서 탐색해야 할 때 효과적이다.
  예: 판매 성과 대시보드, 마케팅 캠페인 모니터링, 실시간 데이터 추적, 비즈니스 KPI 시각화

### ■ 문제: 어떻게 하면 데이터 분석 결과를 효과적으로 공유하고 사용자 상호작용을 지원할 수 있을까?

- 목적:
  - 주요 비즈니스 지표를 한눈에 볼 수 있는 대시보드 구축
  - 사용자가 데이터를 필터링하고 세부 정보를 탐색할 수 있는 기능 구현
  - 다양한 시각화 요소를 통합하여 종합적인 인사이트 제공
  - 웹 기반으로 누구나 접근하고 활용할 수 있는 환경 구축

### - Dash 설치 및 기본 구조
Dash를 사용하기 위해서는 먼저 필요한 패키지를 설치해야 합니다.

```bash
pip install dash dash-bootstrap-components pandas plotly
```

Dash 애플리케이션의 기본 구조는 다음과 같습니다:

```python
# 기본 구조 예시
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Dash 애플리케이션 초기화
app = dash.Dash(__name__)

# 레이아웃 정의 (HTML 및 Dash 컴포넌트로 구성)
app.layout = html.Div([
    # 대시보드 내용
])

# 콜백 함수 정의 (상호작용 처리)
@app.callback(
    Output('output-component-id', 'property'),
    [Input('input-component-id', 'property')]
)
def update_output(input_value):
    # 데이터 처리 및 출력 업데이트
    return output_value

# 서버 실행
if __name__ == '__main__':
    app.run_server(debug=True)
```

### - 슈퍼스토어 데이터 대시보드 구현
이제 슈퍼스토어 데이터를 활용하여 실제 대시보드를 구현해 보겠습니다.

```python
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import numpy as np

# 데이터 로드
df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")
df['주문 일자'] = pd.to_datetime(df['주문 일자'])
df['연도'] = df['주문 일자'].dt.year
df['월'] = df['주문 일자'].dt.month
df['분기'] = df['주문 일자'].dt.quarter

# Dash 애플리케이션 초기화 (Bootstrap 테마 적용)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 앱 제목 설정
app.title = "슈퍼스토어 매출 대시보드"

# 대시보드 레이아웃 구성
app.layout = dbc.Container([
    # 헤더 섹션
    dbc.Row([
        dbc.Col(html.H1("슈퍼스토어 매출 대시보드", className="text-center p-3 mb-2 bg-primary text-white"), width=12)
    ]),
    
    # 필터 섹션
    dbc.Row([
        # 기간 선택
        dbc.Col([
            html.Label("기간 선택:"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['주문 일자'].min(),
                end_date=df['주문 일자'].max(),
                max_date_allowed=df['주문 일자'].max(),
                className="mb-3"
            )
        ], width=4),
        
        # 제품 대분류 선택
        dbc.Col([
            html.Label("제품 대분류:"),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': cat, 'value': cat} for cat in df['제품 대분류'].unique()],
                value=df['제품 대분류'].unique().tolist(),
                multi=True,
                className="mb-3"
            )
        ], width=4),
        
        # 지역 선택
        dbc.Col([
            html.Label("지역:"),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': region, 'value': region} for region in df['지역'].unique()],
                value=df['지역'].unique().tolist(),
                multi=True,
                className="mb-3"
            )
        ], width=4)
    ], className="mb-4"),
    
    # KPI 카드 섹션
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("총 매출", className="card-title"),
                html.H2(id="total-sales", className="card-text text-primary")
            ])
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("총 수익", className="card-title"),
                html.H2(id="total-profit", className="card-text text-success")
            ])
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("평균 수익률", className="card-title"),
                html.H2(id="profit-margin", className="card-text text-info")
            ])
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("주문 건수", className="card-title"),
                html.H2(id="order-count", className="card-text text-warning")
            ])
        ]), width=3)
    ], className="mb-4"),
    
    # 그래프 섹션 - 첫 번째 줄
    dbc.Row([
        # 월별 매출 추이 그래프
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("월별 매출 및 수익 추이"),
                dbc.CardBody(dcc.Graph(id="monthly-trend"))
            ])
        ], width=8),
        
        # 제품 대분류별 매출 비중 파이 차트
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("제품 대분류별 매출 비중"),
                dbc.CardBody(dcc.Graph(id="category-pie"))
            ])
        ], width=4)
    ], className="mb-4"),
    
    # 그래프 섹션 - 두 번째 줄
    dbc.Row([
        # 지역별 매출 막대 그래프
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("지역별 매출"),
                dbc.CardBody(dcc.Graph(id="region-bar"))
            ])
        ], width=6),
        
        # 제품 대분류별 수익률 막대 그래프
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("제품 대분류별 수익률"),
                dbc.CardBody(dcc.Graph(id="category-profit-margin"))
            ])
        ], width=6)
    ], className="mb-4"),
    
    # 데이터 테이블 섹션
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("상위 판매 제품"),
                dbc.CardBody(
                    dash_table.DataTable(
                        id='top-products-table',
                        columns=[
                            {"name": "제품 대분류", "id": "제품 대분류"},
                            {"name": "제품 중분류", "id": "제품 중분류"},
                            {"name": "제품명", "id": "제품명"},
                            {"name": "매출", "id": "매출", "type": "numeric", "format": {"specifier": ",.0f"}},
                            {"name": "수익", "id": "수익", "type": "numeric", "format": {"specifier": ",.0f"}},
                            {"name": "수익률", "id": "수익률", "type": "numeric", "format": {"specifier": ".2%"}}
                        ],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left'},
                        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                        style_data_conditional=[
                            {
                                'if': {'filter_query': '{수익률} < 0', 'column_id': '수익률'},
                                'backgroundColor': '#FFCDD2',
                                'color': 'red'
                            },
                            {
                                'if': {'filter_query': '{수익률} > 0.2', 'column_id': '수익률'},
                                'backgroundColor': '#C8E6C9',
                                'color': 'green'
                            }
                        ],
                        page_size=10
                    )
                )
            ])
        ], width=12)
    ])
], fluid=True)

# 콜백 함수 정의 - 필터링된 데이터 생성
@app.callback(
    [Output("total-sales", "children"),
     Output("total-profit", "children"),
     Output("profit-margin", "children"),
     Output("order-count", "children"),
     Output("monthly-trend", "figure"),
     Output("category-pie", "figure"),
     Output("region-bar", "figure"),
     Output("category-profit-margin", "figure"),
     Output("top-products-table", "data")],
    [Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("category-filter", "value"),
     Input("region-filter", "value")]
)
def update_dashboard(start_date, end_date, selected_categories, selected_regions):
    # 데이터 필터링
    filtered_df = df[
        (df['주문 일자'] >= start_date) &
        (df['주문 일자'] <= end_date) &
        (df['제품 대분류'].isin(selected_categories)) &
        (df['지역'].isin(selected_regions))
    ]
    
    if filtered_df.empty:
        # 필터링된 데이터가 없는 경우 기본값 반환
        return (
            "데이터 없음", "데이터 없음", "데이터 없음", "데이터 없음",
            px.line(title="데이터가 없습니다"),
            px.pie(title="데이터가 없습니다"),
            px.bar(title="데이터가 없습니다"),
            px.bar(title="데이터가 없습니다"),
            []
        )
    
    # KPI 계산
    total_sales = filtered_df['매출'].sum()
    total_profit = filtered_df['수익'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    order_count = filtered_df['주문 번호'].nunique()
    
    # 1. 월별 매출 및 수익 추이 그래프
    monthly_data = filtered_df.groupby(pd.Grouper(key='주문 일자', freq='M')).agg({
        '매출': 'sum',
        '수익': 'sum'
    }).reset_index()
    
    monthly_fig = go.Figure()
    monthly_fig.add_trace(go.Scatter(
        x=monthly_data['주문 일자'], 
        y=monthly_data['매출'],
        name='매출',
        line=dict(color='royalblue', width=2)
    ))
    monthly_fig.add_trace(go.Scatter(
        x=monthly_data['주문 일자'], 
        y=monthly_data['수익'],
        name='수익',
        line=dict(color='green', width=2)
    ))
    monthly_fig.update_layout(
        xaxis_title='날짜',
        yaxis_title='금액',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode="x unified"
    )
    
    # 2. 제품 대분류별 매출 비중 파이 차트
    category_data = filtered_df.groupby('제품 대분류').agg({
        '매출': 'sum'
    }).reset_index()
    
    pie_fig = px.pie(
        category_data, 
        values='매출', 
        names='제품 대분류',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    pie_fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1)
    )
    
    # 3. 지역별 매출 막대 그래프
    region_data = filtered_df.groupby('지역').agg({
        '매출': 'sum'
    }).reset_index().sort_values('매출', ascending=False)
    
    region_fig = px.bar(
        region_data,
        x='지역',
        y='매출',
        color='지역',
        text='매출',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    region_fig.update_layout(
        xaxis_title='지역',
        yaxis_title='매출',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    region_fig.update_traces(
        texttemplate='%{y:,.0f}',
        textposition='outside'
    )
    
    # 4. 제품 대분류별 수익률 막대 그래프
    category_profit_data = filtered_df.groupby('제품 대분류').agg({
        '매출': 'sum',
        '수익': 'sum'
    }).reset_index()
    category_profit_data['수익률'] = (category_profit_data['수익'] / category_profit_data['매출']) * 100
    category_profit_data = category_profit_data.sort_values('수익률', ascending=False)
    
    profit_margin_fig = px.bar(
        category_profit_data,
        x='제품 대분류',
        y='수익률',
        color='수익률',
        text='수익률',
        color_continuous_scale='RdYlGn'
    )
    profit_margin_fig.update_layout(
        xaxis_title='제품 대분류',
        yaxis_title='수익률 (%)',
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    profit_margin_fig.update_traces(
        texttemplate='%{y:.1f}%',
        textposition='outside'
    )
    
    # 5. 상위 판매 제품 테이블
    product_data = filtered_df.groupby(['제품 대분류', '제품 중분류', '제품명']).agg({
        '매출': 'sum',
        '수익': 'sum'
    }).reset_index()
    product_data['수익률'] = product_data['수익'] / product_data['매출']
    top_products = product_data.sort_values('매출', ascending=False).head(10)
    
    # 결과 반환
    return (
        f"₩{total_sales:,.0f}",
        f"₩{total_profit:,.0f}",
        f"{profit_margin:.1f}%",
        f"{order_count:,}",
        monthly_fig,
        pie_fig,
        region_fig,
        profit_margin_fig,
        top_products.to_dict('records')
    )

# 서버 실행
if __name__ == '__main__':
    app.run_server(debug=True)
```

### - 분석 결과 해석

#### ✅ 대시보드의 주요 구성 요소 및 기능
✔ **필터링 기능**: 기간, 제품 대분류, 지역 등을 선택하여 원하는 데이터만 분석 가능
✔ **KPI 카드**: 총 매출, 총 수익, 평균 수익률, 주문 건수 등 핵심 지표를 한눈에 확인 가능
✔ **시계열 분석**: 월별 매출 및 수익 추이를 통해 시간에 따른 비즈니스 성과 변화 파악
✔ **비중 분석**: 제품 대분류별 매출 비중을 통해 중요 제품군 식별
✔ **지역별 성과**: 지역별 매출 비교를 통해 핵심 시장 및 성장 기회 파악
✔ **수익성 분석**: 제품 대분류별 수익률 비교를 통해 고수익 및 저수익 제품군 식별
✔ **상세 데이터**: 상위 판매 제품 테이블을 통해 세부 정보 확인 및 조치 사항 도출

#### ✅ 대시보드를 통한 비즈니스 인사이트
✔ **제품 포트폴리오 최적화**: 매출 비중 및 수익률 분석을 통해 제품 포트폴리오 조정 가능
✔ **지역 타겟팅**: 지역별 성과 비교를 통해 효과적인 지역 마케팅 전략 수립 가능
✔ **시즌별 전략**: 시간에 따른 매출 변화 패턴을 분석하여 시즌별 프로모션 계획 수립 가능
✔ **수익성 개선**: 수익률이 낮은 제품군 및 지역에 대한 가격 전략 및 비용 구조 재검토 가능

### - Dash 대시보드의 배포 및 공유 방법

웹 기반 대시보드를 팀원 및 이해관계자와 공유하는 방법에는 여러 가지가 있습니다.

```python
# 로컬 네트워크에서 공유하는 경우
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
```

클라우드 플랫폼을 통한 배포:
- Heroku: 무료 티어로 시작 가능한 PaaS 플랫폼
- AWS Elastic Beanstalk: 확장성과 안정성이 우수한 서비스
- Google Cloud Run: 컨테이너 기반 배포를 지원하는 서비스
- Dash Enterprise: Plotly에서 제공하는 엔터프라이즈급 호스팅 및 관리 서비스

### ■ 결론 및 실행 전략

🚀 **데이터 기반 의사결정 강화**: Dash 대시보드를 통해 모든 이해관계자가 데이터에 접근하고 분석할 수 있는 환경을 구축한다.

🚀 **사용자 경험 최적화**: 직관적인 UI/UX와 필터링 기능을 통해 기술적 배경이 없는 사용자도 쉽게 데이터를 탐색할 수 있도록 한다.

🚀 **대시보드 커스터마이징**: 사용자의 피드백을 반영하여 지속적으로 대시보드를 개선하고, 필요에 따라 새로운 시각화 요소나 기능을 추가한다.

🚀 **자동화 및 실시간 업데이트**: 데이터 소스와의 연결을 자동화하여 최신 데이터가 실시간으로 반영되는 시스템을 구축한다.

🚀 **확장성 고려**: 데이터 양이 증가하거나 사용자가 늘어나는 경우를 대비하여 확장 가능한 아키텍처로 설계한다.

Dash를 활용한 웹 대시보드는 데이터 분석 결과를 효과적으로 공유하고 조직 전체가 데이터 기반 문화를 형성하는 데 큰 도움을 준다.
특히 Python을 기반으로 하기 때문에 데이터 과학자나 분석가가 별도의 웹 개발 지식 없이도 전문적인 대시보드를 구축할 수 있어 효율적이다.
필터링, 드릴다운, 인터랙티브 그래프 등 다양한 기능을 활용하여 사용자가 능동적으로 데이터를 탐색하고 인사이트를 얻을 수 있는 환경을 제공한다.
