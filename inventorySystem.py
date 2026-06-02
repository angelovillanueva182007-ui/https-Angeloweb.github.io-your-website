import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Inventory Dashboard",
    page_icon="📦",
    layout="wide"
)

DATA_FILE = "inventory.csv"

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    color: white;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: bold;
    height: 3em;
}

h1,h2,h3,p,label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(
        columns=["Product", "Flavor", "Quantity", "Price"]
    )

# =========================
# HEADER
# =========================

st.markdown(
    '<div class="main-title">📦 Inventory Management System</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="card">
<h3>Welcome 👋</h3>
<p>Manage products, flavors, quantities and prices easily.</p>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("➕ Add Product")

product = st.sidebar.text_input("Product Name")
flavor = st.sidebar.text_input("Available Flavor")
quantity = st.sidebar.number_input(
    "Quantity",
    min_value=0,
    step=1
)

price = st.sidebar.number_input(
    "Price (₱)",
    min_value=0.0
)

if st.sidebar.button("Add Product"):

    if product:

        new_row = pd.DataFrame({
            "Product": [product],
            "Flavor": [flavor],
            "Quantity": [quantity],
            "Price": [price]
        })

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

        df.to_csv(DATA_FILE, index=False)

        st.success("✅ Product Added")
        st.rerun()

# =========================
# DASHBOARD
# =========================

total_products = len(df)

total_stock = (
    int(df["Quantity"].sum())
    if not df.empty
    else 0
)

inventory_value = (
    (df["Quantity"] * df["Price"]).sum()
    if not df.empty
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📦 Products",
        total_products
    )

with col2:
    st.metric(
        "📊 Total Stock",
        total_stock
    )

with col3:
    st.metric(
        "💰 Inventory Value",
        f"₱{inventory_value:,.2f}"
    )

st.divider()

# =========================
# SEARCH
# =========================

search = st.text_input(
    "🔍 Search Product"
)

if search:
    display_df = df[
        df["Product"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]
else:
    display_df = df

# =========================
# INVENTORY TABLE
# =========================

st.subheader("📋 Inventory")

st.dataframe(
    display_df,
    use_container_width=True
)

st.divider()

# =========================
# EDIT PRODUCT
# =========================

st.subheader("✏ Edit Product")

if not df.empty:

    selected = st.selectbox(
        "Select Product",
        df["Product"]
    )

    row = df[
        df["Product"] == selected
    ].iloc[0]

    new_product = st.text_input(
        "Product",
        value=row["Product"]
    )

    new_flavor = st.text_input(
        "Flavor",
        value=row["Flavor"]
    )

    new_qty = st.number_input(
        "Quantity",
        value=int(row["Quantity"])
    )

    new_price = st.number_input(
        "Price",
        value=float(row["Price"])
    )

    if st.button("Update Product"):

        idx = df[
            df["Product"] == selected
        ].index[0]

        df.loc[idx, "Product"] = new_product
        df.loc[idx, "Flavor"] = new_flavor
        df.loc[idx, "Quantity"] = new_qty
        df.loc[idx, "Price"] = new_price

        df.to_csv(
            DATA_FILE,
            index=False
        )

        st.success(
            "✅ Product Updated"
        )

        st.rerun()

st.divider()

# =========================
# DELETE PRODUCT
# =========================

st.subheader("🗑 Delete Product")

if not df.empty:

    delete_product = st.selectbox(
        "Choose Product",
        df["Product"],
        key="delete"
    )

    if st.button(
        "Delete Product"
    ):

        df = df[
            df["Product"]
            != delete_product
        ]

        df.to_csv(
            DATA_FILE,
            index=False
        )

        st.success(
            "✅ Product Deleted"
        )

        st.rerun()