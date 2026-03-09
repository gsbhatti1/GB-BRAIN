``` pinescript
/*backtest
start: 2023-01-08 00:00:00
end: 2024-01-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © melihtuna
// developer: @KivancOzbilgic
// author: @KivancOzbilgic
// strategy converter: @crypto_melih
//@version=4

strategy("Profit Maximizer Strategy Long-Short", shorttitle="PMax-Strategy", overlay=true, default_qty_type=strategy.cash, default_qty_value=10000, initial_capital=10000, currency=currency.USD, commission_value=0, commission_type=strategy.commission.percent)

src = input(hl2, title="Source")
Periods = input(title="ATR Length", type=input.integer, defval=10)
Multiplier = input(title="ATR Multiplier", type=input.float, step=0.1, defval=3.0)
mav = input(title="Moving Average Type", defval="EMA", options=["SMA", "EMA", "WMA", "TMA", "VAR", "WWMA", "ZLEMA", "TSF"])
length = input(10, "Moving Average Length", minval=1)
condition = input(title="Signal Type", defval="Only Crossing Signals", options=["Only Crossing Signals", "Only Price/Pmax Crossing Signals"])
changeATR= input(title="Change ATR Calculation Method ?", type=input.bool, defval=true)
showsupport = input(title="Show Moving Average?", type=input.bool, defval=true)
//showsignalsk = input(title="Show Crossing Signals?", 
```