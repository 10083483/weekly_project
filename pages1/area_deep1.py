import streamlit as st
from util import price_population as pp
from util import transports_check as trc
from util import unsold_check as usc
from util import income_check as inc

def app():
    st.title('[회귀분석]')
    #지역 인구 체크-----------------------------
    
    
    pp.main()


#    st.write('''
#        > •인구 체크결과 : 
#        '''
#    )
#    st.write('''
#        서울특별시에는 다른 지방보다 2배 이상의 인구가 밀집되어있다.
#        '''
#        )
