import streamlit as st
from yahoo_fin import stock_info as si
import pandas as pd

# Function to fetch data for each category
def get_yahoo_finance_data(category):
    try:
        if category == "Most Active":
            data = si.get_day_most_active()
        elif category == "Top Gainers":
            data = si.get_day_gainers()
        elif category == "Top Losers":
            data = si.get_day_losers()
        else:
            data = pd.DataFrame()
        return data
    except Exception as e:
        st.error(f"Error fetching data for {category}: {e}")
        return pd.DataFrame()

# Streamlit App
st.title("Yahoo Finance Stock Data")

st.sidebar.title("Stock Categories")
categories = ["Most Active", "Top Gainers", "Top Losers"]
selected_category = st.sidebar.radio("Select Category", categories)

# Fetch and display data
st.header(f"{selected_category} Stocks")
data = get_yahoo_finance_data(selected_category)

if not data.empty:
    st.dataframe(data)
else:
    st.write("No data available.")
