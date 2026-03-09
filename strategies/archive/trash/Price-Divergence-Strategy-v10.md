> Name

Price-Divergence-Strategy-v10

> Author

ChaoZhang

> Strategy Description

Created by Request: This is a trend trading strategy that uses Price Divergence detection signals confirmed by the "Murrey's Math Oscillator" (Donchanin Channel based).

Strategy Code Based on:
Price Divergence Detector V2 by RicardoSantos
UCS_Murrey's Math Oscillator by Ucsgears
Strategy Risk Management Based on:
Strategy Code Example by JayRogers


**backtest**
 ![IMG](https://www.fmz.com/upload/asset/fe14c620de17b78dc2.png) 

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Method (0=rsi, 1=macd, 2=stoch, 3=volume, 4=acc/dist, 5=fisher, 6=cci):|
|v_input_2|true|Show Labels|
|v_input_3|false|Show Channel|
|v_input_4|true|Use Hidden Divergence in Strategy|
|v_input_5|true|Use Regular Divergence in Strategy|
|v_input_6|5|RSI/STOCH/Volume/ACC-DIST/Fisher/cci Smooth:|
|v_input_7_close|0|MACD Source:: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_8|12|MACD Fast:|
|v_input_9|26|MACD Slow:|
|v_input_10|9|MACD Smooth Signal:|
|v_input_11|100|MMLO Look back Length|
|v_input_12|2|Minimum Quadrant for MMLO Support|
|v_input_13|false|Take Profit Points|
|v_input_14|false|Stop Loss Points|
|v_input_15|100|Trailing Stop Loss Points|
|v_input_16|false|Trailing Stop Loss Offset Points|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-04-30 00:00:00
end: 2022-05-29 23:59:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//
// Title:   [STRATEGY][UL]Price Divergence Strategy V1.1
// Author:  JustUncleL
// Date:    23-Oct-2016
// Version: v1.1
//
// Description:
//  A trend trading strategy that uses Price Divergence detection signals, which
//  are confirmed by the "Murrey's Math Oscillator" (Donchanin Channel based).
//
//  *** USE AT YOUR OWN RISK ***
//
// Modifications:
//  1.0 - original
//  1.1 - PineScript V4 update 21-Aug-2021
//
// References:
//  Strategy Based on:
//  - [RS]Price Divergence Detector V2 by RicardoSantos
//  - UCS_Murrey's Math Oscillator by Ucsgears
//  Some code borrowed from:
//  - "Strategy Code Example by JayRogers"  
//  Information on Divergence Trading:
//  - http://www.babypips.com/school/high-school/trading-divergences
//
strategy(title='[STRATEGY][UL]Price Divergence Strategy v1.1', pyramiding=0, overlay=true, initial_capital=10000, calc_on_every_tick=false, currency=currency.USD, 
  default_qty_type=strategy.percent_of_equity, default_qty_value=10)
//  ||  General Input:
method = input(title='Method (0=rsi, 1=macd, 2=stoch, 3=volume, 4=acc/dist, 5=fisher, 6=cci):', type=input.integer, defval=1, minval=0, maxval=6)
SHOW_LABEL = input(title='Show Labels', type=input.bool, defval=true)
SHOW_CHANNEL = input(title='Show Channel', type=input.bool, defval=false)
uHid = input(true, title="Use Hidden Divergence in Strategy")
uReg = input(true, title="Use Regular Divergence in Strategy")
//  ||  RSI / STOCH / VOLUME / ACC/DIST Input:
rsi_smooth = input(title='RSI/STOCH/Volume/ACC-DIST/Fisher/cci Smooth:', type=input.integer, defval=5)
//  ||  MACD Input:
macd_src = input(title='MACD Source:', type=input.source, defval=close)
macd_fast = input(title='MACD Fast:', type=input.integer, defval=12)
macd_slow = input(title='MACD Slow:', type=input.integer, defval=26)
macd_smooth = input(title='MACD Smooth Signal:', type=input.integer, defval=9)
//  ||  Functions:
f_top_fractal(_src) =>
    _src[4] < _src[2] and _src[3] < _src[2] and _src[2] > _src[1] and 
       _src[2] > _src[0]
f_bot_fractal(_src) =>
    _src[4] > _src[2] and _src[3] > _src[2] and _src[2] < _src[1] and 
       _src[2] < _src[0]
f_fractalize(_src) =>
    f_bot_fractal__1 = f_bot_fractal(_src)
    f_top_fractal(_src) ? 1 : f_bot_fractal__1 ? -1 : 0

//  ||••>   START MACD FUNCTION
f_macd(_src, _fast, _slow, _smooth) =>
    _fast_ma = sma(_src, _fast)
    _slow_ma = sma(_src, _slow)
    _macd = _fast_ma - _slow_ma
    _signal = ema(_macd, _smooth)
    _hist = _macd - _signal
    _hist
//  ||<••   END MACD FUNCTION

//  ||••>   START ACC/DIST FUNCTION
f_accdist(_smooth) =>
    _return = sma(cum(close == high and close == low or high == low ? 0 : (2 * close - low - high) / (high - low) * volume), _smooth)
    _return
//  ||<••   END ACC/DIST FUNCTION

//  ||••>   START FISHER FUNCTION
f_fisher(_src, _window) =>
    _h = highest(_src, _window)
    _l = lowest(_src, _window)
    _value0 = 0.0
    _fisher = 0.0
    _value0 := .66 * ((_src - _l) / max(_h - _l, .001) - .5) + .67 * nz(_value0[1])
    _value1 = _value0 > .99 ? .999 : _value0 < -.99 ? -.999 : _value0
    _fisher := .5 * log((1 + _value1) / max(1 - _value1, .001)) + .5 * nz(_fisher[1])
    _fisher
//  ||<••   END FISHER FUNCTION

rsi_1 = rsi(high, rsi_smooth)
f_macd__1 = f_macd(macd_src, macd_fast, macd_slow, macd_smooth)
stoch_1 = stoch(close, high, low, rsi_smooth)
sma_1 = sma(volume, rsi_smooth)
f_accdist__1 = f_accdist(rsi_smooth)
f_fisher__1 = f_fisher(high, rsi_smooth)
cci_1 = cci(high, rsi_smooth)
method_high = method == 0 ? rsi_1 : method == 1 ? f_macd__1 : 
   method == 2 ? stoch_1 : method == 3 ? sma_1 : method == 4 ? f_accdist__1 : 
   method == 5 ? f_fisher__1 : method == 6 ? cci_1 : na

rsi_2 = rsi(low, rsi_smooth)
f_macd__2 = f_macd(macd_src, macd_fast, macd_slow, macd_smooth)
stoch_2 = stoch(close, high, low, rsi_smooth)
sma_2 = sma(volume, rsi_smooth)
f_accdist__2 = f_accdist(rsi_smooth)
f_fisher__2 = f_fisher(low, rsi_smooth)
cci_2 = cci(low, rsi_smooth)
method_low = method == 0 ? rsi_2 : method == 1 ? f_macd__2 : 
   method == 2 ? stoch_2 : method == 3 ? sma_2 : method == 4 ? f_accdist__2 : 
   method == 5 ? f_fisher__2 : method == 6 ? cci_2 : na

fractal_top = f_fractalize(method_high) > 0 ? method_high[2] : na
fractal_bot = f_fractalize(method_low) < 0 ? method_low[2] : na

high_prev = valuewhen(fractal_top, method_high[2], 1)
high_price = valuewhen(fractal_top, high[2], 1)
low_prev = valuewhen(fractal_bot, method_low[2], 1)
low_price
``` 

This Pine Script defines a strategy based on detecting price divergences using the "Murrey's Math Oscillator" and various technical indicators (RSI, MACD, Stochastic, Volume, ACDIST, Fisher). The script includes customizable parameters for method selection, label display, and divergence detection. It also provides an example backtest period and exchange configuration. Adjustments can be made to the strategy according to your specific trading requirements.