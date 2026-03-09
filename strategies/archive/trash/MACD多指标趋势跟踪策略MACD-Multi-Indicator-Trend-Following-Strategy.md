``` pinescript
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
Yellow = #fcf932

// Getting inputs
fast_length = input.int(title="Fast Length", defval=12)
slow_length = input.int(title="Slow Length", defval=26)
src3 = input(title="Source", type=input.source, defval=close)
signal_length = input.int(title="Signal Smoothing", minval=1, maxval=50, defval=9)
sma_source = input.string(title="Oscillator MA Type", options=["SMA", "EMA"], defval="EMA")
sma_signal = input.string(title="Signal Line MA Type", options=["SMA", "EMA"], defval="EMA")

// Plot colors
col_macd = input(color=#2962FF, title="MACD Line  ", group="Color Settings", inline="MACD")
col_signal = input(color=#FF6D00, title="Signal Line  ", group="Color Settings", inline="Signal")
col_grow_above = input(color=#26A69A, title="Above   Grow", group="Histogram", inline="Above")
col_fall_above = input(color=#B2DFDB, title="Fall", group="Histogram", inline="Above")
col_grow_below = input(color=#FFCDD2, title="Below Grow", group="Histogram", inline="Below")
col_fall_below = input(color=#FF5252, title="Fall", group="Histogram", inline="Below")

// Calculating
fast_ma = ta.sma(src3, fast_length) when sma_source == "SMA" else ta.ema(src3, fast_length)
slow_ma = ta.sma(src3, slow_length) when sma_source == "SMA" else ta.ema(src3, slow_length)
macd = fast_ma - slow_ma
signal = ta.sma(macd, signal_length) when sma_signal == "SMA" else ta.ema(macd, signal_length)
hist = macd - signal

//@version=5
//indicator(title="Moving Average Exponential", shorttitle="EMA", overlay=true, timeframe="", timeframe_gaps=true)
len = input.int(200, minval=1, title="Length")
src2 = input(src3, title="Source")
offset = input.int(title="Offset", defval=0, minval=-500, maxval=500)
Bahubali = ta.ema(src2, len)
//plot(Bahubali, "EMA", color=color.blue, offset=offset)

//@version=5
//indicator(title="Williams Alligator", shorttitle="Alligator", overlay=true, timeframe="", timeframe_gaps=true)
jawLength = input.int(13, minval=1, title="Jaw Length")
teethLength = input.int(8, minval=1, title="Teeth Length")
lipsLength = input.int(5, minval=1, title="Lips Length")
jawOffset = input.int(title="Jaw Offset", defval=8)
teethOffset = input.int(title="Teeth Offset", defval=5)
lipsOffset = input.int(title="Lips Offset", defval=3)

jaw = smma(hl2, jawLength)
teeth = smma(hl2, teethLength)
lips = smma(hl2, lipsLength)

plot(jaw, "Jaw", offset=jawOffset, color=color(#2962FF))
plot(teeth, "Teeth", offset=teethOffset, color=color(#FFFF00))
plot(lips, "Lips", offset=lipsOffset, color=color(#FFA500))

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
```