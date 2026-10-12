import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='신세계라이브쇼핑 | 재고 운영 효율성 분석', page_icon='📊', layout='wide')
st.title('신세계라이브쇼핑 | 직접 판매 확대와 재고 운영 효율성')
st.caption('2023~2025년 감사보고서 기반 · 단위: 억 원 · 공시된 재무수치 및 명시된 가정 활용')

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
    with st.expander('왜 분석하나요? · 어떻게 계산하나요? · 무엇을 알 수 있나요?', expanded=False):
        a, b, c = st.columns(3)
        a.markdown('**분석 목적**')
        a.write(why)
        b.markdown('**계산 방법**')
        b.write(how)
        c.markdown('**해석과 한계**')
        c.write(meaning)


def line_chart(columns, title, unit='억 원'):
    fig = go.Figure()
    for col in columns:
        fig.add_trace(go.Scatter(
            x=DATA['연도'], y=DATA[col], mode='lines+markers+text', name=col,
            text=[fmt(v, 1) for v in DATA[col]], textposition='top center'
        ))
    fig.update_layout(title=title, yaxis_title=unit, height=380,
                      legend=dict(orientation='h', y=-0.25), margin=dict(t=60, b=70))
    fig.update_xaxes(tickvals=[2023, 2024, 2025])
    st.plotly_chart(fig, use_container_width=True)


def data_table(columns, percentages=()):
    view = DATA[columns].copy()
    formats = {c: ('{:.2f}%' if c in percentages else '{:,.2f}') for c in columns if c != '연도'}
    st.dataframe(view.style.format(formats, na_rep='—'), hide_index=True, use_container_width=True)


intro, trends, quality, scenario, conclusion = st.tabs([
    '① 문제 발견', '② 판매수익·재고 비교', '③ 재고평가손실', '④ 재고 활용도 시나리오', '⑤ 결론'
])

with intro:
    st.header('감사보고서에서 출발한 경영 질문')
    st.markdown('송출수수료 부담과 TV 시청 감소 등 산업적 위험요인에도 불구하고 신세계라이브쇼핑의 **영업이익은 2023년 131.7억 원에서 2025년 202.3억 원으로 53.6% 증가**했습니다. 다만 같은 기간 **재고자산은 143.1% 증가**했습니다.')
    st.markdown('영업이익과 재고자산의 증가율 차이는 **점검 질문의 출발점**이지 비효율의 증거는 아닙니다. 재고가 증가한 배경에는 직접 판매 확대, 신규 상품 준비, 적정 안전재고 확보 등 여러 가능성이 있습니다.')
    st.info('**핵심 질문:** 직접 판매 확대 과정에서 필요한 재고와 추가 점검이 필요한 재고를 어떻게 구분하고, 자금 배분 의사결정에 연결할 수 있을까?')
    a, b, c = st.columns(3)
    a.metric('영업이익 증가 (2023→2025)', f"{(DATA.loc[2, '영업이익']/DATA.loc[0, '영업이익']-1)*100:.1f}%")
    b.metric('재고자산 증가 (2023→2025)', f"{(DATA.loc[2, '재고자산']/DATA.loc[0, '재고자산']-1)*100:.1f}%")
    c.metric('2025년 당기 재고평가손실', f"{DATA.loc[2, '당기 재고평가손실(환입)']:.2f}억 원")
    st.markdown('#### 분석 순서')
    st.markdown('**① 성장과 재고 증가 확인 → ② 판매수익 대비 재고 활용도 분석 → ③ 평가손실 점검 → ④ 복수의 가정 비교 → ⑤ 추가 확인 항목과 관리 방안 제시**')
    line_chart(['영업이익', '재고자산'], '영업이익과 재고자산 추이')
    st.warning('**자료 범위:** 재화 판매수익과 재고자산은 전사 수치입니다. 모두 자체 브랜드(PB)에 해당한다고 볼 수 없고, 재고 증가의 원인을 자체 브랜드 확대만으로 확정할 수도 없습니다.')

