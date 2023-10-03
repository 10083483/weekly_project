import streamlit as st
from PIL import Image
from matplotlib import font_manager
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

font_path = 'data/NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_path, size=20)

########### 금리 데이터프레임 생성 ###########
file_path = 'data/interest_df.csv'
df_interest = pd.read_csv(file_path, index_col='Year', parse_dates=['Year'])
df_interest.index = df_interest.index.strftime('%Y')

########### 매매가, 금리 데이터프레임 생성 ###########
file_path_2 = 'data/merge_corr.csv'
df_merge = pd.read_csv(file_path_2, index_col='Date', parse_dates=['Date'])
df_merge.index = df_merge.index.strftime('%Y-%m')


########### 인허가, 착공, 준공 데이터프레임 생성 ###########
file_path_3 = 'data/const_record_all.csv'
df_const = pd.read_csv(file_path_3, index_col = 'Year', parse_dates = ['Year'])
df_const.index = df_const.index.strftime('%Y')



def desc_1():
    st.write('#### 아파트 면적별 매매평균가격 변화 추이(전국 평균)')
    
    image_1 = Image.open('data/price_sqm_1.png')
    st.image(image_1)
    
def desc_2():
    st.write('#### 아파트 면적별 매매평균가격 변화 추이(지역별)')
    
    image_2 = Image.open('data/price_sqm_2.png')
    st.image(image_2)

def plot_interest_rate(df_interest):
    # 그래프 객체 생성
    fig = plt.figure(figsize=(15, 8))
    plt.title('금리 변동 추이', fontproperties=fontprop)
    
    # 그래프 그리기
    x = df_interest.index
    y = df_interest['금리']
    plt.plot(x, y, linestyle='-', color='skyblue', marker='o', markersize=6)
    
    plt.xlabel('연도', fontproperties=fontprop)
    plt.ylabel('금리', fontproperties=fontprop)
    
    plt.grid(True, linestyle='--')
    
    # 그래프 출력
    st.write('#### 금리 변동 추이')
    st.pyplot(fig)
    
def merge_corr_result():
    corr_result = df_merge[['매매가(전국평균)', '금리']].corr()
    return corr_result

# 산점도 그래프 및 선형 회귀분석 함수
def plot_scatter_and_regression(x, y):
    plt.figure(figsize=(10, 4))
    plt.title('한국은행 기준금리 및 아파트 매매 가격 변화', fontproperties=fontprop)
    plt.scatter(x, y, color='lightcoral', label='데이터')

    # 선형 회귀분석 수행
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # 회귀선 생성
    regression_line = slope * x + intercept

    # 회귀선 그래프 추가
    plt.plot(x, regression_line, color='olive', label='회귀선')

    # x축과 y축에 레이블 추가
    plt.xlabel('기준금리 변화', fontproperties=fontprop)
    plt.ylabel('아파트 매매 가격 변화', fontproperties=fontprop)

    # 그래프에 그리드 추가
    plt.grid(True, linestyle='--')

    # 범례 추가
    plt.legend(loc='best', prop=fontprop)

    # 그래프 출력
    st.pyplot(plt.gcf())

def linear_regression_analysis(X, y):
    # 선형 회귀 모델 생성 및 훈련
    model = LinearRegression()
    model.fit(X, y)

    # 모델 예측
    y_pred = model.predict(X)

    # R-squared 계산
    r2 = r2_score(y, y_pred)

    # 결과 반환
    return r2

def scipy_linear_regression_analysis(x, y):
    from scipy import stats
    
    # 선형 회귀 분석 수행
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    return slope, intercept, r_value, p_value, std_err

def print_df_const():
    st.write('#### 인허가, 착공, 준공 데이터 변화 추이(전국 평균)')
    st.dataframe(df_const)

def plot_const_all(df_const):
    x = df_const.index
    y_Permit = df_const['인허가실적']
    y_Start = df_const['착공실적']
    y_End = df_const['준공실적']

    # 그래프 객체 생성
    fig = plt.figure(figsize=(15, 8))
    plt.title('아파트 주택건설 인허가/착공/준공 추이', fontproperties=fontprop)

    # 그래프 그리기
    plt.plot(x, y_Permit, linestyle='-', color='lightcoral', marker='o', markersize=6, label='인허가실적')
    plt.plot(x, y_Start, linestyle='-', color='skyblue', marker='o', markersize=6, label='착공실적')
    plt.plot(x, y_End, linestyle='-', color='olive', marker='o', markersize=6, label='준공실적')

    plt.xlabel('연도', fontproperties=fontprop)
    plt.ylabel('실적(단위:호)', fontproperties=fontprop)
    plt.legend(loc='best', prop=fontprop)  # 범례 표시
    plt.grid(True, linestyle='--')
    #plt.xticks(rotation=45)
    plt.ticklabel_format(axis='y', useOffset=False, style='plain')  # y 축이 지수로 표현되는 것을 수정

    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])  # y 축 천단위 콤마 표시

    # 그래프 출력
    st.write('#### 아파트 주택건설 인허가/착공/준공 추이')
    st.pyplot(fig)
    
    