import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import datetime

# ---------- DATABASE ----------
conn = sqlite3.connect('inventory.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quantity INTEGER,
    price REAL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    quantity INTEGER,
    total REAL,
    date TEXT
)''')

conn.commit()

# ---------- FUNCTIONS ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

def add_item(name, quantity, price):
    c.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
              (name, quantity, price))
    conn.commit()

def get_items():
    c.execute("SELECT * FROM inventory")
    return c.fetchall()

def record_sale(name, qty, price):
    total = qty * price
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("INSERT INTO sales (item_name, quantity, total, date) VALUES (?, ?, ?, ?)",
              (name, qty, total, date))

    # reduce stock
    c.execute("UPDATE inventory SET quantity = quantity - ? WHERE name=?",
              (qty, name))

    conn.commit()

def get_sales():
    c.execute("SELECT * FROM sales")
    return c.fetchall()

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- UI STYLE ----------
st.set_page_config(page_title="Inventory System", layout="wide")

st.markdown("""
    <style>
    .metric-card {
        padding: 15px;
        border-radius: 12px;
        background-color: #1e1e1e;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGIN / REGISTER ----------
st.title("📦 Smart Inventory Dashboard")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if menu == "Register":
    st.subheader("Create Account")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        if add_user(u, p):
            st.success("Account created!")
        else:
            st.error("Username exists")

elif menu == "Login":
    st.subheader("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(u, p):
            st.session_state.logged_in = True
            st.success("Welcome!")
        else:
            st.error("Invalid login")

# ---------- MAIN DASHBOARD ----------
if st.session_state.logged_in:

    st.sidebar.success("Logged In")

    page = st.sidebar.selectbox("Navigation", [
        "Dashboard",
        "Inventory",
        "Sales",
        "Analytics"
    ])

    # ---------- DASHBOARD ----------
    if page == "Dashboard":
        st.header("📊 Overview")

        items = get_items()
        sales = get_sales()

        total_items = len(items)
        total_sales = sum([s[3] for s in sales]) if sales else 0
        total_orders = len(sales)

        col1, col2, col3 = st.columns(3)

        col1.metric("Items", total_items)
        col2.metric("Revenue", f"₱{total_sales:.2f}")
        col3.metric("Orders", total_orders)

    # ---------- INVENTORY ----------
    elif page == "Inventory":
        st.header("📦 Inventory")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Add Item")
            name = st.text_input("Item Name")
            qty = st.number_input("Quantity", min_value=1)
            price = st.number_input("Price", min_value=0.0)

            if st.button("Add Item"):
                add_item(name, qty, price)
                st.success("Added!")

        with col2:
            st.subheader("Current Stock")
            df = pd.DataFrame(get_items(), columns=["ID", "Name", "Qty", "Price"])
            st.dataframe(df, use_container_width=True)

    # ---------- SALES ----------
    elif page == "Sales":
        st.header("💰 Record Sale")

        items = get_items()
        item_names = [i[1] for i in items]

        selected = st.selectbox("Select Item", item_names)

        qty = st.number_input("Quantity", min_value=1)

        item_data = [i for i in items if i[1] == selected][0]
        price = item_data[3]

        st.write(f"Price: ₱{price}")

        if st.button("Confirm Sale"):
            record_sale(selected, qty, price)