with trends:
    st.header('2025년에는 재고 증가 속도가 판매수익 증가 속도를 앞섰을까?')
    explain(
        '판매 확대에 비해 재고 보유 규모가 빠르게 증가했는지 살펴봅니다.',
        '연도별 재화 판매수익·재고자산 증가율을 비교합니다. 평균 재고자산은 전년 말과 당년 말 재고의 평균으로 계산합니다. 재화 판매수익을 평균 재고자산으로 나눈 보조지표도 확인합니다.',
        '증가율과 보조지표의 변화는 재고 운영 점검 필요성을 보여주지만, 상품별 재고 부족·과잉이나 원인을 직접 증명하지는 못합니다.'
    )
    data_table(['연도', '재화 판매수익', '재고자산', '재화 판매수익 증가율(%)',
                '재고자산 증가율(%)', '평균 재고자산', '판매수익/평균재고(배)'],
               percentages=['재화 판매수익 증가율(%)', '재고자산 증가율(%)'])
    line_chart(['재화 판매수익', '재고자산'], '재화 판매수익과 재고자산 추이')
    growth_sales = DATA.loc[2, '재화 판매수익 증가율(%)']
    growth_inv = DATA.loc[2, '재고자산 증가율(%)']
    a, b, c = st.columns(3)
    a.metric('2025년 재화 판매수익 증가율', f'{growth_sales:.1f}%')
    b.metric('2025년 재고자산 증가율', f'{growth_inv:.1f}%')
    c.metric('2025년 증가율 격차(재고−판매)', f'{growth_inv-growth_sales:+.1f}%p')
    a, b = st.columns(2)
    a.metric('2024년 판매수익 / 평균재고', f"{DATA.loc[1, '판매수익/평균재고(배)']:.2f}배")
    b.metric('2025년 판매수익 / 평균재고', f"{DATA.loc[2, '판매수익/평균재고(배)']:.2f}배")
    st.info('**관찰:** 2024년에는 재화 판매수익 증가율이 재고 증가율보다 높았지만, 2025년에는 재고 증가율이 더 높았습니다. 판매수익/평균재고 비율도 2024년 약 11.30배에서 2025년 약 9.06배로 낮아졌습니다.')
    st.caption('이 비율은 매출원가가 아닌 재화 판매수익을 사용한 보조지표이며 정식 재고자산회전율이 아닙니다. 2023년은 2022년 말 재고 수치가 없어 계산하지 않았습니다. 기말 재고는 특정 시점의 잔액이므로 연간 판매수익과 비교할 때 해석에 주의해야 합니다.')

with quality:
    st.header('재고 규모뿐 아니라 가치 하락 위험도 확인')
    explain(
        '재고가 증가하더라도 정상적으로 판매될 수 있다면 반드시 비효율이라고 판단할 수 없습니다. 재고 가치에 대한 회계적 조정도 함께 확인합니다.',
        '연말 재고평가손실충당금 잔액과 당기 재고평가손실(환입)을 구분합니다. 충당금 비율은 연말 충당금을 평가 전 재고자산(장부금액+충당금)으로 나누어 계산합니다.',
        '충당금 비율과 당기 평가손실 증가는 추가 점검 신호지만, 어떤 상품이 원인인지 또는 향후 손실이 얼마인지까지는 공개 재무제표만으로 알 수 없습니다.'
    )
    data_table(['연도', '재고자산', '평가손실충당금', '당기 재고평가손실(환입)', '평가손실충당금 비율(%)'],
               percentages=['평가손실충당금 비율(%)'])
    line_chart(['평가손실충당금'], '연말 재고평가손실충당금 잔액')
    a, b = st.columns(2)
    a.metric('2024년 평가손실충당금 비율', f"{DATA.loc[1, '평가손실충당금 비율(%)']:.2f}%")
    b.metric('2025년 평가손실충당금 비율', f"{DATA.loc[2, '평가손실충당금 비율(%)']:.2f}%")
    st.info('**관찰:** 당기 재고평가손실(환입)은 2023년 -0.75억 원(환입), 2024년 +0.97억 원(손실), 2025년 +3.29억 원(손실)입니다. 연말 평가손실충당금 잔액도 2023년 5.89억 원에서 2025년 10.16억 원으로 증가했습니다.')
    st.caption('평가손실충당금은 연말에 남아 있는 평가 조정 누적 잔액이며, 당기 재고평가손실은 해당 연도 손익에 반영된 금액입니다. 둘은 같은 지표가 아닙니다.')

