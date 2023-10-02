import streamlit as st
from util import price_income as pi
from PIL import Image

image1 = Image.open('images/price_income_01.png')
image2 = Image.open('images/price_income_02.png')

def app():
    st.title('[회귀분석]')
    st.image(image1)
    st.markdown("""---""")       
    
    pi.main()
    st.markdown("""---""")    
    st.image(image2)
