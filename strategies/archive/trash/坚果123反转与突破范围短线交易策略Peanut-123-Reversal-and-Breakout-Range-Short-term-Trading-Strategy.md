``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 01/07/2019
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
//    Breakout Range Short Strategy
//
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing)
    vSlow = sma(stoch(close, high, low, Length), KSmoothing)
    vFast < Level ? vTrue : na
    vSlow > Level ? vTrue : na

BreakoutRangeShort(Look Bak) =>
    lowestLow = ta.lowest(low, Look Bak)
    close < lowestLow ? true : na

strategy("Peanut-123-Reversal-and-Breakout-Range-Short-term-Trading-Strategy", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 10)
    length = input(14, title = "Length")
    kSmoothing = input(true, title = "KSmoothing")
    dLength = input(3, title = "DLength")
    level = input(50, title = "Level")
    lookBak = input(4, title = "Look Bak")
    tradeReverse = input(false, title = "Trade reverse")

    isReversalBuy = (close > close[1] and close > close[2] and vSlow < level)
    isReversalSell = (close < close[1] and close < close[2] and vFast > level)
    isBreakoutSell = BreakoutRangeShort(lookBak)

    if (isReversalBuy and isBreakoutSell)
        strategy.entry("Buy", strategy.long)
    else if (isReversalSell and isBreakoutSell)
        strategy.entry("Sell", strategy.short)

    plotshape(series = isReversalBuy, title = "Buy Signal", location = location.belowbar, color = color.green, style = shape.triangleup, size = size.small)
    plotshape(series = isReversalSell, title = "Sell Signal", location = location.abovebar, color = color.red, style = shape.triangledown, size = size.small)
```

This Pine Script code implements the described strategy with the specified parameters and logic.