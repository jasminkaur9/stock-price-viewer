# Milestone 1: Data Collection & Display

## Goal
Fetch daily OHLCV data for any ticker and display key metrics + data table.

## Steps
1. `st.set_page_config(layout="wide")` for full-width dashboard
2. Sidebar: `st.text_input("Ticker")`, `st.date_input` x2, `st.button("Fetch Data")`
3. `@st.cache_data(ttl=300)` function using `yf.download()`
4. Flatten `pd.MultiIndex` columns if present
5. Key metrics: 5-column `st.metric` row with close delta
6. Period summary: 4-column row with high/low/avg/days
7. Data table: `st.dataframe` with `height=400`

## Edge Cases
- Invalid ticker → `data.empty` → show `st.error`
- Single trading day → `prev = latest` (change = 0)
- Weekend/holiday range → empty DataFrame
