"# online-event-ticket-booking-platform" 
```mermaid
sequenceDiagram
    autonumber
    participant U as Customer
    participant S as Streamlit
    participant A as FastAPI
    participant D as MySQL (SQLAlchemy)

    U->>S: Clicks "Book Ticket"
    S->>A: POST /orders {event_id, seat_id}
    A->>D: Check Seat Status (SELECT)
    alt Seat is Available
        D-->>A: Status: Available
        A->>D: Update Status to 'RESERVED' (Atomic Update)
        A->>D: Create Order (Status: Pending)
        A-->>S: 201 Created (Order ID)
        S-->>U: Show Payment Screen
    else Seat is Taken
        D-->>A: Status: Sold/Reserved
        A-->>S: 409 Conflict
        S-->>U: Error: Seat no longer available
    end
```

## Run Locally

### Backend (FastAPI)
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Start the API:
```
uvicorn backend.main:app --reload
```

### Frontend (Streamlit)
1. In a new terminal, run:
```
streamlit run frontend/app.py
```

### Notes
- Default API base URL is `http://127.0.0.1:8000`.
- You can override it with `API_BASE_URL` environment variable.
