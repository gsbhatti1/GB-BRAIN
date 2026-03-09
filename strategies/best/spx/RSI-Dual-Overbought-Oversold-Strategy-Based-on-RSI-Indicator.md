> Name

Dual-Overbought-Oversold-Strategy-Based-on-RSI-Indicator

> Author

ChaoZhang

> Strategy Description



```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-09-12 00:00:00
Period: 4d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("test1", "t1", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value=100, initial_capital=200, currency=currency.USD)
//user input
k_param = input(title="k length", type=input.integer, defval=14)
d_param = input(title="d length", type=input.integer, defval=3)
rsi_param = input(title="RSI", type=input.integer, defval=5)
upper = input(title="overbought", type=input.integer, defval=80)
lower = input(title="oversold", type=input.integer, defval=20)

//calculation
rsi = rsi(close, rsi_param)
stochastic = 100 * (rsi - lowest(rsi, k_param)) / (highest(rsi, k_param) - lowest(rsi, k_param))
SMA = sma(stochastic, d_param)

//DRAW
plot(upper, color=color.blue, linewidth=2, title="overbought")
plot(lower, color=color.blue, linewidth=2, title="oversold")
plot(rsi, color=rsi>upper?color.red:rsi<lower?color.green:color.black, linewidth=2,title="RSI overbought oversold")
plot(stochastic, color=color.purple, title="Oscillation Index")
plot(SMA, color=color.orange, title="Moving Average")

//trading
shortposition = crossover(rsi, upper)
longposition = crossunder(rsi, lower)
strategy.entry("sell", false, when=(shortposition))
strategy.entry("buy", true, when=(longposition))
strategy.exit("stop profit", profit=close*0.013/syminfo.mintick)
```

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|k_param|14|k length|
|d_param|3|d length|
|rsi_param|5|RSI|
|upper|80|overbought|
|lower|20|oversold|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-09-12 00:00:00
Period: 4d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("test1", "t1", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value=100, initial_capital=200, currency=currency.USD)
//user input
k_param = input(title="k length", type=input.integer, defval=14)
d_param = input(title="d length", type=input.integer, defval=3)
rsi_param = input(title="RSI", type=input.integer, defval=5)
upper = input(title="overbought", type=input.integer, defval=80)
lower = input(title="oversold", type=input.integer, defval=20)

//calculation
rsi = rsi(close, rsi_param)
stochastic = 100 * (rsi - lowest(rsi, k_param)) / (highest(rsi, k_param) - lowest(rsi, k_param))
SMA = sma(stochastic, d_param)

//DRAW
plot(upper, color=color.blue, linewidth=2, title="overbought")
plot(lower, color=color.blue, linewidth=2, title="oversold")
plot(rsi, color=rsi>upper?color.red:rsi<lower?color.green:color.black, linewidth=2,title="RSI overbought oversold")
plot(stochastic, color=color.purple, title="Oscillation Index")
plot(SMA, color=color.orange, title="Moving Average")

//trading
shortposition = crossover(rsi, upper)
longposition = crossunder(rsi, lower)
strategy.entry("sell", false, when=(shortposition))
strategy.entry("buy", true, when=(longposition))
strategy.exit("stop profit", profit=close*0.013/syminfo.mintick)
```


> Detail

https://www.fmz.com/strategy/426604

> Last Modified

2023-09-13 16:58:55