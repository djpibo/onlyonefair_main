import streamlit as st

class Euljiro:

    @staticmethod
    def set_title(company_name):
        st.set_page_config(page_title=f"{company_name}", layout="wide")

    @staticmethod
    def show_text(text):
        st.write(text)
