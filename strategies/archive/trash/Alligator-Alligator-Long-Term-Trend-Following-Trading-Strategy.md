> Source (PineScript)

```pinescript
/*backtest
start: 2023-05-11 00:00:00
end: 2024-05-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//_______ <licence>
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://www.mozilla.org/en-US/MPL/2.0/
```

> Strategy Parameters

```pinescript
//@version=5
strategy("Alligator Long-Term Trend Following Trading Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Alligator Indicator
j = ta.sma(close, 13) + (ta.sma(close, 8) - ta.sma(close, 13)) * 8 / 13
t = ta.sma(close, 8) + (ta.sma(close, 5) - ta.sma(close, 8)) * 5 / 8
l = ta.sma(close, 5) + (ta.sma(close, 3) - ta.sma(close, 5)) * 3 / 5

// Plot Alligator Indicator
plot(j, color=color.red)
plot(t, color=color.orange)
plot(l, color=color.green)

// Trading Logic
if (j > t and t > l and close > j)
    strategy.entry("Long", strategy.long)

if (close < j)
    strategy.close("Long")

```

> Disclaimer

```pinescript
//_______ <disclaimer>
// This Pine Script™ code is for educational purposes only. The author does not guarantee the accuracy of this script or its performance in real trading conditions. Users should conduct their own research and testing before using this script.
```

> References

```pinescript
//_______ <references>
// Williams, R. (1986). Alligator Trading System. Technical Analysis: The Complete Guide to Market Timing, Vol. 2.
```

This section includes the Pine Script code for implementing the Alligator Long-Term Trend Following Trading Strategy based on the provided strategy description and parameters.