import streamlit as st
from matplotlib import font_manager
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
font_path = 'data/NanumGothic.ttf'
#한글 폰트 출력
fontprop = font_manager.FontProperties(fname=font_path, size=20)
file_path = 'data/qc_df.csv'
def plotshow(qc_df):
    fig = plt.figure(figsize=(12, 6))
    plt.title('기온(°C) 변화', fontproperties=fontprop)

    plt.plot(qc_df.index, qc_df['기온(°C)'], marker='o', linestyle='-')
    plt.xlabel('시간', fontproperties=fontprop)
    plt.ylabel('기온(°C)', fontproperties=fontprop)
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
def desc():
    st.write('#### QC (결과 그래프, Gap Filling)')
    st.write('''
    1. 결측 검사
    2. 물리 한계 검사 
    3. 단계검사 
    결측치 없음
    
    4. 지속성 검사:단계검사에서 산출한 값의 절대값을 사용하여 시간별로 60개씩 합한 값을 구한다. 합계 한 값이 0.1보다 작으면 60개 전부 오류 처리
    
    오류값 480개 생성
    결측값을 바로 앞의 값으로 채움
    ''')
    st.write('##결과 그래프')
    
    qc_df = pd.read_csv(file_path)
    qc_df.index=pd.to_datetime(qc_df['일시'])
    plotshow(qc_df)

    
    st.write('#### 기초통계 (1시간, 3시간, 8시간, 1일) 평균값 산출')
    df_grouped60m = qc_df.groupby(pd.Grouper(freq='60T')).mean()
    plotshow(df_grouped60m)
    df_grouped180m = qc_df.groupby(pd.Grouper(freq='180T')).mean()
    plotshow(df_grouped180m)
    df_grouped480m = qc_df.groupby(pd.Grouper(freq='480T')).mean()
    plotshow(df_grouped480m)
    df_grouped1d = qc_df.groupby(pd.Grouper(freq='D')).mean()
    plotshow(df_grouped1d)