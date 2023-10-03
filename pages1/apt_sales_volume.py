import streamlit as st
from util import sales_volume as sv

def app():
    st.title('[회귀분석] 아파트 매매량 분석')   
    sv.main()

