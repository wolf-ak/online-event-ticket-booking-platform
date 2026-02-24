import streamlit as st
from api_handler import fetch_all_refunds, process_refund

def show_support():
    st.title("🎧 Support & Refund Center")
    
    if st.session_state.get("role") not in ["support", "admin"]:
        st.error("Access Denied. Support staff only.")
        return

    st.subheader("Pending Refund Requests")
    refunds = fetch_all_refunds()
    
    if not refunds:
        st.info("No pending refunds at the moment.")
        return

    for refund in refunds:
        with st.container(border=True):
            st.write(f"**Refund ID:** {refund.get('id')} | **Order ID:** {refund.get('order_id')}")
            st.write(f"**Status:** {refund.get('status')}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Approve", key=f"app_{refund.get('id')}"):
                    res = process_refund(refund.get('id'), "approved")
                    if res.status_code == 200:
                        st.success("Refund Approved!")
                        st.rerun()
            with col2:
                if st.button("Reject", key=f"rej_{refund.get('id')}"):
                    res = process_refund(refund.get('id'), "rejected")
                    if res.status_code == 200:
                        st.warning("Refund Rejected.")
                        st.rerun()