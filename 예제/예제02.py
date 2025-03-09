### **예제2. 막대 그래프 (Bar Plot)**

### **1. 막대 그래프가 언제 필요한가?**  
# ✅ 카테고리별 비교 분석을 할 때 유용함.  
# ✅ 특정 값(예: 매출, 수익, 주문 수)을 그룹별로 시각적으로 비교할 때 효과적.  
# ✅ 지역별 매출, 제품 카테고리별 수익, 고객 세그먼트별 주문량 등 비교 데이터를 쉽게 해석할 수 있음.  

import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv('/mnt/data/SUPERSTORE_2019.csv')

# 월별 매출 계산
df['주문 일자'] = pd.to_datetime(df['주문 일자'])
df['월'] = df['주문 일자'].dt.strftime('%Y-%m')
월별매출 = df.groupby('월')['매출'].sum().reset_index()

# 막대 그래프 생성
fig = px.bar(월별매출, x='월', y='매출', 
             title='월별 매출 비교', 
             labels={'월': '월', '매출': '매출액'},
             text=월별매출['매출'].round(2))

# 그래프 스타일 업데이트
fig.update_traces(textposition='outside')  # 막대 위에 값 표시
fig.show()

### **📌 막대 그래프 vs 선 그래프 차이점**
# | 그래프 유형 | 사용 목적 |
# |---|---|
# | **선 그래프 (Line Plot)** | 시간의 흐름에 따른 데이터 변화를 분석하는 데 적합 (예: 주가, 기온, 트렌드 분석) |
# | **막대 그래프 (Bar Plot)** | 특정 그룹(카테고리) 간 데이터를 비교하는 데 적합 (예: 지역별 매출, 제품별 판매량) |

### **🧐 추가 연습 문제**
질문 1: 2019년 월별 총 매출은 어떻게 변하는가?

🔎 목적:

연간 매출 패턴을 분석하여 성수기와 비수기를 파악하고, 
특정 월에 매출이 급증하거나 감소하는 이유를 조사할 수 있음.
이 데이터를 바탕으로 마케팅 및 프로모션 전략을 수립 가능.

import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv', encoding='utf-8')

# 날짜 컬럼 변환
df['주문 일자'] = pd.to_datetime(df['주문 일자'])
df['월'] = df['주문 일자'].dt.month  # 월 컬럼 추가

# 월별 매출 집계
monthly_sales = df.groupby('월')['매출'].sum().reset_index()

# 막대 그래프 생성
fig = px.bar(monthly_sales, x='월', y='매출',
             title='2019년 월별 총 매출',
             labels={'월': '월', '매출': '총 매출액'},
             text=monthly_sales['매출'].round(2))

fig.update_traces(textposition='outside')  # 막대 위에 값 표시
fig.show()

모든 월이 다 표시되려면: 

import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv', encoding='utf-8')

# 주문 일자를 datetime 형식으로 변환
df['주문 일자'] = pd.to_datetime(df['주문 일자'])

# 월 추출
df['월'] = df['주문 일자'].dt.month

# 월별 총 매출 집계
monthly_sales = df.groupby('월')['매출'].sum().reset_index()

# 모든 월이 표시되도록 설정
fig = px.bar(monthly_sales, x='월', y='매출', 
              title='2019년 월별 총 매출',
              labels={'월': '월', '매출': '총 매출액'},
              text_auto='.2s')  # 막대 위에 값 표시

