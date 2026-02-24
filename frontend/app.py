import streamlit as st
from datetime import datetime, date, time

from api import api_request


# Streamlit page settings
st.set_page_config(page_title="Event Ticket Booking", layout="wide")


def init_session():
    # Keep auth state in session for a simple login flow
    if "token" not in st.session_state:
        st.session_state.token = None
    if "role" not in st.session_state:
        st.session_state.role = None


def logout():
    # Clear auth state
    st.session_state.token = None
    st.session_state.role = None


def login_register():
    # Login and registration screen
    st.header("Login / Register")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            payload = {"email": email, "password": password}
            ok, data, error = api_request("POST", "/auth/login", payload=payload)
            if ok:
                st.session_state.token = data["access_token"]
                st.session_state.role = data["role"]
                st.success("Login successful")
            else:
                st.error(error)

    with tab_register:
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        role = st.selectbox(
            "Role",
            ["customer", "admin", "organizer", "entry_manager", "support"]
        )

        if st.button("Register"):
            payload = {
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }
            ok, _, error = api_request("POST", "/auth/register", payload=payload)
            if ok:
                st.success("Registration successful. Please login.")
            else:
                st.error(error)


def show_events():
    # Public event listing for logged-in users
    st.header("Events")
    ok, data, error = api_request("GET", "/booking/events", st.session_state.token)
    if not ok:
        st.error(error)
        return

    if not data:
        st.info("No events found.")
        return

    st.table(data)


def book_tickets():
    # Customer booking flow: select event, seats, create order, pay
    st.header("Book Tickets")

    ok, events, error = api_request("GET", "/booking/events", st.session_state.token)
    if not ok:
        st.error(error)
        return

    if not events:
        st.info("No events available.")
        return

    event_map = {}
    for event in events:
        label = f"{event['id']} - {event['name']}"
        event_map[label] = event

    selected_label = st.selectbox("Select Event", list(event_map.keys()))
    selected_event = event_map[selected_label]

    ok, seats, error = api_request(
        "GET",
        f"/booking/events/{selected_event['id']}/seats",
        st.session_state.token
    )
    if not ok:
        st.error(error)
        return

    available_seats = []
    for seat in seats:
        if seat["status"] == "available":
            available_seats.append(seat)

    if not available_seats:
        st.warning("No available seats for this event.")
        return

    seat_labels = []
    seat_id_map = {}
    for seat in available_seats:
        label = f"{seat['seat_number']} (id {seat['id']})"
        seat_labels.append(label)
        seat_id_map[label] = seat["id"]

    selected_seats = st.multiselect("Select Seats", seat_labels)
    payment_mode = st.selectbox("Payment Mode", ["card", "upi", "cash"])

    if st.button("Create Order"):
        seat_ids = [seat_id_map[label] for label in selected_seats]
        payload = {
            "event_id": selected_event["id"],
            "seat_ids": seat_ids,
            "payment_mode": payment_mode
        }
        ok, order, error = api_request(
            "POST",
            "/booking/orders",
            st.session_state.token,
            payload
        )
        if ok:
            st.success(f"Order created. ID: {order['id']}")
            st.session_state.last_order_id = order["id"]
        else:
            st.error(error)

    if "last_order_id" in st.session_state:
        if st.button("Pay For Last Order"):
            order_id = st.session_state.last_order_id
            ok, _, error = api_request(
                "POST",
                f"/booking/orders/{order_id}/pay",
                st.session_state.token
            )
            if ok:
                st.success("Payment successful.")
            else:
                st.error(error)


def my_orders():
    # Show current user's orders
    st.header("My Orders")
    ok, data, error = api_request("GET", "/booking/my-orders", st.session_state.token)
    if ok:
        st.table(data)
    else:
        st.error(error)


def my_tickets():
    # Show current user's tickets
    st.header("My Tickets")
    ok, data, error = api_request("GET", "/tickets/my", st.session_state.token)
    if ok:
        st.table(data)
    else:
        st.error(error)


