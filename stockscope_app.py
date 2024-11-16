import streamlit as st
import yfinance as yf
import pandas as pd

# List of companies (ticker symbols)
companies = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA']

# Function to fetch stock data
def get_stock_data(tickers):
    stock_data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")  # Fetching the latest data
        price = history['Close'].iloc[-1]
        change = (history['Close'].pct_change().iloc[-1]) * 100  # Calculate percentage change
        stock_data.append({'Company': ticker, 'Price': price, 'Change (%)': change})
    return pd.DataFrame(stock_data)

# Streamlit App layout
st.title('Stock Market Dashboard')
st.write('This app shows the stock price and percentage change for a list of companies.')

# Get stock data
stock_df = get_stock_data(companies)

# Display data in a table
st.dataframe(stock_df)

# Optionally, you can also visualize the data in a chart
st.line_chart(stock_df.set_index('Company')['Price'])
