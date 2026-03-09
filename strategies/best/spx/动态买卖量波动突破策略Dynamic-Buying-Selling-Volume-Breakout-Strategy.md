> Name

Dynamic-Buying-Selling-Volume-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/139cd49422931c76044.png)

[trans]

## Overview
This strategy determines long and short positions through customized timeframe buying and selling volume, combined with weekly VWAP and Bollinger Bands for filtering, to achieve high-probability trend tracking. It also introduces a dynamic take profit and stop loss mechanism to effectively control one-sided risks.

## Strategy Principle  
1. Calculate buying and selling volume indicators within the customized timeframe
- BV: Buying Volume, caused by buying at low point
- SV: Selling Volume, caused by selling at high point
2. Process buying and selling volume
- Smooth by 20-period EMA
- Separate processed buying and selling volume into positive and negative
3. Judge indicator direction
- Greater than 0 is bullish; less than 0 is bearish
4. Determine divergence combined with weekly VWAP and Bollinger Bands
- Price above VWAP and indicator bullish is a long signal
- Price below VWAP and indicator bearish is a short signal
5. Dynamic take profit and stop loss
- Set percentage of take profit and stop loss based on daily ATR

## Strategy Advantages  
1. Buying and selling volume reflects real market momentum, capturing potential energy of trends
2. Weekly VWAP judges longer timeframe trend direction; Bollinger Bands determine breakout signals
3. Dynamic ATR sets take profit and stop loss to maximize profit locking and avoid over-tuning

## Risks  
1. Buying and selling volume data has certain errors that may cause misjudgment
2. Single indicator combined judgment tends to generate false signals
3. Improper Bollinger Bands parameter settings can narrow down valid breakouts

## Optimization Directions  
1. Optimize with multiple timeframe buying and selling volume indicators
2. Add trading volume and other auxiliary indicators for filtering
3. Dynamically adjust Bollinger Bands parameters to improve breakout efficiency  

## Conclusion  
This strategy fully utilizes the predictability of buying and selling volume, generating high-probability signals supplemented by VWAP and Bollinger Bands. It effectively controls risk through dynamic take profit and stop loss mechanisms, making it an efficient and stable quantitative trading strategy. As parameters and rules continue to be optimized, its performance is expected to become more significant.

||

## Overview
This strategy determines long and short positions through customized timeframe buying and selling volume, combined with weekly VWAP and Bollinger Bands for filtering, to achieve high-probability trend tracking. It also introduces a dynamic take profit and stop loss mechanism to effectively control one-sided risks.

## Strategy Principle  
1. Calculate buying and selling volume indicators within the customized timeframe
- BV: Buying Volume, caused by buying at low point
- SV: Selling Volume, caused by selling at high point
2. Process buying and selling volume
- Smooth by 20-period EMA
- Separate processed buying and selling volume into positive and negative
3. Judge indicator direction
- Greater than 0 is bullish; less than 0 is bearish
4. Determine divergence combined with weekly VWAP and Bollinger Bands
- Price above VWAP and indicator bullish is a long signal
- Price below VWAP and indicator bearish is a short signal
5. Dynamic take profit and stop loss
- Set percentage of take profit and stop loss based on daily ATR

## Advantages  
1. Buying and selling volume reflects real market momentum, capturing potential energy of trends
2. Weekly VWAP judges longer timeframe trend direction; Bollinger Bands determine breakout signals
3. Dynamic ATR sets take profit and stop loss to maximize profit locking and avoid over-tuning

## Risks  
1. Buying and selling volume data has certain errors that may cause misjudgment
2. Single indicator combined judgment tends to generate false signals
3. Improper Bollinger Bands parameter settings can narrow down valid breakouts

## Optimization Directions  
1. Optimize with multiple timeframe buying and selling volume indicators
2. Add trading volume and other auxiliary indicators for filtering
3. Dynamically adjust Bollinger Bands parameters to improve breakout efficiency  

## Conclusion  
This strategy fully utilizes the predictability of buying and selling volume, generating high-probability signals supplemented by VWAP and Bollinger Bands. It effectively controls risk through dynamic take profit and stop loss mechanisms, making it an efficient and stable quantitative trading strategy. As parameters and rules continue to be optimized, its performance is expected to become more significant.

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_timeframe_1|60|(?Entry Settings)customTimeframe|
|v_input_bool_1|true|allow_long|
|v_input_bool_2|false|allow_short|
|v_input_int_1|20|(?Volatility Settings)length|
|v_input_float_1|2|StdDev|
|v_input_float_2|100|(?Dynamic Risk Management)TP Multiplier for Long entries |
|v_input_float_3|true|SL Multiplier for Long entries|
|v_input_float_4|100|TP Multiplier for Short entries |
|v_input_float_5|5|SL Multiplier for Short entries|

## Source (PineScript)

```pinescript
/*backtest
start: 2022-12-19 00:00:00
end: 2023-12-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © original author ceyhun
//@ exlux99 update

//@version=5
strategy('Buying Selling Volume Strategy', format=format.volume, precision=0, overlay=false)

weekly_vwap = request.security(syminfo.tickerid, "W", ta.vwap(hlc3))

vi = false
customTimeframe = input.timeframe("60", group="Entry Settings")

allow_long = input.bool(true, group="Entry Settings")
allow_short = input.bool(false, group="Entry Settings")

xVolume = request.security(syminfo.tickerid, customTimeframe, volume)
xHigh = request.security(syminfo.tickerid, customTimeframe, high)
xLow = request.security(syminfo.tickerid, customTimeframe, low)
xClose = request.security(syminfo.tickerid, customTimeframe, close)

BV = xHigh == xLow ? 0 : xVolume * (xClose - xLow) / (xHigh - xLow)
SV = xHigh == xLow ? 0 : xVolume * (xHigh - xClose) / (xHigh - xLow)

vol = xVolume > 0 ? xVolume : 1
TP = BV + SV
BPV = BV / TP * vol
SPV = SV / TP * vol
TPV = BPV + SPV

tavol20 = request.security(syminfo.tickerid, customTimeframe, ta.ema(vol, 20))
tabv20= request.security(syminfo.tickerid, customTimeframe, ta.ema(BV, 20))
tasv20= request.security(syminfo.tickerid, customTimeframe, ta.ema(SV, 20))
VN = vol / tavol20
BPN = BV / tabv20 * VN * 100
SPN = SV / tasv20 * VN * 100
TPN = BPN + SPN

xbvp = request.security(syminfo.tickerid, customTimeframe,-math.abs(BPV))
xbpn = request.security(syminfo.tickerid, customTimeframe,-math.abs(BPN))
xspv = request.security(syminfo.tickerid, customTimeframe,-math.abs(SPV))
xspn = request.security(syminfo.tickerid, customTimeframe,-math.abs(SPN))

BPc1 = BPV > SPV ? BPV : xbvp
BPc2 = BPN > SPN ? BPN : xbpn
SPc1 = SPV > BPV ? SPV : xspv
SPc2 = SPN > BPN ? SPN : xspn
BPcon = vi ? BPc2 : BPc1
SPcon = vi ? SPc2 : SPc1


minus = BPcon + SPcon
plot(minus, color = BPcon > SPcon  ? color.green : color.red , style=plot.style_columns) 

length = input.int(20, minval=1, group="Volatility Settings")
src = minus//input(close, title="Source")
mult = input.float(2.0, minval=0.001, maxval=50, title="StdDev", group="Volatility Settings")
xtasma = request.security(syminfo.tickerid, customTimeframe,
```