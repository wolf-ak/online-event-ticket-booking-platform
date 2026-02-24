import streamlit as st
from api_handler import fetch_events, book_ticket
from components.ui_elements import event_card

def show_home():
    st.title("🎟️ Upcoming Events")
    
    events = fetch_events()
    if not events:
        st.info("No events found. Check back later!")
        return

    cols = st.columns(3)
    for idx, event in enumerate(events):
        with cols[idx % 3]:
            if event_card(event):
                if "token" not in st.session_state:
                    st.warning("Please log in to book tickets.")
                else:
                    res = book_ticket(event['id'], event['ticket_price'])
                    if res.status_code == 200:
                        st.success("Ticket Booked Successfully!")
                    else:
                        st.error("Booking Failed.")