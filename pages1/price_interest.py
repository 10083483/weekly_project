import streamlit as st
from util import price_interest_desc as pd


def app():
    st.title('아파트 면적별 매매평균가격 변화 분석')
    
    
    pd.desc_1()
    st.text("")
    st.text("")

    
    pd.desc_2()
    st.text("")
    st.write('''
             --> 2018년부터 2023년까지 한국의 아파트 매매가는 전반적으로 상승하는 경향을 보이고 있다.
             ''')
    st.text("")
    st.text("")
    
    
    pd.plot_interest_rate(pd.df_interest)
    st.text("")
    st.write('''
             --> 아파트 매매가에 영향을 주는 '금리' 변동 추이를 조사한 결과이며, 금리는 2021년 이후 계속 상승했다.
             ''')
    st.text("")
    st.text("")
    
    
    ###########################################################     
    # 상관 계수 결과 출력
    correlation_result = pd.merge_corr_result()
    st.write('#### 아파트 매매가(전국평균)과 금리의 상관 계수')
    st.write(correlation_result)
    st.write('''
             --> 상관계수는 0.254946으로 약한 선형관계를 보이고 있다. (금리가 증가할 때 아파트 매매가도 증가하는 추세)
             ''')
    st.text("")
    st.text("")
             
             
    ###########################################################         
    # 기준금리와 아파트 매매 가격 데이터 가져오기
    x = pd.df_merge['금리']
    y = pd.df_merge['매매가(전국평균)']
    
    
    ########################################################### 
    # plot_scatter_and_regression 함수 호출
    st.write("#### '금리'와 '아파트 매매 가격' 산점도")
    pd.plot_scatter_and_regression(x, y)
    st.write('''
             설명추가
             ''')
    st.text("")
    st.text("")      
            
    
    ###########################################################       
    st.write('#### scikit-learn을 사용한 선형회귀분석')
    # 선형 회귀분석 수행
    r2_score_result = pd.linear_regression_analysis(x.values.reshape(-1, 1), y)
    st.write(f'R-squared (결정 계수): {r2_score_result}')
    st.text("")
    st.write('''
             --> R-squared 값이 0.06으로 매우 낮으므로, 금리만으로는 아파트 매매 가격의 변화를 설명하기에는 충분하지 않다고 할 수 있다.
             ''')
    st.text("")
    st.text("")
    
    
    ###########################################################
    st.write('#### SciPy를 사용한 선형회귀분석')  
    slope, intercept, r_value, p_value, std_err = pd.scipy_linear_regression_analysis(x, y)
    st.write(f'선형 회귀식: y = {slope:.4f}x + {intercept:.4f}')
    st.write(f'R-squared (결정 계수): {r_value**2:.4f}')
    st.write(f'p-값: {p_value:.4f}')
    st.write(f'표준 오차: {std_err:.4f}')
    st.text("")
    st.write('''
             --> 이 결과는 금리와 아파트 매매 가격 간의 어떤 관계를 나타내지만, 설명력은 매우 낮으며 다른 중요한 변수들을 고려해야 함을 보여준다.
             ''')
    st.text("")
    st.text("")
    
    
    ###########################################################
    st.write('#### 결과설명')
    st.write('''
             --> 통상적으로 금리가 올라가면 주택가격이 내려가는데, 정 반대 현상이 나타나고 있다. 이러한 현상의 원인 중 하나는 '주택 공급부족'이다.
             ''')
    st.text("")
    st.text("")
    
    
    ###########################################################
    pd.print_df_const()
    st.text("")
    st.text("")
    
    
    pd.plot_const_all(pd.df_const)
    st.text("")
    st.write('''
             --> 아파트 건설 인허가, 착공, 준공추이 모두 감소하는 경향을 보이고 있다. 
             ''')
    st.text("")
    st.text("")
    