import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "world_happiness_2023.csv"

df = pd.read_csv(DATA_FILE)
df.columns = [
    "Country",
    "Region",
    "Score",
    "GDP",
    "Social_Support",
    "Life_Expectancy",
    "Freedom",
    "Generosity",
    "Corruption"
]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Filters")

regions = ["All"] + sorted(df["Region"].unique())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

top_n = st.sidebar.slider(
    "Show Top N Countries",
    min_value=5,
    max_value=20,
    value=10
)

# -----------------------------
# Filter data
# -----------------------------
if selected_region == "All":
    filtered = df.copy()
else:
    filtered = df[df["Region"] == selected_region]

top = filtered.nlargest(top_n, "Score").sort_values("Score")

# -----------------------------
# Title
# -----------------------------
st.title("🌍 World Happiness Dashboard")

st.caption(
    "Source: World Happiness Report 2023"
)

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries",
    len(filtered)
)

col2.metric(
    "Average Happiness",
    f"{filtered['Score'].mean():.2f}"
)

col3.metric(
    "Happiest Country",
    filtered.nlargest(1, "Score")["Country"].values[0]
)

st.divider()

# -----------------------------
# Two columns
# -----------------------------
left, right = st.columns(2)

# -----------------------------
# Chart 1
# -----------------------------
with left:

    st.subheader("Top Countries by Happiness")

    fig1 = px.bar(
        top,
        x="Score",
        y="Country",
        orientation="h",
        color="Score",
        color_continuous_scale="Blues",
        labels={
            "Score":"Happiness Score",
            "Country":""
        }
    )

    fig1.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=12),
        margin=dict(l=10,r=10,t=30,b=10)
    )

    fig1.update_traces(marker_line_width=0)

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# -----------------------------
# Chart 2
# -----------------------------
with right:

    st.subheader("GDP vs Happiness")

    fig2 = px.scatter(
        filtered,
        x="GDP",
        y="Score",
        color="Region",
        hover_name="Country",
        size="Life_Expectancy"
    )

    fig2.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=12),
        margin=dict(l=10,r=10,t=30,b=10)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# -----------------------------
# Third chart
# -----------------------------
st.subheader("Freedom vs Happiness")

fig3 = px.scatter(
    filtered,
    x="Freedom",
    y="Score",
    color="Freedom",
    color_continuous_scale="RdYlGn",
    hover_name="Country"
)

fig3.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(size=12),
    margin=dict(l=10,r=10,t=30,b=10)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)
