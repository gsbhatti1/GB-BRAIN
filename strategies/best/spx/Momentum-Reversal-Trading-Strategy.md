``` pinescript
/*backtest
start: 2023-01-11 00:00:00
end: 2024-01-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tsujimoto0403

//@version=5
strategy("Momentum-Reversal-Trading-Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

//input value 
malongperiod=input.int(200, "period of long term sma", group="Parameters")
mashortperiod=input.int(10, "period of short term sma", group="Parameters")
stoprate=input.int(5, "stoploss percentages", group="Parameters")
profit=input.int(20, "take profit percentages", group="Parameters")
startday=input(title="start trade day", defval=timestamp("01 Jan 2000 13:30 +0000"), group="Period")
endday=input(title="finish date day", defval=timestamp("1 Jan 2099 19:30 +0000"), group="Period")

//plot indicators that we use 
malong=ta.sma(close, malongperiod)
mashort=ta.sma(close, mashortperiod)

plot(malong, color=color.aqua, line.style=line.style_solid, linewidth=2, title="200-period SMA")
plot(mashort, color=color.red, line.style=line.style_solid, linewidth=2, title="10-period SMA")

//strategy conditions 
if (close >= malong and close > mashort and ta.rsi(close, 3) < 30 and time >= startday and time <= endday)
    strategy.entry("Buy", strategy.long)

// stop loss and take profit 
if (strategy.position_size > 0)
    strategy.exit("Stop Loss", "Buy", stop=close * (1 - stoprate/100))
    strategy.exit("Take Profit", "Buy", limit=close * (1 + profit/100))

// plot chart 
plotshape(series=close >= malong and close > mashort and ta.rsi(close, 3) < 30, location=location.belowbar, color=color.green, style=shape.labeldown, title="Entry Signal")
```