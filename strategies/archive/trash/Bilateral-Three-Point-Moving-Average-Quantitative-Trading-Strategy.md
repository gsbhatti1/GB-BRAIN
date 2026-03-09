``` pinescript
/*backtest
start: 2023-01-24 00:00:00
end: 2024-01-30 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 25/06/2018
// The FVE is a pure volume indicator. Unlike most of the other indicators 
// (except OBV), price change doesn't come into the equation for the FVE (price 
// is not multiplied by volume), but is only used to determine whether money is 
// flowing in or out of the stock. This is contrary to the current trend in the 
// design of modern money flow indicators. The author decided against a price-volume 
// indicator for the following reasons:
// - A pure volume indicator has more power to contradict.
// - The number of buyers or sellers (which is assessed by volume) will be the same, 
//     regardless of the price fluctuation.
// - Price-volume indicators tend to spike excessively at breakouts or breakdowns.
//
// You can change long to short in the Input Settings
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
strategy("Bilateral-Three-Point-Moving-Average-Quantitative-Trading-Strategy", overlay=true)

nPeriod = input(22, title="Period")
factor = input(0.3, title="Factor")
tradeReverse = input(False, title="Trade reverse")

// Calculate XHL2 and XHLC3
highN = high(nPeriod)
lowN = low(nPeriod)
closeN = close(nPeriod)

xhl2 = (highN + lowN) / 2
xhlc3 = (highN + lowN + closeN) / 3

// Calculate nMF, nRES
nMF = xhl2 - close
nRES = xhlc3 - xhl2

// Determine trend direction and generate signals
if (nMF > factor)
    plot(nMF, color=green, title="Upward Trend")
    strategy.entry("Buy", when=nRES > 0)
elseif (nMF < -factor)
    plot(nMF, color=red, title="Downward Trend")
    strategy.entry("Sell", when=nRES < 0)

// Trade reverse
if tradeReverse and nRES * strategy.position_size < 0
    if strategy.is_long
        strategy.close("Buy")
    elif strategy.is_short
        strategy.close("Sell")

plot(nMF, title="nMF", color=black)
```

This script implements the "Bilateral-Three-Point-Moving-Average-Quantitative-Trading-Strategy" as described. It calculates the XHL2 and XHLC3 indicators based on recent price data and uses them to determine buy/sell signals. The strategy can be adjusted for trading in reverse if needed.