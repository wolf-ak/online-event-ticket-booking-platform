import streamlit as st
from api_handler import login_user, register_user

def show_auth():
    st.title("🔐 Authentication")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            res = login_user(email, password)
            if res.status_code == 200:
                data = res.json()
                st.session_state["token"] = data["access_token"]
                st.session_state["role"] = data["role"]
                st.success("Logged in successfully! Please refresh or go to Home.")
            else:
                st.error("Invalid credentials")

    with tab2:
        reg_name = st.text_input("Full Name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        reg_role = st.selectbox("Role", ["customer", "organizer"])
        
        if st.button("Register"):
            res = register_user(reg_name, reg_email, reg_password, reg_role)
            if res.status_code == 200:
                st.success("Registered successfully! You can now log in.")
            else:
                st.error("Registration failed. Email might exist.")