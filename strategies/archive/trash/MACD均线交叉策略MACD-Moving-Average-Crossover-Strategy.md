```plaintext
## Strategy Principle

This strategy combines the MACD indicator and the moving average indicator, performing long transactions when they give signals in the same direction.

The specific transaction logic is:

1. Calculate the FAST MACD value, generally taking the 12-day exponential moving average (EMA).

2. Calculate the SLOW MACD value, generally taking the 26-day EMA.

3. The MACD value is calculated as FAST minus SLOW.

4. Calculate the signal line of MACD, generally taking the 9-day simple moving average (SMA).

5. Calculate the 9-day and 26-day SMAs.

6. When MACD crosses above the signal line, consider going long.

7. When the 9-day SMA crosses above the 26-day SMA, go long.

8. When MACD falls below the signal line and the 9-day SMA falls below the 26-day SMA, close the position.

This strategy fully utilizes the overbought/oversold judgment of the MACD and the trend-following ability of the moving average to combine both for trading, thereby increasing the success rate.

## Strategic Advantages

- The MACD determines overbought/oversold conditions, while the moving average determines the trend.
- The combination provides high-probability long opportunities.
- Clear rules that are easy to implement.

## Strategy Risk

- Optimization is required to determine the best parameters.
- Only go long; unable to take advantage of short opportunities.
- Trading with the general trend may increase losses.

## Summary

This strategy leverages the strengths of both MACD and moving averages to determine market rhythm. However, it focuses solely on long trading and requires attention to parameter optimization.
```

```pinescript
/*backtest
start: 2023-09-06 00:00:00
end: 2023-09-13 00:00:00
Period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("MACD Cross+MA", overlay=true)
//@version=4

// Getting inputs
fast_length = input(title="Fast Length", type=input.integer, defval=12)
slow_length = input(title="Slow Length", type=input.integer, defval=26)
src = input(title="Source", type=input.source, defval=close)
signal_length = input(title="Signal Smoothing", type=input.integer, minval = 1, maxval = 50, defval = 9)
sma_source = input(title="Simple MA(Oscillator)", type=input.bool, defval=false)
sma_signal = input(title="Simple MA(Signal Line)", type=input.bool, defval=false)

// === INPUT BACKTEST RANGE ===
FromYear = input(defval = 2019, title = "From Year", minval = 2009)
FromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromDay = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
ToYear = input(defval = 9999, title = "To Year", minval = 2009)
ToMonth = input(defval = 12, title = "To Month", minval = 1, maxval = 12)
ToDay = input(defval = 31, title = "To Day", minval = 1, maxval = 31)

// === FUNCTION EXAMPLE ===
start = timestamp(FromYear, FromMonth, FromDay, 00, 00) // backtest start window
finish = timestamp(ToYear, ToMonth, ToDay, 23, 59) // backtest finish window
window() => time >= start and time <= finish ? true : false // create function "within window of time"

//Calculating
fast_ma = sma_source ? sma(src, fast_length) : ema(src, fast_length)
slow_ma = sma_source ? sma(src, slow_length) : ema(src, slow_length)
macd = fast_ma - slow_ma
signal = sma_signal ? sma(macd, signal_length) : ema(macd, signal_length)
hist=macd-signal

//plot
plot(sma(close,9),color=color.red)
plot(sma(close,26),color=color.green)

//Condition
BMacdcondition= (macd>signal)
SMacdcondition= (macd<signal)
longCondition = crossover(sma(close, 9), sma(close, 26))
shortCondition = crossunder(sma(close, 9), sma(close, 26))

//entry
if (BMacdcondition) and window()
    longCondition
    strategy.entry("LONG", strategy.long)
if (shortCondition) and window()
    SMacdcondition
    strategy.close("LONG", qty_percent=100, comment="หนีตาย")
```

> Detail

https://www.fmz.com/strategy/426816

> Last Modified

2023-09-14 17:03:47
```