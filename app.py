import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='신세계라이브쇼핑 | 재고 운영 효율성 분석', page_icon='📊', layout='wide')
st.title('신세계라이브쇼핑 | 직접 판매 확대와 재고 운영 효율성')
st.caption('2023~2025년 감사보고서 기반 · 금액 단위: 억 원 · 공시 사실과 시뮬레이션을 구분')

DATA = pd.DataFrame({
    '연도': [2023, 2024, 2025],
    '재화 판매수익': [429.75170, 897.39742, 1068.36959],
    '수수료수익': [1586.36413, 1679.12335, 1512.06904],
    '재고자산': [53.83442, 105.01678, 130.87079],
    '평가손실충당금': [5.89497, 6.86792, 10.15865],
    '당기 재고평가손실(환입)': [-0.75412, 0.97295, 3.29073],
    '영업이익': [131.67878, 176.67756, 202.30575],
})
DATA['재화 판매수익 증가율(%)'] = DATA['재화 판매수익'].pct_change() * 100
DATA['재고자산 증가율(%)'] = DATA['재고자산'].pct_change() * 100
DATA['평균 재고자산'] = (DATA['재고자산'] + DATA['재고자산'].shift(1)) / 2
DATA['판매수익/평균재고(배)'] = DATA['재화 판매수익'] / DATA['평균 재고자산']
DATA['평가 전 재고자산'] = DATA['재고자산'] + DATA['평가손실충당금']
DATA['평가손실충당금 비율(%)'] = DATA['평가손실충당금'] / DATA['평가 전 재고자산'] * 100

def fmt(value, digits=1):
    return '—' if pd.isna(value) else f'{value:,.{digits}f}'

def explain(why, how, meaning):
    with st.expander('이 분석을 왜 하나요? · 어떻게 계산하나요? · 무엇을 판단하나요?', expanded=True):
        a,b,c=st.columns(3)
        a.markdown('**왜?**'); a.write(why)
        b.markdown('**어떻게?**'); b.write(how)
        c.markdown('**무엇을 판단?**'); c.write(meaning)

def chart_line(columns, title, y_title='억 원'):
    fig=go.Figure()
    for col in columns:
        fig.add_trace(go.Scatter(x=DATA['연도'],y=DATA[col],mode='lines+markers+text',name=col,
                                 text=[fmt(x,1) for x in DATA[col]],textposition='top center'))
    fig.update_layout(title=title,yaxis_title=y_title,legend=dict(orientation='h',y=-0.25),height=380,margin=dict(t=60,b=60))
    fig.update_xaxes(tickvals=[2023,2024,2025])
    st.plotly_chart(fig,use_container_width=True)

intro, trends, quality, scenario, conclusion=st.tabs([
    '① 문제 발견','② 판매수익과 재고 비교','③ 재고평가손실 확인','④ 목표 재고 시나리오','⑤ 결론·면접 설명'
])

with intro:
    st.header('감사보고서에서 출발한 경영 질문')
    st.markdown('2023~2025년 **재화 판매수익은 약 149% 증가**했습니다. 같은 기간 **재고자산도 약 143% 증가**했고, 2023년에는 환입됐던 재고평가손실이 2024~2025년에는 손실로 나타났습니다.')
    st.info('**핵심 질문:** 직접 상품 판매 확대 과정에서 재고 부담도 커졌는데, 재고를 충분히 효율적으로 활용하고 있는가?')
    a,b,c=st.columns(3)
    a.metric('재화 판매수익 증가',f"{(DATA.iloc[2]['재화 판매수익']/DATA.iloc[0]['재화 판매수익']-1)*100:.1f}%",'2023 → 2025')
    b.metric('재고자산 증가',f"{(DATA.iloc[2]['재고자산']/DATA.iloc[0]['재고자산']-1)*100:.1f}%",'2023 → 2025')
    c.metric('2025년 당기 재고평가손실',f"{DATA.iloc[2]['당기 재고평가손실(환입)']:.2f}억",'2023년에는 0.75억 환입',delta_color='off')
    st.markdown('#### 분석 순서')
    st.markdown('**① 직접 판매수익 확대 확인 → ② 재고 증가 속도 비교 → ③ 평가손실 점검 → ④ 목표 재고 활용도 설정 → ⑤ 평균 재고 축소 여지 계산**')
    st.warning('재화 판매수익 전체가 자체 브랜드(PB) 매출이라는 뜻은 아닙니다. 또한 재고 증가의 원인을 직접 판매 확대 하나로 확정할 수 없습니다.')

