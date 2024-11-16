import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf

# Function to scrape Yahoo Finance
def get_yahoo_finance_data(category):
    base_url = f"https://finance.yahoo.com/{category}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(base_url, headers=headers)
    
    if response.status_code != 200:
        st.error(f"Failed to fetch data for {category}. Status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "W(100%)"})
    if not table:
        st.error(f"Could not find data for {category}.")
        return pd.DataFrame()

    rows = table.find_all("tr")
    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        data.append([col.text.strip() for col in cols])

    columns = [header.text.strip() for header in rows[0].find_all("th")]
    return pd.DataFrame(data, columns=columns)

# Streamlit App
st.title("Yahoo Finance Stock Data")

st.sidebar.title("Stock Categories")
categories = {
    "Most Active": "most-active",
    "Top Gainers": "gainers",
    "Top Losers": "losers",
}

selected_category = st.sidebar.radio("Select Category", list(categories.keys()))

# Display data
st.header(f"{selected_category} Stocks")
data = get_yahoo_finance_data(categories[selected_category])
if not data.empty:
    st.dataframe(data)
