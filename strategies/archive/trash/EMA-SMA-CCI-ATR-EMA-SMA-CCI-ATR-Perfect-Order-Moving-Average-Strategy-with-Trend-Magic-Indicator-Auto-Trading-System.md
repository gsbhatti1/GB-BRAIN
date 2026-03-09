> Source (PineScript)

```pinescript
/* backtest
start: 2024-08-26 00:00:00
end: 2024-09-24 00:00:00
*/

//@version=5
indicator("EMA-SMA-CCI-ATR-Perfect Order Moving Average Strategy with Trend Magic Indicator", shorttitle="EPMAS-TMI")

ema45 = ta.ema(close, 45)
sma90 = ta.sma(close, 90)
sma180 = ta.sma(close, 180)

cciValue = ta.cci(20)
atrValue = ta.atr(14)

trendMagicColor = na
if (ema45 > sma90 and sma90 > sma180) or (ema45 < sma90 and sma90 < sma180)
    trendMagicColor := color.red
else if ta.crossover(cciValue, -80)
    trendMagicColor := color.green
else if ta.crossunder(cciValue, 80)
    trendMagicColor := color.blue

plot(ema45, title="EMA45", color=color.blue)
plot(sma90, title="SMA90", color=color.orange)
plot(sma180, title="SMA180", color=color.red)

plotshape(series=trendMagicColor, location=location.belowbar, color=color, style=shape.triangleup, size=size.small, title="Trend Magic Color")

longCondition = ema45 > sma90 and sma90 > sma180 and ta.crossover(cciValue, -80)
if (ta.change(trendMagicColor) and longCondition)
    strategy.entry("Long", strategy.long)

shortCondition = ema45 < sma90 and sma90 < sma180 and ta.crossunder(cciValue, 80)
if (ta.change(trendMagicColor) and shortCondition)
    strategy.entry("Short", strategy.short)

stopLoss = ta.valuewhen(ta.crossover(ema45, sma90), sma90, 1)
takeProfit = stopLoss * 1.5

strategy.exit("Take Profit", from_entry="Long", limit=takeProfit, stop=stopLoss)
```

This Pine Script code implements the strategy described in the document. It uses EMA45, SMA90, and SMA180 to identify trend conditions and a custom Trend Magic indicator based on CCI and ATR for confirming signals. The script also includes entry and exit conditions with stop-loss and take-profit levels set according to risk-reward principles.