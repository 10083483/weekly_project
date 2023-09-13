import streamlit as st
from util import time_series_desc as td

def app():
    st.subheader("Time Series")

    td.desc()
    
    