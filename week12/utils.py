# utils.py — shared by every page

import pandas as pd
import streamlit as st
from pathlib import Path

# =============================================================================
# Load data once and cache it
# =============================================================================
@st.cache_data
def load_data():
    # data folder is inside week12
    path = Path(__file__).parent / "data" / "airbnb_london.csv"

    df = pd.read_csv(path)

    # Cap prices at the 95th percentile to remove extreme outliers
    p95 = df["price"].quantile(0.95)
    df = df[df["price"] <= p95].copy()

    return df, p95


# =============================================================================
# Keep filters alive when switching pages
# =============================================================================
def init_filters(df):
    defaults = {
        "flt_rooms": list(df["room_type"].unique()),
        "flt_hoods": sorted(df["neighbourhood"].unique()),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
        else:
            st.session_state[key] = st.session_state[key]

    # Keep slider value alive
    if "flt_price" in st.session_state:
        st.session_state["flt_price"] = st.session_state["flt_price"]


# =============================================================================
# Shared sidebar
# =============================================================================
def sidebar_filters(df, p95):
    init_filters(df)

    with st.sidebar:
        st.header("🔎 Filters")

        st.multiselect(
            "Room type",
            df["room_type"].unique(),
            key="flt_rooms"
        )

        st.multiselect(
            "Neighbourhood",
            sorted(df["neighbourhood"].unique()),
            key="flt_hoods"
        )

        min_p = int(df["price"].min())
        max_p = int(df["price"].max()) + 1

        st.slider(
            "Price (£/night)",
            min_p,
            max_p,
            value=(min_p, max_p),
            key="flt_price",
        )

        st.divider()

        st.caption(
            f"Prices capped at 95th percentile (£{p95:.0f}) "
            "to remove extreme outliers."
        )

    filtered = df[
        df["room_type"].isin(st.session_state.flt_rooms)
        & df["neighbourhood"].isin(st.session_state.flt_hoods)
        & df["price"].between(*st.session_state.flt_price)
    ]

    if filtered.empty:
        st.warning("No listings match current filters.")
        st.stop()

    return filtered