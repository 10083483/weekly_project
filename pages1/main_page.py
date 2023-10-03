import streamlit as st
import pandas as pd
from PIL import Image

image1 = Image.open('images/members.png')
image2 = Image.open('images/main.png')
def app():
    #st.title('4조')
    st.image(image2)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    
    st.image(image1)