def validate_ticket():
    # Entry manager ticket validation
    st.header("Validate Ticket")
    ticket_id = st.number_input("Ticket ID", min_value=1, step=1)
    if st.button("Validate"):
        ok, _, error = api_request(
            "POST",
            f"/tickets/{int(ticket_id)}/validate",
            st.session_state.token
        )
        if ok:
            st.success("Ticket validated successfully.")
        else:
            st.error(error)


def request_refund():
    # Customer refund request
    st.header("Request Refund")
    order_id = st.number_input("Order ID", min_value=1, step=1)
    reason = st.text_input("Reason")
    if st.button("Submit Refund Request"):
        payload = {"order_id": int(order_id), "reason": reason}
        ok, _, error = api_request(
            "POST",
            "/refunds",
            st.session_state.token,
            payload
        )
        if ok:
            st.success("Refund request submitted.")
        else:
            st.error(error)


def my_refunds():
    # Customer refund list
    st.header("My Refund Requests")
    ok, data, error = api_request("GET", "/refunds/my", st.session_state.token)
    if ok:
        st.table(data)
    else:
        st.error(error)


def manage_refunds():
    # Admin/Support refund management
    st.header("All Refund Requests")
    ok, data, error = api_request("GET", "/refunds", st.session_state.token)
    if not ok:
        st.error(error)
        return

    st.table(data)

    refund_id = st.number_input("Refund ID", min_value=1, step=1)
    status = st.selectbox("Status", ["approved", "rejected"])
    if st.button("Update Refund Status"):
        payload = {"status": status}
        ok, _, error = api_request(
            "PATCH",
            f"/refunds/{int(refund_id)}",
            st.session_state.token,
            payload
        )
        if ok:
            st.success("Refund status updated.")
        else:
            st.error(error)


def create_support_case():
    # Customer support case creation
    st.header("Support Request")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    if st.button("Submit Support Case"):
        payload = {"subject": subject, "message": message}
        ok, _, error = api_request(
            "POST",
            "/support",
            st.session_state.token,
            payload
        )
        if ok:
            st.success("Support case created.")
        else:
            st.error(error)


def my_support_cases():
    # Customer support case list
    st.header("My Support Cases")
    ok, data, error = api_request("GET", "/support/my", st.session_state.token)
    if ok:
        st.table(data)
    else:
        st.error(error)


def manage_support_cases():
    # Admin/Support support case management
    st.header("All Support Cases")
    ok, data, error = api_request("GET", "/support", st.session_state.token)
    if not ok:
        st.error(error)
        return

    st.table(data)

    case_id = st.number_input("Case ID", min_value=1, step=1)
    status = st.selectbox("Case Status", ["open", "closed"])
    if st.button("Update Case Status"):
        payload = {"status": status}
        ok, _, error = api_request(
            "PATCH",
            f"/support/{int(case_id)}",
            st.session_state.token,
            payload
        )
        if ok:
            st.success("Support case updated.")
        else:
            st.error(error)


def admin_venue_event():
    # Admin screens for venue and event setup
    st.header("Admin: Venues and Events")

    st.subheader("Create Venue")
    venue_name = st.text_input("Venue Name")
    venue_city = st.text_input("City")
    venue_capacity = st.number_input("Total Capacity", min_value=1, step=1)
    venue_address = st.text_input("Address")
    if st.button("Create Venue"):
        payload = {
            "name": venue_name,
            "city": venue_city,
            "total_capacity": int(venue_capacity),
            "address": venue_address
        }
        ok, _, error = api_request(
            "POST",
            "/events/venues",
            st.session_state.token,
            payload
        )
        if ok:
            st.success("Venue created.")
        else:
            st.error(error)

    st.subheader("Create Event")
    event_name = st.text_input("Event Name")
    event_desc = st.text_area("Description")
    event_category = st.text_input("Category")
    event_date = st.date_input("Event Date", date.today())
    event_time = st.time_input("Event Time", time(18, 0))
    event_price = st.number_input("Ticket Price", min_value=0, step=1)
    venue_id = st.number_input("Venue ID", min_value=1, step=1)
    organizer_id = st.number_input("Organizer ID", min_value=1, step=1)

    if st.button("Create Event"):
        event_datetime = datetime.combine(event_date, event_time)
        payload = {
            "name": event_name,
            "description": event_desc,
            "category": event_category,
            "event_date": event_datetime.isoformat(),
            "ticket_price": int(event_price),
            "venue_id": int(venue_id),
            "organizer_id": int(organizer_id)
        }
        ok, _, error = api_request(
            "POST",
            "/events",
            st.session_state.token,
            payload
        )
        if ok:
            st.success("Event created.")
        else:
            st.error(error)

    st.subheader("Update Event Status")
    update_event_id = st.number_input("Event ID to Update", min_value=1, step=1)
    status = st.selectbox("Event Status", ["upcoming", "closed", "cancelled"])
    if st.button("Update Status"):
        payload = {"status": status}
        ok, _, error = api_request(
            "PATCH",
            f"/events/{int(update_event_id)}/status",
            st.session_state.token,
            payload
        )
        if ok:
            st.success("Event status updated.")
        else:
            st.error(error)


