import streamlit as st
import plotly.express as px
from utils import load_data

st.title("📈 Trends")

df = load_data()

country = st.selectbox(
    "Choose a country",
    sorted(df["country"].unique())
)

country_df = df[df["country"] == country]

fig = px.line(
    country_df,
    x="year",
    y="lifeExp",
    markers=True,
    title=f"Life Expectancy in {country}"
)

st.plotly_chart(fig, use_container_width=True)