> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|2|Lookback for Inside Bar|
|v_input_source_1_close|0|_____ falls above HIGH of inside bar (Long condition): close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_source_2_close|0|_____ falls below LOW of inside bar (Short condition): close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_source_3_close|0|EMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|50|EMA Length|
|v_input_bool_1|false|(?ADX)Average Directional Index (ADX)|
|v_input_3|14|ADX Smoothing|
|v_input_4|14|DI Length|
|v_input_5|25|ADX Threshold|
|v_input_bool_2|true|(?Date Range)Start|
|v_input_6|timestamp(1 Jan 2019)|startPeriodTime|
|v_input_bool_3|true|End|
|v_input_7|timestamp(31 Dec 2030)|endPeriodTime|
|v_input_string_1|0|(?Trade Direction)Trade Direction: Long and Short|Long Only|Short Only|
|v_input_float_1|10.5|(?Take Profit)Take Profit 1 - Target %|
|v_input_int_1|25|% Of Position|
|v_input_float_2|11|Take Profit 2 - Target %|
|v_input_int_2|25|% Of Position|
|v_input_float_3|11.5|Take Profit 3 - Target %|
|v_input_int_3|25|% Of Position|
|v_input_float_4|12|Take Profit 4 - Target %|
|v_input_float_5|4|(?Stop Loss)Stop Loss (%)|
|v_input_float_6|true|(?Leverage)Leverage|
|v_input_string_2|CRYPTANEX_99FTX_Strategy-Name-Here|(?ProfitView Alert Syntax)Alert Syntax Prefix|
|v_input_bool_4|false|(?Dashboard)Show Dashboard|


> Source (PineScript)

```pinescript
//@version=5
strategy("Automated-Quantitative-Trading-Strategy-Based-on-Inside-Bar-and-Moving-Average", overlay=true)

// Inside Bar Parameters
insideBarLookback = input.int(2, minval=1, title="Lookback for Inside Bar")
longCondition = ta.crossover(v_input_source_1_close, high)
shortCondition = ta.crossunder(v_input_source_2_close, low)

// EMA Parameters
emaSource = input.source(close, title="EMA Source")
emaLength = input.int(50, minval=1, title="EMA Length")
ema = ta.ema(emaSource, emaLength)

// ADX Parameters
adxOn = v_input_bool_1
adxSmoothing = input.int(14, minval=1, title="ADX Smoothing")
diLength = input.int(14, minval=1, title="DI Length")
adxThreshold = input.float(25.0, title="ADX Threshold")

// Date Range Parameters
startDate = input.time(timestamp("2019-01-01 00:00:00"), title="Start")
endDate = input.time(timestamp("2030-12-31 23:59:59"), title="End")

// Trade Direction Parameters
tradeDirection = input.string("Long and Short", title="Trade Direction", options=["Long Only", "Short Only", "Long and Short"])

// Take Profit Parameters
tp1 = input.float(10.5, title="Take Profit 1 - Target %")
tp1PositionPercent = input.int(25, title="% of Position")
tp2 = input.float(11, title="Take Profit 2 - Target %")
tp2PositionPercent = input.int(25, title="% of Position")
tp3 = input.float(11.5, title="Take Profit 3 - Target %")
tp3PositionPercent = input.int(25, title="% of Position")
tp4 = input.float(12, title="Take Profit 4 - Target %")

// Stop Loss Parameters
stopLossPercent = input.float(4, title="Stop Loss (%)")

// Leverage
leverage = input.bool(true, title="Leverage")

// ProfitView Alert Syntax
alertPrefix = input.string("CRYPTANEX_99FTX_Strategy-Name-Here", title="ProfitView Alert Syntax Prefix")

// Dashboard
showDashboard = input.bool(false, title="Show Dashboard")

// Plotting
plotshape(series=longCondition, title="Long Condition", location=location.belowbar, color=color.green, style=shape.labelup, text="LONG")
plotshape(series=shortCondition, title="Short Condition", location=location.abovebar, color=color.red, style=shape.labeldown, text="SHORT")

// Strategy Logic
if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Take Profit and Stop Loss Logic
if (strategy.position_size > 0)
    tp1Level = strategy.position_avg_price * (1 + tp1 / 100)
    tp2Level = strategy.position_avg_price * (1 + tp2 / 100)
    tp3Level = strategy.position_avg_price * (1 + tp3 / 100)
    tp4Level = strategy.position_avg_price * (1 + tp4 / 100)
    stopLossLevel = strategy.position_avg_price * (1 - stopLossPercent / 100)

    strategy.exit("Take Profit 1", from_entry="Long", limit=tp1Level)
    strategy.exit("Take Profit 2", from_entry="Long", limit=tp2Level)
    strategy.exit("Take Profit 3", from_entry="Long", limit=tp3Level)
    strategy.exit("Take Profit 4", from_entry="Long", limit=tp4Level)
    strategy.exit("Stop Loss", from_entry="Long", stop=stopLossLevel)

    strategy.exit("Take Profit 1", from_entry="Short", limit=tp1Level)
    strategy.exit("Take Profit 2", from_entry="Short", limit=tp2Level)
    strategy.exit("Take Profit 3", from_entry="Short", limit=tp3Level)
    strategy.exit("Take Profit 4", from_entry="Short", limit=tp4Level)
    strategy.exit("Stop Loss", from_entry="Short", stop=stopLossLevel)
```
```