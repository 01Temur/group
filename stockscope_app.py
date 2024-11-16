import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to scrape stock data from Yahoo Finance
def scrape_yahoo_finance(category_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(category_url, headers=headers)

    if response.status_code != 200:
        st.error(f"Failed to fetch data from Yahoo Finance. Status code: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "W(100%)"})

    if not table:
        st.error("No stock data found on the page.")
        return pd.DataFrame()

    # Extract table headers
    headers = [header.text.strip() for header in table.find_all("th")]
    # Extract table rows
    rows = table.find_all("tr")[1:]  # Skip the header row

    data = []
    for row in rows:
        cols = row.find_all("td")
        data.append([col.text.strip() for col in cols])

    return pd.DataFrame(data, columns=headers)

# Streamlit App
st.title("Yahoo Finance Stock Data")

# Define URLs for each category
categories = {
    "Most Active": "https://finance.yahoo.com/most-active",
    "Top Gainers": "https://finance.yahoo.com/markets/stocks/gainers",
    "Top Losers": "https://finance.yahoo.com/markets/stocks/losers",
}

# Sidebar for category selection
st.sidebar.title("Stock Categories")
selected_category = st.sidebar.radio("Select Category", list(categories.keys()))

# Display data
st.header(f"{selected_category} Stocks")
category_url = categories[selected_category]
stock_data = scrape_yahoo_finance(category_url)

if not stock_data.empty:
    st.dataframe(stock_data)
else:
    st.write("No data available.")
