import streamlit as st
import plotly.express as px
from utils import load_data

st.title("🔍 Compare Countries")

df = load_data()

countries = sorted(df["country"].unique())

country1 = st.selectbox(
    "Country 1",
    countries,
    index=0
)

country2 = st.selectbox(
    "Country 2",
    countries,
    index=1
)

compare = df[df["country"].isin([country1, country2])]

fig = px.line(
    compare,
    x="year",
    y="lifeExp",
    color="country",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)