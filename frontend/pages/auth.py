import streamlit as st
from api_handler import login

def render():
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login(email, password)

        if "access_token" in result:
            st.session_state.token = result["access_token"]
            st.session_state.role = result["role"]
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid credentials")