with trends:
    st.header('판매수익이 늘어난 만큼 재고도 늘었을까?')
    explain('재고 확대가 직접 판매수익 확대 속도와 비슷한지 확인합니다.',
            '연도별 증가율을 비교하고, 재화 판매수익을 기초·기말 평균 재고자산으로 나눕니다.',
            '2025년에는 판매수익 증가보다 재고 증가가 더 빨랐는지, 평균 재고 활용도가 하락했는지 확인합니다.')
    view=DATA[['연도','재화 판매수익','재고자산','재화 판매수익 증가율(%)','재고자산 증가율(%)','평균 재고자산','판매수익/평균재고(배)']].copy()
    st.dataframe(view.style.format({c:'{:,.2f}' for c in view.columns if c!='연도'},na_rep='—'),hide_index=True,use_container_width=True)
    chart_line(['재화 판매수익','재고자산'],'재화 판매수익과 재고자산의 추이')
    a,b=st.columns(2)
    with a:
        st.metric('2024년 판매수익 / 평균 재고',f"{DATA.loc[1,'판매수익/평균재고(배)']:.2f}배")
    with b:
        st.metric('2025년 판매수익 / 평균 재고',f"{DATA.loc[2,'판매수익/평균재고(배)']:.2f}배")
    st.success('**관찰:** 2024년에는 판매수익 증가율이 재고 증가율보다 높았지만, 2025년에는 재고 증가율이 더 높았습니다. 판매수익 / 평균 재고 비율도 약 11.30배 → 9.06배로 하락했습니다.')
    st.caption('주의: 이 비율은 매출원가가 아닌 재화 판매수익을 사용한 보조지표로, 정식 재고자산회전율이 아닙니다. 2023년은 2022년 말 재고를 포함한 평균 재고가 필요하므로 계산하지 않았습니다.')

with quality:
    st.header('재고의 양뿐 아니라 가치도 점검')
    explain('재고가 늘어도 정상적인 가격으로 팔 수 있다면 문제가 아닐 수 있습니다.',
            '연말 평가손실충당금과 당기 평가손실(환입)을 각각 확인합니다.',
            '2025년에는 재고 증가 외에 상품의 예상 판매가능가치 변화가 있었는지 추가 점검할 필요가 있습니다.')
    st.dataframe(DATA[['연도','재고자산','평가손실충당금','당기 재고평가손실(환입)','평가손실충당금 비율(%)']].style.format({
        '재고자산':'{:,.2f}','평가손실충당금':'{:,.2f}','당기 재고평가손실(환입)':'{:+,.2f}','평가손실충당금 비율(%)':'{:.2f}%'
    }),hide_index=True,use_container_width=True)
    chart_line(['평가손실충당금'],'연말 평가손실충당금 잔액')
    st.info('**핵심:** 2023년 당기 0.75억 원 환입 → 2024년 0.97억 원 손실 → 2025년 3.29억 원 손실. 다만 특정 상품이나 브랜드가 원인인지는 감사보고서만으로 알 수 없습니다.')
    st.caption('평가손실충당금은 연말 누적 잔액이고, 당기 평가손실은 그 해 손익에 반영된 금액입니다. 둘을 혼동하지 않습니다.')

