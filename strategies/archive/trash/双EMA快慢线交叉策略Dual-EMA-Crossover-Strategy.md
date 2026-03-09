> Name

Dual EMA Crossover Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/209e374f223308fa9fe.png)
[trans]
### Overview

The Dual EMA Crossover Strategy is a quantitative trading strategy that opens and closes positions based on the crossover of two EMA lines with different periods. This strategy is simple, effective, easy to understand, and commonly used in quantitative trading.

### Strategy Logic

The strategy uses two EMA lines, one is a 25-period EMA line as the fast line, and the other is a 50-period EMA line as the slow line. When the fast line crosses above the slow line, go long. When the fast line crosses below the slow line, go short.

After going long, set the take profit to 2% of the entry price and the stop loss to 2% of the entry price. When the price reaches the take profit or stop loss, close the position. Going short is the same.

The core of this strategy is to use the crossover of the EMA fast and slow lines to judge market trends and reversals. When the fast line crosses above, it is judged as a bull market and goes long. When the fast line crosses below, it is judged as a bear market and goes short. Take profit and stop loss are set to lock in profits and control risks.

### Advantage Analysis

The Dual EMA Crossover Strategy has the following advantages:

1. The idea is clear and the logic is simple, easy to understand and implement.
2. The fast and slow lines work together to capture medium and short-term trends.
3. It can follow the trend in a timely manner and seize market turning points.
4. The risk control is in place with reasonable take profit and stop loss settings.

In general, this strategy judges the market clearly, utilizes the advantages of the EMA itself, and obtains good medium and short-term returns while controlling risks.

### Risk Analysis

The Dual EMA Crossover Strategy also has some risks:

1. In case of violent market fluctuations, EMA crossover signals may be inaccurate, with a probability of misjudgement.
2. Unreasonable take profit and stop loss points may miss bigger moves or take on greater losses.
3. The impact of trading fees and slippage cannot be ignored either.

These risks can be optimized and solved in the following ways:

1. Combine other indicators to judge the market and avoid misjudged EMA crossover signals.
2. Test and optimize the take profit and stop loss points to strike a balance between returns and risks.
3. Choose trading platforms with low fees and appropriately increase position sizes.

### Optimization Directions

The main optimization directions for this strategy include:

1. Optimize the EMA period parameters to find the best parameter combination.
2. Increase other indicators for judgement to form a trading combination and improve accuracy.
3. Dynamically adjust take profit and stop loss points. For example, when the loss reaches a certain level, expand the stop loss point, and when the profit reaches a certain level, move the take profit point.
4. Distinguish bull and bear markets for directional trading.

These optimizations can improve return and win rates while keeping the strategy simple and clear.

### Summary

In summary, the Dual EMA Crossover Strategy is a very practical quantitative trading strategy. It is easy to understand and implement, and effectively captures market trends. At the same time, it has room for optimization. Further improvements on return rates can be achieved through parameter tuning and combinations. The simplicity and directness of this strategy is worth learning and applying for investors.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|25|(?[EMA]----------)Short|
|v_input_int_2|50|Long|
|v_input_bool_1|true|(?[TP & SL%]----------)Long - |
|v_input_float_1|2|TP|
|v_input_float_2|2|SL|
|v_input_bool_2|false|Short - |
|v_input_float_3|2|TP|
|v_input_float_4|2|SL|
|v_input_1|timestamp(0001-01-01)|(?[Backtest]----------)Start|
|v_input_2|timestamp(9999-01-01)|End|
|v_input_bool_3|false|Backtest BGcolor|
|v_input_bool_4|false|Position BGcolor|
|v_input_string_1|0|(?[IRISBOT]----------)Exchange: binance|bybit|upbit|
|v_input_string_2|account1|Account|
|v_input_string_3|BTC/USDT|Symbol|
|v_input_string_4|sema-x|Strategy|
|v_input_string_5|token|Token|
|v_input_float_5|100|Ratio(%)|
|v_input_float_6|true|Leverage|
|v_input_bool_5|false|View alert msg|


> Source (PineScript)

```pinescript
// Strategy: SEMA-X (SEMA CROSS) [AB] : Simple EMA cross strategy Alert & Backtest
// 1. 2 EMA cross
// 2. Next candle entry
// 3. TP & SL

//@version=5
strategy("SEMA-X", "SEMA-X", overlay=false, margin_long=1,
         initial_capital=1000000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, leverage=true)

// Parameters
ema_short_length = input.int(25, title="(?[EMA]----------)Short")
ema_long_length = input.int(50, title="Long")
take_profit = input.float(2, title="(?[TP & SL%]----------)Long - TP")
stop_loss = input.float(2, title="SL")
take_profit_short = input.float(2, title="TP")
stop_loss_short = input.float(2, title="SL")
backtest_start = input.time(timestamp("0001-01-01"), title="(?[Backtest]----------)Start")
backtest_end = input.time(timestamp("9999-01-01"), title="End")
backtest_bgcolor = input.bool(false, title="Backtest BGcolor")
position_bgcolor = input.bool(false, title="Position BGcolor")
exchange = input.string("binance", title="Exchange: binance|bybit|upbit")
account = input.string("account1", title="Account")
symbol = input.string("BTC/USDT", title="Symbol")
strategy_name = input.string("sema-x", title="Strategy")
token = input.string("token", title="Token")
ratio_percent = input.float(100, title="Ratio(%)")
leverage = input.bool(true, title="Leverage")
view_alert = input.bool(false, title="View alert msg")

// EMA Calculation
ema_short = ta.ema(close, ema_short_length)
ema_long = ta.ema(close, ema_long_length)

// Entry Conditions
long_entry = ta.crossover(ema_short, ema_long)
short_entry = ta.crossunder(ema_short, ema_long)

// Take Profit and Stop Loss
long_stop_loss = strategy.position_avg_price * (1 - stop_loss / 100)
long_take_profit = strategy.position_avg_price * (1 + take_profit / 100)
short_stop_loss = strategy.position_avg_price * (1 + stop_loss / 100)
short_take_profit = strategy.position_avg_price * (1 - take_profit / 100)

// Position Management
if (long_entry)
    strategy.entry("Long", strategy.long, comment="Long Entry")
    strategy.exit("Long TP/SL", "Long", limit=long_take_profit, stop=long_stop_loss)

if (short_entry)
    strategy.entry("Short", strategy.short, comment="Short Entry")
    strategy.exit("Short TP/SL", "Short", limit=short_take_profit, stop=short_stop_loss)

// Backtest Configuration
backtest = time >= backtest_start and time <= backtest_end
if (backtest)
    strategy.entry("Backtest Long", strategy.long, when=long_entry)
    strategy.exit("Backtest Long TP/SL", "Backtest Long", limit=long_take_profit, stop=long_stop_loss)
    strategy.entry("Backtest Short", strategy.short, when=short_entry)
    strategy.exit("Backtest Short TP/SL", "Backtest Short", limit=short_take_profit, stop=short_stop_loss)

// Plotting
plotshape(series=long_entry, title="Long Entry", location=location.belowbar, color=color.green, style=shape.labelup, text="Long")
plotshape(series=short_entry, title="Short Entry", location=location.abovebar, color=color.red, style=shape.labeldown, text="Short")
```

This PineScript code implements the Dual EMA Crossover Strategy as described.