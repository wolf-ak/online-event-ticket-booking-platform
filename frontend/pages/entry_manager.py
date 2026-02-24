import streamlit as st
from components.ui_elements import logout_button, section_title

def render():
    logout_button()
    section_title("Entry Validation")

    ticket_id = st.text_input("Enter Ticket ID")

    if st.button("Validate Ticket"):
        st.success("Ticket validated (API integration pending)")