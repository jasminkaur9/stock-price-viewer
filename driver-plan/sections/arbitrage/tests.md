# Arbitrage Finder — Test Instructions

## Unit Tests (pytest)

### Test Currency Detection
```python
def test_currency_detection():
    assert get_ticker_currency("AAPL") == "USD"
    assert get_ticker_currency("SHOP.TO") == "CAD"
    assert get_ticker_currency("RELIANCE.NS") == "INR"
    assert get_ticker_currency("RIO.L") == "GBp"
    assert get_ticker_currency("7203.T") == "JPY"
```

### Test Sub-Unit Conversion
```python
def test_sub_unit_currencies():
    # GBp: price in pence, must divide by 100 before FX
    assert SUB_UNIT_CURRENCIES["GBp"] == ("GBP", 100)
    assert SUB_UNIT_CURRENCIES["ILA"] == ("ILS", 100)
    assert SUB_UNIT_CURRENCIES["ZAc"] == ("ZAR", 100)
```

### Test Spread Calculation
```python
def test_spread_same_ticker():
    """Same ticker should have 0% spread."""
    # Download AAPL twice, compute spread
    # Expected: spread = 0.0 for all dates

def test_spread_same_currency():
    """RELIANCE.NS vs .BO: same currency, near-zero spread."""
    # Expected: avg |spread| < 0.5%

def test_spread_cross_currency():
    """SHOP vs SHOP.TO: USD vs CAD, should be within ~2%."""
    # Expected: avg |spread| < 2%
```

### Test GBp Bug Prevention
```python
def test_rio_arbitrage_reasonable():
    """RIO vs RIO.L: prices should be within ~5% after conversion."""
    # If GBp not handled: spread would be ~9900% (100x error)
    # Expected: avg |spread| < 5%
```

## Integration Tests

### Test Full Flow
1. Fetch SHOP + SHOP.TO for last 30 days
2. Verify both DataFrames non-empty
3. Verify currency detection (USD, CAD)
4. Verify forex CADUSD=X returns data
5. Verify merged DataFrame has overlapping dates
6. Verify spread is reasonable (-5% to +5%)

### Test Edge Cases
1. Invalid ticker → empty DataFrame → error message
2. Future dates → empty DataFrame → error message
3. Same ticker both inputs → spread = 0%
4. Weekend-only range → empty → warning message
