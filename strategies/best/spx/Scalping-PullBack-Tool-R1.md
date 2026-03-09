```pinescript
/*backtest
start: 2022-05-12 00:00:00
end: 2022-05-18 23:59:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//

study(title="Scalping PullBack Tool R1.1 by JustUncleL", shorttitle="SCALPTOOL R1.1", overlay=true)

//
// Revision:        1.1
// Original Author: JustUncleL
//
// Description:
//    This study project is a Scalping Pullback trading Tool that incorporates the majority of the indicators
//    needed to analyse and scalp Trends for Pull Backs and reversals intended for lower time frame
//    charts upto 15min, but it should work just as well on higher time frame charts for
//    longer term trades.
//
//    This Tool can be used with Heikin Ashi (HA) candle charts or normal candle charts, HA candles
//    will show a cleaner/smoother looking candle trend  but not show true prices.
//
//    Incorporated within this tool are the following indicators:
//    1. Trader selectable important EMAs in an EMA style Ribbon: 
//       - Green = fast EMA (default=89)
//       - Blue  = medium EMA (default=200) 
//       - Black = slow EMA (default=600)
//    2. The PAC EMA (default=34) High/Low+Close creates the Price Action Channel (PAC).
//    3. Fractals
//    4. HH, LH, LL, HL finder may help with drawing Trend lines and mini Trend Lines.
//    5. Coloured coded Bar high lighting based on the PAC: 
//       - blue = bar closed above PAC
//       - red  = bar closed below PAC
//       - gray = bar closed inside PAC
//       - red line = PAC EMA (34) of bar close
//    6. Coloured chart Background to indicate Trend direction 
//       (NOTE: slow EMA(600) is not used in this Algo):
//       - green  = Trend direction is up when PAC and fast EMA(89) are above medium EMA(200).
//       - red    = Trend direction is down when PAC and fast EMA(89) are below medium EMA(200).
//       - yellow = Trend direction is in transition.
//    7. Pullback is defined as Price starts outside the PAC and then pulls back into the PAC
//       closing the opposite side of the PAC centre line, then a recovery arrow can occur.
//    8. Coloured Alert Arrows:
//       - maroon down arrow  = Pullback recovery Sell alert
//       - green up arrow     = Pullback recovery Buy alert
//    9. Option to force Heikin Ashi candles in Algo calculations.
//
// Setup and hints:
//
//  - I also add "Sweetspot Gold RN" indicator to the chart as well to help with support and resistance
//    finding and shows where the important "00" and "0" lines are.
//  - When price is above the PAC (blue bars) we are only looking to buy as price comes back to the PAC.
//  - When price is below the PAC (red bars), we are only looking to sell when price comes back to the PAC.
//  - What we’re looking for when price comes back into the PAC, we draw mini Trendlines using the Fractals
//    and HH/LL points to guide your TL drawing.
//  - Now look for the trend to pull back and break the drawn mini TL. That's where we can place the scalp
//    trade.
//  - So we are looking for continuation signals in terms of a strong, momentum driven pullbacks 
//    of the PAC EMA (34).
//  - The other EMAs are there to check for other Pullbacks when PAC EMA (34) is broken.
//  - Other than the "Sweetspot Gold RN" indicator, you should not need any other indicator to scalp
//    for pullbacks.

strategy("Scalping PullBack Tool R1.1", overlay=true)

v_input_1 = input(34, title="PAC channel length")
v_input_2 = input(89, title="fast EMA length")
v_input_3 = input(200, title="medium EMA length")
v_input_4 = input(600, title="slow EMA length")
v_input_5 = input(true, title="Show fast EMA")
v_input_6 = input(true, title="Show medium EMA")
v_input_7 = input(false, title="Show slow EMA")
v_input_8 = input(false, title="Show HH/LL")
v_input_9 = input(true, title="Show Fractals")
v_input_10 = input(false, title="Show Ideal Fractals Only")
v_input_11 = input(true, title="Show coloured Bars around PAC")
v_input_12 = input(true, title="Show TrendDirection/TrendDirection Alert Arrows")
v_input_13 = input(3, title="Pullback Lookback for PAC Cross Check")
v_input_14 = input(false, title="Show Alert Arrows Only on Closed Candles")
v_input_15 = input(true, title="Show TrendBGcolor")
v_input_16 = input(true, title="Use Heikin Ashi Candles in Algo Calculations")

// Define the Heikin Ashi candles
heikinashi = v_input_16 ? heikinashi(close) : close

// Define the EMAs
fast_ema = ema(heikinashi, v_input_2)
med_ema = ema(heikinashi, v_input_3)
slow_ema = ema(heikinashi, v_input_4)

// Define the PAC channel
p_ac_length = v_input_13 + 1
p_ac_high = highest(high, p_ac_length) 
p_ac_low = lowest(low, p_ac_length) 
p_ac_close = close

// Draw the PAC
plot(p_ac_high, color=color.blue)
plot(p_ac_low, color=color.red)

// Define the bars' colors based on their relation to the PAC
bar_color = na
if (close > p_ac_close)
    bar_color := color.blue
else if (close < p_ac_close)
    bar_color := color.red
else 
    bar_color := color.gray

bgcolor(bar_color, transp=90)

// Plot the EMAs
plot(fast_ema, title="fast EMA", color=color.green, linewidth=2) when v_input_5
plot(med_ema, title="medium EMA", color=color.blue, linewidth=2) when v_input_6
plot(slow_ema, title="slow EMA", color=color.black, linewidth=2) when v_input_7

// Plot the Fractals
fractal = request.security(syminfo.tickerid, "1", fractal(close))
plotshape(series=fractal, location=location.belowbar, color=color.red, style=shape.triangleup)

// Plot the TrendDirection arrows
trend_up = close > p_ac_close and fast_ema > med_ema
trend_down = close < p_ac_close and fast_ema < med_ema
plotarrow(series=trend_up ? 1 : na, color=color.green, title="Buy Alert")
plotarrow(series=trend_down ? -1 : na, color=color.maroon, title="Sell Alert")

// Show alerts only on closed candles
alertcondition(trend_up and close[1] < p_ac_close, title="Buy Alert", message="Buy Alert")
alertcondition(trend_down and close[1] > p_ac_close, title="Sell Alert", message="Sell Alert")
```

This script is designed to be used with Pine Script in TradingView for scalping pullbacks. It includes Heikin Ashi candles, EMAs, PAC channel, fractals, and trend direction arrows. The setup instructions and hints are embedded within the comments of the script.