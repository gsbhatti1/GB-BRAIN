``` pinescript
/*backtest
start: 2022-02-08 00:00:00
end: 2022-05-08 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// ©Hotchachachaa, Rest in Peace Pheonix Algo(aka Doug) your community misses you and we extend our deepest sympathies to your family.
//@version=5
//
//This indicator is based on the TMA-Divergence indicator created by PhoenixBinary for the TMA discord Community. Since Phoenix is no longer part of the community,
//we did our best to recreate the indicator for the community's continued use, updates, and revisions.
indicator("TMA-Legacy", overlay=false)

////////////////////////////////////inputs////////////////////////////////////////////////

displayRSI = input.string(title="RSI Type", defval="RSI Divergence", options=["RSI Divergence","RSI Smoothed","RSI Momentum"], group="Main Settings")
lenrsinordiv = input.int(title="RSI Normal Length", defval=14, minval=1, group= "RSI Normal")
lenrsismodiv = input.int(title="RSI Smoothed Length", defval=40, minval=1, group = "RSI Smoothed" )
lenrsissmoma = input.int(title="RSI Smoothed MA", defval=40,minval=1, group = "RSI Smoothed" )
lenrsimomdiv = input.int(title="RSI Normal Length", defval=5 ,minval=1, group = "RSI Momentum")
rsimommalen = input.int(34, minval=1, title="Smooth RSI MA Length",group="RSI Momentum")
srcrsidiv = input(title="RSI Source", defval=close, group="Main Settings")
lbR = input.int(title="Pivot Lookback Right", defval=5,minval=1,group="Divergence Spotter")
lbL = input.int(title="Pivot Lookback Left", defval=5,minval=1,group="Divergence Spotter")
rangeUpper = input.int(title="Max of Lookback Range", defval=60,minval=1,group="Divergence Spotter")
rangeLower = input.int(title="Min of Lookback Range", defval=5,minval=1,group="Divergence Spotter")
plotBull = input.bool(title="Plot Bullish", defval=true,group="Divergence Spotter")
plotHiddenBull = input.bool(title="Plot Hidden Bullish", defval=true,group="Divergence Spotter")
plotBear = input.bool(title="Plot Bearish", defval=true,group="Divergence Spotter")
plotHiddenBear = input.bool(title="Plot Hidden Bearish", defval=true,group="Divergence Spotter")
bearColorrsidiv = color.red
bullColorrsidiv = color.green
hiddenBullColor = color.new(color.green, 80)
hiddenBearColor = color.new(color.red, 80)
textColor = color.white
noneColor = color.new(color.white, 100)
lenDisplay= displayRSI == "RSI Divergence" ? lenrsinordiv: displayRSI == "RSI Smoothed" ? lenrsismodiv: na
rsiValue1 = ta.rsi(srcrsidiv, lenrsinordiv)

// ### Smoothed MA

averageSource = rsiValue1
typeofMA1 = "SMMA"
length_ma1 = 50
f_smma(averageSource, averageLength) =>
    smma = 0.0
    smma := na(smma[1]) ? ta.sma(averageSource, averageLength) : (smma[1] * (averageLength - 1) + averageSource) / averageLength
    smma
    
f_smwma(averageSource, averageLength) =>
    smwma = 0.0
    smwma := na(smwma[1]) ? ta.wma(averageSource, averageLength) : (smwma[1] * (averageLength - 1) + 
```