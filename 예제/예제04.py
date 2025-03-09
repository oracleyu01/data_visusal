### **예제 4. 산점도 (Scatter Plot)**

### **1. 산점도가 언제 필요한가?**  
# ✅ 두 개의 연속형 변수 간 관계를 시각적으로 분석할 때 유용함.  
# ✅ 변수 간 상관관계(correlation)를 파악하고 트렌드를 발견할 수 있음.  
# ✅ 예: 매출과 수익의 관계, 할인율과 매출의 영향, 고객 연령과 구매 금액 분석 등.  

import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv')

# 산점도 생성 (매출 vs 수익)
fig = px.scatter(df, x='매출', y='수익',
                 title='매출과 수익의 관계',
                 labels={'매출': '매출액', '수익': '수익액'},
                 opacity=0.7)

# 그래프 스타일 업데이트
fig.update_layout(xaxis_title='매출', yaxis_title='수익')
fig.show()

### **📌 산점도 vs 히스토그램 차이점**
# | 그래프 유형 | 사용 목적 |
# |---|---|
# | **산점도 (Scatter Plot)** | 두 개의 연속형 변수 간 관계를 분석 (예: 매출 vs 수익, 할인율 vs 판매량) |
# | **히스토그램 (Histogram)** | 데이터의 분포와 빈도를 분석하는 데 적합 (예: 매출 분포, 고객 수익률) |

### **🧐 추가 연습 문제**

2019년 매출과 수익 간의 관계를 분석하세요.

1. 매출이 증가할수록 수익도 증가하는가?

df = pd.read_csv('c:\\data\\SUPERSTORE_2019.csv')

# 매출-수익 산점도 생성
fig = px.scatter(df, x='매출', y='수익',
                 title='매출과 수익의 관계',
                 labels={'매출': '매출액', '수익': '수익액'},
                 opacity=0.7)

fig.update_layout(xaxis_title='매출', yaxis_title='수익')
fig.show()

2. 수익이 음수(손실)인 거래가 가장 많이 발생하는 매출 구간은 어디인가?

 수익이 음수(손실)인 거래만 필터링
loss_data = df[df['수익'] < 0]

# 손실이 많이 발생하는 매출 구간 확인
loss_bins = pd.cut(loss_data['매출'], bins=10)  # 매출을 10개의 구간으로 나눔
loss_summary = loss_data.groupby(loss_bins)['수익'].count().reset_index()
loss_summary.columns = ['매출 구간', '손실 거래 수']
print(loss_summary)

매출 구간별 손실 거래 수를 분석한 결과,
"(-2934.626, 590160.168]" 구간(즉, 약 0~590K 매출 구간)에서 손실 거래가 가장 많이 발생(2,846건).
매출이 낮은 경우 손실 발생 가능성이 높음을 의미.

3. 손실이 발생하는 주요 원인은 무엇일까? 할인율이 높은 경우일 가능성이 있는가?

# 손실 거래에서 할인율이 높은지 분석
loss_transactions = df[df['수익'] < 0]
print(loss_transactions[['매출', '수익', '할인율']].describe())  # 할인율 평균 및 분포 확인

# 할인율과 수익의 관계를 시각화
fig = px.scatter(df, x='할인율', y='수익',
                 title='할인율과 수익의 관계',
                 labels={'할인율': '할인율', '수익': '수익액'},
                 opacity=0.7)
fig.show()


4. 매출 대비 가장 높은 수익률(수익/매출 비율)을 기록한 상위 10개의 거래를 분석하세요.

# 매출 대비 가장 높은 수익률을 기록한 상위 10개 거래 찾기
df['수익률'] = df['수익'] / df['매출']
top_profit_transactions = df.nlargest(10, '수익률')
print(top_profit_transactions)
