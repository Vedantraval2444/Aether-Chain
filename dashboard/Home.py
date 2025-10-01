import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AetherChain Home", page_icon="🏠", layout="wide")

API_URL = "http://backend_api:8000"

@st.cache_data(ttl=60)
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {endpoint}: {e}")
        return pd.DataFrame()

st.title("🏠 AetherChain: Supply Chain Intelligence Hub")
st.markdown("Welcome to the central command for your supply chain. Get instant alerts and an overview of your operations.")

st.divider()

# --- LOW STOCK ALERTS ---
st.header("⚠️ Low Stock Alerts")
with st.container(border=True):
    alerts_df = fetch_data("inventory/alerts/")
    if not alerts_df.empty:
        st.error(f"Found {len(alerts_df)} products with low stock!")
        st.dataframe(alerts_df, use_container_width=True)
    else:
        st.success("All products are adequately stocked. No alerts.")
        
st.divider()

# --- HIGH-LEVEL KPIS ---
st.header("Operational Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Suppliers", fetch_data("suppliers/").shape[0])
with col2:
    st.metric("Total Unique Products", fetch_data("products/").shape[0])
with col3:
    st.metric("Total Warehouses", fetch_data("warehouses/").shape[0])