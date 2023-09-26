import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
import openpyxl
import os

#한글 폰트 출력
font_path = 'data/NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_path, size=15)
# 스트림릿에 한글 폰트 적용
plt.rc('font', family=fontprop.get_name())

# 파일 경로
excel_dir = 'data/area/unsold_check/'

#------------------------------------------------------------------
# 스트림릿 앱 정의
def unsold_desc():
    
    st.subheader('지역별 미분양 아파트 그래프')
    # 엑셀 파일 목록 가져오기
    excel_files = [f for f in os.listdir(excel_dir) if f.endswith('.xlsx')]
    
    # 모든 엑셀 파일을 담을 빈 데이터프레임 생성
    merged_df = pd.DataFrame()
    
    # 각 엑셀 파일을 읽어서 데이터프레임으로 변환 후 리스트에 추가
    for excel_file in excel_files:
        # 파일명에서 지역명 추출
        region_name = os.path.splitext(excel_file)[0]  # 파일명에서 확장자 제거
        region_name = region_name.replace(' 미분양 현황', '')  # ' 미분양 현황' 부분 제거
    
        # 엑셀 파일을 데이터프레임으로 읽기
        df = pd.read_excel(os.path.join(excel_dir, excel_file))
    
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
        
    # 인덱스를 연도와 월로 변환
    merged_df.index = merged_df.index.strftime('%Y/%m')
    
    merged_df.drop('경기도', axis = 1, inplace = True)
    
    #그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
     
       
    # 데이터프레임을 그래프로 플로팅
    merged_df.plot(figsize=(12, 8), legend=True, ax = ax)
    plt.title('미분양 데이터 시각화', fontproperties=fontprop)
    plt.xlabel('연도', fontproperties=fontprop)
    plt.ylabel('미분양 건수', fontproperties=fontprop)
    # 범례를 그래프 밖 오른쪽에 배치
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop=fontprop)
    plt.grid(True)
    #plt.show()
    st.pyplot(fig)
