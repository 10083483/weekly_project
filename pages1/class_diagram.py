import streamlit as st
from util import class_diagram_desc as cd


def app():
    st.title('Multipage Class Diagram')
    cd.desc()