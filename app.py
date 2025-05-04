import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os

# Set Streamlit page config early
st.set_page_config(page_title="🚗 Car Dashboard", layout="wide")

# Load data with caching
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "vehicles_us.csv")
    df = pd.read_csv(path)
    df = df.dropna(subset=["selling_price", "name", "year"])
    return df

df = load_data()

st.title("🚗 Car Advertisement Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    price_range = st.slider(
        "Selling Price Range", 
        int(df.selling_price.min()), 
        int(df.selling_price.max()), 
        (5000, 30000)
    )
    models = st.multiselect("Car Models", df["name"].unique(), default=list(df["name"].unique()))

# Filter the data
filtered_df = df[
    (df["selling_price"] >= price_range[0]) &
    (df["selling_price"] <= price_range[1]) &
    (df["name"].isin(models))
]

# Price Distribution chart
st.subheader("📈 Selling Price Distribution")
fig_price = px.histogram(filtered_df, x="selling_price", nbins=30, title="Selling Price Distribution")
st.plotly_chart(fig_price, use_container_width=True)

# Scatter plot: Price vs Year
st.subheader("📊 Scatter Plot: Price vs Year")
scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x="year:Q",
    y="selling_price:Q",
    color="fuel:N",
    tooltip=["name", "selling_price", "year"]
).interactive()
st.altair_chart(scatter, use_container_width=True)

# CSV Export
st.subheader("📥 Download Filtered Data")
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_vehicles.csv",
    mime="text/csv"
)