# x축을 1부터 12까지 모든 월을 표시하도록 설정
fig.update_layout(
    xaxis=dict(
        tickmode='linear',  # 선형 간격으로 틱 설정
        dtick=1,            # 틱 간격을 1로 설정
        tick0=1,            # 첫 번째 틱을 1로 설정
        range=[0.5, 12.5],  # x축 범위 설정 (여백 추가)
        ticktext=['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],  # 사용자 정의 틱 레이블
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # 틱 위치
    )
)

fig.show()

📌 인사이트 및 비즈니스 전략:

💡 1. 성수기(매출이 높은 시기) 활용 전략

5월6월, 8월12월은 매출이 높은 기간이므로, 프로모션/마케팅 강화
특히 10월~12월은 연말 시즌으로 매출이 높으므로, 적극적인 할인 및 마케팅 캠페인 기획 필요

💡 2. 비수기(매출이 낮은 시기) 개선 전략

2월, 4월, 7월은 매출이 낮은 비수기이므로 할인 행사, 프로모션 등을 통해 수요 촉진
고객 유입을 늘리기 위해 멤버십 할인, 무료 배송, 번들 상품 판매 등의 전략을 고려

💡 3. 7월의 매출 하락 원인 분석 필요

6월(390M) → 7월(190M)으로 매출이 절반 수준으로 감소
여름 휴가철로 인해 소비가 줄었을 가능성이 있음 → 여름맞이 프로모션, 특가 상품 판매 필요

💡 4. 연말 성수기 대비 인프라 최적화

10월~12월 매출 급증을 고려해 재고 확보, 물류 시스템 최적화, 고객 서비스 강화 필요
빠른 배송 옵션, VIP 고객 대상 특별 할인 적용 가능


문제. 지역별 총 매출은 어떻게 다른가?

목적: 어느 지역에서 매출이 가장 많이 발생하는지 분석하여 주요 판매 지역을 식별할 수 있음.
활용: 지역별 맞춤형 마케팅 전략, 물류 및 유통 최적화


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 데이터 로드
df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv', encoding='utf-8')

# 지역별 총 매출 집계
region_sales = df.groupby('지역')['매출'].sum().reset_index()

# 매출을 백만 단위로 변환
region_sales['매출_백만'] = region_sales['매출'] / 1000000

# 매출 내림차순 정렬 (선택사항)
region_sales = region_sales.sort_values('매출', ascending=False)

# 막대 그래프 생성
fig = px.bar(region_sales, x='지역', y='매출_백만',
             title='2019년 지역별 총 매출 비교',
             labels={'지역': '지역', '매출_백만': '총 매출액'},
             color_discrete_sequence=['royalblue'])  # 파란색 계열 막대 사용

# 값 레이블 포맷팅 (예: 310M)
region_sales['매출_레이블'] = region_sales['매출_백만'].apply(lambda x: f"{int(x)}M")

# 사용자 정의 막대 생성
fig = go.Figure(go.Bar(
    x=region_sales['지역'],
    y=region_sales['매출_백만'],
    text=region_sales['매출_레이블'],
    textposition='inside',  # 막대 내부에 텍스트 표시
    marker_color='royalblue',  # 파란색 계열 막대
    width=0.6  # 막대 너비 조정
))

# 레이아웃 설정
fig.update_layout(
    title={
        'text': '2019년 지역별 총 매출 비교',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20, 'color': 'darkblue'}
    },
    xaxis_title='지역',
    yaxis_title='총 매출액',
    yaxis=dict(
        gridcolor='lightgray',  # 그리드 색상
        gridwidth=0.5,         # 그리드 너비
        showgrid=True          # 그리드 표시
    ),
    plot_bgcolor='aliceblue',  # 배경색 설정
    height=600,                # 그래프 높이
    width=1000,                # 그래프 너비
    font=dict(size=14)         # 기본 폰트 크기
)

# 텍스트 스타일 설정
fig.update_traces(
    textfont=dict(
        size=16,
        color='white',
        family='Arial'
    ),
    marker=dict(
        line=dict(width=0)  # 막대 테두리 제거
    )
)

# Y축 범위 설정 (값 위에 여유 공간 추가)
max_value = region_sales['매출_백만'].max()
fig.update_yaxes(range=[0, max_value * 1.1])

fig.show()


✅ 1. 수도권 중심으로 마케팅 강화

이미 가장 높은 매출을 기록하는 지역이므로, 고객 유지 및 VIP 고객 유치 전략 필요
프리미엄 제품 및 맞춤형 프로모션 진행

✅ 2. 영남 지역 매출 확대

부산, 대구 등 대도시 타겟 광고 및 온·오프라인 마케팅 강화
수도권과 비슷한 판매 전략 적용 가능

✅ 3. 충청, 호남 지역 맞춤형 전략

수도권, 영남 대비 매출이 낮지만 지역 특화 상품 홍보 및 할인 이벤트 진행
지방 고객을 위한 무료 배송 이벤트 적용 고려

✅ 4. 강원, 제주 지역 매출 확대 방안

여행객 및 관광객을 타겟으로 한 상품 기획
온라인 채널을 활용한 강원, 제주 특산물 홍보 및 배송 서비스 강화
SNS 및 인플루언서를 활용한 지역 특화 상품 마케팅

✅ 5. 전체적인 매출 극대화를 위한 가격 및 프로모션 전략

지역별 할인율 최적화 → 매출 증가와 이익률 균형 유지
특정 지역(강원, 제주 등)의 구매 장벽 해소 (예: 무료 배송, 지역 특화 상품 홍보 등)
