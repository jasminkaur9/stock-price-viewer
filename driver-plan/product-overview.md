# Stock Price Viewer — Product Overview

## The Problem
No quick, clean way to pull stock data and visualize daily prices interactively without wrestling with APIs or chart configs. Additionally, investors interested in cross-listed stocks lack a simple tool to spot price discrepancies across exchanges.

## Success Looks Like
1. Enter a ticker, pick a date range, see an interactive daily price chart with zoom/pan/range selectors
2. View key metrics (close, change, high/low, volume) at a glance
3. Compare multiple tickers on a normalized basis
4. Detect arbitrage opportunities for cross-listed stocks with automatic currency conversion

## Building On (Existing Foundations)
- **yfinance** — Free stock data, no API key, returns pandas DataFrames
- **Plotly** — Interactive candlestick/line charts with built-in range selectors
- **Streamlit** — Instant web UI with tabs, sidebar, metrics, caching

## What Was Built

### Section 1: Data Collection & Display
- Sidebar controls: ticker input, date range picker
- Cached data fetching via yfinance (5-minute TTL)
- Key metrics row: close with change delta, open, high, low, volume
- Period summary: period high/low, average close, trading days
- Scrollable OHLCV data table with CSV download

### Section 2: Interactive Price Chart
- Plotly candlestick and line chart modes (togglable)
- Volume subplot with color-coded bars
- Moving average overlays: SMA 20, 50, 200 (togglable)
- Range selector buttons: 1M, 3M, 6M, YTD, 1Y, All
- Unified hover crosshair

### Section 3: Enhancements
- Multi-ticker comparison with normalized % change chart
- CSV data export

### Section 4: Arbitrage Finder (Bonus)
- Cross-exchange price comparison with auto currency detection
- Forex conversion via yfinance (handles USD, CAD, INR, GBP, JPY, etc.)
- Sub-unit currency handling (GBp pence / 100, ILA, ZAc)
- Spread analysis chart with configurable threshold bands
- Opportunity table with CSV export

## Tech Stack
- **UI:** Streamlit 1.54+
- **Data:** yfinance
- **Charts:** Plotly 6.5+ (go.Candlestick, go.Scatter, go.Bar)
- **Processing:** pandas, numpy

## Known Limitations
- yfinance is unofficial and can break when Yahoo changes their backend
- Daily close data only — no intraday resolution for arbitrage timing
- Arbitrage spread doesn't account for transaction costs, FX fees, or settlement timing
- Sub-unit currency map covers GBp, ILA, ZAc — other sub-units may exist
