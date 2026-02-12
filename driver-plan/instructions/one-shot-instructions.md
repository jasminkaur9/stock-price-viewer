# Stock Price Viewer — Implementation Instructions

**What you're receiving:**
- Working Streamlit app with all features implemented
- Single-file architecture (`app.py`) suitable for the current scope
- Cached data fetching, interactive Plotly charts, arbitrage detection

**What you need to build/extend:**
- Alternative data sources if yfinance proves unreliable
- Deployment configuration (Docker, Streamlit Cloud)
- Additional technical indicators or analysis features
- Persistence layer if watchlists/alerts are needed

---

## Milestone 1: Foundation (Data Collection & Display)

**Goal:** Fetch and display stock data with key metrics.

**Implementation:**
1. Set up Streamlit with wide layout, sidebar for controls
2. Sidebar: ticker text input, date range pickers, fetch button
3. `fetch_stock_data()` with `@st.cache_data(ttl=300)` — downloads via yfinance, flattens MultiIndex columns
4. Key metrics row: 5 `st.metric` columns — Close (with delta), Open, High, Low, Volume
5. Period summary row: Period High, Period Low, Avg Close, Trading Days
6. Data table: `st.dataframe` with formatted dates and rounded values

**Key decisions:**
- `ttl=300` (5 min cache) balances freshness vs API load
- MultiIndex flatten handles both single and multi-ticker yfinance responses
- Single-day edge case: falls back to same row for prev close (change = 0)

---

## Milestone 2: Interactive Price Chart

**Goal:** Plotly chart with candlestick/line, volume, SMA, range selectors.

**Implementation:**
1. Sidebar additions: chart type radio (Candlestick/Line), volume checkbox, SMA checkboxes (20/50/200)
2. `make_subplots(rows=2, shared_xaxes=True)` — price on top (70%), volume on bottom (30%)
3. Candlestick: `go.Candlestick(x, open, high, low, close)`
4. Line: `go.Scatter(x, y=close, mode="lines")`
5. SMA overlays: `rolling(window).mean()` with dotted lines (orange/blue/purple)
6. Volume: `go.Bar` with green/red coloring based on close vs open
7. Range selectors: 1M, 3M, 6M, YTD, 1Y, All via `rangeselector` buttons
8. Layout: `xaxis_rangeslider_visible=False`, `hovermode="x unified"`

**Key decisions:**
- Volume row hidden when unchecked (subplot row count changes dynamically)
- SMA only shown when data length >= window size
- Unified hover shows all values at crosshair

---

## Milestone 3: Multi-Ticker & Export

**Goal:** Compare tickers and download data.

**Implementation:**
1. Sidebar: compare tickers text input (comma-separated)
2. `fetch_multi()` downloads each ticker separately, handles MultiIndex
3. Normalization: `((close / first_close) - 1) * 100` for % change from start
4. Comparison chart: `go.Scatter` per ticker, 5-color palette cycling
5. CSV download: `st.download_button` with `display_df.to_csv()`

---

## Milestone 4: Arbitrage Finder

**Goal:** Cross-exchange arbitrage detection with currency conversion.

**Implementation:**
1. New tab via `st.tabs(["Price Viewer", "Arbitrage Finder"])`
2. Sidebar: two ticker inputs (Exchange 1/2), threshold slider (0.01-10%, default 0.1%)
3. Currency detection: `yf.Ticker(symbol).info["currency"]`
4. Sub-unit currency map: `{"GBp": ("GBP", 100), "ILA": ("ILS", 100), "ZAc": ("ZAR", 100)}`
5. Forex conversion: download `{CURRENCY}USD=X`, align dates, multiply
6. Sub-unit handling: divide price by divisor BEFORE multiplying by FX rate
7. Spread calculation: `(price1 - price2) / price2 * 100`
8. Opportunity detection: `abs(spread) >= threshold`
9. Charts: price comparison (two lines in USD), spread with threshold bands (hlines)
10. Opportunity table: filtered DataFrame with CSV download

**Critical bug to avoid:**
- `GBp` (pence) from yfinance means prices are in 1/100 of GBP
- `GBpUSD=X` returns the SAME rate as `GBPUSD=X` (not divided by 100)
- Must divide price by 100 before applying GBP→USD rate
- Without this fix, London-listed stocks show 100x wrong arbitrage spreads
