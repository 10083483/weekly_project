import streamlit as st
from util import price_population as pp
from PIL import Image


image1 = Image.open('images/price_populations_01.png')
image2 = Image.open('images/price_populations_02.png')

def app():
    st.title('[회귀분석]')
    st.image(image1)
    st.markdown("""---""")
    #지역 인구 체크-----------------------------
        
    pp.main()
    
    st.markdown("""---""")
    st.image(image2)
    
    pp.result_sumary()

    