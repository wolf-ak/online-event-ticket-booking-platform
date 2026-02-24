from fastapi import FastAPI
from backend.database import engine, Base
from backend.models import user, venue, event, seat, order, ticket

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Backend is running"}