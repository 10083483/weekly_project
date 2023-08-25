import streamlit as st

# Custom imports 
from util import MultiPage
from pages import class_diagram, main_page, time_series # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Data Storyteller Application")

# Add all your applications (pages) here
app.add_page("class_diagram", data_upload.app)
app.add_page("main_page", metadata.app)
app.add_page("time_series", machine_learning.app)

# The main app
app.run()