with scenario:
    st.header('가정별 재고 활용도 비교: 목표를 정하기 전 규모를 가늠하기')
    st.markdown('**2025년 재화 판매수익을 일정하게 유지한다는 가정**에서 여러 활용도 수준에 대응하는 평균 재고자산을 비교합니다. **2024년 수준은 과거 참고값일 뿐 최적 목표나 의무 회복 수준이 아닙니다.**')
    explain(
        '2025년 재고 활용도 하락이 어느 정도의 평균 재고 차이와 연결되는지 가정별로 살펴봅니다. 이를 통해 추가 검토할 규모를 파악합니다.',
        '가정별 평균 재고 = 2025년 재화 판매수익 ÷ 가정 활용도. 실제 2025년 평균 재고와의 차이를 계산합니다. 2024년 활용도는 과거 실적 참고선으로만 제시합니다.',
        '가정별 차이는 평균 재고의 수학적 차이입니다. 감축이 바람직하거나 실행 가능하다는 판단, 현금 유입·이익 개선 효과를 뜻하지 않습니다. 상품별 판매속도·품절 위험·안전재고·발주 리드타임·할인 비용 검토가 선행돼야 합니다.'
    )
    actual_ratio = float(DATA.loc[2, '판매수익/평균재고(배)'])
    past_ratio = float(DATA.loc[1, '판매수익/평균재고(배)'])
    sales = float(DATA.loc[2, '재화 판매수익'])
    actual_avg = float(DATA.loc[2, '평균 재고자산'])
    st.caption(f'2025년 실제 활용도: {actual_ratio:.2f}배 · 2024년 과거 참고값: {past_ratio:.2f}배')
    target = st.slider('비교할 가정 활용도 (배)', min_value=8.0, max_value=13.0,
                       value=10.0, step=0.05,
                       help='분석자가 설정하는 가정입니다. 2024년 실적이나 공식 경영 목표로 자동 확정되지 않습니다.')
    assumed_avg = sales / target
    difference = actual_avg - assumed_avg
    a, b, c = st.columns(3)
    a.metric('2025년 실제 평균 재고', f'{actual_avg:,.1f}억 원')
    b.metric('선택 가정의 평균 재고', f'{assumed_avg:,.1f}억 원')
    c.metric('실제와 가정의 차이', f'{difference:+,.1f}억 원')
    comparisons = pd.DataFrame({
        '비교 기준': ['2025년 실제', '가정 10.0배', '2024년 과거 참고값', '사용자 선택 가정'],
        '활용도(배)': [actual_ratio, 10.0, past_ratio, target],
    })
    comparisons['해당 평균 재고(억 원)'] = sales / comparisons['활용도(배)']
    comparisons['실제 평균 재고와 차이(억 원)'] = actual_avg - comparisons['해당 평균 재고(억 원)']
    st.dataframe(comparisons.style.format({'활용도(배)': '{:.2f}', '해당 평균 재고(억 원)': '{:,.2f}',
                                            '실제 평균 재고와 차이(억 원)': '{:+,.2f}'}),
                 hide_index=True, use_container_width=True)
    fig = go.Figure(go.Bar(
        x=['2025년 실제 평균 재고', '선택 가정의 평균 재고'],
        y=[actual_avg, assumed_avg],
        text=[f'{actual_avg:.1f}억', f'{assumed_avg:.1f}억'], textposition='outside'
    ))
    fig.update_layout(title='실제 평균 재고와 선택 가정 비교', yaxis_title='억 원', height=360)
    st.plotly_chart(fig, use_container_width=True)
    if difference > 0:
        st.info(f'**가정별 비교:** 활용도 {target:.2f}배를 적용하면 평균 재고가 실제보다 약 {difference:,.1f}억 원 적게 계산됩니다. 이는 실행이 검증된 감축 목표가 아닙니다.')
    elif difference < 0:
        st.info(f'**가정별 비교:** 활용도 {target:.2f}배를 적용하면 평균 재고가 실제보다 약 {abs(difference):,.1f}억 원 많게 계산됩니다. 감축 여지로 해석하지 않습니다.')
    else:
        st.info('선택한 가정에서 실제 평균 재고와 차이가 없습니다.')
    st.warning('**해석 주의:** 판매수익/평균재고는 매출원가 기반의 정식 재고자산회전율이 아닌 보조지표입니다. 재고를 줄여도 동일한 판매수익이 유지된다는 가정은 검증되지 않았습니다. 평균 재고 차이는 현금 유입, 비용 절감, 이익 증가 또는 연말 재고 감축액과 같지 않습니다.')

