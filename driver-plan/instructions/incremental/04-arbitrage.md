# Milestone 4: Cross-Exchange Arbitrage Finder

## Goal
Compare same stock on two exchanges, auto-convert currencies, detect spread opportunities.

## Steps
1. Add `st.tabs(["Price Viewer", "Arbitrage Finder"])` — wrap existing content in tab 1
2. Sidebar: two ticker inputs (Exchange 1/2), threshold slider (0.01-10%, step 0.01)
3. Currency detection: `yf.Ticker(symbol).info["currency"]`
4. Define sub-unit map: `{"GBp": ("GBP", 100), "ILA": ("ILS", 100), "ZAc": ("ZAR", 100)}`
5. `convert_to_usd()`:
   - If USD, return as-is
   - If sub-unit currency, look up main currency and divisor
   - Download forex pair `{MAIN_CURRENCY}USD=X`
   - Align dates, compute `(price / divisor) * fx_rate`
6. Merge on common trading dates, compute spread USD and %
7. Opportunity detection: `abs(spread_pct) >= threshold`
8. Summary metrics: 2 rows of 4 `st.metric` each
9. Price comparison chart: two `go.Scatter` lines in USD
10. Spread chart: `go.Scatter` line + `go.Bar` for opportunities + `add_hline` for thresholds
11. Opportunity table + CSV download

## Critical: Sub-Unit Currency Bug
```
GBp (pence) ≠ GBP (pounds)
yfinance returns RIO.L close as 7279.00 (pence)
GBpUSD=X returns 1.36 (same as GBPUSD=X — NOT divided by 100)

WRONG: 7279 * 1.36 = $9,899 (100x too high)
RIGHT: (7279 / 100) * 1.36 = $98.99 (matches RIO on NYSE at ~$99)
```

## Edge Cases
- Same currency (RELIANCE.NS vs .BO): no forex needed, spread near 0%
- No overlapping dates: show warning
- Missing forex data: fallback to raw prices (same-currency assumption)
