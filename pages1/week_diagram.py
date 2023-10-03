import streamlit as st
from PIL import Image

image1 = Image.open('images/diagram.png')

def app():
    st.title('프로젝트 진행 다이어그램')
    st.markdown("""[주제] 시계열 데이터를 활용한 아파트매매가 변동분석""")       
    st.image(image1)
    #st.markdown("""---""")       
    
    #pi.main()
    #st.markdown("""---""")    
    #st.image(image2)
