import streamlit as st
import plotly.express as px

# Shared data loading used by every page
@st.cache_data
def load_data():
    return px.data.gapminder()