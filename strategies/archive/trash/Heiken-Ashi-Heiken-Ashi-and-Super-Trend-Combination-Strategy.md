``` pinescript
/*backtest
start: 2022-12-08 00:00:00
end: 2023-12-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © RingsCherrY

//@version=5

strategy("Heiken Ashi & Super Trend", overlay=true, pyramiding=1, initial_capital = 10000, default_qty_type=strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.02)

///////////////////////////////////////////////////
////////////////////Function///////////////////////
///////////////////////////////////////////////////


heikinashi_open = request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, open)
heikinashi_high = request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, high)
heikinashi_low  = request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, low)
heikinashi_close= request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close)
heikinashi_color = heikinashi_open < heikinashi_close ? #53b987 : #eb4d5c
// plotbar(heikinashi_open, heikinashi_high, heikinashi_low, heikinashi_close, color=heikinashi_color)

x_sma(x, y) =>
    sumx = 0.0
    for i = 0 to y - 1
        sumx := sumx + x[i] / y
    sumx

x_rma(src, length) =>
    alpha = 1/length
    sum = 0.0
    sum := na(sum[1]) ? x_sma(src, length) : alpha * src + (1 - alpha) * nz(sum[1])

x_atr(length) =>
    trueRange = na(heikinashi_high[1])? heikinashi_high-heikinashi_low : math.max(math.max(heikinashi_high - heikinashi_low, math.abs(heikinashi_high - heikinashi_close[1])), math.abs(heikinashi_low - heikinashi_close[1]))
    //true range can be also calculated with ta.tr(true)
    x_rma(trueRange, length)

x_supertrend(factor, atrPeriod) =>
    src = (heikinashi_high+heikinashi_low)/2
    atr = x_atr(atrPeriod)
    multiplier = factor * atr
    upperband = src + multiplier
    lowerband = src - multiplier

    // Calculate the Super Trend direction
    trendDirection := na(trendDirection[1]) ? 1 : (close > upperband[trendDirection] ? 1 : 0)
    
    superTrend = na(superTrend[1]) ? upperband : (trendDirection == 1 and close < lowerband[trendDirection] ? lowerband : trendDirection == 1 ? upperband : superTrend[1])
    
    // Plot the Super Trend lines
    plot(superTrend, "SuperTrend", color=heikinashi_color)
    
    // Entry conditions
    longCondition = close > superTrend and prevSuperTrend <= superTrend
    shortCondition = close < superTrend and prevSuperTrend >= superTrend
    
    if (longCondition)
        strategy.entry("Long", strategy.long)
        
    if (shortCondition) 
        strategy.entry("Short", strategy.short)

```

This script includes the calculation of Heikin Ashi candles, ATR, and Super Trend signals. It also provides entry conditions based on the crossover of price with the Super Trend line.