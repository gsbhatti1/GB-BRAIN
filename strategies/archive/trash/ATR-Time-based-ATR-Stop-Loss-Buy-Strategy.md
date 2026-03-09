> Name

Time-based-ATR-Stop-Loss-Buy-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d21064b565fc14ad9a.png)
[trans]

### Overview

The core idea of this strategy is to combine time and ATR indicators to set the buy-in timing and stop loss points. The strategy issues a timed buy signal at the specified time point, uses the closing price at that time as the purchase price, and then sets the stop loss point at the purchase price plus the ATR value. This can filter out some unsuitable buy-in timings while using ATR to control risks.

### Strategy Principle  

The strategy consists of the following main parts:  

1. **Input Parameters**: Including buy-in time `timeTrade` and ATR parameter `atrLength`. `timeTrade` determines the buy-in time, and `atrLength` determines the period parameter of ATR.

2. **Calculate ATR Indicator**: Calculate the ATR value `atrValue` based on the `atrLength` parameter.

3. **Define Buy Conditions**: Generate buy signals when the combination of hours and minutes equals `timeTrade`.

4. **Issue Buy Order**: Go long when the buy condition is met, and record the purchase price `buyprice`.

5. **Set Stop Loss Point**: The stop loss point is set at the purchase price plus the ATR value. Stop loss exit when price breaks this point.

6. **Plotting**: Plot the stop loss level line.

### Advantage Analysis   

The biggest advantage of this strategy is the double confirmation of buy-in timing and stop loss point by time and ATR indicator. This avoids blindly following the market to buy in, and effectively controls risks. Secondly, the stop loss point set by ATR is dynamically changing, which can set a reasonable stop loss range according to market fluctuation. Finally, the strategy logic is simple and easy to understand and track.

### Risk Analysis  

The main risks of this strategy include:  

1. Improper setting of buy-in time may miss better buy-in opportunities or buy in undesirable markets.  

2. Improper parameter settings of ATR will affect strategy performance if stop loss point is too large or too small.   

3. Unable to track long-term trends effectively, more suitable for short-term operations.  

4. Fundamental analysis factors are not considered.

### Optimization Directions   

This strategy can be further optimized in the following aspects:  

1. Determine a more scientific buy-in time by combining multi-factor models.  

2. Optimize ATR parameter settings by combining volatility models.  

3. Increase trend tracking mechanism to adapt to longer holding periods.   

4. Incorporate fundamental analysis to judge the reasonableness of buy-in timing.  

### Conclusion  

Overall, this is a relatively simple and intuitive high frequency intraday trading strategy. The core idea is to use the double confirmation of time and ATR indicators to determine the buy-in timing and stop loss points. The advantages are controllable risks and relatively easy to implement. But there are also problems like insufficient selection of buy-in timing and inadequate parameter optimization. Future optimizations can be made from introducing more factors, dynamic parameter optimization, trend tracking etc.

||

### Overview  

The core idea of this strategy is to combine time and ATR indicators to set the buy-in timing and stop loss points. The strategy issues a timed buy signal at the specified time point, uses the closing price at that time as the purchase price, and then sets the stop loss point at the purchase price plus the ATR value. This can filter out some unsuitable buy-in timings while using ATR to control risks.

### Strategy Principle  

The strategy consists of the following main parts:  

1. **Input Parameters**: Including buy-in time `timeTrade` and ATR parameter `atrLength`. `timeTrade` determines the buy-in time, and `atrLength` determines the period parameter of ATR.

2. **Calculate ATR Indicator**: Calculate the ATR value `atrValue` based on the `atrLength` parameter.

3. **Define Buy Conditions**: Generate buy signals when the combination of hours and minutes equals `timeTrade`.

4. **Issue Buy Order**: Go long when the buy condition is met, and record the purchase price `buyprice`.

5. **Set Stop Loss Point**: The stop loss point is set at the purchase price plus the ATR value. Stop loss exit when price breaks this point.

6. **Plotting**: Plot the stop loss level line.

### Advantage Analysis  

The biggest advantage of this strategy is the double confirmation of buy-in timing and stop loss point by time and ATR indicator. This avoids blindly following the market to buy in, and effectively controls risks. Secondly, the stop loss point set by ATR is dynamically changing, which can set a reasonable stop loss range according to market fluctuation. Finally, the strategy logic is simple and easy to understand and track.

### Risk Analysis  

The main risks of this strategy include:  

1. Improper setting of buy-in time may miss better buy-in opportunities or buy in undesirable markets.  

2. Improper parameter settings of ATR will affect strategy performance if stop loss point is too large or too small.   

3. Unable to track long-term trends effectively, more suitable for short-term operations.  

4. Fundamental analysis factors are not considered.

### Optimization Directions  

This strategy can be further optimized in the following aspects:  

1. Determine a more scientific buy-in time by combining multi-factor models.  

2. Optimize ATR parameter settings by combining volatility models.  

3. Increase trend tracking mechanism to adapt to longer holding periods.   

4. Incorporate fundamental analysis to judge the reasonableness of buy-in timing.  

### Conclusion  

Overall, this is a relatively simple and intuitive high frequency intraday trading strategy. The core idea is to use the double confirmation of time and ATR indicators to determine the buy-in timing and stop loss points. The advantages are controllable risks and relatively easy to implement. But there are also problems like insufficient selection of buy-in timing and inadequate parameter optimization. Future optimizations can be made from introducing more factors, dynamic parameter optimization, trend tracking etc.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|700|(?Time Settings)Trade Execution Time (HHMM)|
|v_input_2|14|(?ATR Settings)ATR Length|


> Source (PineScript)

```pinescript
//@version=5
strategy("Time-based Strategy with ATR Stop Loss", overlay=true)

// Initialize take profit levels
var float takeProfitLevel = na
var float takeProfitLevelForSell = na
var float buyprice = na
var float sellprice = na

// Input for the time when the trade should be executed
tradeTime = input(700, "Trade Execution Time (HHMM)", "Specify the time in HHMM format", group="Time Settings")

// Calculate ATR for the last 5 minutes
atrLength = input(14, "ATR Length", "Specify ATR length", group="ATR Settings")
atrValue = request.security(syminfo.tickerid, "5", ta.atr(atrLength))

// Define conditions for buy and sell
buyCondition = hour * 100 + minute == tradeTime // and strategy.position_size == 0
sellCondition = hour * 100 + minute == tradeTime // and strategy.position_size > 0

// Execute Buy and Sell orders

if (buyCondition)
    strategy.entry("Buy", strategy.long)
    buyprice := close
    takeProfitLevel := buyprice + atrValue
    strategy.exit("Take Profit BUY", from_entry="Buy", limit = takeProfitLevel)

// if (sellCondition)
//     strategy.entry("Sell", strategy.short)
//     sellprice := close
//     takeProfitLevelForSell := sellprice - atrValue
//     strategy.exit("Take Profit Sell", from_entry="Sell", limit=takeProfitLevelForSell)

// Plot horizontal lines for take profit levels
plot(takeProfitLevel, color=color.green, title="Take Profit Level")
```