import streamlit as st
from pages.auth import show_auth
from pages.home import show_home
from pages.dashboard import show_dashboard
from pages.admin import show_admin
from pages.support_dashboard import show_support
from pages.entry_manager import show_entry_manager

st.set_page_config(page_title="Event System", layout="wide")

st.sidebar.title("Navigation")

# 1. Determine User Role
role = st.session_state.get("role", "guest")

# 2. Build Menu based on the 5 Roles
if role == "guest":
    menu = ["Home", "Login / Register"]
elif role == "customer":
    menu = ["Home", "My Tickets", "Logout"]
elif role == "organizer":
    menu = ["Home", "Organizer Panel", "Logout"]
elif role == "admin":
    menu = ["Home", "Admin Panel", "Support Dashboard", "Logout"]
elif role == "support":
    menu = ["Support Dashboard", "Logout"]
elif role == "entry_manager":
    menu = ["Validate Tickets", "Logout"]

choice = st.sidebar.radio("Go to", menu)

# 3. Route to the correct page
if choice == "Home":
    show_home()
elif choice == "Login / Register":
    show_auth()
elif choice == "My Tickets":
    show_dashboard()
elif choice == "Organizer Panel" or choice == "Admin Panel":
    show_admin()
elif choice == "Support Dashboard":
    show_support()
elif choice == "Validate Tickets":
    show_entry_manager()
elif choice == "Logout":
    st.session_state.clear()
    st.success("Logged out successfully!")
    st.rerun()