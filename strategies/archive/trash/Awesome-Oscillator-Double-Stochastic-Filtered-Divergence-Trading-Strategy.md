``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Fixed AO Divergence Strategy", shorttitle="Fixed AO+Stoch", overlay=true)

// Calculate Awesome Oscillator
ao() => ta.sma(hl2, 5) - ta.sma(hl2, 34)
aoVal = ao()

// Stochastic Oscillator
stochK = ta.stoch(close, high, low, 14)
stochD = ta.sma(stochK, 3)

// Simplify the divergence detection logic
// For educational purposes, we will define a basic divergence detection mechanism
// Real-world application would require more sophisticated logic

// Detect bullish and bearish divergences based on AO and price action
bullishDivergence = (close > close[1]) and (aoVal < aoVal[1])
bearishDivergence = (close < close[1]) and (aoVal > aoVal[1])

// Stochastic Overbought/Oversold conditions
stochOverbought = (stochK > 80) and (stochD > 80)
stochOversold = (stochK < 20) and (stochD < 20)

// Filtered signals
confirmedBullishSignal = bullishDivergence and stochOversold
confirmedBearishSignal = bearishDivergence and stochOverbought

// Plot signals
plotshape(series=confirmedBullishSignal, style=shape.triangleup, location=location.belowbar, color=color.green, title="Bullish Divergence", text="BUY")
plotshape(series=confirmedBearishSignal, style=shape.triangledown, location=location.abovebar, color=color.red, title="Bearish Divergence", text="SELL")
```