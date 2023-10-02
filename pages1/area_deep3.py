import streamlit as st
from util import price_unsold as pu
from PIL import Image

image1 = Image.open('images/price_unsold_01.png')
image2 = Image.open('images/price_unsold_02.png')

def app():
    st.title('[회귀분석]')
    st.image(image1)
    st.markdown("""---""")    
    
    pu.main()
    st.markdown("""---""")    
    st.image(image2)