with scenario:
    st.header('목표 재고 활용도를 달성한다면?')
    st.markdown('2025년 **재화 판매수익을 유지**한다고 가정하고, 목표 판매수익/평균재고 비율을 하나만 조정해 봅니다.')
    explain('2025년 판매수익 대비 평균 재고 활용도가 2024년보다 낮아진 점을 검토합니다.',
            '필요 평균 재고 = 2025년 재화 판매수익 ÷ 목표 비율. 현행 평균 재고와의 차이를 계산합니다.',
            '목표 비율을 달성하려면 평균 재고를 얼마나 줄여야 하는지 운영 목표를 세웁니다.')
    base=DATA.loc[2,'판매수익/평균재고(배)']
    benchmark=DATA.loc[1,'판매수익/평균재고(배)']
    target=st.slider('목표 판매수익 / 평균 재고 (배)',min_value=8.0,max_value=13.0,
                     value=round(float(benchmark),2),step=0.05,
                     help='2024년 실제 비율을 기본 목표로 설정했습니다. 다른 조건은 고정합니다.')
    st.caption(f'2025년 실제 {base:.2f}배  |  2024년 기준 {benchmark:.2f}배')
    sales=DATA.loc[2,'재화 판매수익']
    actual_avg=DATA.loc[2,'평균 재고자산']
    needed=sales/target
    difference=actual_avg-needed
    a,b,c=st.columns(3)
    a.metric('2025년 실제 평균 재고',f'{actual_avg:,.1f}억')
    b.metric('목표 달성 시 필요한 평균 재고',f'{needed:,.1f}억')
    c.metric('평균 재고 축소 여지',f'{max(difference,0):,.1f}억' if difference>=0 else '축소 여지 없음')
    if difference>=0:
        st.success(f'**시나리오 결과:** 2025년 판매수익을 유지하고 목표 {target:.2f}배를 달성한다면 평균 재고는 약 {difference:,.1f}억 원 낮아질 수 있습니다.')
    else:
        st.warning(f'목표 {target:.2f}배는 현재 수준보다 낮습니다. 이 경우 필요한 평균 재고가 현행보다 약 {-difference:,.1f}억 원 많아지므로 축소 목표로 적절하지 않습니다.')
    fig=go.Figure(go.Bar(x=['2025년 실제 평균 재고','목표 달성 시 필요 평균 재고'],y=[actual_avg,needed],
                         text=[f'{actual_avg:.1f}억',f'{needed:.1f}억'],textposition='outside'))
    fig.update_layout(title='평균 재고자산 비교',yaxis_title='억 원',height=350)
    st.plotly_chart(fig,use_container_width=True)
    st.warning('**중요:** 이 차이는 평균 재고의 운영 목표치이지, 확정적인 현금 유입·비용 절감·영업이익 증가액이 아닙니다. 연말 재고와도 구분해야 합니다. 실제 실현 여부는 상품별 발주·판매속도·안전재고·할인 비용 등을 검토해야 합니다.')

with conclusion:
    st.header('경영지원 관점의 결론')
    st.markdown('**발견:** 재화 판매수익은 2023~2025년 약 149% 증가했지만, 2025년에는 재고 증가 속도가 판매수익 증가 속도를 앞질렀습니다. 평균 재고 활용도는 2024년 11.30배에서 2025년 9.06배로 낮아졌고, 당기 재고평가손실도 증가했습니다.')
    st.markdown('**분석:** 2024년 수준의 재고 활용도를 목표로 할 경우, 2025년 판매수익을 유지한다는 단순 가정에서 평균 재고자산 약 23.4억 원을 줄이는 시나리오가 도출됩니다.')
    st.markdown('**제언:** 회사 내부의 상품별 재고 보유기간, 판매속도, 할인판매 비율, 반품 및 안전재고 수준을 확인해 저회전 상품의 발주량과 판매 시점을 조정하는 방안을 검토합니다.')
    st.markdown('#### 면접에서 40초 설명')
    st.info('“신세계라이브쇼핑의 감사보고서를 분석하면서 2023년부터 2025년까지 재화 판매수익이 약 149% 증가한 점에 주목했습니다. 그러나 같은 기간 재고자산도 약 143% 증가했고, 2025년에는 재고 증가율이 판매수익 증가율을 웃돌았습니다. 이에 생성형 AI를 활용해 재고 운영 효율성 분석 프로그램을 구현했습니다. 판매수익을 평균 재고자산으로 나눈 보조지표를 계산한 결과, 2024년 11.30배에서 2025년 9.06배로 낮아졌습니다. 2024년 수준으로 회복하는 시나리오에서는 평균 재고 약 23억 원의 축소 여지가 나타났습니다. 다만 이는 가정에 따른 목표치로, 실제 의사결정을 위해서는 상품별 판매속도와 발주 데이터를 추가 확인해야 한다고 판단했습니다.”')
    st.caption('자료: 신세계라이브쇼핑 2023·2024·2025년 감사보고서. 매출 구성은 수익 주석, 재고와 평가손실은 재고자산 주석, 영업이익은 손익계산서 기준입니다.')
