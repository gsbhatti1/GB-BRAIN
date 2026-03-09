```pinescript
/*backtest
start: 2022-04-23 00:00:00
end: 2022-05-22 23:59:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

study(shorttitle="BBAWE", title="Bollinger Awesome Alert R1.1 by JustUncleL", overlay=true)

// Author: Lawrie Steven
// Date:   22-Apr-2017
// Revision: R1
//
// Description:
// ============
// This indicator is an implementation of the Bollinger Band and Awesome Oscillator
// scalping system.
// This technique is for those who want the most simple method that is
// very effective. It is BEST traded during the busiest trading hours,
// 3am to 12am EST NY time. This method doesn't work in sideways markets, only in
// volatile trending markets.
//
// Time Frames: 1, 5, 10, 15 ,30 min.
// Currency pairs: majors.
//
// Other Chart indicators:
// - Add Awesome Oscillator.
// - Optionally Add Squeeze Indicator.
//
// Here's the strategy:
// --------------------
// Going LONG:
// Enter a long position when the black 3 EMA has crossed up through the Bollinger red 
// middle band MA. At the same time, the Awesome should be approaching or crossing 
// its zeroline, going up. Optionally Close price also must stay below the upper BB.
// This is indicated by "Buy" alert.
//
// Going SHORT:
// Enter a short position when the black 3 EMA has crossed down through the Bollinger red
// middle band MA. At the same time, the Awesome should be approaching or crossing its 
// zero line, going down. Optionally Close price also must stay above the lower BB.
// This is indicated by the "Sell" Alert.
// 
// Take profit:
// 10-20 pips depending on pair or When Awesome Oscillator turns a different color.
//
// HINTS: Best trades tend to occur when price reversing bounce off outer band and 
// and outside Optional Bollinger Squeeze indication.
//
// References:
// -----------
// - https://www.forexstrategiesresources.com/scalping-forex-strategies-iii/337-bollinger-bands-and-chaos-awesome-scalping-system
// - "Squeeze Momentum Indicator [LazyBear]"
//
// Modifications
// -------------
// 6-Sept-2019 :
//      - Added optional extra condition that the signal candle close price must stay within the Bollinger Bands.
//        This helps remove some of the oversized signal candles, these candles have a lower success probabilty.
//      - Added Alarm system Alerts for BUY and SELL.
// 28-Sept-2019 :
//      - Added optional BB squeeze filter. The squeeze Algo is based on the current relative width of the BB, 
//        it is NOT based on the LazyBear Algo.
// 08-Aug-2020
//      - Converted to Pinescript V4
// 11-Aug-2020
//      - Modified "alertcondition" calls to include the close placeholder, this forces the compiler to
//        recognize the as a placeholder alert and other placeholders can be accessed in the alarm
//        message.
//

// === INPUTS ===

// Bollinger Bands Inputs
bb_use_ema = input(false, title="Use EMA for Bollinger Band")
bb_filter = input(false, title="Filter Buy/Sell with Bollinger Bands")
sqz_filter = input(false, title="Flter Buy/Sell with BB squeeze")
bb_length = input(20, minval=1, title="Bollinger Length")
bb_source = input(close, title="Bollinger Source")
bb_mult = input(2.0, title="Base Multiplier", minval=0.5, maxval=10)
// EMA inputs
fast_ma_len = input(3, title="Fast EMA length", minval=2)
// Awesome Inputs
nLengthSlow = input(34, minval=1, title="Awesome Length Slow")
nLengthFast = input(5, minval=1, title="Awesome Length Fast")

// === /INPUTS ===

sqz_length = input(100, "BB Relative Squeeze Length", minval=5)
sqz_threshold = input(50, "BB Squeeze Threshold %", maxval=99, step=5)

// === SERIES ===

// Breakout Indicator Inputs
ema_1 = ema(bb_source, bb_length)
sma_1 = sma(bb_source, bb_length)
bb_basis = bb_use_ema ? ema_1 : sma_1
fast_ma = ema(bb_source, fast_ma_len)

// Deviation
// * I'm sure there's a way I could write some of this cleaner, but meh.
dev = stdev(bb_source, bb_length)
bb_dev = bb_mult * dev

// Upper bands
bb_upper = bb_basis + bb_dev
// Lower Bands
bb_lower = 
```