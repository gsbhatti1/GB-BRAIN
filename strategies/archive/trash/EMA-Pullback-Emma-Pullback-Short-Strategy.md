``` pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-17 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="Linor Pullback Short Strategy", shorttitle="EMA Pullback", overlay=true)

// Define strategy parameters
ema_length = input(50, title="EMA Length")
pullback_candles = input(3, title="Number of Pullback Candles")
engulfing_candles = input(1, title="Number of Engulfing Candles")
stop_loss = input(1, title="Stop Loss (in ATR)")

// Calculate the EMA
ema = ema(close, ema_length)

// Define bearish impulse condition
bearish_impulse = crossover(close, ema)

// Define pullback condition
pullback_condition = false
for i = 1 to pullback_candles
    if close[i] > close[i - 1]
        pullback_condition := true
    else
        pullback_condition := false

// Define engulfing condition
engulfing_condition = false
for i = 1 to engulfing_candles
    if close[i] < open[i] and close[i-1] > open[i-1]
        engulfing_condition := true
    else
```

## Conclusion

This strategy first uses EMA to determine the trend direction, then combines pullback and engulfing pattern to generate short signals, a typical trend reversal strategy. By combining trend judgment and pattern recognition, it can effectively catch reversal opportunities. After parameter optimization, good results can be achieved. Overall, this strategy has easy operation, controllable risk, and is suitable for short-term trading. Its advantage lies in timely catching reversal trends, with a clear stop loss point. In general, this strategy has good practical value.

[/trans]

> Strategy Arguments

| Argument | Default | Description |
| ---- | ---- | ---- |
| v_input_1 | 50 | EMA Length |
| v_input_2 | 3 | Number of Pullback Candles |
| v_input_3 | true | Number of Engulfing Candles |
| v_input_4 | true | Stop Loss (in ATR) |

> Source (PineScript)

``` pinescript
//@version=4
strategy(title="Linor Pullback Short Strategy", shorttitle="EMA Pullback", overlay=true)

// Define strategy parameters
ema_length = input(50, title="EMA Length")
pullback_candles = input(3, title="Number of Pullback Candles")
engulfing_candles = input(1, title="Number of Engulfing Candles")
stop_loss = input(1, title="Stop Loss (in ATR)")

// Calculate the EMA
ema = ema(close, ema_length)

// Define bearish impulse condition
bearish_impulse = crossover(close, ema)

// Define pullback condition
pullback_condition = false
for i = 1 to pullback_candles
    if close[i] > close[i - 1]
        pullback_condition := true
    else
        pullback_condition := false

// Define engulfing condition
engulfing_condition = false
for i = 1 to engulfing_candles
    if close[i] < open[i] and close[i-1] > open[i-1]
        engulfing_condition := true
    else
```