from datetime import datetime, timedelta
import random
import os
import sys

# Ensure project root is on sys.path for direct script execution
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.database import SessionLocal, Base, engine
from backend.models.user import User
from backend.models.venue import Venue
from backend.models.event import Event
from backend.models.seat import Seat
from backend.models.order import Order
from backend.models.order_seat import OrderSeat
from backend.models.ticket import Ticket
from backend.models.refund import RefundRequest
from backend.models.support import SupportCase
from backend.utils.hash import hash_password


def seed():
    # Drop all existing tables and recreate them to sync with models
    print("Resetting database schema...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database schema recreated.")

    db = SessionLocal()
    try:
        random.seed(42)
        
        print("Creating users...")
        # Create users
        admin = User(
            name="Admin User",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            role="admin"
        )
        organizer = User(
            name="Organizer User",
            email="organizer@example.com",
            password_hash=hash_password("organizer123"),
            role="organizer"
        )
        entry_manager = User(
            name="Entry Manager",
            email="entry@example.com",
            password_hash=hash_password("entry123"),
            role="entry_manager"
        )
        support = User(
            name="Support User",
            email="support@example.com",
            password_hash=hash_password("support123"),
            role="support"
        )

        # Extra customers for demo
        customers = []
        for i in range(1, 6):
            customers.append(
                User(
                    name=f"Customer {i}",
                    email=f"customer{i}@example.com",
                    password_hash=hash_password("customer123"),
                    role="customer"
                )
            )

        db.add_all([admin, organizer, entry_manager, support] + customers)
        db.commit()
        
        print("Creating venues and events...")

        # Create venues
        venues = [
            Venue(
                name="City Hall Arena",
                city="New York",
                total_capacity=120,
                address="123 Main Street, New York"
            ),
            Venue(
                name="Lakeside Expo",
                city="Chicago",
                total_capacity=150,
                address="88 Lake Road, Chicago"
            ),
            Venue(
                name="Sunset Theatre",
                city="San Francisco",
                total_capacity=90,
                address="501 Sunset Blvd, San Francisco"
            )
        ]
        db.add_all(venues)
        db.commit()

        # Create events with mixed statuses
        now = datetime.utcnow()
        events = [
            Event(
                name="Live Concert Night",
                description="An evening of live music.",
                category="Music",
                event_date=now + timedelta(days=7),
                ticket_price=500,
                venue_id=venues[0].id,
                organizer_id=organizer.id,
                status="upcoming"
            ),
            Event(
                name="Tech Summit 2026",
                description="Talks, demos, and networking.",
                category="Conference",
                event_date=now + timedelta(days=14),
                ticket_price=800,
                venue_id=venues[1].id,
                organizer_id=organizer.id,
                status="upcoming"
            ),
            Event(
                name="Food Carnival",
                description="Street food and live shows.",
                category="Festival",
                event_date=now + timedelta(days=3),
                ticket_price=300,
                venue_id=venues[2].id,
                organizer_id=organizer.id,
                status="upcoming"
            ),
            Event(
                name="Retro Movie Night",
                description="Classic cinema experience.",
                category="Film",
                event_date=now - timedelta(days=2),
                ticket_price=250,
                venue_id=venues[2].id,
                organizer_id=organizer.id,
                status="closed"
            ),
            Event(
                name="Cancelled Workshop",
                description="Event cancelled for demo.",
                category="Workshop",
                event_date=now + timedelta(days=10),
                ticket_price=400,
                venue_id=venues[1].id,
                organizer_id=organizer.id,
                status="cancelled"
            )
        ]
        db.add_all(events)
        db.commit()

        # Create seats per event
        for event in events:
            for i in range(1, 31):
                seat = Seat(
                    event_id=event.id,
                    seat_number=f"A{i}",
                    status="available"
                )
                db.add(seat)
        db.commit()

        # Create sample orders and tickets for customers
        customers_db = db.query(User).filter(User.role == "customer").all()
        upcoming_events = [e for e in events if e.status == "upcoming"]

        for customer in customers_db:
            # Two orders per customer
            for _ in range(2):
                event = random.choice(upcoming_events)
                seats = db.query(Seat).filter(
                    Seat.event_id == event.id,
                    Seat.status == "available"
                ).limit(2).all()

                if not seats:
                    continue

                for seat in seats:
                    seat.status = "booked"

                order = Order(
                    user_id=customer.id,
                    event_id=event.id,
                    total_amount=event.ticket_price * len(seats),
                    payment_mode=random.choice(["card", "upi", "cash"]),
                    order_status="confirmed"
                )
                db.add(order)
                db.commit()
                db.refresh(order)

                for seat in seats:
                    link = OrderSeat(order_id=order.id, seat_id=seat.id)
                    db.add(link)
                    ticket = Ticket(order_id=order.id, seat_id=seat.id, status="valid")
                    db.add(ticket)

                db.commit()

        # Create refund requests (mix of pending, approved, rejected)
        some_orders = db.query(Order).limit(3).all()
        for i, order in enumerate(some_orders):
            status = ["pending", "approved", "rejected"][i % 3]
            refund = RefundRequest(
                order_id=order.id,
                user_id=order.user_id,
                reason="Unable to attend",
                message="Requesting refund for demo",
                status=status
            )
            db.add(refund)

            if status == "approved":
                order.order_status = "refunded"
                order_seats = db.query(OrderSeat).filter(
                    OrderSeat.order_id == order.id
                ).all()
                for order_seat in order_seats:
                    seat = db.query(Seat).filter(Seat.id == order_seat.seat_id).first()
                    if seat:
                        seat.status = "available"
                    ticket = db.query(Ticket).filter(
                        Ticket.order_id == order.id,
                        Ticket.seat_id == order_seat.seat_id
                    ).first()
                    if ticket:
                        ticket.status = "refunded"

        db.commit()

        # Create support cases
        for i, customer in enumerate(customers_db[:3], start=1):
            case = SupportCase(
                user_id=customer.id,
                subject=f"Support Request {i}",
                message="Need help with booking for demo",
                status="open" if i % 2 == 1 else "closed"
            )
            db.add(case)

        db.commit()

        print("Seed data inserted successfully.")
        print("Logins:")
        print("admin@example.com / admin123")
        print("organizer@example.com / organizer123")
        print("customer1@example.com / customer123")
        print("customer2@example.com / customer123")
        print("customer3@example.com / customer123")
        print("entry@example.com / entry123")
        print("support@example.com / support123")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
