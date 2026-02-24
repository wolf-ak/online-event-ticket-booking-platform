from fastapi import FastAPI
from backend.database import engine, Base
from backend.models import user, venue, event, seat, order, ticket, refund, support, order_seat
from backend.routers.auth_router import router as auth_router
from backend.routers.event_router import router as event_router
from backend.routers.booking_router import router as booking_router
from backend.routers.refund_router import router as refund_router
from backend.routers.support_router import router as support_router
from backend.routers.ticket_router import router as ticket_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(booking_router)
app.include_router(refund_router)
app.include_router(support_router)
app.include_router(ticket_router)


@app.get("/")
def home():
    return {"message": "Backend is running"}
