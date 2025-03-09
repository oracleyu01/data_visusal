### **예제3. 히스토그램 (Histogram)**

### **1. 히스토그램이 언제 필요한가?**  
# ✅ 데이터의 분포(Distribution)를 분석할 때 유용함.  
# ✅ 특정 값(예: 매출, 주문 수, 수익)이 어떻게 분포되어 있는지 시각적으로 표현 가능.  
# ✅ 이상치(outlier) 탐지, 데이터의 집중도(중앙값, 범위) 등을 확인할 때 효과적.  

import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv', encoding='utf-8')

# 할인율 히스토그램 생성
fig = px.histogram(
    df, 
    x='할인율',
    nbins=20,
    color_discrete_sequence=['#FBBC05'],  # 구글 옐로우
    opacity=0.7,
    title="2019년 주문별 할인율 분포"
)

# 평균선 추가
avg_discount = df['할인율'].mean()
fig.add_vline(x=avg_discount, line_dash="dash", line_color="#4285F4")  # 구글 블루

# 디자인 간소화
fig.update_layout(
    plot_bgcolor='white',
    font_family="Arial",
    xaxis_title="할인율",
    yaxis_title="주문 건수",
    xaxis=dict(tickformat='.0%')  # 할인율을 백분율로 표시
)

fig.show()

할인율 분포 그래프에서 발견한 주요 인사이트:

1.대부분의 주문(약 4,000건)은 할인 없이(0%) 판매되었음
2.10% 할인대가 두 번째로 높은 빈도를 보임(약 2,100건)
3.평균 할인율은 약 15%로 나타남(파란 점선)
4.40-50% 구간에 소규모 피크가 있어 특정 프로모션 전략이 존재함을 시사
5.20-30%와 30-40% 할인율은 상대적으로 적게 사용됨
6.60% 이상의 높은 할인율은 거의 사용되지 않음

이 패턴은 무할인 판매와 소규모 할인(10%)이 주요 판매 전략이며, 40-50% 특별 프로모션이 제한적으로 활용됨을 보여줍니다.


### **📌 히스토그램 vs 막대 그래프 차이점**
# | 그래프 유형 | 사용 목적 |
# |---|---|
# | **히스토그램 (Histogram)** | 데이터의 분포와 빈도를 분석하는 데 적합 (예: 매출 분포, 고객 수익률) |
# | **막대 그래프 (Bar Plot)** | 특정 그룹(카테고리) 간 데이터를 비교하는 데 적합 (예: 지역별 매출, 제품별 판매량) |

### **🧐 추가 연습 문제**

문제. 주문 후 배송까지 걸린 일수를 히스토그램으로 시각화하세요.


import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv', encoding='utf-8')

# 배송 일자와 주문 일자를 datetime으로 변환
df['주문 일자'] = pd.to_datetime(df['주문 일자'])
df['배송 일자'] = pd.to_datetime(df['배송 일자'])

# 배송 소요 일수 계산
df['배송 소요일'] = (df['배송 일자'] - df['주문 일자']).dt.days

# 배송 소요일 히스토그램 생성
fig = px.histogram(
    df, 
    x='배송 소요일',
    nbins=15,
    color_discrete_sequence=['#3498DB'],  # 파란색 계열
    opacity=0.8,
    title="주문별 배송 소요일 분포"
)

# 평균 배송 소요일 수직선 추가
avg_delivery_days = df['배송 소요일'].mean()
fig.add_vline(
    x=avg_delivery_days, 
    line_dash="dash", 
    line_color="#E74C3C",  # 빨간색 계열
    annotation_text=f"평균: {avg_delivery_days:.1f}일",
    annotation_position="top right",
    annotation_font=dict(color="#E74C3C")
)

# 디자인 설정
fig.update_layout(
    plot_bgcolor='white',
    font_family="Malgun Gothic, Arial",  # 한글 폰트 추가
    font_size=14,
    xaxis_title="배송 소요일",
    yaxis_title="주문 건수",
    margin=dict(l=50, r=50, t=80, b=50),
    xaxis=dict(tickmode='linear'),  # 정수 간격으로 표시
    bargap=0.1
)

# 마우스오버 정보 형식 설정
fig.update_traces(
    hovertemplate='배송 소요일: %{x}일<br>주문 건수: %{y}건'
)

fig.show()

주문별 배송 소요일 분포 그래프에서 발견한 주요 인사이트:

1.대다수의 주문이 4일 이내에 배송되고 있으며, 특히 4일째 배송이 완료되는 주문이 가장 많음(약 3,100건)
2.평균 배송 소요일은 4.0일로, 이는 기업의 배송 프로세스가 4일을 기준으로 최적화되어 있음을 시사함
35일 소요되는 배송이 두 번째로 많은데(약 2,400건), 4-5일이 전체 배송의 과반수를 차지함
당일(0일) 및 익일(1일) 배송은 상대적으로 적은 비중을 차지하여, 초고속 배송은 제한적으로 제공됨
7일 이상 소요되는 장기 배송은 매우 드물어, 대부분의 주문이 일주일 이내에 처리됨
2-3일 배송도 상당수 존재하여(각각 약 1,500건, 1,100건), 배송 시간은 다양한 요인(지역, 제품 유형 등)에 영향받는 것으로 보임

이러한 패턴은 물류 최적화, 고객 기대치 관리, 배송 서비스 개선에 중요한 시사점을 제공합니다.
