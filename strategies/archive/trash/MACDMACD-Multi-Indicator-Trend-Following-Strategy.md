> Name

MACD Multi-Indicator Trend Following Strategy MACD-Multi-Indicator-Trend-Following-Strategy

> Author

ChaoZhang

## Strategy Logic 

This strategy integrates MACD, moving averages, alligator lines and more to identify trend direction for trend following.

The logic is:

1. Compute MACD short, long, and histogram lines
2. Use histogram direction to determine short-term trend
3. Plot multiple moving averages to gauge price position 
4. Alligator lines judge overall trend strength
5. Combining above indicators, go long/short when aligned
6. Stop loss when indicators flip for early reversal

By synthesizing multiple indicators, it aims to trade strong trends and cut losses early when reversals happen.

## Advantages 

- MACD judges short-term trend and strength 
- MA positions determine mid-to-long term trends
- Alligator shows overall trend strength 
- Multiple indicators improve accuracy

## Risks 

- Extensive parameter optimization needed  
- Conflicting signals hard to interpret 
- Lagging issues with MAs etc.

## Summary 

This strategy attempts to comprehensively determine trend direction using multiple indicators. But lagging issues and signal conflicts warrant caution despite optimization.

||

```pinescript
/*backtest
start: 2023-09-06 00:00:00
end: 2023-09-13 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("5MSM VISHNU", overlay=true, process_orders_on_close=true)
//indicator(title="mahakaal", shorttitle="mahakaal", timeframe="", timeframe_gaps=true)

green = #26A69A
red = #FF0000
yellow = #fcf932

// Getting inputs
fast_length = input.int(title="Fast Length", defval=12)
slow_length = input.int(title="Slow Length", defval=26)
src3 = input.source(title="Source", defval(close))
signal_length = input.int(title="Signal Smoothing", minval=1, maxval=50, defval=9)
sma_source = input.string(title="Oscillator MA Type", defval="EMA", options=["SMA", "EMA"])
sma_signal = input.string(title="Signal Line MA Type", defval="EMA", options=["SMA", "EMA"])

// Plot colors
col_macd = input.color(#2962FF, title="MACD Line  ", group="Color Settings", inline="MACD")
col_signal = input.color(#FF6D00, title="Signal Line  ", group="Color Settings", inline="Signal")
col_grow_above = input.color(#26A69A, title="Above   Grow", group="Histogram", inline="Above")
col_fall_above = input.color(#B2DFDB, title="Fall", group="Histogram", inline="Above")
col_grow_below = input.color(#FFCDD2, title="Below Grow", group="Histogram", inline="Below")
col_fall_below = input.color(#FF5252, title="Fall", group="Histogram", inline="Below")

// Calculating
fast_ma = ta.sma(src3, fast_length) if (sma_source == "SMA") else ta.ema(src3, fast_length)
slow_ma = ta.sma(src3, slow_length) if (sma_source == "SMA") else ta.ema(src3, slow_length)
macd = fast_ma - slow_ma
signal = ta.sma(macd, signal_length) if (sma_signal == "SMA") else ta.ema(macd, signal_length)
hist = macd - signal

//@version=5
//indicator(title="Moving Average Exponential", shorttitle="EMA", overlay=true, timeframe="", timeframe_gaps=true)
len = input.int(200, minval=1, title="Length")
src2 = input.source(title="Source")
offset = input.int(title="Offset", defval=0, minval=-500, maxval=500)
Bahubali = ta.ema(src2, len)

//@version=5
//indicator(title="Williams Alligator", shorttitle="Alligator", overlay=true, timeframe="", timeframe_gaps=true)
smma(src, length) =>
    smma = 0.0
    if na(smma[1])
        smma := ta.sma(src, length)
    else
        smma := (smma[1] * (length - 1) + src) / length

jaw_length = input.int(13, minval=1, title="Jaw Length")
teeth_length = input.int(8, minval=1, title="Teeth Length")
lips_length = input.int(5, minval=1, title="Lips Length")
jaw_offset = input.int(title="Jaw Offset", defval=8)
teeth_offset = input.int(title="Teeth Offset", defval=5)
lips_offset = input.int(title="Lips Offset", defval=3)

jaw = smma(hl2, jaw_length)
teeth = smma(hl2, teeth_length)
lips = smma(hl2, lips_length)

if (hist > 9) 
    hist := 10

if (hist < -9)
    hist := -10

// Compose alert message
// Entry
alert_msg_long_entry =  
             "BUY ? {{ticker}} CE " + str.tostring(math.floor((close - 100)/100)*100)       + "\n"   + 
             "####################\n\n" + 
             "{{strategy.order.id}}? Target 1:  "         + str.tostring(math.round(close + 35))       + "\n"   + 
             "{{strategy.order.id}}? Target 2:  "         + str.tostring(math.round(close + 45))       + "\n"   +  
             "\n"   +  
             "{{strategy.order.id}} Stop Loss: "         + str.tostring(math.round(clos