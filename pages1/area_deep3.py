import streamlit as st
from util import price_unsold as pu

def app():
    st.title('[회귀분석]')
      
    
    pu.main()

