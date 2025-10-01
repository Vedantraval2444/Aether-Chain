import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inventory Analysis", page_icon="📦", layout="wide")

API_URL = "http://backend_api:8000"

# Use a session object for caching
if 'session' not in st.session_state:
    st.session_state.session = requests.Session()

@st.cache_data(ttl=60)
def fetch_data(endpoint):
    try:
        response = st.session_state.session.get(f"{API_URL}/{endpoint}?limit=500")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException:
        return pd.DataFrame()

st.title("📦 Advanced Inventory Analysis")

# --- DATA LOADING AND MERGING ---
with st.spinner("Loading inventory data..."):
    inventory_df = fetch_data("inventory/")
    products_df = fetch_data("products/")
    warehouses_df = fetch_data("warehouses/")

if inventory_df.empty or products_df.empty or warehouses_df.empty:
    st.warning("Could not load all necessary data. Please ensure the backend is running and data has been generated.")
    st.stop()

# Merge data for rich analysis
merged_df = pd.merge(inventory_df, products_df, left_on='product_id', right_on='id', suffixes=('_inv', '_prod'))
merged_df['inventory_value'] = merged_df['quantity'] * merged_df['price']

# --- VISUALIZATIONS ---
st.header("Top N Most Stocked Products")
with st.container(border=True):
    top_n = st.slider("Select number of products to display:", 5, 50, 10)
    top_products = merged_df.groupby('name')['quantity'].sum().nlargest(top_n).reset_index()
    fig_top_prod = px.bar(top_products, x='name', y='quantity', title=f'Top {top_n} Most Stocked Products', labels={'name': 'Product Name', 'quantity': 'Total Quantity'})
    st.plotly_chart(fig_top_prod, use_container_width=True)

st.header("Warehouse Utilization")
with st.container(border=True):
    inventory_by_warehouse = merged_df.groupby('warehouse_id')['quantity'].sum().reset_index()
    warehouse_utilization = pd.merge(warehouses_df, inventory_by_warehouse, left_on='id', right_on='warehouse_id')
    fig_wh_util = px.bar(warehouse_utilization, x='location', y=['capacity', 'quantity'], 
                         barmode='group', title='Warehouse Capacity vs. Current Stock',
                         labels={'location': 'Warehouse Location', 'value': 'Count'}, height=500)
    st.plotly_chart(fig_wh_util, use_container_width=True)

st.header("Inventory Value Distribution")
with st.container(border=True):
    fig_treemap = px.treemap(merged_df, path=[px.Constant("All Products"), 'name'], values='inventory_value',
                             title='Inventory Value by Product',
                             color='inventory_value', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_treemap, use_container_width=True)