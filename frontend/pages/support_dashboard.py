import streamlit as st
from components.ui_elements import logout_button, section_title

def render():
    logout_button()
    section_title("Support Dashboard")

    st.write("View and manage refund requests (API integration pending)")