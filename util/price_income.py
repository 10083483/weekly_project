import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import pandas_datareader.data as web
from datetime import datetime
import matplotlib.ticker as ticker

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

#아파트매매가 결과 출력
from util import price_population as pp
#한글 폰트 출력
from matplotlib import font_manager, rc

#한글 폰트 출력
font_path = 'data/NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_path, size=20)
rc('font', family=fontprop.get_name())

file_path1 = 'data/area/APT_prices.xlsx'
#file_path2 = 'data/area/unsold_check/시도별_1인당_지역내총생산__지역총소득__개인소득_20230913164525.xlsx'

#-----------------------------------------------------------------------------
def income_check():
    df = pd.read_excel('data/area/income_check/시도별_1인당_지역내총생산__지역총소득__개인소득_20230913164525.xlsx')
    
    #1인당 개인소득
    df3 = df[['시도별', '2013.2','2014.2','2015.2','2016.2','2017.2','2018.2','2019.2','2020.2','2021.2']]
    df3.columns = ['시도별', '2013','2014','2015','2016','2017','2018','2019','2020','2021']
    
    df3= df3.drop(0)
    df3= df3.set_index('시도별')
    
    df3= df3.T
    
    df3 = df3[['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
           '세종특별자치시']]
    df3.columns = ['서울_1인당소득','부산_1인당소득','대구_1인당소득', '인천_1인당소득', '광주_1인당소득', '대전_1인당소득', '울산_1인당소득','세종_1인당소득']
    return df3
#--------------------------------------------------------

#합치기
# 데이터프레임 합치기
def merge_dataframes(df_avg, data):
    result = pd.merge(df_avg, data, left_index=True, right_index=True)
    data = result.reset_index()
    data.rename(columns={'index': '연도'}, inplace=True)
    return data

#--------------------------------------------------------


# 지역별 선형 회귀 모델 생성과 시각화
def create_matplotlib(data):
# 각 지역에 대한 선형 회귀 모델 생성
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']
    
    for region in regions:
        # 해당 지역의 데이터 추출
        region_data = data[['연도', f'{region}_평균매매가', f'{region}_1인당소득']].dropna()
    
        # 독립 변수와 종속 변수 선택
        X = region_data[f'{region}_1인당소득'].values.reshape(-1, 1)
        y = region_data[f'{region}_평균매매가'].values
    
        # 선형 회귀 모델 생성 및 학습
        model = LinearRegression()
        model.fit(X, y)
    
        # 모델 예측
        y_pred = model.predict(X)
    
        # R-squared 계산
        r2 = r2_score(y, y_pred)
    
        # 새로운 도화지 생성
        # 모델 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # 모델 시각화
        plt.scatter(X, y, label=region)
        plt.plot(X, model.predict(X), color='red', linestyle='-', linewidth=2)
        plt.xlabel(f'{region}_1인당소득', fontproperties=fontprop)
        plt.ylabel(f'{region}_평균매매가', fontproperties=fontprop)
        plt.title(f'선형 회귀 - {region}', fontproperties=fontprop)
        plt.legend()
        st.pyplot(fig)
        st.write(f'[{region} 모델 요약 정보]')
        
        # 상수 (절편) 추가
        #X_with_intercept = sm.add_constant(X)
        
        # 선형 회귀 모델 생성 (statsmodels 사용)
        #model_sm = sm.OLS(y, X_with_intercept).fit()
        
        # 모델 요약 정보 출력
        #st.write(model_sm.summary())
    
        # 회귀 계수 출력
        st.write(f'•{region}의 회귀 계수 (기울기): {model.coef_[0]}')
        st.write(f'•{region}의 절편: {model.intercept_}')
        st.write(f'•R-squared (결정 계수): {r2}')
        
        
#--------------------------------------------------------
# 메인 함수
def main():
    st.subheader('아파트 매매가와 미분양 수 회귀분석,r-score 분석')
    #st.write("")
    
    price = pp.check_price()
    income = income_check()
    
    data = merge_dataframes(price, income)
    
    #st.dataframe(price)
    #st.dataframe(unsold)
    st.dataframe(data)
        
    create_matplotlib(data)






