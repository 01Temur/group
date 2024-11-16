import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# App configuration
st.set_page_config(page_title="Forex Economic Calendar", layout="wide")

# Sample static data (replace with API fetching logic for live data)
def fetch_calendar_data():
    """Fetch economic calendar data (static or dynamic via API)."""
    # Example static data
    data = [
        {"Date": "2024-11-17", "Time": "12:30", "Country": "US", "Event": "Retail Sales", "Impact": "High", "Previous": "0.6%", "Forecast": "0.7%"},
        {"Date": "2024-11-18", "Time": "09:00", "Country": "UK", "Event": "Inflation Rate", "Impact": "Medium", "Previous": "3.1%", "Forecast": "3.0%"},
        {"Date": "2024-11-19", "Time": "14:00", "Country": "US", "Event": "FOMC Minutes", "Impact": "High", "Previous": "-", "Forecast": "-"},
        {"Date": "2024-11-19", "Time": "11:00", "Country": "EU", "Event": "GDP Growth Rate", "Impact": "Medium", "Previous": "1.2%", "Forecast": "1.1%"},
    ]
    return pd.DataFrame(data)

# Load calendar data
calendar_data = fetch_calendar_data()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    countries = st.multiselect("Select Countries", options=calendar_data["Country"].unique(), default=calendar_data["Country"].unique())
    impacts = st.multiselect("Select Impact Levels", options=["High", "Medium", "Low"], default=["High", "Medium", "Low"])
    start_date = st.date_input("Start Date", value=datetime.now().date())
    end_date = st.date_input("End Date", value=(datetime.now() + timedelta(days=7)).date())

# Filter data
filtered_data = calendar_data[
    (calendar_data["Country"].isin(countries)) &
    (calendar_data["Impact"].isin(impacts)) &
    (pd.to_datetime(calendar_data["Date"]) >= pd.Timestamp(start_date)) &
    (pd.to_datetime(calendar_data["Date"]) <= pd.Timestamp(end_date))
]

# Display calendar data
st.title("Forex Economic Calendar")
st.write("View upcoming economic events with their expected and previous impacts on the global markets.")

# Calendar table
if not filtered_data.empty:
    st.table(filtered_data)
else:
    st.warning("No events match the selected filters.")

# Visualize events by country and impact
st.subheader("Events Distribution")
event_counts = filtered_data.groupby(["Country", "Impact"]).size().reset_index(name="Count")
if not event_counts.empty:
    st.bar_chart(event_counts.set_index("Country")["Count"])
else:
    st.info("No data available for visualization.")
