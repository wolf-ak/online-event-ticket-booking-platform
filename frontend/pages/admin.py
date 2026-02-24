import streamlit as st
from api_handler import create_event

def show_admin():
    st.title("⚙️ Organizer Panel")
    
    if st.session_state.get("role") != "organizer":
        st.error("Access Denied. You must be an organizer to view this page.")
        return

    with st.form("add_event_form"):
        st.subheader("Launch New Event")
        name = st.text_input("Event Name")
        category = st.text_input("Category (e.g., Music, Tech)")
        date = st.date_input("Event Date")
        price = st.number_input("Ticket Price ($)", min_value=1)
        venue_id = st.number_input("Venue ID", min_value=1)
        organizer_id = st.number_input("Your Organizer ID", min_value=1)
        
        if st.form_submit_button("Create Event"):
            # Date needs to be formatted as string for FastAPI DateTime
            date_str = date.strftime("%Y-%m-%dT00:00:00")
            res = create_event(name, category, date_str, int(price), int(venue_id), int(organizer_id))
            
            if res.status_code == 200:
                st.success("Event Created Successfully!")
            else:
                st.error("Failed to create event.")