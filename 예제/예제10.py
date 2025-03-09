▣ 예제10. Sunburst Chart - 고객 세그먼트별 지역별 매출 분석  

Sunburst Chart는 계층적 데이터를 한눈에 볼 수 있는 강력한 시각화 도구이다. 이를 통해 지역별 고객 세그먼트에 따른 매출 분포를 효과적으로 분석할 수 있다.  

1. Sunburst Chart가 언제 필요한가?  

- 계층적 데이터를 시각적으로 탐색할 때 유용하다.  
- 그룹 간 비율을 한눈에 파악할 수 있어, 매출 기여도를 분석하는 데 적합하다.  
- 예: 지역별, 고객 세그먼트별 매출 기여도 분석  

2. 문제: 고객 세그먼트별 지역별 매출 차이는 어떻게 되는가?  

목적:  
- 고객 세그먼트별 매출이 지역마다 어떻게 다른지 분석  
- 특정 지역에서 높은 매출을 차지하는 고객 그룹을 식별  
- 매출이 낮은 지역 및 고객 세그먼트에 대한 전략 수립  

3. 데이터 로드 및 Sunburst Chart 생성  

import pandas as pd  
import plotly.express as px  

df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")  

df_grouped = df.groupby(["지역", "고객 세그먼트"])["매출"].sum().reset_index()  

fig = px.sunburst(df_grouped,   
                  path=["지역", "고객 세그먼트"],  
                  values="매출",  
                  title="고객 세그먼트별 지역별 매출 분포")  

fig.update_layout(  
    width=800,  
    height=600,  
    font=dict(size=14)  
)  

fig.show()  

4. 분석 결과 해석  

✅ 지역별 매출 기여도 분석  
✔ 수도권이 전체 매출에서 가장 높은 비중을 차지  
✔ 영남, 충청 등 일부 지역에서도 특정 고객 세그먼트가 높은 매출을 발생  

✅ 고객 세그먼트별 매출 비교  
✔ 기업 고객이 일부 지역에서 높은 매출을 보이며, B2B 시장이 주요 매출원임을 시사  
✔ 소비자 및 홈 오피스 고객도 지역에 따라 매출 패턴이 다름  

✅ 매출 최적화 전략  
✔ 수도권: 고매출 고객층을 대상으로 프리미엄 서비스 제공  
✔ 영남, 충청: 기업 고객 대상의 추가 영업 기회 발굴  
✔ 매출이 낮은 지역: 마케팅 및 프로모션을 통해 고객 유입 증가  

5. 추가 분석 - 지역별 매출 차이가 통계적으로 유의한가?  

지역별 매출 차이가 단순한 우연인지, 실제로 유의미한 차이인지 검증하기 위해 가설 검정을 수행할 수 있다.  

import pandas as pd  
from scipy.stats import f_oneway, kruskal  

df = pd.read_csv("c:\\data\\SUPERSTORE_2019.csv")  

sales_groups = [df[df["지역"] == region]["매출"].dropna() for region in df["지역"].unique()]  

anova_result = f_oneway(*sales_groups)  
kruskal_result = kruskal(*sales_groups)  

print("ANOVA 결과:", anova_result)  
print("Kruskal-Wallis 결과:", kruskal_result)  

6. 분석 결과 해석  

✅ ANOVA 결과 해석  
✔ p-value < 0.05 → 지역별 매출 차이가 통계적으로 유의미함  
✔ p-value >= 0.05 → 지역별 매출 차이가 유의하지 않음  

✅ Kruskal-Wallis 결과 해석  
✔ p-value < 0.05 → 정규성을 가정하지 않아도 지역별 매출 차이가 존재함  
✔ p-value >= 0.05 → 매출 차이가 우연일 가능성이 있음  

7. 결론 및 실행 전략  

🚀 수도권은 기존 고객을 유지하고, 프리미엄 서비스를 제공하여 고매출을 유지해야 함  
🚀 영남, 충청 지역은 추가적인 B2B 영업 기회를 발굴하여 기업 고객 유치를 확대할 필요가 있음  
🚀 매출이 낮은 지역에서는 타겟 마케팅을 통해 고객 유입을 증가시키는 전략이 필요  

Sunburst Chart를 활용하여 지역 및 고객 세그먼트별 매출을 분석한 후, 가설 검정을 통해 차이가 통계적으로 유의한지 확인하면 더욱 정밀한 데이터 기반 전략을 수립할 수 있다.
