``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-15 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=5
strategy(title="Outside Bar EMA Crossover Strategy with EMA Shift", shorttitle="Outside Bar EMA Cross", overlay=true)

// Input for EMA lengths
lenEMA1 = input.int(5, title="EMA 5 Length")
lenEMA2 = input.int(9, title="EMA 9 Length")

// Input for EMA 9 shift
emaShift = input.int(1, title="EMA 9 Shift", minval=0)

// Calculate EMAs
ema1 = ta.ema(close, lenEMA1)
ema2 = ta.ema(close, lenEMA2)

// Apply shift to EMA 9
ema2Shifted = na(ema2[emaShift]) ? na : ema2[emaShift]  // Shift EMA 9 using offset

// Plot EMAs
plot(ema1, title="EMA 5", color=color.blue, linewidth=2)
plot(ema2Shifted, title="EMA 9 Shifted", color=color.red, linewidth=2)

// Outside Bar condition
outsideBar() => high > high[1] and low < low[1]

// Cross above EMA 5 and EMA 9 (shifted)
crossAboveEMA = close > ema1 and close > ema2Shifted

// Cross below EMA 5 and EMA 9 (shifted)
crossBelowEMA = close < ema1 and close < ema2Shifted

// Outside Bar cross above EMA 5 and EMA 9 (shifted)
outsideBarCrossAbove = outsideBar() and crossAboveEMA

// Outside Bar cross below EMA 5 and EMA 9 (shifted)
outsideBarCrossBelow = outsideBar() and crossBelowEMA

// Plot shapes for visual signals
plotshape(series=outsideBarCrossAbove, title="Outside Bar Cross Above", location=location.belowbar, color=color.green, style=shape.labelup, text="Buy", textcolor=color.white)
plotshape(series=outsideBarCrossBelow, title="Outside Bar Cross Below", location=location.abovebar, color=color.red, style=shape.labeldown, text="Sell", textcolor=color.white)

// Calculate
```