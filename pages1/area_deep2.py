import streamlit as st
from util import price_transports as pt
from PIL import Image

image1 = Image.open('images/price_transport_01.png')
image2 = Image.open('images/price_transport_02.png')

def app():
    st.title('[회귀분석]')
    st.image(image1)
    st.markdown("""---""")  
    
    pt.main()

    st.markdown("""---""")
    st.image(image2)
