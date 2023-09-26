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
file_path2 = 'data/area/transports_check/'

#-----------------------------------------------------------------------------
def result1_check():
    # 도시철도
    price = pp.check_price()
    # 빈 데이터프레임 생성
    
    merged_df = pd.DataFrame()
    
    # 2014년부터 2022년까지의 데이터를 읽어서 연도별로 처리
    for year in range(2014, 2023):
        # 파일명 생성
        filename = f'{file_path2}{year}년_대중교통.xlsx'
        
        # 엑셀 파일 읽기
        df = pd.read_excel(filename, skiprows=7)
        
        # 필요한 컬럼 선택 및 이름 변경
        df = df.iloc[:,:4]
        df = df[['Unnamed: 0', '통행량', '통행량.1']]
        df = df.iloc[0:9,:]
        df.columns = ['지역', '도시철도', '버스전체']
        df = df.iloc[1:9,:]
    
        
        
        # 지역별 대중교통 데이터를 각각의 연도 컬럼으로 변경
        df1 = df.iloc[:,0:2]
        df1.columns = ['지역', str(year)]
        df1 = df1.set_index('지역')
        df1 = df1.T
        
        # 연도별 데이터를 빈 데이터프레임에 추가
        merged_df = pd.concat([merged_df, df1])
    
    #이 코드를 실행하면 2014년부터 2022년까지의 연도별 대중교통 데이터가 합쳐진 merged_df 데이터프레임이 생성됩니다.
    merged_df= merged_df.iloc[:,:8]   
    merged_df = merged_df.rename_axis(None, axis=1)
    merged_df.columns = ['서울_도시철도','부산_도시철도','대구_도시철도', '인천_도시철도', '광주_도시철도', '대전_도시철도', '울산_도시철도','세종_도시철도']  
    
    # '연도'를 공통 컬럼으로 사용하여 merge
    result = pd.merge(price, merged_df, left_index=True, right_index=True)

    result= result.reset_index()

    result.rename(columns={'index': '연도'}, inplace=True)

    result.fillna(method='ffill', inplace=True)
    #result= result.fillna(method='ffill')

    # 모든 열에 대해 ,와 % 기호 제거하고 숫자로 변환
    columns_to_convert = ['서울_도시철도', '부산_도시철도', '대구_도시철도', '인천_도시철도', '광주_도시철도', '대전_도시철도', '울산_도시철도', '세종_도시철도']
    for column in columns_to_convert:
        result[column] = result[column].str.replace(',', '').str.replace('-', '0').astype(float)

    # 결측치를 0으로 대체
    result.fillna(0, inplace=True)
    #result= result.fillna(method='ffill')

    result= result.set_index('연도')
    
    return result
    
#--------------------------------------------------------
def result2_check(data):
    #버스 체크
    
    # 빈 데이터프레임 생성
    merged_df2 = pd.DataFrame()
    
    # 2014년부터 2022년까지의 데이터를 읽어서 연도별로 처리
    for year in range(2014, 2023):
        # 파일명 생성
        filename = f'{file_path2}{year}년_대중교통.xlsx'
    
        # 엑셀 파일 읽기
        df = pd.read_excel(filename, skiprows=7)
    
        # 필요한 컬럼 선택 및 이름 변경
        df = df.iloc[:,:4]
        df = df[['Unnamed: 0', '통행량', '통행량.1']]
        df = df.iloc[0:9,:]
        df.columns = ['지역', '도시철도', '버스전체']
        df = df[['지역','버스전체']]
        df2 = df.iloc[1:9,:]
    
    
    
        # 지역별 대중교통 데이터를 각각의 연도 컬럼으로 변경
        df2.columns = ['지역', str(year)]
        df2 = df2.set_index('지역')
        df2 = df2.T
    
        # 연도별 데이터를 빈 데이터프레임에 추가
        merged_df2 = pd.concat([merged_df2, df2])
    
        #이 코드를 실행하면 2014년부터 2022년까지의 연도별 대중교통 데이터가 합쳐진 merged_df 데이터프레임이 생성됩니다.
    
    merged_df2= merged_df2.iloc[:,:8]
    
    merged_df2 = merged_df2.rename_axis(None, axis=1)
    
    merged_df2.columns = ['서울_버스전체','부산_버스전체','대구_버스전체', '인천_버스전체', '광주_버스전체', '대전_버스전체', '울산_버스전체','세종_버스전체']
    
    # 2017년 데이터를 2016년 데이터로 대체
    # 데이터 상태가 이상한것 을 대체함
    merged_df2.loc['2017'] = merged_df2.loc['2016']
    
    merged_df2.fillna(method='ffill', inplace=True)
    
    # 모든 열에 대해 ,와 % 기호 제거하고 숫자로 변환
    columns_to_convert = ['서울_버스전체','부산_버스전체','대구_버스전체', '인천_버스전체', '광주_버스전체', '대전_버스전체', '울산_버스전체','세종_버스전체']
    for column in columns_to_convert:
        merged_df2[column] = merged_df2[column].str.replace(',', '').str.replace('-', '0').astype(float)
    
    merged_df2.fillna(method='ffill', inplace=True)
    
    result2 = pd.merge(data, merged_df2, left_index=True, right_index=True)
    
    result2 = result2.reset_index()
    
    result2 .rename(columns={'index': '연도'}, inplace=True)
    
    return result2
#--------------------------------------------------------


# 지역별 선형 회귀 모델 생성과 시각화
def create_matplotlib(data):
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']
    
    for region in regions:
        # 독립 변수 선택 (도시철도, 버스전체)
        X = data[[f'{region}_도시철도', f'{region}_버스전체']]
    
        # 종속 변수 선택 (평균매매가)
        y = data[f'{region}_평균매매가']
    
        # 상수 (절편) 추가
        X = sm.add_constant(X)
    
        # 선형 회귀 모델 생성
        model = sm.OLS(y, X).fit()
    
        # 모델 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
                
        # 산점도
        plt.scatter(X[f'{region}_도시철도'], y, label=f'{region}_도시철도')
        plt.scatter(X[f'{region}_버스전체'], y, label=f'{region}_버스전체')
        
        # 회귀선
        plt.plot(X[f'{region}_도시철도'], model.predict(X), color='red', linestyle='-', linewidth=2, label=f'{region}_도시철도 회귀선')
        plt.plot(X[f'{region}_버스전체'], model.predict(X), color='green', linestyle='-', linewidth=2, label=f'{region}_버스전체 회귀선')
        
        plt.xlabel(f'{region}_도시철도 & {region}_버스전체', fontproperties=fontprop)
        plt.ylabel(f'{region}_평균매매가', fontproperties=fontprop)
        plt.title(f'다중 선형 회귀 - {region}', fontproperties=fontprop)
        plt.legend()
        st.pyplot(fig)
        
        # 모델 요약 정보 출력
        st.write(f'{region} 모델 요약 정보:')
        st.write(model.summary())
    
#--------------------------------------------------------
# 메인 함수
def main():
    st.subheader('아파트 매매가와 대중교통 다중회귀분석 분석')
    #st.write("")
    
    result1 = result1_check()
    result2 = result2_check(result1)
    
    st.dataframe(result2)
    
    
    create_matplotlib(result2)







