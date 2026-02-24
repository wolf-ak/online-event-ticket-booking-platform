import streamlit as st
from api_handler import fetch_my_orders

def show_dashboard():
    st.title("🎫 My Tickets")
    
    if "token" not in st.session_state:
        st.warning("Please log in to view your tickets.")
        return

    orders = fetch_my_orders()
    if not orders:
        st.info("You haven't booked any tickets yet.")
        return

    for order in orders:
        with st.container(border=True):
            st.write(f"**Order ID:** {order.get('id')}")
            st.write(f"**Amount Paid:** ${order.get('total_amount')}")
            st.write(f"**Status:** {order.get('order_status')}")