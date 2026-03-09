``` pinescript
/*backtest
start: 2024-12-06 00:00:00
end: 2025-01-04 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI and Bollinger Bands Synergistic Swing Trading Strategy", overlay=true, commission_type=strategy.commission.percent, commission_value=0.1, slippage=3)

// Input Parameters
rsiLength = input.int(14, minval=1, title="RSI Length")
rsiOverbought = input.int(60, minval=50, maxval=100, title="RSI Overbought Level") // Relaxed level
rsiOversold = input.int(40, minval=0, maxval=50, title="RSI Oversold Level")       // Relaxed level
bbLength = input.int(20, minval=1, title="Bollinger Bands Length")
bbMult = input.float(2.0, minval=0.1, maxval=5, title="Bollinger Bands StdDev Multiplier")
maLength = input.int(50, minval=1, title="Moving Average Length")

// RSI Calculation
rsi = ta.rsi(close, rsiLength)

// Bollinger Bands Calculation
bbBasis = ta.sma(close, bbLength)
bbDev = bbMult * ta.stdev(close, bbLength)
bbUpper = bbBasis + bbDev
bbLower = bbBasis - bbDev

// Moving Average
ma = ta.sma(close, maLength)

// Buy Signal: Price near or below lower Bollinger Band AND RSI below oversold level
buySignal = (close <= bbLower * 1.01) and (rsi < rsiOversold)

// Sell Signal: Price near or above upper Bollinger Band OR RSI above overbought level
sellSignal = (close >= bbUpper * 0.99) or (rsi > rsiOverbought)

// Date Range Inputs
startDate = input.timestamp("2018-01-01 00:00", title="Start Date")
endDate = input.timestamp("2069-12-31 23:59", title="End Date")
inDateRange = not ta.barssince(ta.time >= startDate) or ta.barssince(ta.time <= endDate)

// Strategy Logic
if buySignal and inDateRange
    strategy.entry("RSI+BB Buy Signal", strategy.long)
    
if sellSignal
    strategy.exit("RSI+BB Sell Signal", "RSI+BB Buy Signal", profit=0.02)
```

This script implements the described RSI and Bollinger Bands synergistic swing trading strategy using Pine Script in TradingView. The buy and sell conditions, as well as the parameters for the moving averages and Bollinger Bands, are set according to the provided description.