import streamlit as st
from PIL import Image

def desc():
    #st.write('#### class_diagram')
    
    class_diagram = Image.open('data/class_diagram.png')
    st.image(class_diagram)