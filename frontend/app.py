import streamlit as st
import pandas as pd
from datetime import datetime, date, time

from api import api_request


# Streamlit page settings
st.set_page_config(page_title="Event Ticket Booking", layout="wide")


def apply_global_styles():
    st.markdown(
        """
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;700&display=swap");

        html, body, [class*="css"]  {
            font-family: "Manrope", sans-serif;
        }
        .stApp {
            background: radial-gradient(1200px 600px at 20% -10%, #0b1220 0%, #0b1220 45%, #0f172a 100%);
            color: #e2e8f0;
        }
        .block-container {
            padding-top: 2rem;
        }
        .app-hero {
            padding: 1.25rem 1.5rem;
            border-radius: 18px;
            border: 1px solid #1f2937;
            background: linear-gradient(135deg, #0f172a 0%, #111827 60%, #0f172a 100%);
            color: #f8fafc;
            margin-bottom: 1.25rem;
            box-shadow: 0 10px 30px rgba(2, 6, 23, 0.6);
        }
        .app-hero h1 {
            font-size: 1.8rem;
            margin: 0 0 0.35rem 0;
            font-weight: 700;
        }
        .app-hero p {
            margin: 0;
            color: #94a3b8;
        }
        .card {
            padding: 1rem 1.1rem;
            border-radius: 16px;
            border: 1px solid #1f2937;
            background: #0f172a;
            box-shadow: 0 6px 18px rgba(2, 6, 23, 0.45);
        }
        .card-title {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 0.15rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .card-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #f8fafc;
        }
        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #e2e8f0;
            margin: 0.5rem 0 0.75rem 0;
        }
        .sidebar-brand {
            font-weight: 700;
            font-size: 1.05rem;
            color: #e2e8f0;
        }
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox select,
        .stMultiSelect select,
        .stDateInput input,
        .stTimeInput input {
            background-color: #0b1220 !important;
            color: #e2e8f0 !important;
            border: 1px solid #1f2937 !important;
        }
        .stButton>button {
            background: #2563eb;
            color: #ffffff;
            border: 0;
            border-radius: 10px;
            padding: 0.45rem 1rem;
            font-weight: 600;
        }
        .stButton>button:hover {
            background: #1d4ed8;
            color: #ffffff;
        }
        .stDataFrame, .stTable {
            background: #0b1220;
            color: #e2e8f0;
        }
        div[data-testid="stSidebar"] {
            background-color: #0b1220;
            border-right: 1px solid #1f2937;
        }
        div[data-testid="stSidebar"] * {
            color: #e2e8f0;
        }
        .stTabs [role="tab"] {
            color: #cbd5f5;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            color: #f8fafc;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="app-hero">
            <h1>Online Event Ticket Booking System</h1>
            <p>Discover events, reserve seats, and manage your bookings with clarity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def to_dataframe(data):
    if data is None:
        return pd.DataFrame()
    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict):
        return pd.DataFrame([data])
    return pd.DataFrame({"value": [data]})


def show_table(data, height=360, key=None):
    df = to_dataframe(data)
    if df.empty:
        st.info("No data to display.")
        return
    st.dataframe(
        df,
        use_container_width=True,
        height=height,
        hide_index=True,
        key=key,
    )


def metric_row(items):
    cols = st.columns(len(items))
    for idx, item in enumerate(items):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">{item['label']}</div>
                    <div class="card-value">{item['value']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


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
    st.markdown('<div class="section-title">Login or create your account</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="section-title">Events</div>', unsafe_allow_html=True)
    ok, data, error = api_request("GET", "/booking/events", st.session_state.token)
    if not ok:
        st.error(error)
        return

    if not data:
        st.info("No events found.")
        return
    metric_row(
        [
            {"label": "Events", "value": len(data)},
            {"label": "Categories", "value": len({item.get("category") for item in data if item.get("category")})},
            {"label": "Cities", "value": len({item.get("city") for item in data if item.get("city")})},
        ]
    )
    show_table(data)


def book_tickets():
    # Customer booking flow: select event, seats, create order, pay
    st.markdown('<div class="section-title">Book Tickets</div>', unsafe_allow_html=True)

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
    with st.container():
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Selected Event</div>
                <div class="card-value">{selected_event.get('name', 'Event')}</div>
                <div style="color:#475569; margin-top:0.25rem;">
                    {selected_event.get('category', 'General')} · {selected_event.get('event_date', 'TBA')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

    metric_row(
        [
            {"label": "Available Seats", "value": len(available_seats)},
            {"label": "Price", "value": selected_event.get("ticket_price", "N/A")},
            {"label": "Venue", "value": selected_event.get("venue_id", "N/A")},
        ]
    )

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
    st.markdown('<div class="section-title">My Orders</div>', unsafe_allow_html=True)
    ok, data, error = api_request("GET", "/booking/my-orders", st.session_state.token)
    if ok:
        show_table(data)
    else:
        st.error(error)


def my_tickets():
    # Show current user's tickets
    st.markdown('<div class="section-title">My Tickets</div>', unsafe_allow_html=True)
    ok, data, error = api_request("GET", "/tickets/my", st.session_state.token)
    if ok:
        show_table(data)
    else:
        st.error(error)


def validate_ticket():
    # Entry manager ticket validation
    st.markdown('<div class="section-title">Validate Ticket</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-title">Request Refund</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-title">My Refund Requests</div>', unsafe_allow_html=True)
    ok, data, error = api_request("GET", "/refunds/my", st.session_state.token)
    if ok:
        show_table(data)
    else:
        st.error(error)


def manage_refunds():
    # Admin/Support refund management
    st.markdown('<div class="section-title">All Refund Requests</div>', unsafe_allow_html=True)
    ok, data, error = api_request("GET", "/refunds", st.session_state.token)
    if not ok:
        st.error(error)
        return

    show_table(data)

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
    st.markdown('<div class="section-title">Support Request</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="section-title">My Support Cases</div>', unsafe_allow_html=True)
    ok, data, error = api_request("GET", "/support/my", st.session_state.token)
    if ok:
        show_table(data)
    else:
        st.error(error)


def manage_support_cases():
    # Admin/Support support case management
    st.markdown('<div class="section-title">All Support Cases</div>', unsafe_allow_html=True)
    ok, data, error = api_request("GET", "/support", st.session_state.token)
    if not ok:
        st.error(error)
        return

    show_table(data)

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
    st.markdown('<div class="section-title">Admin: Venues and Events</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="section-title">Organizer: Seats and Orders</div>', unsafe_allow_html=True)

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
            show_table(data)
        else:
            st.error(error)


def render_app():
    # Main page router based on role
    apply_global_styles()
    render_hero()

    if not st.session_state.token:
        login_register()
        return

    st.sidebar.markdown('<div class="sidebar-brand">Event Console</div>', unsafe_allow_html=True)
    st.sidebar.caption("Manage bookings, events, and support")
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
