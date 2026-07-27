import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.title("🌍 Overview")

df = load_data()

st.write("### Dataset Preview")
st.dataframe(df.head())

st.write("### GDP per Capita vs Life Expectancy")

fig = px.scatter(
    df,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True
)

st.plotly_chart(fig, use_container_width=True)