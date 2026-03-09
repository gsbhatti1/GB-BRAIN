``` pinescript
/*backtest
start: 2023-11-26 00:00:00
end: 2023-12-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Kana with S/R Strategy", title = "KANA with S/R", overlay=true)

len = input(20, title="Length")
multiplier1 = input(true, title="multiplier1")
multiplier2 = input(2, title="multiplier2")
multiplier3 = input(3, title="multiplier3")
srtTimeFrame = input(240, title="Support Resistance TimeFrame")
useSupportResistance = input(true, title="Use Support/Resistance")
takeProfitPercent = input(0.5, title="Take Profit Percent")
useTakeProfit = input(false, title="Use Take Profit")
closeSource = input(close, title="Source: close", options=[close, high, low, open, hl2, hlc3, hlcc4, ohlc4])

// Strategy Description
strategy.description = "This is a fast breakout strategy based on Japanese candlestick technical analysis, combined with moving average indicators and support resistance indicators to determine trend and position. Its main idea is to wait for a fast price breakout and take profit quickly after the confirmation of moving average and trend indicators."

// Strategy Logic
sma = sma(closeSource, len)
ema = ema(closeSource, len * 10)
upTrend = sma > ema
downTrend = sma < ema

// Support and Resistance
supportResistance = request.security(syminfo.tickerid, srtTimeFrame, ta.sma(close, len))
supportResistanceLevel = if useSupportResistance
    supportResistance
else
    na

// Breakout Condition
breakoutCondition = if upTrend and closeSource > open and not na(supportResistanceLevel)
    true
else if downTrend and closeSource < open and not na(supportResistanceLevel)
    true
else
    false

// Enter and Exit
if breakoutCondition
    strategy.entry("Buy", strategy.long)
    // Stop Loss
    stopLossLevel = supportResistanceLevel + multiplier1 * atr(len)
    strategy.exit("Stop Loss", from_entry="Buy", stop=stopLossLevel)
    // Take Profit
    takeProfitLevel = supportResistanceLevel + multiplier2 * atr(len)
    if useTakeProfit
        strategy.exit("Take Profit", from_entry="Buy", limit=takeProfitLevel)
    
// Plotting
plot(sma, color=color.blue, title="SMA")
plot(ema, color=color.red, title="EMA")
```