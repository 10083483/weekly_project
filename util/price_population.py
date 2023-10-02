import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pandas_datareader.data as web
from datetime import datetime
import matplotlib.ticker as ticker

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#한글 폰트 출력

from matplotlib import font_manager, rc

#한글 폰트 출력
font_path = 'data/NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_path, size=20)
rc('font', family=fontprop.get_name())

file_path1 = 'data/area/APT_prices.xlsx'
file_path2 = 'data/area/population_check/201312_202212_주민등록인구및세대현황_연간.csv'

def check_price():
    #파일 경로
    df = pd.read_excel(file_path1)
    
    df = df.set_index('Unnamed: 0')
    df.rename_axis(index=None, columns=None, inplace=True)
    df.index = df.index.strftime('%Y')
    
    df = df[['서울','부산','대구', '인천', '광주', '대전', '울산','세종']]
    
    # 인덱스를 연도로 변경하여 연도별 평균 구하기
    result = df.groupby(df.index).mean()
    
    df = result
    
    # 인덱스를 datetime 형식으로 변환
    df.index = pd.to_datetime(df.index)
    
    # 원하는 열 선택
    selected_columns = ['서울','부산','대구', '인천', '광주', '대전', '울산','세종']
    df_selected = df[selected_columns]
    
    #평균 계산
    df_avg = df_selected.resample('12M',closed='left').mean()
    
    df_avg.index = df_avg.index.strftime('%Y')
    
    
    df_avg.columns = ['서울_평균매매가','부산_평균매매가','대구_평균매매가', '인천_평균매매가', '광주_평균매매가', '대전_평균매매가', '울산_평균매매가','세종_평균매매가']
    
    return df_avg

#-----------------------------------------------------------------------------
def po_check():
    #인구수 체크
    po = pd.read_csv(file_path2, encoding='EUC-KR')
    
    po = po.T
    
    po.columns = po.iloc[0]
    po = po[1:]
    
    # 컬럼 이름에서 괄호와 괄호 안의 내용 삭제
    po.columns = po.columns.str.replace(r'\(.*\)', '')
    
    po.reset_index()
    #print(po.head())
    
    po.loc[['2013년_총인구수','2014년_총인구수','2015년_총인구수','2016년_총인구수','2017년_총인구수','2018년_총인구수','2019년_총인구수','2020년_총인구수','2021년_총인구수','2022년_총인구수'],:]
    
    filtered_po = po.loc[['2013년_총인구수','2014년_총인구수','2015년_총인구수','2016년_총인구수','2017년_총인구수','2018년_총인구수','2019년_총인구수','2020년_총인구수','2021년_총인구수','2022년_총인구수'],:]
    
    filtered_po.index = filtered_po.index.astype(str)
    
    # 1. 인덱스에서 '_총인구수' 제거
    filtered_po.index = filtered_po.index.str.replace('년_총인구수', '')
    
    # 열이름 제거
    filtered_po.columns.name = None
    
    #시계열 변환
    filtered_po.index = pd.to_datetime(filtered_po.index) # 인덱스를 datetime 자료형으로 변환
    
    # 연도만 남기고 'yyyy' 형식으로 변경
    filtered_po.index = filtered_po.index.strftime('%Y')
    
    
     # 데이터프레임의 모든 열에 대해 ',' 제거하고 숫자로 변환
    filtered_po = filtered_po.replace(',', '', regex=True).astype(float)
    
    #1000명단위 조절
    filtered_po = filtered_po.div(1000)
    
    # 마지막 데이터가 8월 1일 데이터가 남아 있음 해당 부분 삭제
    filtered_po.drop('전국  ', axis=1, inplace=True)
    
    
    # 광역시 기준 분할
    filtered_po_7 = filtered_po[['서울특별시  ', '부산광역시  ', '대구광역시  ', '인천광역시  ', '광주광역시  ',
           '대전광역시  ', '울산광역시  ', '세종특별자치시  ']]
    
    filtered_po_7.columns = ['서울_인구수','부산_인구수','대구_인구수', '인천_인구수', '광주_인구수', '대전_인구수', '울산_인구수','세종_인구수']
    
    return filtered_po_7
#--------------------------------------------------------
#합치기
# 데이터프레임 합치기
def merge_dataframes(df_avg, population_data):
    result = pd.merge(df_avg, population_data, left_index=True, right_index=True)
    data = result.reset_index()
    data.rename(columns={'index': '연도'}, inplace=True)
    return data


# 지역별 선형 회귀 모델 생성과 시각화
def create_matplotlib(data):
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']
    for region in regions:
        region_data = data[['연도', f'{region}_평균매매가', f'{region}_인구수']].dropna()
        X = region_data[f'{region}_인구수'].values.reshape(-1, 1)
        y = region_data[f'{region}_평균매매가'].values
        model = LinearRegression()
        model.fit(X, y)
        # 모델 예측
        y_pred = model.predict(X)
        # R-squared 계산
        r2 = r2_score(y, y_pred)

        # 그래프 시각화      
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.scatter(X, y, label=region)
        plt.plot(X, model.predict(X), color='red', linestyle='-', linewidth=2)
        plt.xlabel(f'{region}_인구수', fontproperties=fontprop)
        plt.ylabel(f'{region}_평균매매가', fontproperties=fontprop)
        plt.title(f'선형 회귀 - {region}', fontproperties=fontprop)
        plt.legend()
        st.pyplot(fig)
        # 회귀 계수와 절편 정보를 표시
        st.write(f'• {region}의 회귀 계수 (기울기): {model.coef_[0]}')
        st.write(f'• {region}의 절편: {model.intercept_}')
        st.write(f'• R-squared (결정 계수): {r2}')
    

# 메인 함수
def main():
    st.subheader('평균 아파트 매매가와 인구수의 선형 회귀,r-score 분석')
    #st.write("")
    
    price = check_price()
    po = po_check()
    data = merge_dataframes(price, po)
    
    st.dataframe(data)
    
    create_matplotlib(data)
    
def result_sumary():
    result_summary = """
    **결과 정리**
    
    - 인천과 세종은 인구 수와 양의 상관관계, 나머지는 음의 관계를 가지고 있습니다.
    
    - 인천과 울산, 세종은 결정 계수가 0.7보다 낮아 아파트 매매가의 변화를 설명하기에는 부족한 것으로 보입니다.
    서울, 부산, 대구, 광주, 대전은 인구 수에 따른 매매가와 강한 관련이 있을 가능성이 높다고 보입니다.
    """
    st.markdown(result_summary)
    
