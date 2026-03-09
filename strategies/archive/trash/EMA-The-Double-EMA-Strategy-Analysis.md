``` pinescript
/*backtest
start: 2023-02-21 00:00:00
end: 2024-02-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
// This can only draw so many lines. Use bar replay to go back further
strategy("Strategy Lines", shorttitle="Strategy Lines", overlay=true, max_lines_count=500)

//###########################################################################################################################################
// Replace your strategy here
//###########################################################################################################################################

shortEMA = ta.ema(close, input(9, title="Short EMA Length"))
longEMA = ta.ema(close, input(21, title="Long EMA Length"))

// Entry conditions for long and short positions
longCondition = ta.crossover(shortEMA, longEMA)
shortCondition = ta.crossunder(shortEMA, longEMA)

//###########################################################################################################################################
// Strategy Lines
//###########################################################################################################################################

var timeLow = bar_index
var line li = na
var openLPrice = 0.0000
var openSPrice = 0.0000

LongWColor = input.color(color.rgb(0,255,0,0),"Long Win Color", group="Strategy Lines")
LongLColor = input.color(color.rgb(0,0,255,0),"Long Loss Color", group="Strategy Lines")
ShortWColor = input.color(color.rgb(255,255,0,0),"Short Win Color", group="Strategy Lines")
ShortLColor = input.color(color.rgb(255,0,0,0),"Short Loss Color", group="Strategy Lines")
WinFontColor = input.color(color.rgb(0,0,0,0),"Win Font Color", group="Strategy Lines")
LossFontColor = input.color(color.rgb(255,255,255,0),"Loss Font Color", group="Strategy Lines")

if (longCondition)
    li := line.new(x1=bar_index, y1=openLPrice, x2=bar_index, y2=openLPrice, color=LongWColor, width=3, style=line.style_dotted)
    strategy.entry("Long Entry", strategy.long)

if (shortCondition)
    li := line.new(x1=bar_index, y1=openSPrice, x2=bar_index, y2=openSPrice, color=ShortLColor, width=3, style=line.style_dotted)
    strategy.close("Long Entry")
    strategy.entry("Short Entry", strategy.short)

plotshape(series=strategy.position_size != 0, title="Position Size Indicator", location=location.belowbar, color=WinFontColor, style=shape.labeldown, text="Position Opened")

// Add labels for win and loss
if (longCondition)
    label.new(x=bar_index, y=openLPrice, text="Long Win", color=LongWColor, style=label.style_labelup)

if (shortCondition)
    label.new(x=bar_index, y=openSPrice, text="Short Loss", color=ShortLColor, style=label.style_labeldown)

```

This completes the translation of your trading strategy document into English. The Pine Script has been adjusted to include all necessary parts and ensure that the code remains as provided.