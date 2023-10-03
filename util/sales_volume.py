import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pandas_datareader.data as web
from datetime import datetime
import matplotlib.ticker as ticker

from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#한글 폰트 출력
from matplotlib import font_manager, rc

font_path = 'data/NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_path, size=12)

file_path1 = 'data/'

def dataPreprocessing():
    #파일 경로
    
    kb_data = pd.read_excel(file_path1+'아파트매매거래량-거래규모.xlsx', engine='openpyxl')
    unemployment = pd.read_excel(file_path1+'성_교육정도별_실업률_20230925133115.xlsx', engine='openpyxl', header=[0])
    
    # kb_data 데이터프레임 생성
    kb_df = kb_data.transpose()# 열과 행을 바꾸기
    # 첫 번째 행을 열 이름으로 설정
    kb_df.columns = kb_df.iloc[0]
    # 첫 번째 행 제거 (이제 열 이름으로 설정되었으므로)
    kb_df = kb_df[1:]
    # 인덱스를 datetime 형식으로 변환
    kb_df.index = pd.to_datetime(kb_df.index, format="'%y.%m").strftime('%y-%m')
    kb_df['전체'] = kb_df['전체'].astype(float)
    
    # unemployment 데이터프레임
    unemployment['시점'] = unemployment['시점'].astype(str)
    # '시점' 열을 인덱스로 지정
    unemployment.set_index('시점', inplace=True)
    unemployment = unemployment.drop(unemployment.index[0])
    # 인덱스를 datetime 형식으로 변환
    unemployment.index = pd.to_datetime(unemployment.index, format='%Y.%m').strftime('%y-%m')
    unemployment['계'] = unemployment['계'].astype(float)
    
    
    

    
    return kb_data

#-----------------------------------------------------------------------------
def show(kb_data):
    st.subheader('아파트 매매 거래량(거래규모)')
    st.dataframe(kb_data)
    
    st.subheader('아파트 매매량 변화와 소비자심리지수 변화')
    st.image('data/img_CSI1.png')
    st.image('data/img_CSI2.png')
    st.write(f'•아파트 매매량 변화와 소비자심리지수 변화의 상관계수: -0.080')
    st.write(f'•R-squared (결정 계수): 0.0064')
    st.write('아파트 매매 거래량과 소비자심리지수(CCI) 간의 선형 관계가 매우 약하거나 존재하지 않는다는 것을 시사합니다.')
    
    st.subheader('아파트 매매량 변화와 실업률 변화')
    st.image('data/img_une1.png')
    st.image('data/img_une2.png')
    st.write(f'•아파트 매매량 변화와 실업률 변화의 상관계수:  0.3854')
    st.write(f'•R-squared (결정 계수): 0.1485')
    st.write('R-squared 값인 0.1485는 상대적으로 낮은 값으로, 회귀 모델이 주어진 데이터의 변동성을 14.85% 정도 설명하고 있다는 것을 나타냅니다.모델의 예측 능력이 낮다는 것을 시사합니다.')
    
    st.subheader('아파트 매매량 변화와 소비자물가지수 변화')
    st.image('data/img_CPI1.png')
    st.image('data/img_CPI2.png')
    st.write(f'•아파트 매매량 변화와 소비자물가지수 변화의 상관계수: -0.5145')
    st.write(f'•R-squared (결정 계수): 0.2924')
    st.write('R-squared 값인 0.2924는 상대적으로 낮은 값으로, 회귀 모델이 주어진 데이터의 변동성을 29.24% 정도 설명하고 있다는 것을 나타냅니다. 다시 말해, 이 모델은 데이터의 변동 중 약 29.24%만을 설명하고 나머지 변동은 모델로 설명되지 않는다고 할 수 있습니다. 모델의 예측 능력이 낮다는 것을 시사합니다.')
    
    st.subheader('아파트 매매량 변화와 기준금리 변화')
    st.image('data/img_IR1.png')
    st.image('data/img_IR2.png')
    st.write(f'•아파트 매매량 변화와 기준금리 변화의 상관계수: -0.655')
    st.write(f'•R-squared (결정 계수): 0.4684')
    st.write('상관계수를 토대로,음의 상관관계, 기준금리가 상승할 때 아파트 매매량은 하락하는 경향이 있다고 해석이 가능하다.')
    st.write('결정 계수를 토대로 해당 회귀 모델이 주어진 데이터의 변동성을 약 46.84% 정도 설명한다고 할 수 있습니다. 이는 비교적 중간 정도의 설명력을 갖는 모델이라고 볼 수 있습니다. 어느정도 상관성을 가진다고 볼 수 있습니다.')
    
# 메인 함수
def main():

    kb_data=dataPreprocessing()
    show(kb_data)

