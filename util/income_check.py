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


#------------------------------------------------------------------
# 스트림릿 앱 정의
def income_desc():
    st.subheader('지역별 1인당 평균소득 그래프')
    
    df = pd.read_excel('data/area/income_check/시도별_1인당_지역내총생산__지역총소득__개인소득_20230913164525.xlsx')
    
    #1인당 개인소득
    df3 = df[['시도별', '2013.2','2014.2','2015.2','2016.2','2017.2','2018.2','2019.2','2020.2','2021.2']]
    df3.columns = ['시도별', '2013','2014','2015','2016','2017','2018','2019','2020','2021']
    
    df3= df3.drop(0)
    df3= df3.set_index('시도별')
    
    df3= df3.T
    
    df3 = df3[['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
           '세종특별자치시']]
    
    # 그래프 객체 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    
    plt.title('시도별 1인당 평규개인소득 비교', fontproperties=fontprop)
    
    # 각 시도별로 선 그래프 그리기
    for column in df3.columns:
        plt.plot(df3.index, df3[column], marker='o', label=column)
    
    # 그래프에 제목과 레이블 추가
    plt.xlabel('연도', fontproperties=fontprop)
    plt.ylabel('1인당 평균개인소득', fontproperties=fontprop)
    
    # 범례를 그래프 밖 오른쪽에 배치
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop=fontprop)
    
    # 그래프 출력
    #plt.xticks(df.columns)
    plt.grid(True)
    #plt.tight_layout()
    st.pyplot(fig)
    
    
    
    