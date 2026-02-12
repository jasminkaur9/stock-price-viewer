# Milestone 2: Interactive Price Chart

## Goal
Plotly chart with candlestick/line modes, volume subplot, SMA overlays, range selectors.

## Steps
1. Sidebar: `st.radio("Chart Type", ["Candlestick", "Line"])`, volume checkbox, SMA checkboxes
2. `make_subplots(rows=2, shared_xaxes=True, row_heights=[0.7, 0.3])`
3. Candlestick trace: `go.Candlestick(x, open, high, low, close)`
4. Line trace: `go.Scatter(x, y=close, mode="lines")`
5. SMA: `data["Close"].rolling(window).mean()` → `go.Scatter` with dash="dot"
6. Volume: `go.Bar` colored green (close>=open) / red (close<open), opacity=0.5
7. Range selector: `rangeselector` with 1M/3M/6M/YTD/1Y/All buttons
8. Layout: disable rangeslider, unified hover, horizontal legend above chart

## Key Details
- SMA colors: 20=#FF6D00, 50=#2962FF, 200=#AA00FF
- Only show SMA when `len(data) >= window`
- Dynamic subplot rows: 1 row when volume hidden, 2 when shown
