``` pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2025-02-16 08:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy('[Hoss] Combined Strategy', overlay=true)

// Indikator 1: [Hoss] VWAP Deviation
indicator_vwap = input.bool(true, title="Show VWAP Deviation Indicator", group="Visibility")
length = input.int(60, title="VWAP Length", group="VWAP Settings")
src = input(close, title="Source", group="VWAP Settings")

// Berechnungen für VWAP
vwmean = ta.wma(src, length)
dev = ta.stdev(src, length)
basis = vwmean
upper_dev2 = vwmean + dev * 2
lower_dev2 = vwmean - dev * 2

// Plotting VWAP Deviation
plot(indicator_vwap ? basis : na, color=color.gray, title='Basis', linewidth=2)
plot1 = plot(indicator_vwap ? upper_dev2 : na, color=color.red, title='Upper Dev 2', linewidth=2)
plot2 = plot(indicator_vwap ? lower_dev2 : na, color=color.green, title='Lower Dev 2', linewidth=2)
fill(plot1, plot2, color=color.new(color.green, 80), title='Deviation Band')

// Indikator 2: [Hoss] OBV RSI
indicator_obv_rsi = input.bool(true, title="Show OBV RSI Indicator", group="Visibility")
len = input.int(14, title="RSI Length", group="OBV RSI Settings")
obv = ta.cum(ta.change(src) > 0 ? volume : ta.change(src) < 0 ? -volume : 0)
rsi = ta.rsi(obv, len)

// Plotting OBV RSI
plot(indicator_obv_rsi ? rsi : na, color=color.blue, title='OBV RSI', linewidth=2)
hline(30, 'Oversold Line', color=color.red, linestyle=hline.style_dotted, width=1)
hline(70, 'Overbought Line', color=color.orange, linestyle=hline.style_dotted, width=1)

// Entry Conditions
longCondition = (indicator_obv_rsi and rsi <= 30) and (close < lower_dev2)
shortCondition = (indicator_obv_rsi and rsi >= 70) and (close > upper_dev2)

if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit Condition
exitPrice = input.float(1.006, title="Exit Price Ratio", group="Risk Management")
takeProfit = ta.percent Change(close[1], close) * exitPrice

if (close >= takeProfit or close <= lower_dev2)
    strategy.close("Long")

if (close <= -takeProfit or close >= upper_dev2)
    strategy.close("Short")

// Risk Management
strategy.exit("Exit Long", "Long", stop=ta.percentChange(close, 1) * -exitPrice)
strategy.exit("Exit Short", "Short", stop=ta.percentChange(close, 1) * exitPrice)

```

This Pine Script translates the provided Chinese text into English and integrates it with a basic implementation of the strategy in TradingView's Pine Script. The script includes plotting of VWAP deviation bands, OBV RSI lines, entry and exit conditions, as well as risk management features such as stop-losses and take-profits.