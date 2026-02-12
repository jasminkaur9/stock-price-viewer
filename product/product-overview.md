# Stock Price Viewer

## The Problem
No quick, clean way to pull stock data and visualize daily prices interactively without wrestling with APIs or chart configs.

## Success Looks Like
Enter a ticker, pick a date range, see an interactive daily price chart with zoom/pan/range selector. View key metrics at a glance.

## How We'd Know We're Wrong
If yfinance data is unreliable or too slow, or if the app feels clunkier than just opening Yahoo Finance in a browser.

## Building On (Existing Foundations)
- **yfinance** — Free stock data, no API key, returns pandas DataFrames
- **Plotly** — Interactive candlestick/line charts with built-in range selectors
- **Streamlit** — Instant web UI, zero frontend code

## The Unique Part
A focused, clean Streamlit app that combines data fetching + interactive charting in one seamless experience. Ticker input, date range, chart type selection, key price metrics — all working together.

## Tech Stack
- **UI:** Streamlit
- **Data:** yfinance
- **Charts:** Plotly (go.Candlestick, go.Scatter)
- **Processing:** pandas

## Open Questions
- Multi-ticker comparison in scope?
- Technical indicators (moving averages, volume) desired?
