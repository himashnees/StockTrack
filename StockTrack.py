import streamlit as st
import yfinance as yf
import pandas as pd
import requests

st.set_page_config(page_title="Indian Stock Price Finder", layout="centered")

st.title("📈 Indian Stock Price - Last 5 Trading Days")
st.write("Enter an NSE/BSE stock name or ticker and get the last 5 available trading days including today, if market data is available.")

# Common Indian stock name mapping
STOCK_MAP = {
    "reliance": "RELIANCE",
    "tcs": "TCS",
    "infosys": "INFY",
    "hdfc bank": "HDFCBANK",
    "icici bank": "ICICIBANK",
    "sbi": "SBIN",
    "state bank of india": "SBIN",
    "axis bank": "AXISBANK",
    "wipro": "WIPRO",
    "hcl": "HCLTECH",
    "hcl tech": "HCLTECH",
    "itc": "ITC",
    "tata motors": "TATAMOTORS",
    "maruti": "MARUTI",
    "bajaj finance": "BAJFINANCE",
    "asian paints": "ASIANPAINT",
    "sun pharma": "SUNPHARMA",
    "larsen": "LT",
    "l&t": "LT",
    "kotak bank": "KOTAKBANK",
    "bharti airtel": "BHARTIARTL"
}

def clean_input(user_input):
    return user_input.strip()

def resolve_symbol(user_input, exchange):
    user_input = clean_input(user_input)
    lower_input = user_input.lower()

    # If user already enters .NS or .BO
    if user_input.upper().endswith(".NS") or user_input.upper().endswith(".BO"):
        return user_input.upper()

    # If user enters company name
    base_symbol = STOCK_MAP.get(lower_input, user_input.upper().replace(" ", ""))

    if exchange == "NSE":
        return f"{base_symbol}.NS"
    else:
        return f"{base_symbol}.BO"

def get_last_5_days(symbol):
    stock = yf.Ticker(symbol)

    # Fetch more than 5 calendar days because weekends/holidays may exist
    data = stock.history(period="15d", interval="1d")

    if data.empty:
        return None

    data = data.reset_index()
    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]
    data["Date"] = pd.to_datetime(data["Date"]).dt.date

    # Last 5 trading days
    return data.tail(5)

stock_input = st.text_input("Enter stock name or ticker", placeholder="Example: Reliance, TCS, INFY, HDFCBANK")

exchange = st.selectbox("Select Exchange", ["NSE", "BSE"])

if st.button("Generate"):
    if not stock_input.strip():
        st.warning("Please enter a stock name or ticker.")
    else:
        symbol = resolve_symbol(stock_input, exchange)
        st.write(f"Fetching data for: **{symbol}**")

        result = get_last_5_days(symbol)

        if result is None:
            st.error("Could not fetch stock data. Please check the stock name/ticker or try the other exchange.")
            st.info("Example NSE tickers: RELIANCE.NS, TCS.NS, INFY.NS")
            st.info("Example BSE tickers: RELIANCE.BO, TCS.BO, INFY.BO")
        else:
            st.success("Last 5 available trading days")
            st.dataframe(result, use_container_width=True)

            st.line_chart(result.set_index("Date")["Close"])
