# Section-by-Section Prompt Template

Use this template when extending the app one feature at a time.

---

## Template

I have a working Streamlit stock price viewer. I want to add **[SECTION NAME]**.

**Current app has:**
- Tab 1 (Price Viewer): OHLCV data fetch, metrics, candlestick/line chart, volume, SMA 20/50/200, multi-ticker comparison, CSV export
- Tab 2 (Arbitrage Finder): cross-exchange comparison, auto currency conversion (with sub-unit handling), spread analysis, opportunity detection

**What I want to add:**
[Describe the feature]

**Constraints:**
- Use Streamlit for UI (`st.plotly_chart`, `st.metric`, `st.dataframe`)
- Use `@st.cache_data` for any new API calls
- Keep calculation logic in pure functions (no Streamlit imports)
- Handle empty/error states gracefully
- Match existing chart style (Plotly, unified hover, horizontal legend)

**Files to modify:**
- `app.py` — Main application (add new tab or extend existing)
- `requirements.txt` — If new dependencies needed

---

## Example Extensions

### Add RSI Indicator
"Add RSI (14-period) as a subplot below the price chart. Toggle on/off from sidebar."

### Add Bollinger Bands
"Add Bollinger Bands (20-period, 2 std dev) as an overlay on the price chart. Toggle from sidebar."

### Add Intraday Data
"Add an interval selector (1m, 5m, 15m, 1h, 1d) in the sidebar. Adjust yfinance download accordingly."

### Add Watchlist
"Add a watchlist feature: save favorite tickers to a local JSON file, show them as quick-select buttons in the sidebar."

### Add Alerts
"Monitor a list of tickers and notify (via st.toast) when price crosses a user-defined threshold."