with conclusion:
    st.header('경영지원 관점의 결론')
    st.markdown('#### 1. 감사보고서에서 확인한 사실')
    st.markdown('- 2023~2025년 재화 판매수익은 약 **149%**, 재고자산은 약 **143%** 증가했습니다.\n- 2025년에는 재고자산 증가율이 재화 판매수익 증가율을 웃돌았고, 판매수익/평균재고 보조지표는 **2024년 11.30배 → 2025년 9.06배**로 하락했습니다.\n- 당기 재고평가손실은 **2024년 0.97억 원 → 2025년 3.29억 원**으로 증가했습니다.')
    st.markdown('#### 2. 가정별 비교에서 알 수 있는 점')
    st.write('2025년 재화 판매수익을 유지한다고 가정하고 활용도 수준을 달리하면 필요한 평균 재고 규모도 달라집니다. 2024년의 11.30배를 참고값으로 적용할 때 약 23.4억 원의 차이가 계산되지만, 과거 수준이 최적 목표라는 뜻도 실제 감축 가능액이라는 뜻도 아닙니다.')
    st.markdown('#### 3. 현재 자료만으로 판단할 수 없는 점')
    st.write('전사 공시수치만으로 재고 증가가 신규 상품 준비, 안전재고 확보, 과잉 발주 또는 판매 부진 중 무엇 때문인지 구분할 수 없습니다. 따라서 재고 감축을 먼저 결정하기보다 필요한 재고와 저회전 재고를 구분해야 합니다.')
    st.markdown('#### 4. 경영지원 제언: 판단 기준을 추가로 확보')
    st.markdown('**① 상품·브랜드별 확인:** 판매속도, 재고 보유기간, 수요 예측, 품절률, 발주 리드타임, 할인율, 반품률, 평가손실을 점검합니다.\n\n**② 원인별 대응:** 판매 확대에 필요한 재고는 유지하고, 저회전 재고는 상품기획·물류 부서와 발주량·판매계획 조정을 검토합니다. 할인판매는 예상 회수액과 마진 감소를 함께 비교한 뒤 판단합니다.\n\n**③ 자금 운영 연결:** 재고 수준의 변화가 운전자본과 현금 소요에 미치는 영향을 검토하되, 실제 현금 회수 시점과 규모는 별도로 추정합니다.')
    st.caption('자료: 신세계라이브쇼핑 2023·2024·2025년 감사보고서. 수익 구성은 수익 주석, 재고와 평가손실은 재고자산 주석, 영업이익은 손익계산서 기준입니다. 일부 소수점은 표시 과정에서 반올림했습니다.')
