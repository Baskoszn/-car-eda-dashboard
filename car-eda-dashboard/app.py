import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os

# Set page config early
st.set_page_config(page_title="🚗 Car Dashboard", layout="wide")

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "vehicles_us.csv")
    df = pd.read_csv(path)
    df = df.dropna(subset=["price", "model", "manufacturer"])
    return df

df = load_data()

st.title("🚗 Car Advertisement Dashboard")

# Filters
with st.sidebar:
    st.header("Filters")
    price_range = st.slider("Price Range", int(df.price.min()), int(df.price.max()), (5000, 30000))
    manufacturers = st.multiselect("Manufacturer", df["manufacturer"].unique(), default=list(df["manufacturer"].unique()))

filtered_df = df[
    (df["price"] >= price_range[0]) &
    (df["price"] <= price_range[1]) &
    (df["manufacturer"].isin(manufacturers))
]

# Charts
st.subheader("📈 Price Distribution")
fig_price = px.histogram(filtered_df, x="price", nbins=30, title="Price Distribution")
st.plotly_chart(fig_price, use_container_width=True)

st.subheader("📊 Scatter Plot: Price vs Year")
scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x="model_year:Q",
    y="price:Q",
    color="manufacturer:N",
    tooltip=["model", "price", "model_year"]
).interactive()
st.altair_chart(scatter, use_container_width=True)

# CSV Export
st.subheader("📥 Download Filtered Data")
st.download_button("Download CSV", data=filtered_df.to_csv(index=False), file_name="filtered_vehicles.csv", mime="text/csv")
