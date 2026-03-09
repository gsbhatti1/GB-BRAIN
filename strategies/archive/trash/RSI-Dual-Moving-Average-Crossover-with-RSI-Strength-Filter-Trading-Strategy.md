``` pinescript
/*backtest
start: 2024-06-20 00:00:00
end: 2024-12-01 00:00:00
period: 3d
basePeriod: 3d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("EMA and SMA Crossover with RSI14 Filtering", overlay=true)

// Define parameters for EMA, SMA, and RSI
ema5_length = 5
sma10_length = 10
rsi14_length = 14
rsi60_level = 60
rsi50_level = 50

// Calculate EMAs, SMAs, and RSI
ema5 = ta.ema(close, ema5_length)
sma10 = ta.sma(close, sma10_length)
rsi14 = ta.rsi(close, rsi14_length)

// Define Crossover Conditions
positive_crossover = ta.crossover(ema5, sma10)
negative_crossover = ta.crossunder(ema5, sma10)

// Define RSI filter conditions
rsi_above_60 = rsi14 > rsi60_level
rsi_below_50 = rsi14 < rsi50_level

// Condition: price below 60 on RSI 14 and later crosses above for Buy
price_below_rsi60 = close < rsi14
price_above_rsi60 = close > rsi14

// Condition: price above 50 on RSI 14 and later crosses below for Sell
price_above_rsi50 = close > rsi14
price_below_rsi50 = close < rsi14

// Trading logic
var bool active_buy_trade = false
var bool active_sell_trade = false

// Buy Condition: EMA 5 crosses above SMA 10 and RSI 14 is above 60, and price breaks through the RSI level
if (positive_crossover and not active_buy_trade)
    if (rsi_above_60 and (price_below_rsi60 or ta.crossover(close, rsi14)))
        strategy.entry("Buy", strategy.long)

// Sell Condition: EMA 5 crosses below SMA 10 and RSI 14 is below 50, and price breaks through the RSI level
if (negative_crossover and not active_sell_trade)
    if (rsi_below_50 and (price_above_rsi50 or ta.crossunder(close, rsi14)))
        strategy.entry("Sell", strategy.short)

// Exit Conditions: Close positions based on RSI levels breaking through price levels
if (not positive_crossover) // EMA 5 crosses below SMA 10
    if (rsi_below_50 and (price_above_rsi50 or ta.crossunder(close, rsi14)))
        strategy.close("Buy")
        
if (not negative_crossover) // EMA 5 crosses above SMA 10
    if (rsi_above_60 and (price_below_rsi60 or ta.crossover(close, rsi14)))
        strategy.close("Sell")

// Displaying the moving averages and RSI on the chart
plot(ema5, title="EMA5", color=color.blue)
plot(sma10, title="SMA10", color=color.red)
hline(rsi60_level, "RSI 60 Level", color=color.green)
hline(rsi50_level, "RSI 50 Level", color=color.orange)
```

This script implements the trading strategy as described in the document. It uses Pine Script to define and execute the strategy on a chart with appropriate visualizations for moving averages and RSI levels.