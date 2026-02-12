import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Price Viewer", page_icon="📈", layout="wide")

st.title("Stock Price Viewer")
tab_main, tab_arbitrage = st.tabs(["Price Viewer", "Arbitrage Finder"])

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Ticker Symbol", value="AAPL").upper().strip()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())

    st.divider()
    chart_type = st.radio("Chart Type", ["Candlestick", "Line"], horizontal=True)
    show_volume = st.checkbox("Show Volume", value=True)

    st.divider()
    st.subheader("Moving Averages")
    sma_20 = st.checkbox("SMA 20", value=False)
    sma_50 = st.checkbox("SMA 50", value=False)
    sma_200 = st.checkbox("SMA 200", value=False)

    st.divider()
    st.subheader("Compare Tickers")
    compare_input = st.text_input(
        "Additional tickers (comma-separated)",
        placeholder="e.g. MSFT, GOOGL, TSLA",
    )

    st.divider()
    st.subheader("Arbitrage Finder")
    arb_ticker_1 = st.text_input("Exchange 1 Ticker", placeholder="e.g. RELIANCE.NS").upper().strip()
    arb_ticker_2 = st.text_input("Exchange 2 Ticker", placeholder="e.g. RELIANCE.BO").upper().strip()
    arb_threshold = st.slider("Spread Threshold (%)", min_value=0.01, max_value=10.0, value=0.1, step=0.01)

    fetch_button = st.button("Fetch Data", type="primary", use_container_width=True)

# --- Data Fetching ---
@st.cache_data(ttl=300)
def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start, end=end, progress=False)
    if data.empty:
        return pd.DataFrame()
    # Flatten multi-level columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.index = pd.to_datetime(data.index)
    return data

# Sub-unit currencies: price is in sub-units, forex is in main units
# GBp = pence (1/100 GBP), ILA = agorot (1/100 ILS), ZAc = cents (1/100 ZAR)
SUB_UNIT_CURRENCIES = {
    "GBp": ("GBP", 100),
    "ILA": ("ILS", 100),
    "ZAc": ("ZAR", 100),
}

@st.cache_data(ttl=300)
def get_ticker_currency(ticker_symbol: str) -> str:
    try:
        info = yf.Ticker(ticker_symbol).info
        return info.get("currency", "USD")
    except Exception:
        return "USD"

@st.cache_data(ttl=300)
def fetch_forex(pair: str, start: str, end: str) -> pd.Series:
    """Fetch forex daily close. pair like 'INRUSD=X' for INR to USD."""
    df = yf.download(pair, start=start, end=end, progress=False)
    if df.empty:
        return pd.Series(dtype=float)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df["Close"]

