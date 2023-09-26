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
file_path2 = 'data/area/unsold_check/'

#-----------------------------------------------------------------------------
def unsold_check1():
    # 엑셀 파일 목록 가져오기
    excel_files = [f for f in os.listdir(file_path2) if f.endswith('.xlsx')]
    
    # 모든 엑셀 파일을 담을 빈 데이터프레임 생성
    merged_df = pd.DataFrame()
    
    # 각 엑셀 파일을 읽어서 데이터프레임으로 변환 후 리스트에 추가
    for excel_file in excel_files:
        # 파일명에서 지역명 추출
        region_name = os.path.splitext(excel_file)[0]  # 파일명에서 확장자 제거
        region_name = region_name.replace(' 미분양 현황', '')  # ' 미분양 현황' 부분 제거
    
        # 엑셀 파일을 데이터프레임으로 읽기
        df = pd.read_excel(os.path.join(file_path2, excel_file))
    
        df= df.T
        df.columns = df.iloc[0]
        df = df[1:]
        df = df[['미분양']]
    
        df.columns = [region_name]
    
        # '미분양' 열만 선택하여 데이터프레임을 합치기
   
        merged_df = pd.concat([merged_df, df], axis=1)
    
    # 따옴표 제거
    merged_df.index = merged_df.index.str.replace("'", "")
    
    # 인덱스를 날짜 형식으로 변환
    merged_df.index = pd.to_datetime(merged_df.index, format='%y.%m')
    
    # 인덱스를 1년 단위로 수정
    merged_df.index = merged_df.index.strftime('%Y')
    
    
    
    merged_df.drop('경기도', axis = 1, inplace = True)
    
    # 인덱스를 연도로 변경하여 연도별 평균 구하기
    merged_df = merged_df.groupby(merged_df.index).sum()
    merged_df= merged_df[['서울시 ', '부산시', '대구시', '인천시', '광주시 ', '대전시', '울산시', '세종']]
    merged_df.columns = ['서울_미분양', '부산_미분양', '대구_미분양', '인천_미분양', '광주_미분양', '대전_미분양', '울산_미분양', '세종_미분양']
    
    return merged_df
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
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']
    
    for region in regions:
        # 해당 지역의 데이터 추출
        region_data = data[['연도', f'{region}_평균매매가', f'{region}_미분양']].dropna()
    
        # 독립 변수와 종속 변수 선택
        X = region_data[f'{region}_미분양'].values.reshape(-1, 1)
        y = region_data[f'{region}_평균매매가'].values
    
        # 선형 회귀 모델 생성 및 학습
        model = LinearRegression()
        model.fit(X, y)
    
        # 모델 예측
        y_pred = model.predict(X)
    
        # R-squared 계산
        r2 = r2_score(y, y_pred)
    
        # 모델 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # 모델 시각화
        plt.scatter(X, y, label=region)
        plt.plot(X, model.predict(X), color='red', linestyle='-', linewidth=2)
        plt.xlabel(f'{region}_미분양', fontproperties=fontprop)
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
    unsold = unsold_check1()
    
    data = merge_dataframes(price, unsold)
    
    #st.dataframe(price)
    #st.dataframe(unsold)
    st.dataframe(data)
        
    create_matplotlib(data)






