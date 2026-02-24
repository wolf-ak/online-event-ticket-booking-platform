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

        payment_mode = st.selectbox(
            f"Payment Mode for Event {event['id']}",
            ["card", "upi", "cash"],
            key=f"payment_mode_{event['id']}"
        )
        seats = st.text_input(f"Seats for Event {event['id']} (comma separated)")
        
        if st.button(f"Book Event {event['id']}"):
            seat_list = [seat.strip() for seat in seats.split(",") if seat.strip()]
            seat_ids = []
            seat_error = None
            try:
                seat_ids = [int(seat_id) for seat_id in seat_list]
            except ValueError:
                seat_error = "Seat IDs must be numbers"

            if seat_error:
                st.error(seat_error)
            elif not seat_ids:
                st.error("Please enter at least one seat ID")
            else:
                result = book_ticket(
                    st.session_state.token,
                    event["id"],
                    seat_ids,
                    payment_mode
                )

                if "id" in result:
                    st.success(f"Order #{result['id']} created successfully")
                elif "message" in result:
                    st.success(result["message"])
                else:
                    st.error(result.get("detail", "Booking Failed"))
