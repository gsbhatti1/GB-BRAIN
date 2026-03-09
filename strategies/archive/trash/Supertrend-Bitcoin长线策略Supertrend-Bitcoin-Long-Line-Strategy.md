> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|ATR Length|
|v_input_float_1|3|Factor|
|v_input_2|7|ADX Smoothing|
|v_input_3|7|DI Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-26 00:00:00
end: 2024-02-01 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Supertrend Bitcoin Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=1000, margin_long=0.1)

atrPeriod = input(10, "ATR Length")
factor = input.float(3.0, "Factor", step = 0.01)

[_, direction] = ta.supertrend(atrPeriod, factor)

rsi21 = ta.rsi(close, 21)
rsi3 = ta.rsi(close, 3)
rsi28 = ta.rsi(close, 28)
adx = ta.adx(high, low, close, 14)

longCondition = (direction < 0) and (rsi21 < 66) and (rsi3 > 80) and (rsi28 > 49) and (adx > 20)

if (longCondition)
    strategy.entry("Long", strategy.long)

if (direction > 0)
    strategy.close("Long")
```

This completes the translation of the strategy document. If you have any further requests or need additional adjustments, feel free to let me know!