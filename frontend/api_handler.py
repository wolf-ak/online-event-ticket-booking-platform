import requests

BASE_URL = "http://127.0.0.1:8000"

def login(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    return response.json()

def get_events(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/booking/events", headers=headers)
    return response.json()

def book_ticket(token, event_id, seat_ids, payment_mode):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/booking/orders",
        headers=headers,
        json={"event_id": event_id, "seat_ids": seat_ids, "payment_mode": payment_mode}
    )
    return response.json()
