import streamlit as st
import plotly.express as px
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import load_data, sidebar_filters


# ==========================================================
# Load dataset and apply shared filters
# ==========================================================
df, p95 = load_data()
filtered = sidebar_filters(df, p95)


# ==========================================================
# Page Header
# ==========================================================
st.title("Neighbourhood Price Comparison")
st.caption("Compare one neighbourhood with the currently filtered London market.")


# ==========================================================
# Persistent neighbourhood selector
# ==========================================================
available_neighbourhoods = sorted(filtered["neighbourhood"].unique())

if "selected_neighbourhood" not in st.session_state:
    st.session_state.selected_neighbourhood = available_neighbourhoods[0]

if st.session_state.selected_neighbourhood not in available_neighbourhoods:
    st.session_state.selected_neighbourhood = available_neighbourhoods[0]

st.selectbox(
    "Choose a neighbourhood",
    available_neighbourhoods,
    key="selected_neighbourhood"
)

selected_area = st.session_state.selected_neighbourhood

area_df = filtered[
    filtered["neighbourhood"] == selected_area
]


# ==========================================================
# KPI Cards
# ==========================================================
c1, c2, c3 = st.columns(3)

median_difference = (
    area_df["price"].median()
    - filtered["price"].median()
)

c1.metric(
    "Listings",
    f"{len(area_df):,}"
)

c2.metric(
    "Median Price",
    f"£{area_df['price'].median():.0f}",
    f"£{median_difference:+.0f}"
)

c3.metric(
    "Popular Room Type",
    area_df["room_type"].mode()[0]
)

st.divider()


# ==========================================================
# Histogram Comparison
# ==========================================================
chart_df = filtered.copy()

chart_df["Group"] = chart_df["neighbourhood"].apply(
    lambda x: selected_area if x == selected_area else "Other Areas"
)

fig = px.histogram(
    chart_df,
    x="price",
    color="Group",
    histnorm="percent",
    barmode="overlay",
    nbins=40,
    color_discrete_map={
        selected_area: "#4E79A7",
        "Other Areas": "#BDBDBD"
    },
    labels={
        "price": "Nightly Price (£)",
        "Group": ""
    },
    title=f"Price Distribution: {selected_area} vs Remaining Market"
)

fig.update_traces(
    marker_line_width=0
)

fig.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        orientation="h",
        y=1.05
    ),
    xaxis=dict(
        showgrid=False
    ),
    yaxis=dict(
        gridcolor="#DDDDDD",
        title="% of Listings"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)