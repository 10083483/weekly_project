import streamlit as st

# Custom imports 
from util import MultiPage
# import your pages here
from pages1 import class_diagram, main_page, time_series, price_interest, area_difference,area_deep1, area_deep2, area_deep3,area_deep4

# Create an instance of the app 
app = MultiPage.MultiPage()

# Title of the main page
#st.title("시계열 데이터를 활용한 아파트 매매가의 변동분석")

# Add all your applications (pages) here
app.add_page("Home", main_page.app)
app.add_page("Class Diagram", class_diagram.app)
app.add_page("Time Series", time_series.app)
app.add_page("아파트 면적별 매매평균가격 변화 분석", price_interest.app)
app.add_page("아파트 매매량 분석", apt_sales_volume.app)
app.add_page("지역차이변수 확인 ", area_difference.app)
app.add_page("지역차이분석 01", area_deep1.app)
app.add_page("지역차이분석 02", area_deep2.app)
app.add_page("지역차이분석 03", area_deep3.app)
app.add_page("지역차이분석 04", area_deep4.app)
#app.add_page("지역차이분석 05", area_deep5.app)

# The main app
app.run()
