import streamlit as st
from util import time_series_desc as td

def app():
    st.subheader("streamlit 매뉴얼")

    td.desc()
    
    