with tab_main:
  if fetch_button or "stock_data" in st.session_state:
    if fetch_button:
        with st.spinner(f"Fetching {ticker} data..."):
            data = fetch_stock_data(ticker, str(start_date), str(end_date))
            st.session_state["stock_data"] = data
            st.session_state["ticker"] = ticker
    else:
        data = st.session_state["stock_data"]
        ticker = st.session_state.get("ticker", ticker)

    if data.empty:
        st.error(f"No data found for **{ticker}**. Check the ticker symbol and date range.")
    else:
        # --- Key Metrics ---
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        price_change = latest["Close"] - prev["Close"]
        pct_change = (price_change / prev["Close"]) * 100

        st.subheader(f"{ticker} — Key Metrics")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Close", f"${latest['Close']:.2f}", f"{price_change:+.2f} ({pct_change:+.2f}%)")
        m2.metric("Open", f"${latest['Open']:.2f}")
        m3.metric("High", f"${latest['High']:.2f}")
        m4.metric("Low", f"${latest['Low']:.2f}")
        m5.metric("Volume", f"{latest['Volume']:,.0f}")

        # --- Period Stats ---
        st.subheader("Period Summary")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Period High", f"${data['High'].max():.2f}")
        s2.metric("Period Low", f"${data['Low'].min():.2f}")
        s3.metric("Avg Close", f"${data['Close'].mean():.2f}")
        s4.metric("Total Trading Days", f"{len(data)}")

        # --- Interactive Price Chart ---
        st.subheader(f"{ticker} — Daily Price Chart")

        fig = make_subplots(
            rows=2 if show_volume else 1,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3] if show_volume else [1],
        )

        if chart_type == "Candlestick":
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"],
                    name="OHLC",
                ),
                row=1, col=1,
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data["Close"],
                    mode="lines",
                    name="Close",
                    line=dict(color="#636EFA", width=2),
                ),
                row=1, col=1,
            )

        # --- Moving Average Overlays ---
        sma_config = [(sma_20, 20, "#FF6D00"), (sma_50, 50, "#2962FF"), (sma_200, 200, "#AA00FF")]
        for enabled, window, color in sma_config:
            if enabled and len(data) >= window:
                sma = data["Close"].rolling(window=window).mean()
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=sma,
                        mode="lines",
                        name=f"SMA {window}",
                        line=dict(color=color, width=1.5, dash="dot"),
                    ),
                    row=1, col=1,
                )

        if show_volume:
            colors = [
                "#26a69a" if c >= o else "#ef5350"
                for c, o in zip(data["Close"], data["Open"])
            ]
            fig.add_trace(
                go.Bar(
                    x=data.index,
                    y=data["Volume"],
                    name="Volume",
                    marker_color=colors,
                    opacity=0.5,
                ),
                row=2, col=1,
            )
            fig.update_yaxes(title_text="Volume", row=2, col=1)

        fig.update_layout(
            height=600,
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
        )

        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)

        # Range selector buttons
        fig.update_xaxes(
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="All"),
                ]
            ),
            row=1, col=1,
        )

        st.plotly_chart(fig, use_container_width=True)

        # --- Data Table & CSV Export ---
        st.subheader("Daily OHLCV Data")
        display_df = data.copy()
        display_df.index = display_df.index.strftime("%Y-%m-%d")
        display_df = display_df.round(2)
        st.dataframe(display_df, use_container_width=True, height=400)

        csv = display_df.to_csv()
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{ticker}_{start_date}_{end_date}.csv",
            mime="text/csv",
        )

        # --- Multi-Ticker Comparison ---
        compare_tickers = [
            t.strip().upper()
            for t in compare_input.split(",")
            if t.strip()
        ] if compare_input else []

        if compare_tickers:
            st.subheader("Ticker Comparison (Normalized)")
            all_tickers = [ticker] + compare_tickers

            @st.cache_data(ttl=300)
            def fetch_multi(tickers: tuple, start: str, end: str) -> dict:
                result = {}
                for t in tickers:
                    df = yf.download(t, start=start, end=end, progress=False)
                    if not df.empty:
                        if isinstance(df.columns, pd.MultiIndex):
                            df.columns = df.columns.get_level_values(0)
                        result[t] = df
                return result

            with st.spinner("Fetching comparison data..."):
                multi_data = fetch_multi(tuple(all_tickers), str(start_date), str(end_date))

            if multi_data:
                comp_fig = go.Figure()
                colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
                for i, (t, df) in enumerate(multi_data.items()):
                    # Normalize to percentage change from first day
                    first_close = df["Close"].iloc[0]
                    normalized = ((df["Close"] / first_close) - 1) * 100
                    comp_fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=normalized,
                            mode="lines",
                            name=t,
                            line=dict(color=colors[i % len(colors)], width=2),
                        )
                    )

                comp_fig.update_layout(
                    height=450,
                    hovermode="x unified",
                    yaxis_title="Change from Start (%)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=0, r=0, t=30, b=0),
                )
                comp_fig.update_xaxes(
                    rangeselector=dict(
                        buttons=[
                            dict(count=1, label="1M", step="month", stepmode="backward"),
                            dict(count=3, label="3M", step="month", stepmode="backward"),
                            dict(count=6, label="6M", step="month", stepmode="backward"),
                            dict(step="all", label="All"),
                        ]
                    ),
                )
                st.plotly_chart(comp_fig, use_container_width=True)
            else:
                st.warning("Could not fetch data for the comparison tickers.")
  else:
    st.info("Enter a ticker symbol and click **Fetch Data** to get started.")

