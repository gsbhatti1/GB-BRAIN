```pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Bollinger + RSI, Double Strategy (by ChartArt) v1.1", shorttitle="CA_-_RSI_Bol_Strat_1.1", overlay=true)

// ChartArt's RSI + Bollinger Bands, Double Strategy - Update
//
// Version 1.1
// Idea by ChartArt on January 18, 2015.
//
// This strategy uses the Relative Strength Index (RSI) indicator 
// together with the Bollinger Bands 
// to sell when the price is above the upper Bollinger Band 
// (and to buy when this value is below the lower band).
//
// The strategy only triggers trading signals when both 
// the RSI and the Bollinger Bands indicators are simultaneously in an overbought or oversold state.
//
// In version 1.1, the strategy was simplified for the user
// and made more successful in backtesting. 
//
// List of my work: 
// https://www.tradingview.com/u/ChartArt/
// 
//  __             __  ___       __  ___ 
// /  ` |__|  /\  |__)  |   /\  |__)  |  
// \__, |  | /~~\ |  \  |  /~~\ |  \  |  
// 
// 

///////////// RSI
RSIlength = input(14, title="RSI Period Length")
RSIoverSold = 30
RSIoverBought = 70
price = close
vrsi = rsi(price, RSIlength)


///////////// Bollinger Bands
BBlength = input(20, minval=1, title="Bollinger Period Length")
BBmult = input(2.0, minval=0.001, maxval=50, title="Bollinger Bands Standard Deviation")
BBbasis = sma(price, BBlength)
BBdev = BBmult * stdev(price, BBlength)
BBupper = BBbasis + BBdev
BBlower = BBbasis - BBdev
source = close
buyEntry = crossover(source, BBlower)
sellEntry = crossunder(source, BBupper)
plot(BBbasis, color=color.blue, title="Bollinger Bands SMA Basis Line")
p1 = plot(BBupper, color=color.red, title="Bollinger Bands Upper Line")
p2 = plot(BBlower, color=color.green, title="Bollinger Bands Lower Line")
fill(p1, p2)

// Entry conditions
crossover_rsi = crossover(vrsi, RSIoverSold) and crossover(source, BBlower)
crossunder_rsi = crossunder(vrsi, RSIoverBought) and crossunder(source, BBupper)

///////////// RSI + Bollinger Bands Strategy
if (not na(vrsi))
    if (crossover_rsi)
        strategy.entry("Buy", strategy.long)
    if (crossunder_rsi)
        strategy.close("Buy")
```

This script combines the Relative Strength Index (RSI) and Bollinger Bands to generate buy and sell signals. It uses RSI to identify overbought or oversold conditions while using Bollinger Bands to determine entry points based on price movements relative to the bands.