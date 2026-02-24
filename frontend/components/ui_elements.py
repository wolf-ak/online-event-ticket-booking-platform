import streamlit as st

def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.rerun()

def section_title(text):
    st.markdown(f"## {text}")