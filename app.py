import streamlit as st

# Custom imports 
from util import MultiPage
from pages import class_diagram, main_page, time_series # import your pages here

# Create an instance of the app 
app = MultiPage.MultiPage()

# Title of the main page
st.title("시계열 데이터를 활용한 아파트 매매가의 변동분석")

# Add all your applications (pages) here
app.add_page("Home", main_page.app)
app.add_page("Class Diagram", class_diagram.app)
app.add_page("Time Series", time_series.app)

# The main app
app.run()