# --- Arbitrage Finder Tab ---
with tab_arbitrage:
    st.subheader("Cross-Exchange Arbitrage Finder")
    st.markdown(
        "Compare the same stock listed on two exchanges. "
        "Prices are converted to a common currency (USD) to find spread opportunities."
    )
    st.caption(
        "**Examples:** RELIANCE.NS vs RELIANCE.BO (India NSE vs BSE) | "
        "SHOP vs SHOP.TO (US vs Canada) | RIO vs RIO.L (US vs London) | "
        "TM vs 7203.T (US ADR vs Tokyo)"
    )

    if arb_ticker_1 and arb_ticker_2 and (fetch_button or "arb_data" in st.session_state):
        if fetch_button:
            with st.spinner("Fetching data for both exchanges..."):
                df1 = fetch_stock_data(arb_ticker_1, str(start_date), str(end_date))
                df2 = fetch_stock_data(arb_ticker_2, str(start_date), str(end_date))
                cur1 = get_ticker_currency(arb_ticker_1)
                cur2 = get_ticker_currency(arb_ticker_2)
                st.session_state["arb_data"] = (df1, df2, cur1, cur2)
        else:
            df1, df2, cur1, cur2 = st.session_state.get("arb_data", (pd.DataFrame(), pd.DataFrame(), "USD", "USD"))

        if df1.empty or df2.empty:
            st.error("Could not fetch data for one or both tickers. Verify the symbols.")
        else:
            # Convert both to USD
            @st.cache_data(ttl=300)
            def convert_to_usd(close: pd.Series, currency: str, start: str, end: str) -> pd.Series:
                if currency == "USD":
                    return close
                # Handle sub-unit currencies (GBp, ILA, ZAc)
                divisor = 1
                fx_currency = currency
                if currency in SUB_UNIT_CURRENCIES:
                    fx_currency, divisor = SUB_UNIT_CURRENCIES[currency]
                pair = f"{fx_currency}USD=X"
                fx = fetch_forex(pair, start, end)
                if fx.empty:
                    return close  # fallback: assume same currency
                # Align on common dates
                aligned = pd.DataFrame({"close": close, "fx": fx}).dropna()
                return (aligned["close"] / divisor) * aligned["fx"]

            usd1 = convert_to_usd(df1["Close"], cur1, str(start_date), str(end_date))
            usd2 = convert_to_usd(df2["Close"], cur2, str(start_date), str(end_date))

            # Align on common trading dates
            merged = pd.DataFrame({
                arb_ticker_1: usd1,
                arb_ticker_2: usd2,
            }).dropna()

            if merged.empty:
                st.warning("No overlapping trading dates found between the two tickers.")
            else:
                merged["Spread (USD)"] = merged[arb_ticker_1] - merged[arb_ticker_2]
                merged["Spread (%)"] = (merged["Spread (USD)"] / merged[arb_ticker_2]) * 100
                merged["Opportunity"] = merged["Spread (%)"].abs() >= arb_threshold

                opp_count = merged["Opportunity"].sum()
                total_days = len(merged)

                # --- Summary Metrics ---
                st.subheader("Arbitrage Summary")
                a1, a2, a3, a4 = st.columns(4)
                a1.metric(f"{arb_ticker_1} Currency", cur1)
                a2.metric(f"{arb_ticker_2} Currency", cur2)
                a3.metric("Opportunity Days", f"{opp_count} / {total_days}")
                a4.metric("Avg Spread", f"{merged['Spread (%)'].mean():+.2f}%")

                b1, b2, b3, b4 = st.columns(4)
                b1.metric("Max Spread", f"{merged['Spread (%)'].max():+.2f}%")
                b2.metric("Min Spread", f"{merged['Spread (%)'].min():+.2f}%")
                b3.metric("Std Dev", f"{merged['Spread (%)'].std():.2f}%")
                b4.metric(f"Latest Spread", f"{merged['Spread (%)'].iloc[-1]:+.2f}%")

                # --- Price Comparison Chart ---
                st.subheader("Price Comparison (USD)")
                price_fig = go.Figure()
                price_fig.add_trace(go.Scatter(
                    x=merged.index, y=merged[arb_ticker_1],
                    name=f"{arb_ticker_1} ({cur1}→USD)", mode="lines",
                    line=dict(color="#636EFA", width=2),
                ))
                price_fig.add_trace(go.Scatter(
                    x=merged.index, y=merged[arb_ticker_2],
                    name=f"{arb_ticker_2} ({cur2}→USD)", mode="lines",
                    line=dict(color="#EF553B", width=2),
                ))
                price_fig.update_layout(
                    height=400, hovermode="x unified",
                    yaxis_title="Price (USD)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=0, r=0, t=30, b=0),
                )
                st.plotly_chart(price_fig, use_container_width=True)

                # --- Spread Chart with Threshold ---
                st.subheader("Spread Analysis")
                spread_fig = make_subplots(rows=1, cols=1)

                # Highlight opportunity zones
                opp_dates = merged[merged["Opportunity"]]
                if not opp_dates.empty:
                    spread_fig.add_trace(go.Bar(
                        x=opp_dates.index, y=opp_dates["Spread (%)"],
                        name="Opportunity",
                        marker_color=[
                            "#26a69a" if s > 0 else "#ef5350"
                            for s in opp_dates["Spread (%)"]
                        ],
                        opacity=0.4,
                    ))

                spread_fig.add_trace(go.Scatter(
                    x=merged.index, y=merged["Spread (%)"],
                    name="Spread %", mode="lines",
                    line=dict(color="#636EFA", width=2),
                ))

                # Threshold lines
                spread_fig.add_hline(
                    y=arb_threshold, line_dash="dash", line_color="green",
                    annotation_text=f"+{arb_threshold}%",
                )
                spread_fig.add_hline(
                    y=-arb_threshold, line_dash="dash", line_color="red",
                    annotation_text=f"-{arb_threshold}%",
                )
                spread_fig.add_hline(y=0, line_color="gray", line_width=0.5)

                spread_fig.update_layout(
                    height=400, hovermode="x unified",
                    yaxis_title="Spread (%)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=0, r=0, t=30, b=0),
                )
                st.plotly_chart(spread_fig, use_container_width=True)

                # --- Opportunity Table ---
                if opp_count > 0:
                    st.subheader(f"Arbitrage Opportunities (|spread| >= {arb_threshold}%)")
                    opp_display = opp_dates[[arb_ticker_1, arb_ticker_2, "Spread (USD)", "Spread (%)"]].copy()
                    opp_display.index = opp_display.index.strftime("%Y-%m-%d")
                    opp_display = opp_display.round(4)
                    st.dataframe(opp_display, use_container_width=True, height=300)

                    opp_csv = opp_display.to_csv()
                    st.download_button(
                        label="Download Opportunities CSV",
                        data=opp_csv,
                        file_name=f"arbitrage_{arb_ticker_1}_{arb_ticker_2}.csv",
                        mime="text/csv",
                    )
                else:
                    st.success(f"No arbitrage opportunities found above {arb_threshold}% threshold in this period.")
    elif arb_ticker_1 or arb_ticker_2:
        if not arb_ticker_1 or not arb_ticker_2:
            st.info("Enter both ticker symbols in the sidebar and click **Fetch Data**.")
    else:
        st.info(
            "Enter two ticker symbols for the same stock on different exchanges "
            "in the sidebar, then click **Fetch Data**."
        )
