import streamlit as st
import requests
import uuid
from datetime import date

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

st.title("💰 Personal Expense Tracker")
st.caption("Track where your money is going")

# ── Initialise session state ──────────────────────────────────────────────────
if "idempotency_key" not in st.session_state:
    st.session_state.idempotency_key = str(uuid.uuid4())
if "success_message" not in st.session_state:
    st.session_state.success_message = None


# ── Helper ────────────────────────────────────────────────────────────────────
def fetch_expenses(category=None):
    try:
        params = {"sort": "date_desc"}
        if category and category != "All":
            params["category"] = category
        response = requests.get(f"{API_URL}/expenses", params=params, timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.ConnectionError:
        return [], "Cannot connect to backend. Make sure the API server is running."
    except requests.exceptions.Timeout:
        return [], "Request timed out. Please try again."
    except Exception as e:
        return [], f"Unexpected error: {str(e)}"


# ── Layout ────────────────────────────────────────────────────────────────────
col_form, col_list = st.columns([1, 2])

# ── Left column: Add Expense Form ─────────────────────────────────────────────
with col_form:
    st.subheader("Add New Expense")

    CATEGORIES = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Utilities", "Other"]

    with st.form("add_expense_form", clear_on_submit=True):
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            step=0.01,
            format="%.2f",
            help="Enter amount in rupees"
        )
        category = st.selectbox("Category", CATEGORIES)
        description = st.text_input("Description", placeholder="e.g. Lunch at café")
        expense_date = st.date_input("Date", value=date.today())
        submitted = st.form_submit_button("Add Expense", use_container_width=True)

        if submitted:
            if not description.strip():
                st.error("Please enter a description.")
            elif amount <= 0:
                st.error("Amount must be greater than zero.")
            else:
                payload = {
                    "amount": round(amount, 2),
                    "category": category,
                    "description": description.strip(),
                    "date": str(expense_date),
                    "idempotency_key": st.session_state.idempotency_key,
                }
                try:
                    with st.spinner("Saving..."):
                        res = requests.post(
                            f"{API_URL}/expenses",
                            json=payload,
                            timeout=5
                        )
                    if res.status_code in (200, 201):
                        st.session_state.success_message = f"✅ Expense of ₹{amount:.2f} added!"
                        # Rotate key so next submission is fresh
                        st.session_state.idempotency_key = str(uuid.uuid4())
                        st.rerun()
                    else:
                        st.error(f"Failed to add expense: {res.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Make sure the API server is running.")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try again.")

    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None


# ── Right column: Expense List ────────────────────────────────────────────────
with col_list:
    st.subheader("My Expenses")

    # Filter
    filter_col, refresh_col = st.columns([3, 1])
    with filter_col:
        CATEGORIES_FILTER = ["All", "Food", "Transport", "Shopping", "Health", "Entertainment", "Utilities", "Other"]
        selected_category = st.selectbox("Filter by category", CATEGORIES_FILTER, label_visibility="collapsed")
    with refresh_col:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Fetch
    expenses, error = fetch_expenses(selected_category)

    if error:
        st.error(error)
    elif not expenses:
        st.info("No expenses found. Add your first expense!")
    else:
        # Total
        total = sum(e["amount"] for e in expenses)
        st.metric(label="Total", value=f"₹{total:,.2f}")

        st.divider()

        # Category summary
        with st.expander("📊 Total by Category"):
            category_totals = {}
            for e in expenses:
                category_totals[e["category"]] = category_totals.get(e["category"], 0) + e["amount"]
            for cat, amt in sorted(category_totals.items(), key=lambda x: -x[1]):
                st.write(f"**{cat}**: ₹{amt:,.2f}")

        st.divider()

        # Expense rows
        for expense in expenses:
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.write(f"**{expense['description']}**")
                    st.caption(f"📅 {expense['date']}  •  🏷️ {expense['category']}")
                with c2:
                    st.write("")
                with c3:
                    st.markdown(f"### ₹{expense['amount']:,.2f}")
                st.divider()