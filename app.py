import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import os

# Page setup
st.set_page_config(page_title="🚗 Car Dashboard", layout="wide")

# CSS styling
st.markdown("""
    <style>
        .main { background-color: #f4f6f9; }
        .sidebar .sidebar-content { background-color: #ffffff; padding: 20px; }
        .stSlider, .stMultiSelect, .stSelectbox { color: #333333 !important; }
        .metric-box {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")

    # Expected columns
    required_cols = ["price", "model", "manufacturer", "model_year"]

    # Check which columns are missing
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Missing required column(s) in CSV: {', '.join(missing_cols)}")
        st.stop()

    # Clean
    df = df.dropna(subset=required_cols)
    return df


df = load_data()

st.title("🚗 Car Advertisement Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("🎛️ Filter Listings")

    price_range = st.slider(
        "💰 Price Range",
        int(df["price"].min()), int(df["price"].max()),
        (5000, 30000)
    )

    manufacturers = st.multiselect(
        "🏭 Manufacturer",
        options=sorted(df["manufacturer"].unique()),
        default=list(df["manufacturer"].unique())
    )

    filtered_models = df[df["manufacturer"].isin(manufacturers)]["model"].unique()
    models = st.multiselect(
        "🚘 Model",
        options=sorted(filtered_models),
        default=sorted(filtered_models)
    )

    min_year, max_year = int(df["model_year"].min()), int(df["model_year"].max())
    year_range = st.slider(
        "📅 Model Year Range",
        min_year, max_year, (min_year, max_year)
    )

# Apply filters
filtered_df = df[
    (df["price"].between(price_range[0], price_range[1])) &
    (df["manufacturer"].isin(manufacturers)) &
    (df["model"].isin(models)) &
    (df["model_year"].between(year_range[0], year_range[1]))
]

# Key metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='metric-box'><h4>Total Listings</h4><h2>📦 {:,}</h2></div>".format(len(filtered_df)), unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-box'><h4>Average Price</h4><h2>💵 ${:,.0f}</h2></div>".format(filtered_df["price"].mean()), unsafe_allow_html=True)
with col3:
    st.markdown("<div class='metric-box'><h4>Top Manufacturer</h4><h2>🏆 {}</h2></div>".format(filtered_df["manufacturer"].mode().iloc[0]), unsafe_allow_html=True)

# Charts
st.subheader("📈 Price Distribution")
fig_price = px.histogram(
    filtered_df, x="price", nbins=30,
    title="Distribution of Vehicle Prices",
    color_discrete_sequence=["#2c7be5"]
)
fig_price.update_layout(plot_bgcolor="#f9f9f9", paper_bgcolor="#f9f9f9")
st.plotly_chart(fig_price, use_container_width=True)

st.subheader("🌀 Price vs Model Year")
scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x=alt.X("model_year:Q", title="Model Year"),
    y=alt.Y("price:Q", title="Price (USD)"),
    color="manufacturer:N",
    tooltip=["model", "price", "model_year"]
).interactive().properties(
    height=400
)
st.altair_chart(scatter, use_container_width=True)

# Download
st.subheader("📥 Download Filtered Results")
st.download_button(
    label="Download CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_vehicles.csv",
    mime="text/csv"
)
