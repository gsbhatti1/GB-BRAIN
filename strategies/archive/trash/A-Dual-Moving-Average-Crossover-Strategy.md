> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|Fast MA Length|
|v_input_2|30|Slow MA Length|
|v_input_3|true|Stop Loss (%)|
|v_input_4|2|Take Profit (%)|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-01-12 00:00:00
end: 2024-01-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Moving Average Crossover", overlay=true)

// Define input parameters
fast_length = input(10, title="Fast MA Length")
slow_length = input(30, title="Slow MA Length")
stop_loss_percent = input(1.0, title="Stop Loss (%)", minval=0.1, maxval=10, step=0.1)
take_profit_percent = input(2.0, title="Take Profit (%)", minval=0.1, maxval=10, step=0.1)

// Calculate moving averages
fast_ma = sma(close, fast_length)
slow_ma = sma(close, slow_length)

// Entry conditions
long_condition = crossover(fast_ma, slow_ma)
short_condition = crossunder(fast_ma, slow_ma)

// Plot moving averages on the chart
plot(fast_ma, title="Fast MA", color=color.blue)
plot(slow_ma, title="Slow MA", color=color.red)

// Strategy orders
strategy.entry("Long", strategy.long, when=long_condition)
strategy.entry("Short", strategy.short, when=short_condition)

// Set stop loss and take profit levels
stop_loss_price = close * (1 - stop_loss_percent / 100)
take_profit_price = close * (1 + take_profit_percent / 100)
strategy.exit("Take Profit/Stop Loss", from_entry="Long", stop=stop_loss_price, limit=take_profit_price)
strategy.exit("Take Profit/Stop Loss", from_entry="Short", stop=stop_loss_price, limit=take_profit_price)
```

This Pine Script defines a simple moving average crossover strategy with customizable fast and slow MA lengths, along with adjustable stop loss and take profit levels. The script calculates the moving averages, generates trading signals based on crossovers, and sets up appropriate entry and exit conditions using the `strategy` function in TradingView's Pine Script environment.