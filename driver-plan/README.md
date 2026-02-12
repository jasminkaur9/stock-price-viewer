# Stock Price Viewer

A Streamlit-based interactive stock price viewer with cross-exchange arbitrage detection.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Features

### Tab 1: Price Viewer
- **Data Collection** — Fetch daily OHLCV data via yfinance for any ticker
- **Key Metrics** — Latest close, open, high, low, volume with daily change
- **Interactive Chart** — Candlestick or line chart with Plotly (zoom, pan, hover)
- **Volume Subplot** — Color-coded volume bars (green = up, red = down)
- **Moving Averages** — SMA 20/50/200 overlays (togglable)
- **Range Selectors** — 1M, 3M, 6M, YTD, 1Y, All buttons
- **Multi-Ticker Comparison** — Normalized % change chart for comparing tickers
- **CSV Export** — Download OHLCV data as CSV

### Tab 2: Arbitrage Finder
- **Cross-Exchange Comparison** — Compare same stock on two exchanges
- **Auto Currency Conversion** — Detects currency, converts to USD via live forex
- **Sub-Unit Currency Handling** — Correctly handles GBp (pence), ILA, ZAc
- **Spread Analysis** — Daily spread chart with configurable threshold bands
- **Opportunity Detection** — Highlights days where |spread| exceeds threshold
- **Opportunity CSV Export** — Download arbitrage opportunities

## Tech Stack

| Component | Library | Version |
|-----------|---------|---------|
| UI Framework | Streamlit | 1.54+ |
| Data Source | yfinance | latest |
| Charts | Plotly | 6.5+ |
| Processing | pandas | 2.3+ |

## Validated Pairs

| Exchange 1 | Exchange 2 | Notes |
|-----------|-----------|-------|
| SHOP | SHOP.TO | US vs Canada (USD/CAD) — tight spread ~0.02% |
| RIO | RIO.L | US vs London (USD/GBp) — requires sub-unit fix |
| RELIANCE.NS | RELIANCE.BO | India NSE vs BSE (same currency) — near-zero spread |
| TM | 7203.T | US ADR vs Tokyo (USD/JPY) |

## Validation Results

| Check | Status | Evidence |
|-------|--------|---------|
| Known Answers | PASS | OHLCV matches yfinance raw; SMA = manual mean; arbitrage math verified |
| Reasonableness | PASS | Same-country spreads ~0%; cross-currency spreads <1% for liquid stocks |
| Edge Cases | PASS | Invalid ticker, future dates, single day, weekends all handled |
| AI Blind Spots | FIXED | GBp sub-unit currency bug caught and fixed during validation |

## Future Directions

- Intraday data support for real-time arbitrage monitoring
- Transaction cost modeling (fees, FX spread) for realistic P&L
- Alerts/notifications when spread exceeds threshold
- Historical volatility and correlation analysis
- Portfolio tracker with multi-position support
