import streamlit as st

def event_card(event):
    """Displays an event nicely in a box."""
    with st.container(border=True):
        st.subheader(event.get('name', 'Unnamed Event'))
        st.write(f"🏷️ **Category:** {event.get('category')}")
        st.write(f"📅 **Date:** {event.get('event_date')}")
        st.write(f"💰 **Price:** ${event.get('ticket_price')}")
        return st.button("Buy Ticket", key=f"book_{event.get('id')}")