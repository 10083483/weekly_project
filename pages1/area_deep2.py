import streamlit as st
from util import price_transports as pt

def app():
    st.title('[회귀분석]')
      
    
    pt.main()


#    st.write('''
#        > •인구 체크결과 : 
#        '''
#    )
#    st.write('''
#        서울특별시에는 다른 지방보다 2배 이상의 인구가 밀집되어있다.
#        '''
#        )
