import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Jayraj Market Terminal",
    layout="wide"
)

st.sidebar.title("📊 Market Control Center")

st.sidebar.info("""
Jayraj Market Terminal v2

Live Data:
• Markets
• Crypto
• Pharma Stocks

Refresh: 60 sec
""")
st.sidebar.subheader("⚙ Settings")

chart_period = st.sidebar.selectbox(
    "Chart Period",
    ["1mo", "3mo", "6mo", "1y"],
    index=1
)

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #050816;
}

/* Main title */
h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #1e293b;
    box-shadow: 0 0 15px rgba(0,255,255,0.08);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 30px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0b1120;
}

</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=60000, key="refresh")

st.title("📈 Jayraj Market Terminal")

# Major Assets
assets = {
    "Nifty 50": "^NSEI",
    "S&P 500": "^GSPC",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Gold": "GC=F",
    "USD/INR": "INR=X"
}
cols = st.columns(6)

for i, (name, ticker) in enumerate(assets.items()):
    data = yf.Ticker(ticker).history(period="5d")
    current = round(data["Close"].iloc[-1], 2)
    previous = round(data["Close"].iloc[-2], 2)
    change = round(current - previous, 2)

    with cols[i]:
        st.metric(name, current, change)

st.divider()

# Charts
tab1, tab2, tab3, tab4 = st.tabs(
    ["Nifty 50", "S&P 500", "Bitcoin", "Ethereum"]
)

with tab1:

    nifty_data = yf.Ticker("^NSEI").history(period=chart_period)

    fig = go.Figure(data=[
        go.Candlestick(
            x=nifty_data.index,
            open=nifty_data["Open"],
            high=nifty_data["High"],
            low=nifty_data["Low"],
            close=nifty_data["Close"]
        )
    ])

    fig.update_layout(
        template="plotly_dark",
        height=600,
        title="Nifty 50 Candlestick Chart"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="nifty_chart"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        title="Nifty 50 Candlestick Chart"
    )

st.plotly_chart(
    fig,
    use_container_width=True,
    key="chart2"
)

with tab2:
    st.line_chart(yf.Ticker("^GSPC").history(period="3mo")["Close"])

with tab3:
    st.line_chart(yf.Ticker("BTC-USD").history(period="3mo")["Close"])

with tab4:
    st.line_chart(yf.Ticker("ETH-USD").history(period="3mo")["Close"])

st.divider()

st.subheader("💊 Pharma Watchlist")

pharma = {
    "Sun Pharma": "SUNPHARMA.NS",
    "Cipla": "CIPLA.NS",
    "Dr Reddy": "DRREDDY.NS",
    "Lupin": "LUPIN.NS"
}

for company, ticker in pharma.items():
    data = yf.Ticker(ticker).history(period="5d")

    if len(data) >= 2:
        current = round(data["Close"].iloc[-1], 2)
        previous = round(data["Close"].iloc[-2], 2)

        st.metric(
            company,
            current,
            round(current - previous, 2)
        )

st.divider()

st.subheader("🧠 AI Market Pulse")
nifty_trend = "Bullish"

if nifty_data["Close"].iloc[-1] < nifty_data["Close"].iloc[-5]:
    nifty_trend = "Bearish"

# btc_trend = "Bullish"

# if btc_data["Close"].iloc[-1] < btc_data["Close"].iloc[-5]:
#     btc_trend = "Bearish"

st.info(f"""
📈 Nifty Trend: {nifty_trend}

""")
st.success("Auto-refresh every 60 seconds")
