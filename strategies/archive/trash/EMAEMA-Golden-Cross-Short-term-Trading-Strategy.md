```pinescript
/*backtest
start: 2023-12-07 00:00:00
end: 2023-12-14 00:00:00
Period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © YukalMoon

//@version=5
strategy(title="EMA Golden Cross Short-term Trading Strategy", overlay=true, initial_capital = 1000)


//// input controls

v_input_int_1 = input.int (title = "EMA_L", defval = 9, minval = 1, maxval = 100, step =1)
v_input_int_2 = input.int (title = "EMA_L2", defval = 26, minval = 1, maxval = 100, step =1)
v_input_int_3 = input.int (title = "EMA_S", defval = 100, minval = 1, maxval = 100, step =1)
v_input_int_4 = input.int (title = "EMA_S2", defval = 55, minval = 1, maxval = 100, step =1)


/// EMA setup

shortest = ta.ema(close, v_input_int_1)  // 9-period EMA
short = ta.ema(close, v_input_int_2)    // 26-period EMA
longer = ta.ema(close, v_input_int_3)   // 100-period EMA
longest = ta.ema(close, v_input_int_4)  // 55-period EMA

plot(shortest, color = color.red)
plot(short, color = color.orange)
plot(longer, color = color.aqua)
plot(longest, color = color.yellow)

plot(close)


//// trading signals

EMA1 = ta.ema (close, v_input_int_1)  // 9-period EMA
EMA2 = ta.ema (close, v_input_int_2)  // 26-period EMA
EMA3 = ta.ema (close, v_input_int_3)  // 100-period EMA
EMA4 = ta.ema (close, v_input_int_4)  // 55-period EMA

buy = ta.crossover(EMA1, EMA2)
//sell = ta.crossunder(EMA1, EMA2)

buyexit = ta.crossunder(EMA3, EMA4)
//sellexit = ta.crossover(EMA3, EMA4)


//// strategy execution

strategy.entry ("long", strategy.short, when = buy, comment = "ENTER-SHORT")
//strategy.exit("Exit Long", "long", stop=buyexit, profit=close)  // You can add this to define the exit condition
```

Note: The commented-out `strategy.exit` line was added as an example of how you might define a stop loss or take profit condition. In practice, you would need to uncomment and modify it according to your specific needs.