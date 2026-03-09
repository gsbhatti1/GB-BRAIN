> Name

A Trend-Following Strategy Based on Dynamic Support and Resistance

> Author

ChaoZhang

> Strategy Description


[trans]

This article explains in detail a trend trading strategy that utilizes dynamic support and resistance levels. This strategy employs multiple indicators to set dynamic support and resistance zones, capturing price trends.

I. Strategy Logic

The main components of the strategy include:

1. Calculating the highest high and lowest low over a certain period to define dynamic trading ranges.
2. Computing the ATR indicator and setting upper/lower bands as dynamic stop loss zones.
3. Drawing dynamic support/resistance lines at fixed slopes when price breaks out of the trading range.
4. Generating trade signals when price breaks through dynamic support/resistance levels.

By synthesizing multiple indicators to set dynamic support and resistance zones, trades are only taken on breakouts to filter out unnecessary noise. The stop loss zones also adjust dynamically to market changes.

II. Advantages of the Strategy

The biggest advantage lies in the dynamic zones formed by multiple indicators, which can nimbly detect trend changes.

Another benefit is the banded stop loss zones, which reduce the probability of stops being hit.

Finally, the simple and straightforward method for drawing sloped support/resistance lines makes implementation easy.

III. Potential Risks

However, we should also consider the following potential risks:

Firstly, dynamic levels may lag price moves and become invalidated.

Secondly, stop loss zones set too wide may lead to large losses.

Lastly, improper parameter tuning could result in poor strategy performance.

IV. Summary

This article has detailed a trend-following strategy that uses multiple dynamic indicators to identify support and resistance zones. It can effectively filter out noise and detect trends. However, risks such as indicator lagging and overwide stops should be prevented. Overall, it provides a reasonable approach to utilizing dynamic support and resistance.

||

This is a trading strategy designed to draw trend lines in the form of slopes whenever high points and low points are updated. The upper slope serves as a resistance line, while the lower slope acts as a support line. Traders buy when the closing price crosses the slope.

```pinescript
// backtest
// start: 2023-08-14 00:00:00
// end: 2023-09-13 00:00:00
// period: 2h
// basePeriod: 15m
// exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]

//@version=5
strategy("Donchian Trendline - Support Resistance Slope [UhoKang]", shorttitle="Donchian Trendline", overlay=true, initial_capital=1000000,default_qty_type=strategy.percent_of_equity,default_qty_value=100,commission_value=0.075,slippage=3, process_orders_on_close=true)
///////////////////////////////////// Time ///////////////////////////////////////////////////////////////////////////////
startYear   = input.int(2019, 'Start-Year', confirm=false, inline='1')
startMonth  = input.int(1,    'Month',      confirm=false, inline='1')
startDay    = input.int(1,    'Day',        confirm=false, inline='1')
finishYear  = input.int(2099, 'End-Year',   confirm=false, inline='2')
finishMonth = input.int(1,    'Month',      confirm=false, inline='2')
finishDay   = input.int(1,    'Day',        confirm=false, inline='2')
startTime = timestamp(startYear, startMonth, startDay)
finishTime = timestamp(finishYear, finishMonth, finishDay)
testPeriod = true

//////////////////////// ATR BAND /////////////////////////////////////////////////////////////////////////////////////////
// Inputs
atrPeriod = input.int(title = "ATR Period", defval = 14, minval = 1)
atrBandUpper = input(title = "Source Upper", defval = close)
atrBandLower = input(title = "Source Lower", defval = close)
atrMultiplierUpper = input.int(title = "ATR Multiplier Upper", defval = 1)
atrMultiplierLower = input.int(title = "ATR Multiplier Lower", defval = 1)

// ATR ///////////////////////////////////////////////////////////////////////////////
//------------------------------------------------------------------------------------
atr = ta.atr(atrPeriod)
atrBBUpper = atrBandUpper + (atr * atrMultiplierUpper)
atrBBLower = atrBandLower - (atr * atrMultiplierLower)

/////////////////////////// Big Candle ///////////////////////////////////////////////
//------------------------------------------------------------------------------------
candle_size = close>=open ? close-open :  open-close
candle_grade_guide = atrBBUpper - atrBBLower
candle_grade = candle_size > candle_grade_guide ? 3 : candle_size > candle_grade_guide/2 ? 2 : 1
candle_grade_color = candle_grade == 3 ? color.new(color.black, 0) : candle_grade == 2 ? color.new(color.purple