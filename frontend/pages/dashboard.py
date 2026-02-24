import streamlit as st
from api_handler import get_events, book_ticket
from components.ui_elements import logout_button, section_title

def render():
    logout_button()
    section_title("Available Events")

    events = get_events(st.session_state.token)

    for event in events:
        st.write(f"### {event['name']}")
        st.write(f"Price: ₹{event['ticket_price']}")

        seats = st.text_input(f"Seats for Event {event['id']} (comma separated)")
        
        if st.button(f"Book Event {event['id']}"):
            seat_list = seats.split(",")
            result = book_ticket(
                st.session_state.token,
                event["id"],
                seat_list
            )

            if "message" in result:
                st.success(result["message"])
            else:
                st.error("Booking Failed")