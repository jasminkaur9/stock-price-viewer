# Milestone 3: Multi-Ticker Comparison & CSV Export

## Goal
Compare multiple tickers on normalized basis, download data as CSV.

## Steps
1. Sidebar: `st.text_input` for comma-separated compare tickers
2. Parse input: split by comma, strip, uppercase
3. `fetch_multi()`: loop download each ticker, cache with `@st.cache_data`
4. Normalize: `((close / first_close) - 1) * 100` for % change from start
5. Chart: `go.Scatter` per ticker, cycling through 5-color palette
6. CSV: `st.download_button(data=df.to_csv(), mime="text/csv")`

## Key Details
- Color palette: #636EFA, #EF553B, #00CC96, #AB63FA, #FFA15A
- Comparison chart at 450px height
- Range selectors: 1M, 3M, 6M, All
