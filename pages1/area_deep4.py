import streamlit as st
from util import price_income as pi

def app():
    st.title('[회귀분석]')
      
    
    pi.main()

