import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supplier Explorer", page_icon="🔗", layout="wide")

API_URL = "http://backend_api:8000"

@st.cache_data(ttl=60)
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}?limit=500")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException:
        return pd.DataFrame()

st.title("🔗 Supplier & Graph Explorer")

# --- GRAPH EXPLORER ---
st.header("Supply Chain Path Explorer")
with st.container(border=True):
    products_df = fetch_data("products/")
    if not products_df.empty:
        product_name = st.selectbox("Select a Product to Trace:", products_df['name'].unique())
        if st.button("Trace Supply Path"):
            with st.spinner("Querying graph database..."):
                try:
                    res = requests.get(f"{API_URL}/graph/product-path/{product_name}")
                    res.raise_for_status()
                    path_data = res.json()
                    
                    st.success(f"Path Found for **{path_data['product']}**!")
                    st.graphviz_chart(f'''
                    digraph {{
                        rankdir=LR;
                        node [shape=box, style=rounded, fontname="sans-serif"];
                        "{path_data['country']}" -> "{path_data['supplier']}" [label="Based In"];
                        "{path_data['supplier']}" -> "{path_data['product']}" [label="Supplies"];
                    }}
                    ''')
                except requests.exceptions.RequestException:
                    st.error(f"Could not find supply path for {product_name}.")
    else:
        st.warning("No products available to trace.")

# --- SUPPLIER ANALYSIS ---
st.header("Suppliers by Country")
with st.container(border=True):
    suppliers_df = fetch_data("suppliers/")
    if not suppliers_df.empty:
        country_counts = suppliers_df['country'].value_counts().reset_index()
        country_counts.columns = ['country', 'count']
        fig = px.bar(country_counts, x='country', y='count', title='Number of Suppliers per Country')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No supplier data to display.")