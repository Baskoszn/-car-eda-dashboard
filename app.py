import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os

# Set Streamlit page config early
st.set_page_config(page_title="🚗 Car Dashboard", layout="wide")

# Load data with caching
@st.cache_data(show_spinner="Loading vehicle data...")
def load_data():
    path = os.path.join(os.path.dirname(__file__), "vehicles_us.csv")
    df = pd.read_csv(path)
    df = df.dropna(subset=["selling_price", "name", "year", "fuel"])
    return df

df = load_data()

# Page title and description
st.markdown("## 🚗💸 Car Listings Dashboard")
st.markdown("### Explore used car prices by model, year, and fuel type")

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    price_range = st.slider(
        "💰 Selling Price Range",
        int(df.selling_price.min()),
        int(df.selling_price.max()),
        (5000, 30000)
    )
    models = st.multiselect("🚘 Car Models", df["name"].unique(), default=list(df["name"].unique()))
    years = st.multiselect("📆 Year", sorted(df["year"].unique()), default=sorted(df["year"].unique()))
    fuels = st.multiselect("⛽ Fuel Type", df["fuel"].unique(), default=list(df["fuel"].unique()))

# Filter data
filtered_df = df[
    (df["selling_price"] >= price_range[0]) &
    (df["selling_price"] <= price_range[1]) &
    (df["name"].isin(models)) &
    (df["year"].isin(years)) &
    (df["fuel"].isin(fuels))
]

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Selling Price Distribution")
    fig_price = px.histogram(filtered_df, x="selling_price", nbins=30, title="Selling Price Distribution")
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.markdown("#### 📊 Price vs Year (Interactive)")
    scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
        x="year:Q",
        y="selling_price:Q",
        color="fuel:N",
        tooltip=["name", "selling_price", "year", "fuel"]
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

# CSV Export
st.markdown("### 📥 Download Filtered Data")
st.download_button(
    label="⬇️ Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_vehicles.csv",
    mime="text/csv"
)
