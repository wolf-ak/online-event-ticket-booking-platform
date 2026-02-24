from fastapi import FastAPI
from backend.database import engine, Base
from backend.models import user, venue, event, seat, order, ticket

from backend.routers import (
    auth_router, booking_router, event_router, 
    refund_router, support_router, ticket_router
)

app = FastAPI(title="Event Ticket Booking API")

# Create tables
Base.metadata.create_all(bind=engine)

# Attach routers to the app
app.include_router(auth_router.router)
app.include_router(booking_router.router)
app.include_router(event_router.router)
app.include_router(refund_router.router)
app.include_router(support_router.router)
app.include_router(ticket_router.router)

@app.get("/")
def home():
    return {"message": "Backend is running"}