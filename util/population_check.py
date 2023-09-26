import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime
from matplotlib import font_manager

#한글 폰트 출력
font_path = 'data/NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_path, size=20)

#파일 경로
file_path = 'data/area/population_check/201312_202212_주민등록인구및세대현황_연간.csv'


def po_desc():
    st.subheader('지역별 인구 수 그래프')
    
    po = pd.read_csv(file_path, encoding='EUC-KR')
    
    # 행과 열 전환
    po = po.T
    
    # 열 = 1번째 / 첫줄 행정구열 행 제외
    po.columns = po.iloc[0]
    po = po[1:]
    
    # 컬럼 이름에서 괄호와 괄호 안의 내용 삭제
    po.columns = po.columns.str.replace(r'\(.*\)', '')
    
    # 총 인구수만 선정
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
    
    filtered_po.info()
    
    filtered_po = filtered_po.div(1000)
    
    # 마지막 데이터가 8월 1일 데이터가 남아 있음 해당 부분 삭제
    filtered_po.drop('전국  ', axis=1, inplace=True)
    
    #filtered_po.head(3)
    
    # 광역시 기준 분할
    filtered_po_7 = filtered_po[['서울특별시  ', '부산광역시  ', '대구광역시  ', '인천광역시  ', '광주광역시  ',
           '대전광역시  ', '울산광역시  ', '세종특별자치시  ']]
    
    # 그래프 크기 설정
    #plt.figure(figsize=(12, 6))
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 모든 광역시의 연도별 총 인구수 그래프 그리기
    for column in filtered_po_7.columns:
        plt.plot(filtered_po_7.index, filtered_po_7[column], marker='o', linestyle='-', label=column)
    
    # 그래프 제목 설정
    plt.title('연도별 광역시 총 인구수', fontproperties=fontprop)
    
    # x축 라벨 설정
    plt.xlabel('연도', fontproperties=fontprop)
    
    # y축 라벨 설정
    plt.ylabel('총 인구수', fontproperties=fontprop)
    
    # x축 눈금 라벨 회전
    plt.xticks(rotation=45)
    
    # 범례를 그래프 밖 오른쪽에 배치
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop=fontprop)
    
    # 그래프 표시
    plt.grid(True)
    #plt.show()
    # 스트림릿에 그래프 표시
    st.pyplot(fig)












