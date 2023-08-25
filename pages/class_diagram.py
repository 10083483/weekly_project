import streamlit as st
from util import class_diagram_desc as cd


def app():
    st.title('class_diagram')
    cd.desc()