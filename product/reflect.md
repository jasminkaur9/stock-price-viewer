# Stock Price Viewer — Reflections

## Project Summary

**Product:** Stock Price Viewer with Cross-Exchange Arbitrage Finder
**Sections:** Data Collection, Interactive Charts, Enhancements (SMA/Compare/CSV), Arbitrage Finder
**Tech Stack:** Python + Streamlit + yfinance + Plotly + pandas

## What Worked Well

- **yfinance + Plotly + Streamlit** stack required zero config, zero API keys, instant results
- **Show don't tell** approach — each section was running within minutes, iterated on visible output
- **Validation caught a real bug** — GBp sub-unit currency issue would have silently produced 100x wrong arbitrage numbers for London-listed stocks
- **Incremental building** — Sections 1 → 2 → 3 → arbitrage built naturally on each other
- **Parallel research (分头研究)** upfront saved time by confirming the right libraries before writing any code

## Challenges & Learnings

### yfinance MultiIndex Columns
Every `yf.download()` call can return MultiIndex columns (especially for multi-ticker downloads). Required flatten logic on every download.

**Lesson:** Always flatten immediately after download — make it part of the standard fetch function, not an afterthought.

### Sub-Unit Currencies (GBp Bug)
yfinance reports London-listed stocks in `GBp` (pence), not `GBP` (pounds). The forex pair `GBpUSD=X` returns the same rate as `GBPUSD=X` — NOT divided by 100. This means naive `price * fx_rate` gives 100x wrong answer.

**Lesson:** Always check `yf.Ticker().info["currency"]` and maintain a sub-unit map. This is silent — no error, just wrong numbers. Validation is the only way to catch it.

### Scope Evolution
The arbitrage feature wasn't in the original 3-section plan. It emerged from the user asking "what if the same stock is on two exchanges?" — a natural extension of multi-ticker comparison.

**Lesson:** Plans will be wrong. The R-I loop (Represent <-> Implement) is how real work gets done. Budget for scope to evolve.

## Tech Stack Retrospective

### What Worked
- **Streamlit** — Perfect for analytical dashboards. Sidebar + tabs + metrics + charts in a single file. `st.cache_data` prevents redundant API calls.
- **Plotly** — `go.Candlestick` with built-in range selectors, unified hover, and volume subplots. Best interactive charting for Streamlit.
- **pandas** — Rolling means for SMA, DataFrame alignment for arbitrage merging, CSV export — all trivial.

### What Didn't Work
- **yfinance reliability** — Unofficial library that scrapes Yahoo Finance. Can break without warning. Fine for prototyping, risky for production.
- **Single-file architecture** — `app.py` at ~465 lines is manageable but approaching the limit. Adding more features would require splitting.

### Next Time, Use Instead
| Used | Consider For Production | Why |
|------|------------------------|-----|
| yfinance (free) | Polygon.io or Twelve Data | Official APIs, SLA, reliable |
| Single app.py | Streamlit multi-page (`pages/`) | Better organization at scale |
| In-memory state | SQLite or Redis | Persist watchlists, alert history |

## Time Analysis

**Most productive:** IMPLEMENT stage — show don't tell meant immediate feedback loops.

**Would have saved time:** Knowing about the GBp sub-unit issue upfront. This is a known gotcha in finance data that should be part of any cross-exchange checklist.

## Libraries & Tools to Remember

### Always Use
- `@st.cache_data(ttl=300)` — On every external API call in Streamlit
- `plotly.subplots.make_subplots` — For price + volume stacked charts
- `go.Candlestick` — Don't build candlesticks manually, Plotly has it native

### Avoid
- Trusting `{CURRENCY}USD=X` forex pairs for sub-unit currencies without checking the divisor
- Assuming yfinance column structure is flat — always check for MultiIndex

## Reusable Patterns

### Standard yfinance Fetch
```python
@st.cache_data(ttl=300)
def fetch_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, progress=False)
    if data.empty:
        return pd.DataFrame()
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.index = pd.to_datetime(data.index)
    return data
```

### Sub-Unit Currency Map
```python
SUB_UNIT_CURRENCIES = {
    "GBp": ("GBP", 100),  # pence
    "ILA": ("ILS", 100),  # agorot
    "ZAc": ("ZAR", 100),  # cents
}
```

### 4-Check Validation Framework
1. **Known answers** — Does output match manual calculation?
2. **Reasonableness** — Would you bet money on this?
3. **Edge cases** — Invalid input, empty data, single row, extremes
4. **AI blind spots** — Sub-unit currencies, MultiIndex, timezone assumptions

## Notes for Future Projects

- For any finance app dealing with multiple exchanges, build the sub-unit currency map on day one
- Streamlit + Plotly is the fastest path from zero to interactive finance dashboard
- The DRIVER workflow's insistence on 分头研究 (research first) prevented reinventing wheels
- Validation is not optional for finance tools — silent numerical errors are worse than crashes

---

*Captured using DRIVER*
