import streamlit as st
from yahoo_fin import stock_info as si
import pandas as pd

# Function to fetch data for each category
def fetch_stock_data(category):
    try:
        if category == "Most Active":
            return si.get_day_most_active()
        elif category == "Top Gainers":
            return si.get_day_gainers()
        elif category == "Top Losers":
            return si.get_day_losers()
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data for {category}: {e}")
        return pd.DataFrame()

# Streamlit App
st.title("Yahoo Finance Stock Data")

st.sidebar.title("Stock Categories")
categories = ["Most Active", "Top Gainers", "Top Losers"]
selected_category = st.sidebar.radio("Select a Category", categories)

st.header(f"{selected_category} Stocks")

# Fetch and display stock data
stock_data = fetch_stock_data(selected_category)

if not stock_data.empty:
    st.dataframe(stock_data)
else:
    st.write("No data available for the selected category.")
