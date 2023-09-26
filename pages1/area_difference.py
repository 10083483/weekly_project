import streamlit as st
from util import population_check as poc
from util import transports_check as trc
from util import unsold_check as usc
from util import income_check as inc

def app():
    st.title('지역별 차이점 확인하기')
    #지역 인구 체크-----------------------------
    
    
    poc.po_desc()

    st.write('''
        > •인구 체크결과 : 
        '''
    )
    st.write('''
        서울특별시에는 다른 지방보다 2배 이상의 인구가 밀집되어있다.
        '''
    )    
    #대중교통 체크-----------------------------    
    
    trc.trans_desc()

    
    st.write('''
        > •대중교통 체크결과 : 
        '''
    )
    st.write('''
        서울특별시에는 다른 지방에 비해 도시철도가 발전되어 있으며, 각종 버스들도 역시 많이 운행하고 있다.
        '''
    )
    #미분양 아파트-----------------------------
        
    usc.unsold_desc()
    
    st.write('''
        > •미분양 아파트 체크결과 : 
        '''
    )
    st.write('''
        서울은 타지역에 비해서 미분양 아파트가 거의 없다는 것을 확인이 가능하다.
        '''
    )
    #1인당 개인 소득-----------------------------
        
    inc.income_desc()
    
    st.write('''
        > •1인당 개인소득 체크결과 : 
        '''
    )
    st.write('''
        서울과 울산이 1인당 평균소득이 높으며, 그중에서 서울이 조금 더 높은것을 확인이 가능하다.
        '''
    )