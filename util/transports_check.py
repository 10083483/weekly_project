import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
import openpyxl

#한글 폰트 출력
font_path = 'data/NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_path, size=15)
# 스트림릿에 한글 폰트 적용
plt.rc('font', family=fontprop.get_name())

# 파일 경로
file_path = 'data/area/transports_check/'

#st.set_option('deprecation.showPyplotGlobalUse', False)



# 스트림릿 앱 정의
def trans_desc():
    st.subheader('대중교통 통행량 그래프')
    
    # 3x3 그리드에 서브플롯 그리기
    fig, axs = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(12,12) )
    
    # 범례 항목 생성
    legend_labels = []

    # 초기 범례 생성
    #legend = None
    
    for year in range(2014, 2023):
        # Excel 파일 불러오기
        excel_file = f'{file_path}{year}년_대중교통.xlsx'
        df = pd.read_excel(excel_file, skiprows=8)

        # 데이터 전처리
        df = df.iloc[:, :27]
        df.columns = ['전체', '도시철도', '비율', '버스전체', '비율', '시내버스', '비율', '시외버스', '비율', '좌석버스',
                      '비율', '마을버스', '비율', '간선버스', '비율', '지선버스', '비율', '광역버스', '비율', '순환버스',
                      '비율', '농어촌버스', '비율', '공항버스', '비율', '기타버스', '비율']

        df = df[['전체', '도시철도', '버스전체', '시내버스', '시외버스', '좌석버스', '마을버스', '간선버스', '지선버스',
                 '광역버스', '순환버스', '농어촌버스', '공항버스', '기타버스']]
        df.set_index('전체', inplace=True)
        
        df = df.iloc[:7,:]

        columns_to_convert = ['도시철도', '버스전체', '시내버스', '시외버스', '좌석버스', '마을버스', '간선버스', '지선버스',
                              '광역버스', '순환버스', '농어촌버스', '공항버스', '기타버스']
        for column in columns_to_convert:
            df[column] = df[column].str.replace(',', '').str.replace('-', '0').astype(float)


        df = df[['도시철도', '시내버스', '시외버스', '좌석버스', '마을버스', '간선버스', '지선버스', '광역버스',
                 '순환버스', '농어촌버스', '공항버스', '기타버스']]

        # 그래프 데이터 생성
        x = df.columns[:]  # x축에 들어갈 열 이름들 (버스전체 제외)
        regions = df.index  # 각 지역 이름

        # 각 지역별로 통행량을 선 그래프로 그리기
        row = (year - 2014) // 3  # 서브플롯 행 인덱스 계산
        col = (year - 2014) % 3   # 서브플롯 열 인덱스 계산
        ax = axs[row, col]  # 현재 연도에 해당하는 서브플롯

        for region in regions:
            y = df.loc[region][:]  
            ax.plot(x, y, marker='o', label=region)
            
            # 범례 항목 추가 (첫 해에만 추가)
            if year == 2014:
                legend_labels.append(region)

        # 그래프에 제목과 레이블 추가
        ax.set_title(f'{year}년 대중교통 통행량', fontproperties=fontprop)
        ax.set_xlabel('교통수단', fontproperties=fontprop)
        ax.set_ylabel('통행량', fontproperties=fontprop)
    
        # x축 레이블 회전
        plt.setp(ax.get_xticklabels(), rotation=90)
    
        # 그래프 간 간격 조절
        plt.tight_layout()

    # 범례 추가 (첫 해의 범례 항목으로 한 번만 추가)
    plt.figlegend(legend_labels, loc='lower center', bbox_to_anchor=(0.93, 0.83), prop = font_manager.FontProperties(fname=font_path, size=10))

    # 전체 도화지 출력
    st.pyplot(fig)
'''
def trans_desc():
    st.title('대중교통 통행량 그래프')
    
      
    for year in range(2014, 2023):
        # Excel 파일 불러오기
        excel_file = f'{file_path}{year}년_대중교통.xlsx'
        df = pd.read_excel(excel_file, skiprows=8)

        # 데이터 전처리
        df = df.iloc[:, :27]
        df.columns = ['전체', '도시철도', '비율', '버스전체', '비율', '시내버스', '비율', '시외버스', '비율', '좌석버스',
                      '비율', '마을버스', '비율', '간선버스', '비율', '지선버스', '비율', '광역버스', '비율', '순환버스',
                      '비율', '농어촌버스', '비율', '공항버스', '비율', '기타버스', '비율']

        df = df[['전체', '도시철도', '버스전체', '시내버스', '시외버스', '좌석버스', '마을버스', '간선버스', '지선버스',
                 '광역버스', '순환버스', '농어촌버스', '공항버스', '기타버스']]
        df.set_index('전체', inplace=True)
        
        df = df.iloc[:7,:]

        columns_to_convert = ['도시철도', '버스전체', '시내버스', '시외버스', '좌석버스', '마을버스', '간선버스', '지선버스',
                              '광역버스', '순환버스', '농어촌버스', '공항버스', '기타버스']
        for column in columns_to_convert:
            df[column] = df[column].str.replace(',', '').str.replace('-', '0').astype(float)


        df = df[['도시철도', '시내버스', '시외버스', '좌석버스', '마을버스', '간선버스', '지선버스', '광역버스',
                 '순환버스', '농어촌버스', '공항버스', '기타버스']]

        # 그래프 데이터 생성
        x = df.columns[:]  # x축에 들어갈 열 이름들 (버스전체 제외)
        regions = df.index  # 각 지역 이름


        # 각 지역별로 통행량을 선 그래프로 그리기
        fig, ax = plt.subplots(figsize=(12,6))
        for region in regions:
            y = df.loc[region][:]  # 각 지역의 통행량 데이터 (버스전체 제외)
            plt.plot(x, y, marker='o', label=region)

        # 그래프에 제목과 레이블 추가
        plt.title(f'{year}년 지역별 대중교통 통행량', fontproperties=fontprop)
        plt.xlabel('교통수단', fontproperties=fontprop)
        plt.ylabel('통행량', fontproperties=fontprop)

        # y축 포맷 변경
        formatter = ticker.FuncFormatter(lambda x, pos: f'{int(x / 1e6):,}천만')
        plt.gca().yaxis.set_major_formatter(formatter)
        
        # 범례 추가
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop = font_manager.FontProperties(fname=font_path, size=10))

        # 그래프 출력
        plt.xticks(rotation=90)  # x축 레이블을 90도 회전해서 표시
        plt.tight_layout()  # 레이아웃 조정
        
        # 스트림릿에 그래프 표시
        st.pyplot()
'''
    