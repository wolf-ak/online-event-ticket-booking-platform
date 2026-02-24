import streamlit as st
from pages import auth, home, dashboard, admin, entry_manager, support_dashboard

st.set_page_config(page_title="Event Booking Platform")

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None

def route_user():
    role = st.session_state.role

    if role == "customer":
        dashboard.render()
    elif role == "admin":
        admin.render()
    elif role == "organizer":
        dashboard.render()
    elif role == "entry_manager":
        entry_manager.render()
    elif role == "support":
        support_dashboard.render()
    else:
        home.render()

if st.session_state.token is None:
    auth.render()
else:
    route_user()