import streamlit as st
from api_handler import validate_gate_ticket

def show_entry_manager():
    st.title("🎟️ Gate Ticket Scanner")
    
    if st.session_state.get("role") != "entry_manager":
        st.error("Access Denied. Gate staff only.")
        return

    st.write("Enter the Ticket ID provided by the customer to grant entry.")
    
    ticket_id = st.number_input("Scan / Enter Ticket ID", min_value=1, step=1)
    
    if st.button("Validate Ticket"):
        res = validate_gate_ticket(ticket_id)
        if res.status_code == 200:
            st.success("✅ Ticket is VALID. Grant Entry.")
        else:
            st.error("❌ INVALID or ALREADY USED ticket.")