def organizer_seats_orders():
    # Organizer screens for seat creation and order viewing
    st.header("Organizer: Seats and Orders")

    st.subheader("Add Seats to Event")
    event_id = st.number_input("Event ID", min_value=1, step=1)
    seat_numbers = st.text_area("Seat Numbers (comma separated)")
    if st.button("Add Seats"):
        seat_list = []
        raw = seat_numbers.split(",")
        for item in raw:
            trimmed = item.strip()
            if trimmed:
                seat_list.append({"seat_number": trimmed, "status": "available"})

        ok, _, error = api_request(
            "POST",
            f"/events/{int(event_id)}/seats",
            st.session_state.token,
            seat_list
        )
        if ok:
            st.success("Seats added.")
        else:
            st.error(error)

    st.subheader("View Event Orders")
    orders_event_id = st.number_input("Event ID for Orders", min_value=1, step=1)
    if st.button("Fetch Orders"):
        ok, data, error = api_request(
            "GET",
            f"/events/{int(orders_event_id)}/orders",
            st.session_state.token
        )
        if ok:
            st.table(data)
        else:
            st.error(error)


def render_app():
    # Main page router based on role
    st.title("Online Event Ticket Booking System")

    if not st.session_state.token:
        login_register()
        return

    st.sidebar.button("Logout", on_click=logout)

    role = st.session_state.role

    if role == "customer":
        page = st.sidebar.selectbox(
            "Customer Menu",
            [
                "Browse Events",
                "Book Tickets",
                "My Orders",
                "My Tickets",
                "Refund Request",
                "My Refunds",
                "Support Request",
                "My Support Cases"
            ]
        )

        if page == "Browse Events":
            show_events()
        elif page == "Book Tickets":
            book_tickets()
        elif page == "My Orders":
            my_orders()
        elif page == "My Tickets":
            my_tickets()
        elif page == "Refund Request":
            request_refund()
        elif page == "My Refunds":
            my_refunds()
        elif page == "Support Request":
            create_support_case()
        elif page == "My Support Cases":
            my_support_cases()

    elif role == "admin":
        page = st.sidebar.selectbox(
            "Admin Menu",
            [
                "Venues and Events",
                "All Refunds",
                "All Support Cases"
            ]
        )

        if page == "Venues and Events":
            admin_venue_event()
        elif page == "All Refunds":
            manage_refunds()
        elif page == "All Support Cases":
            manage_support_cases()

    elif role == "organizer":
        page = st.sidebar.selectbox(
            "Organizer Menu",
            [
                "Add Seats and View Orders"
            ]
        )

        if page == "Add Seats and View Orders":
            organizer_seats_orders()

    elif role == "entry_manager":
        page = st.sidebar.selectbox(
            "Entry Manager Menu",
            [
                "Validate Ticket"
            ]
        )
        if page == "Validate Ticket":
            validate_ticket()

    elif role == "support":
        page = st.sidebar.selectbox(
            "Support Menu",
            [
                "All Refunds",
                "All Support Cases"
            ]
        )
        if page == "All Refunds":
            manage_refunds()
        elif page == "All Support Cases":
            manage_support_cases()

    else:
        st.warning("Unknown role. Please contact admin.")


# Boot the app
init_session()
render_app()
