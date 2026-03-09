``` pinescript
/*backtest
start: 2022-12-08 00:00:00
end: 2023-12-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// @version=4

strategy("HYE Mean Reversion SMA [Strategy]", overlay = true )
  
//Strategy inputs
source = input(title = "Source", defval = close)
tradeDirection = input(title="Trade Direction", type=input.string,
     options=["Long Only", "Short Only", "Both"], defval="Long Only") 
smallMAPeriod = input(title = "Small Moving Average", defval = 2)
bigMAPeriod = input(title = "Big Moving Average", defval = 5)
percentBelowToBuy = input(title = "% below to buy", defval = 3)
percentAboveToSell = input(title = "% above to sell", defval = 3)
rsiPeriod = input(title = "RSI Period", defval = 2)
maxRsiLevelForBuy = input(title = "Max RSI Level for Buy", defval = 30)
minRsiLevelForSell = input(title = "Min RSI Level for Sell", defval = 70)
startDate = input(title="Start Date", type=input.integer, defval=2020, minval=1950) 
startMonth = input(title="Start Month", type=input.integer, defval=1, minval=1, maxval=12)
startYear = input(title="Start Year", type=input.integer, defval=2020, minval=1950)
endDate = input(title="End Date", type=input.integer, defval=31, minval=1) 
endMonth = input(title="End Month", type=input.integer, defval=12, minval=1, maxval=12)
endYear = input(title="End Year", type=input.integer, defval=2021, minval=1950)

// Calculate moving averages
smallSMA = sma(source, smallMAPeriod)
bigSMA = sma(source, bigMAPeriod)

// RSI calculation
rsi = rsi(close, rsiPeriod)

// Buy condition: price falls below the small SMA by a certain percentage and RSI is below the buy threshold
buyCondition = (close < smallSMA * (1 - percentBelowToBuy / 100) and rsi < maxRsiLevelForBuy)

// Sell condition: price crosses above the big SMA or RSI is above the sell threshold
sellCondition = (close > bigSMA and not buyCondition) or (rsi > minRsiLevelForSell and not buyCondition)

// Apply trade direction filter
if (tradeDirection == "Long Only")
    strategy.entry("Buy", strategy.long, when=buyCondition)
else if (tradeDirection == "Short Only")
    strategy.close("Buy", when=sellCondition)
else
    strategy.entry("Buy", strategy.long, when=buyCondition)
    strategy.close("Buy", when=sellCondition)

// Plot the moving averages and RSI on the chart
plot(smallSMA, color=color.blue, title="Small SMA")
plot(bigSMA, color=color.red, title="Big SMA")
hline(minRsiLevelForSell, "Min RSI Level for Sell", color=color.orange)
hline(maxRsiLevelForBuy, "Max RSI Level for Buy", color=color.green)

// Define the backtest period
if (year(time) >= startYear and month(time) >= startMonth and dayOfMonth(time) >= startDate) and 
   (year(time) <= endYear and month(time) <= endMonth and dayOfMonth(time) <= endDate)
    strategy.apply_rules()
```

This updated Pine Script reflects the provided arguments and logic described in the document.