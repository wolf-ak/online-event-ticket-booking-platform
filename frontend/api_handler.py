import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"

def get_headers():
    """Attach JWT token if the user is logged in."""
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def login_user(email, password):
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    return res

def register_user(name, email, password, role="customer"):
    data = {"name": name, "email": email, "password": password, "role": role}
    res = requests.post(f"{BASE_URL}/auth/register", json=data)
    return res

def fetch_events():
    res = requests.get(f"{BASE_URL}/booking/events")
    return res.json() if res.status_code == 200 else []

def book_ticket(event_id, total_amount, payment_mode="card"):
    data = {"event_id": event_id, "total_amount": total_amount, "payment_mode": payment_mode}
    res = requests.post(f"{BASE_URL}/booking/orders", json=data, headers=get_headers())
    return res

def fetch_my_orders():
    res = requests.get(f"{BASE_URL}/booking/my-orders", headers=get_headers())
    return res.json() if res.status_code == 200 else []

def create_event(name, category, event_date, ticket_price, venue_id, organizer_id):
    data = {
        "name": name, "category": category, "event_date": event_date, 
        "ticket_price": ticket_price, "venue_id": venue_id, "organizer_id": organizer_id
    }
    res = requests.post(f"{BASE_URL}/events/", json=data, headers=get_headers())
    return res



def fetch_all_refunds():
    """For Support/Admin to view all refunds"""
    res = requests.get(f"{BASE_URL}/refunds/", headers=get_headers())
    return res.json() if res.status_code == 200 else []

def process_refund(refund_id, status):
    """Approve or Reject a refund"""
    res = requests.patch(f"{BASE_URL}/refunds/{refund_id}", json={"status": status}, headers=get_headers())
    return res

def validate_gate_ticket(ticket_id):
    """For Entry Managers to scan tickets"""
    res = requests.post(f"{BASE_URL}/tickets/{ticket_id}/validate", headers=get_headers())
    return res