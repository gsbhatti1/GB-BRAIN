```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2024-01-07 00:00:00
Period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © I11L

//@version=5
strategy("I11L - Buy Low Volatility vs Buy High Volatility Strategy", overlay=false)

mode = input.string("Buy low Volatility", options = ["Buy low Volatility","Buy high Volatility"])
volatilityTargetRatio = input.float(1, minval = 0, maxval = 100, step=0.1, tooltip="1 equals the average atr for the security, a lower value means that the volatility is lower")
atrLength = input.int(14)

atr = ta.atr(atrLength) / close
avg_atr = ta.sma(atr, atrLength*5)
ratio = atr / avg_atr

sellAfterNBarsLength = input.int(5, step=5, minval=0)


var holdingBarsCounter = 0

if(strategy.opentrades > 0)
    holdingBarsCounter := holdingBarsCounter + 1


isBuy = false

if(mode == "Buy low Volatility")
    isBuy := ratio < volatilityTargetRatio
else
    isBuy := ratio > volatilityTargetRatio

isClose = holdingBarsCounter > sellAfterNBarsLength



if(isBuy)
    strategy.entry("Buy", strategy.long)

if(isClo
```