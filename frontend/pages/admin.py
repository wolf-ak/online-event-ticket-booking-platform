import streamlit as st
from components.ui_elements import logout_button, section_title

def render():
    logout_button()
    section_title("Admin Dashboard")

    st.write("Create Event")
    name = st.text_input("Event Name")
    price = st.number_input("Ticket Price", min_value=0)

    if st.button("Create Event"):
        st.success("Event created (API integration pending)")