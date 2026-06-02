import streamlit as st
import sqlite3
import pandas as pd

# -------------------------------
# DATABASE
# -------------------------------
conn = sqlite3.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")
conn.commit()

# -------------------------------
# FUNCTIONS
# -------------------------------
def add_product(name, quantity, price):
    cursor.execute(
        "INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price)
    )
    conn.commit()

def update_product(product_id, name, quantity, price):
    cursor.execute(
        """
        UPDATE products
        SET name=?, quantity=?, price=?
        WHERE id=?
        """,
        (name, quantity, price, product_id)
    )
    conn.commit()

def delete_product(product_id):
    cursor.execute(
        "DELETE FROM products WHERE id=?",
        (product_id,)
    )
    conn.commit()

def get_products():
    return pd.read_sql_query(
        "SELECT * FROM products ORDER BY id DESC",
        conn
    )

# -------------------------------
# UI
# -------------------------------
st.set_page_config(
    page_title="Inventory System",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Management System")

# -------------------------------
# METRICS
# -------------------------------
df = get_products()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Products", len(df))

with col2:
    total_stock = int(df["quantity"].sum()) if not df.empty else 0
    st.metric("Total Stock", total_stock)

with col3:
    total_value = (
        (df["quantity"] * df["price"]).sum()
        if not df.empty else 0
    )
    st.metric("Inventory Value", f"₱{total_value:,.2f}")

st.divider()

# -------------------------------
# ADD PRODUCT
# -------------------------------
st.subheader("Add Product")

with st.form("add_form"):
    name = st.text_input("Product Name")
    quantity = st.number_input(
        "Quantity",
        min_value=0,
        step=1
    )
    price = st.number_input(
        "Price",
        min_value=0.0,
        step=0.01
    )

    submit = st.form_submit_button("Add Product")

    if submit:
        if name.strip():
            add_product(name, quantity, price)
            st.success("Product added successfully!")
            st.rerun()
        else:
            st.error("Enter a product name.")

st.divider()

# -------------------------------
# SEARCH
# -------------------------------
search = st.text_input(
    "🔍 Search Product"
)

if not df.empty and search:
    df = df[
        df["name"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

# -------------------------------
# PRODUCT LIST
# -------------------------------
st.subheader("Inventory")

if df.empty:
    st.info("No products found.")
else:
    for _, row in df.iterrows():

        with st.expander(
            f"{row['name']} | Qty: {row['quantity']} | ₱{row['price']:.2f}"
        ):

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"ID: {row['id']}")
                st.write(f"Quantity: {row['quantity']}")
                st.write(f"Price: ₱{row['price']:.2f}")

            with col2:

                new_name = st.text_input(
                    "Name",
                    value=row["name"],
                    key=f"name_{row['id']}"
                )

                new_qty = st.number_input(
                    "Quantity",
                    min_value=0,
                    value=int(row["quantity"]),
                    key=f"qty_{row['id']}"
                )

                new_price = st.number_input(
                    "Price",
                    min_value=0.0,
                    value=float(row["price"]),
                    key=f"price_{row['id']}"
                )

                c1, c2 = st.columns(2)

                with c1:
                    if st.button(
                        "Update",
                        key=f"update_{row['id']}"
                    ):
                        update_product(
                            row["id"],
                            new_name,
                            new_qty,
                            new_price
                        )
                        st.success("Updated!")
                        st.rerun()

                with c2:
                    if st.button(
                        "Delete",
                        key=f"delete_{row['id']}"
                    ):
                        delete_product(row["id"])
                        st.warning("Deleted!")
                        st.rerun()

# -------------------------------
# TABLE VIEW
# -------------------------------
st.divider()
st.subheader("Table View")

table_df = get_products()

if not table_df.empty:
    st.dataframe(
        table_df,
        use_container_width=True
    )
else:
    st.info("No data available.")