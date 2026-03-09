``` pinescript
//@version=4
// Pine Script v4
// @author ChaoZhang
// Script Library: https://www.fmz.com

study("Triple Moving Average Trading Strategy", shorttitle="TMA Strategy", overlay=true)

// Inputs
v_input_1 = input(50, title="MA1 Period")
v_input_2 = input(type=string, defval="SMA", title="MA1 Type", options=["SMA", "RMA", "EMA", "WMA", "HMA", "DEMA", "TEMA", "VWMA"])
v_input_3_close = input(false, title="MA1 Source: close")
v_input_4 = input(0, title="MA1 Resolution: 00 Current|01 1m|02 3m|03 5m|04 15m|05 30m|06 45m|07 1h|08 2h|09 3h|10 4h|11 1D|12 1W|13 1M")
v_input_5 = input(true, title="MA1 Visible")
v_input_6 = input(100, title="MA2 Period")
v_input_7 = input(type=string, defval="SMA", title="MA2 Type", options=["SMA", "RMA", "EMA", "WMA", "HMA", "DEMA", "TEMA", "VWMA"])
v_input_8_close = input(false, title="MA2 Source: close")
v_input_9 = input(0, title="MA2 Resolution: 00 Current|01 1m|02 3m|03 5m|04 15m|05 30m|06 45m|07 1h|08 2h|09 3h|10 4h|11 1D|12 1W|13 1M")
v_input_10 = input(true, title="MA2 Visible")
v_input_11 = input(200, title="MA3 Period")
v_input_12 = input(type=string, defval="SMA", title="MA3 Type", options=["SMA", "RMA", "EMA", "WMA", "HMA", "DEMA", "TEMA", "VWMA"])
v_input_13_close = input(false, title="MA3 Source: close")
v_input_14 = input(0, title="MA3 Resolution: 00 Current|01 1m|02 3m|03 5m|04 15m|05 30m|06 45m|07 1h|08 2h|09 3h|10 4h|11 1D|12 1W|13 1M")
v_input_15 = input(true, title="MA3 Visible")
v_input_16 = input(false, title="Show Crosses")
v_input_17 = input(0, title="Forecast Bias: Neutral|Bullish|Bearish", options=["Neutral", "Bullish", "Bearish"])
v_input_18 = input(14, title="Forecast Bias Period")
v_input_19 = input(true, title="Forecast Bias Magnitude")
v_input_20 = input(true, title="Show Forecasts")
v_input_21 = input(true, title="Show Ribbons")
v_input_22 = input(true, title="Trade MA 1-2 Crosses")
v_input_23 = input(true, title="Trade MA 1-3 Crosses")
v_input_24 = input(true, title="Trade MA 2-3 Crosses")
v_input_25 = input(30, title="Take Profit Percent")
v_input_26 = input(15, title="Stop Loss Percent")

// Moving Averages
ma1 = v_input_1 >= v_input_6 ? v_input_2 == "SMA" ? sma(close, v_input_1) : 
                            v_input_2 == "RMA" ? rma(close, v_input_1) :
                            v_input_2 == "EMA" ? ema(close, v_input_1) :
                            v_input_2 == "WMA" ? wma(close, v_input_1) :
                            v_input_2 == "HMA" ? hma(close, v_input_1) :
                            v_input_2 == "DEMA" ? dema(close, v_input_1) : 
                            v_input_2 == "TEMA" ? tema(close, v_input_1) : 
                            v_input_2 == "VWMA" ? vwma(high, low, close, volume, v_input_1) : na
ma2 = v_input_6 >= v_input_11 ? v_input_7 == "SMA" ? sma(close, v_input_6) :
                            v_input_7 == "RMA" ? rma(close, v_input_6) :
                            v_input_7 == "EMA" ? ema(close, v_input_6) :
                            v_input_7 == "WMA" ? wma(close, v_input_6) :
                            v_input_7 == "HMA" ? hma(close, v_input_6) :
                            v_input_7 == "DEMA" ? dema(close, v_input_6) : 
                            v_input_7 == "TEMA" ? tema(close, v_input_6) : 
                            v_input_7 == "VWMA" ? vwma(high, low, close, volume, v_input_6) : na
ma3 = v_input_11 >= v_input_6 ? v_input_12 == "SMA" ? sma(close, v_input_11) :
                            v_input_12 == "RMA" ? rma(close, v_input_11) :
                            v_input_12 == "EMA" ? ema(close, v_input_11) :
                            v_input_12 == "WMA" ? wma(close, v_input_11) :
                            v_input_12 == "HMA" ? hma(close, v_input_11) :
                            v_input_12 == "DEMA" ? dema(close, v_input_11) : 
                            v_input_12 == "TEMA" ? tema(close, v_input_11) : 
                            v_input_12 == "VWMA" ? vwma(high, low, close, volume, v_input_11) : na

// Plot MAs
plot(v_input_5 ? ma1 : na, title="MA1", color=color.blue)
plot(v_input_10 ? ma2 : na, title="MA2", color=color.red)
plot(v_input_15 ? ma3 : na, title="MA3", color=color.green)

// Show crosses
if (v_input_16 and crossover(ma1, ma2))
    label.new(x=bar_index, y=high*1.01, text="Buy", style=label.style_label_up, color=color.green)
if (v_input_16 and crossunder(ma1, ma2))
    label.new(x=bar_index, y=low*0.99, text="Sell", style=label.style_label_down, color=color.red)

// Trade logic
longCondition = v_input_22 ? crossover(ma1, ma2) : na
shortCondition = v_input_23 and not v_input_24 ? crossunder(ma1, ma2) : na

if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Take profit and stop loss
takeProfitPercent = v_input_25 / 100.0 * close
stopLossPercent = v_input_26 / 100.0 * close

strategy.exit("Take Profit Long", "Long", limit=takeProfitPercent)
strategy.exit("Stop Loss Long", "Long", stop=stopLossPercent)
strategy.exit("Take Profit Short", "Short", limit=-takeProfitPercent)
strategy.exit("Stop Loss Short", "Short", stop=-stopLossPercent)

```

This script defines the Triple Moving Average (TMA) strategy, allowing users to customize various parameters such as moving average types and periods. It plots the moving averages on the chart and uses crossover and crossunder conditions to generate trading signals for entering long or short positions. Additionally, it sets up take-profit and stop-loss levels based on user-defined percentages of the closing price. The script is designed to be backtested and used in TradingView's Pine Script environment.