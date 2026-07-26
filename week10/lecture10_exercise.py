import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path

st.set_page_config(
    page_title="CO2 Dashboard",
    page_icon="🌱",
    layout="wide"
)

# -------------------------
# Data
# -------------------------

@st.cache_data
def load_data():

    path = Path(__file__).parent / "data" / "co2_emissions.csv"

    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(
        df["Year"].astype(str) + "-01-01"
    )

    return df

df = load_data()

st.title("🌱 CO2 Emissions Explorer")

st.caption("Source: Our World in Data")

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.header("Filters")

    # Region

    regions = ["All"] + sorted(df["Region"].unique())

    selected_region = st.selectbox(
        "Region",
        regions
    )

    # Country list depends on region

    if selected_region == "All":

        country_options = sorted(
            df["Country"].unique()
        )

    else:

        country_options = sorted(
            df[df["Region"] == selected_region]["Country"].unique()
        )

    selected_countries = st.multiselect(
        "Countries",
        country_options,
        default=country_options[:3]
    )

    if not selected_countries:

        st.warning("Select at least one country.")

        st.stop()

    year_range = st.slider(
        "Year Range",
        int(df["Year"].min()),
        int(df["Year"].max()),
        (2000, 2022)
    )

    metric = st.radio(
        "Metric",
        [
            "Total CO2 (Mt)",
            "CO2 per Capita"
        ]
    )

    show_top = st.checkbox(
        "Show only Top Emitter",
        False
    )

# -------------------------
# Filtering
# -------------------------

filtered = df[
    (df["Country"].isin(selected_countries))
    &
    (df["Year"] >= year_range[0])
    &
    (df["Year"] <= year_range[1])
]

if filtered.empty:

    st.warning("No data matches these filters.")

    st.stop()    

# -------------------------
# Metric Selection
# -------------------------

if metric == "Total CO2 (Mt)":

    y_col = "CO2_Mt"

    y_label = "CO2 Emissions (Mt)"

else:

    y_col = "CO2_per_Capita"

    y_label = "CO2 per Capita"

if show_top:
    latest_year = filtered["Year"].max()

    top_country = (
        filtered[filtered["Year"] == latest_year]
        .sort_values(y_col, ascending=False)
        .iloc[0]["Country"]
    )

    filtered = filtered[filtered["Country"] == top_country]

# -------------------------
# Summary
# -------------------------

st.caption(

    f"Showing {len(selected_countries)} countries | "

    f"{selected_region} | "

    f"{year_range[0]}-{year_range[1]} | "

    f"{metric}"

)


# --------------------------------
# Charts
# --------------------------------

col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        filtered,
        x="Year",
        y=y_col,
        color="Country",
        labels={"Year": "Year", y_col: y_label}
    )

    fig1.update_layout(
        title=y_label + " over time",
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial")
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    latest = filtered[
        filtered["Year"] == filtered["Year"].max()
    ].sort_values(y_col)

    fig2 = px.bar(
        latest,
        x=y_col,
        y="Country",
        orientation="h",
        color=y_col,
        title=f"Latest Year Ranking ({filtered['Year'].max()})"
    )

    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial"),
        xaxis=dict(range=[0, latest[y_col].max() * 1.15])
    )

    st.plotly_chart(fig2, use_container_width=True)
