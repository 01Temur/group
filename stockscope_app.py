import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Minimalist black theme styling
st.markdown("""
    <style>
    body {
        background-color: #1c1c1c;
        color: #e0e0e0;
    }
    .css-1v3fvcr {
        background-color: #1c1c1c !important;
    }
    .stButton>button {
        background-color: #00BFFF !important;
        color: white !important;
    }
    .css-2trqyj {
        color: white !important;
    }
    h1, h2, h3, h4, h5 {
        color: #00BFFF;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions for technical indicators
def calculate_sma(data, period=50):
    return data['Close'].rolling(window=period).mean()

def calculate_rsi(data, period=20):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data):
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    return ema_12 - ema_26

# Caching stock data fetching for 5 years
@st.cache_data
def load_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

# Caching company information fetching
@st.cache_data
def get_company_info(ticker):
    stock = yf.Ticker(ticker)
    return stock.info

# Caching model training
@st.cache_resource
def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=10)  # Reduced number of estimators for faster training
    model.fit(X_train, y_train)
    return model

# Formatting function for large numbers
def format_value(val):
    return f"{val / 1e9:.2f}B" if val >= 1e9 else f"{val / 1e6:.2f}M" if val >= 1e6 else f"{val}"

# Main function
def main():
    # Sidebar for ticker input and additional options
    ticker = st.sidebar.text_input("Stock symbol:", "AAPL")
    short_ma_days = st.sidebar.slider("Short-term moving average days:", 10, 100, 10)
    long_ma_days = st.sidebar.slider("Long-term moving average days:", 50, 200, 50)
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
    end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

    # Load stock data and company info
    stock_data = load_stock_data(ticker, start_date, end_date)
    company_info = get_company_info(ticker)

    # 1. Company Information
    st.header("Company Information")
    col1, col2, col3 = st.columns(3)

    try:
        # Display stock information as a dataframe
        stock_info = [
            ("Country", company_info.get('country', 'N/A')),
            ("Sector", company_info.get('sector', 'N/A')),
            ("Industry", company_info.get('industry', 'N/A')),
            ("Market Cap", format_value(company_info.get('marketCap', 'N/A'))),
            ("Enterprise Value", format_value(company_info.get('enterpriseValue', 'N/A'))),
            ("Employees", company_info.get('fullTimeEmployees', 'N/A'))
        ]
        df_stock_info = pd.DataFrame(stock_info, columns=["Stock Info", "Value"])
        col1.dataframe(df_stock_info, width=400, hide_index=True)

        # Display price information as a dataframe
        price_info = [
            ("Current Price", f"${company_info.get('currentPrice', 'N/A'):.2f}"),
            ("Previous Close", f"${company_info.get('previousClose', 'N/A'):.2f}"),
            ("Day High", f"${company_info.get('dayHigh', 'N/A'):.2f}"),
            ("Day Low", f"${company_info.get('dayLow', 'N/A'):.2f}"),
            ("52 Week High", f"${company_info.get('fiftyTwoWeekHigh', 'N/A'):.2f}"),
            ("52 Week Low", f"${company_info.get('fiftyTwoWeekLow', 'N/A'):.2f}")
        ]
        df_price_info = pd.DataFrame(price_info, columns=["Price Info", "Value"])
        col2.dataframe(df_price_info, width=400, hide_index=True)

        # Display business metrics as a dataframe
        biz_metrics = [
            ("EPS (FWD)", f"{company_info.get('forwardEps', 'N/A'):.2f}"),
            ("P/E (FWD)", f"{company_info.get('forwardPE', 'N/A'):.2f}"),
            ("PEG Ratio", f"{company_info.get('pegRatio', 'N/A'):.2f}"),
            ("Div Rate (FWD)", f"${company_info.get('dividendRate', 'N/A'):.2f}"),
            ("Div Yield (FWD)", f"{company_info.get('dividendYield', 'N/A') * 100:.2f}%"),
            ("Recommendation", company_info.get('recommendationKey', 'N/A').capitalize())
        ]
        df_biz_metrics = pd.DataFrame(biz_metrics, columns=["Business Metrics", "Value"])
        col3.dataframe(df_biz_metrics, width=400, hide_index=True)

    except Exception as e:
        st.exception(f"An error occurred: {e}")

    # 2. Technical Analysis and Prediction Model setup
    st.header("Technical Analysis")
    stock_data['SMA_Short'] = calculate_sma(stock_data, short_ma_days)
    stock_data['SMA_Long'] = calculate_sma(stock_data, long_ma_days)
    stock_data['RSI'] = calculate_rsi(stock_data, 20)
    stock_data['MACD'] = calculate_macd(stock_data)

    # Plotting with Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name="Close Price"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Short'], mode='lines', name=f"SMA {short_ma_days}"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['SMA_Long'], mode='lines', name=f"SMA {long_ma_days}"))
    fig.update_layout(title=f"Close Price with SMA {short_ma_days} and SMA {long_ma_days}", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### RSI (20)")
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], mode='lines', name="RSI"))
    fig_rsi.update_layout(title="RSI (20)", template="plotly_dark")
    st.plotly_chart(fig_rsi, use_container_width=True)

    st.write("### MACD")
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], mode='lines', name="MACD"))
    fig_macd.update_layout(title="MACD", template="plotly_dark")
    st.plotly_chart(fig_macd, use_container_width=True)

    # Prediction Model
    st.header("Prediction Model")
    stock_data['Target'] = np.where(stock_data['Close'].shift(-1) > stock_data['Close'], 1, 0)
    feature_columns = ['SMA_Short', 'SMA_Long', 'RSI', 'MACD']
    stock_data = stock_data.dropna(subset=feature_columns + ['Target'])

    features = stock_data[feature_columns]
    target = stock_data['Target']

    if len(features) < 5:
        st.write("Not enough data available for prediction within the selected date range and indicator settings.")
    else:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        model = train_model(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        st.write(f"Prediction Model Accuracy: {accuracy:.2%}")

if __name__ == "__main__":
    main()
