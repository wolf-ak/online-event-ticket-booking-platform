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
    response = requests.get(f"{BASE_URL}/events", headers=headers)
    return response.json()

def book_ticket(token, event_id, seats):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/book",
        headers=headers,
        json={"event_id": event_id, "seats": seats}
    )
    return response.json()