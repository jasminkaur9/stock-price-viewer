# One-Shot Implementation Prompt

Copy and paste this into a coding agent along with `product-overview.md` and `app.py`.

---

I have a working Streamlit stock price viewer app. I need you to help me extend or deploy it.

**What exists:**
- A Streamlit app (`app.py`) with two tabs: Price Viewer and Arbitrage Finder
- Price Viewer: fetches OHLCV data via yfinance, displays metrics, interactive Plotly candlestick/line charts with volume, SMA overlays, multi-ticker comparison, CSV export
- Arbitrage Finder: compares same stock across exchanges, auto currency conversion (handles sub-unit currencies like GBp), spread analysis with threshold detection, opportunity table with CSV export
- Dependencies: streamlit, yfinance, plotly, pandas, numpy

**Before implementing, please clarify:**
1. What extensions do you want? (intraday data, alerts, more indicators, portfolio tracking)
2. Do you need a different data source? (yfinance is free but unofficial — alternatives: Polygon.io, Twelve Data, Tiingo)
3. Deployment target? (Streamlit Cloud, Docker, AWS, local only)
4. Any authentication needed? (user login, API keys management)
5. Database for persisting watchlists or historical analyses?

**Implementation constraints:**
- Keep calculation logic testable (no Streamlit imports in pure functions)
- Use `@st.cache_data` for all API calls
- Validate external inputs (ticker symbols, date ranges)
- Handle yfinance failures gracefully (empty DataFrames, network errors)
- Sub-unit currencies: GBp=/100, ILA=/100, ZAc=/100 — check for others if adding new exchanges
