> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-10 00:00:00
end: 2025-02-08 08:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("SuperTrend on Steroids", overlay=true)

// Input parameters
atrLength = input(10, title="ATR Period")
atrMultiplier = input(3.0, title="ATR Multiplier")
emaLength = input(21, title="EMA Length")
adxLength = input(14, title="ADX Length")
adxSmoothing = input(14, title="ADX Smoothing")

// EMA Calculation
emaValue = ta.ema(close, emaLength)

// VWAP Calculation
vwapValue = ta.vwap(close)

// ATR Calculation
atrValue = ta.atr(atrLength)

// SuperTrend Calculation
var trend = 1
up = hl2 - atrMultiplier * atrValue
dn = hl2 + atrMultiplier * atrValue
up1 = nz(up[1], up)
dn1 = nz(dn[1], dn)
up := close[1] > up1 ? math.max(up, up1) : up
dn := close[1] < dn1 ? math.min(dn, dn1) : dn
trend := trend == -1 and close > dn1 ? 1 : trend == 1 and close < up1 ? -1 : trend

// ADX Calculation
[diplus, diminus, adx] = ta.dmi(adxLength, adxSmoothing)

// Buy/Sell Signals
buySignal = trend == 1 and trend[1] == -1
sellSignal = trend == -1 and trend[1] == 1
```

This is a trend-following strategy using SuperTrend, VWAP, EMA, and ADX indicators. The strategy identifies trend direction using SuperTrend, confirms trends through the relationship between VWAP and EMA, and filters weak trends using ADX. The strategy is designed for intraday trading, particularly on 5-minute, 15-minute, and 1-hour timeframes. The strategy provides clear buy and sell signals, and is designed to be flexible and adaptable to different markets.