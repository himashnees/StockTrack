import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="StockTrack", layout="centered")

st.title("📈 StockTrack")
st.subheader("Indian Stock Price Tracker")
st.write("Enter an NSE or BSE stock name/ticker and get the last 5 available trading days.")

STOCK_MAP = {
    "reliance": "RELIANCE",
    "tcs": "TCS",
    "infosys": "INFY",
    "infy": "INFY",
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


def resolve_symbol(user_input, exchange):
    user_input = user_input.strip()
    lower_input = user_input.lower()

    if user_input.upper().endswith(".NS") or user_input.upper().endswith(".BO"):
        return user_input.upper()

    base_symbol = STOCK_MAP.get(lower_input, user_input.upper().replace(" ", ""))

    if exchange == "NSE":
        return f"{base_symbol}.NS"
    else:
        return f"{base_symbol}.BO"


def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="15d", interval="1d")

    if data.empty:
        return None

    data = data.reset_index()
    data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]
    data["Date"] = pd.to_datetime(data["Date"]).dt.date

    return data.tail(5)


stock_input = st.text_input(
    "Enter stock name or ticker",
    placeholder="Example: Reliance, TCS, INFY, HDFCBANK"
)

exchange = st.selectbox("Select Exchange", ["NSE", "BSE"])

if st.button("Generate"):
    if not stock_input.strip():
        st.warning("Please enter a stock name or ticker.")
    else:
        symbol = resolve_symbol(stock_input, exchange)

        with st.spinner(f"Fetching data for {symbol}..."):
            result = get_stock_data(symbol)

        if result is None:
            st.error("Could not fetch data. Please check the stock name/ticker or try another exchange.")
            st.info("Examples: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS")
        else:
            st.success(f"Showing last 5 trading days for {symbol}")

            st.dataframe(result, use_container_width=True)

            chart_data = result.set_index("Date")["Close"]
            st.line_chart(chart_data)

            latest_close = result.iloc[-1]["Close"]
            st.metric("Latest Closing Price", f"₹{latest_close:.2f}")
