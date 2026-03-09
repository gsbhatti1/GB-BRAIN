---
## Overview

The Noro Shifted Moving Average Stop Loss Strategy is a trend following strategy. It calculates the 3-day simple moving average (SMA), and sets a long line above it by adding a percentage `lo`, and a stop loss line below it by subtracting a percentage `sl`. Take profit lines are also set at a percentage `tp` above the current average holding price.

## Strategy Logic

The core of this strategy involves calculating the 3-day simple moving average (SMA) `ma`. Then, adding a percentage `lo` to `ma` yields the long line `long` for entries. When the price crosses above `long`, long positions are opened. Below `ma`, subtracting a percentage `sl` results in the stop loss line `stop`. If the price falls below `stop`, positions are stopped out. Additionally, take profit lines `take` are set at a percentage `tp` above the current average holding price.

The specific rules are as follows:

1. Calculate 3-day simple moving average (SMA) `ma`
2. Long line `long = ma + (ma * lo%)`
3. Take profit line `take = Current average holding price + (Current average holding price * tp%)`
4. Stop loss line `stop = Current average holding price - (Current average holding price * sl%)`

This setup constructs a trend-following strategy that sets entry, take profit, and stop loss lines based on the SMA benchmark and configurable percentages.

## Advantage Analysis

The main advantage of this strategy is its ability to automatically track trends. By entering long positions during uptrends and short positions during downtrends without needing pattern recognition, it captures intermediate trends effectively. The addition of take profit and stop loss lines ensures automatic exit when trends reverse, limiting potential drawdowns.

Another advantage lies in the flexibility of parameter adjustments. Modifying percentages for entry, take profit, and stop loss can control position sizing and stop loss spacing easily.

## Risk Analysis

The primary risk associated with this strategy is significant slippage. Using stop orders for stop losses can result in substantial price gaps before the trade is executed during a rapid market decline, leading to severe losses.

Another risk arises from inappropriate parameter settings that may cause too frequent entries and exits, increasing transaction costs and fees.

## Optimization Directions

To improve this strategy, consider implementing the following optimizations:

1. Utilize limit orders for stop losses to mitigate slippage risks
2. Add position sizing settings to scale in and out smoothly, reducing trade frequency  
3. Incorporate trend detection filters to avoid false signals in non-trending markets
4. Optimize parameter settings to find the best combination

## Conclusion

The Noro Shifted Moving Average Stop Loss Strategy is a simple yet practical trend-following strategy that can automatically track trends with take profit and stop loss controls to manage risk effectively. The primary risks are significant slippage during rapid market declines and overly frequent trading due to poorly optimized parameters. By enhancing the stop loss method and optimizing parameters, this strategy can be made more robust.

||

## Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|-5|Long-line percentage|
|v_input_2|5|Take-profit percentage|
|v_input_3|2|Stop-loss percentage|


## Source (PineScript)

```pinescript
/*backtest
start: 2023-12-30 00:00:00
end: 2024-01-29 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//2019
//Noro

//@version=4
strategy("Stop-loss", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings
lo = input(-5.0, title = "Long-line percentage")
tp = input(5.0, title = "Take-profit")
sl = input(2.0, title = "Stop-loss")

//SMA
ma = sma(ohlc4, 3)
long = ma + ((ma / 100) * lo)

//Orders
avg = strategy.position_avg_price
if ma > 0
    strategy.entry("Long", strategy.long, limit = long)
    strategy.entry("Take", strategy.short, 0, limit = avg + ((avg / 100) * tp))
    strategy.entry("Stop", strategy.short, 0, stop = avg - ((avg / 100) * sl))
    
//Cancel order
if strategy.position_size == 0
    strategy.cancel("Take")
    strategy.cancel("Stop")

//Lines
plot(long, offset = 1, color = color.black, transp = 0)
take = avg != 0 ? avg + ((avg / 100) * tp) : long + ((long / 100) * tp)
stop = avg != 0 ? avg - ((avg / 100) * sl) : long - ((long / 100) * sl)
takelinecolor = avg == avg[1] and avg != 0 ? color.lime : na
stoplinecolor = avg == avg[1] and avg != 0 ? color.red : na
plot(take, offset = 1, color = takelinecolor, linewidth = 3, transp = 0)
plot(stop, offset = 1, color = stoplinecolor, linewidth = 3, transp = 0)
```

## Detail

https://www.fmz.com/strategy/440438

## Last Modified

2024-01-30 15:49:34
```