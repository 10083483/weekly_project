"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
"""

# Import necessary libraries 
import streamlit as st

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """생성자는 self.pages라는 빈 리스트를 초기화합니다. 이 리스트는 Streamlit 애플리케이션에 포함하려는 페이지(또는 앱)에 관한 정보를 저장할 것입니다."""
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """이 메서드는 페이지(또는 앱)를 MultiPage 객체에 추가하는 데 사용됩니다. 두 개의 인자를 받습니다.

title: 페이지의 제목을 나타내는 문자열입니다.
func: 해당 페이지 내용을 렌더링하는 데 사용될 파이썬 함수입니다.
        """

        self.pages.append({
          
                "title": title, 
                "function": func
            })

    def run(self):
        # Drodown to select the page to run  
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        # run the app function 
        page['function']()
