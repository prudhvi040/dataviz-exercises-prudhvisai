import streamlit as st

st.set_page_config(
    page_title="London Airbnb Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

pg = st.navigation([
    st.Page("pages/01_market.py",
            title="Market Summary",
            icon="📊"),

    st.Page("pages/02_drilldown.py",
            title="Neighbourhood Story",
            icon="📍"),

    st.Page("pages/03_demand.py",
            title="Guest Demand",
            icon="🔥")
])

pg.run()