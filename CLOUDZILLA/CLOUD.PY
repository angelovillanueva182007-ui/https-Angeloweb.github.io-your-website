import streamlit as st
import pandas as pd
import os

# ======================
# CONFIG
# ======================

st.set_page_config(
    page_title="CloudZilla Inventory",
    page_icon="📦",
    layout="wide"
)

DATA_FILE = "inventory.csv"

# ======================
# LOAD DATA
# ======================

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=[
        "Product",
        "Cost Price",
        "Selling Price",
        "Quantity"
    ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# ======================
# CUSTOM CSS
# ======================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f5f7fa,#c3cfe2);
}

.card {
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);
    text-align:center;
}

.metric-value {
    font-size:32px;
    font-weight:bold;
}

.metric-title {
    color:gray;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================

st.title("✨ CloudZilla Inventory System")

# ======================
# SIDEBAR
# ======================

st.sidebar.header("➕ Add Product")

with st.sidebar.form("add_form"):

    product = st.text_input("Product Name")

    cost = st.number_input(
        "Cost Price (₱)",
        min_value=0.0,
        format="%.2f"
    )

    selling = st.number_input(
        "Selling Price (₱)",
        min_value=0.0,
        format="%.2f"
    )

    qty = st.number_input(
        "Quantity",
        min_value=0,
        step=1
    )

    submit = st.form_submit_button("Add Product")

if submit:

    new_row = pd.DataFrame([{
        "Product": product,
        "Cost Price": cost,
        "Selling Price": selling,
        "Quantity": qty
    }])

    df = pd.concat([df, new_row], ignore_index=True)

    save_data(df)

    st.success("Product added!")
    st.rerun()

# ======================
# SEARCH
# ======================

search = st.text_input(
    "🔍 Search Product"
)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Product"]
        .astype(str)
        .str.contains(search, case=False)
    ]

# ======================
# STATS
# ======================

total_products = len(df)

total_qty = (
    df["Quantity"].sum()
    if not df.empty else 0
)

inventory_cost = (
    (df["Cost Price"] * df["Quantity"]).sum()
    if not df.empty else 0
)

profit = (
    ((df["Selling Price"] - df["Cost Price"])
    * df["Quantity"]).sum()
    if not df.empty else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Products", total_products)

with col2:
    st.metric("🧮 Quantity", int(total_qty))

with col3:
    st.metric(
        "💸 Inventory Cost",
        f"₱{inventory_cost:,.2f}"
    )

with col4:
    st.metric(
        "📈 Potential Profit",
        f"₱{profit:,.2f}"
    )

st.divider()

# ======================
# TABLE
# ======================

if not filtered_df.empty:

    filtered_df["Total Value"] = (
        filtered_df["Selling Price"]
        * filtered_df["Quantity"]
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

else:
    st.info("No products found.")

# ======================
# DELETE PRODUCT
# ======================

st.subheader("🗑 Remove Product")

if not df.empty:

    item_to_delete = st.selectbox(
        "Select Product",
        df["Product"]
    )

    if st.button("Delete Product"):

        df = df[df["Product"] != item_to_delete]

        save_data(df)

        st.success("Product deleted!")
        st.rerun()

# ======================
# CLEAR ALL
# ======================

st.subheader("⚠ Inventory Actions")

if st.button("Clear All Inventory"):

    df = pd.DataFrame(columns=[
        "Product",
        "Cost Price",
        "Selling Price",
        "Quantity"
    ])

    save_data(df)

    st.success("Inventory cleared!")
    st.rerun()