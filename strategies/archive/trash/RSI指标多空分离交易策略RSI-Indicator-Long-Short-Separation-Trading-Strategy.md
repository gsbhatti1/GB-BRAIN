``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Nextep

//@version=4
strategy(title="RSI top&bottom destroy", overlay=false, pyramiding=4, default_qty_value=2, default_qty_type=strategy.fixed, initial_capital=10000, currency=currency.USD)

// INPUT Settings --------------------------------------------------------------------------------------------------------------------------------------------------
len = input(title="RSI Period", minval=1, defval=13)
src = input(title="RSI Source", defval=close)

// defining the lookback range for shorts
lbRshort = input(title="Short Lookback Right", defval=1)
lbLshort = input(title="Short Lookback Left", defval=47)

// defining the lookback range for longs
lbRlong = input(title="Long Lookback Right", defval=2)
lbLlong = input(title="Long Lookback Left", defval=14)

// maximum lookback range
maxLB = input(title="Max of Lookback Range", defval=400)

// minimum lookback range
minLB = input(title="Min of Lookback Range", defval=true)

// take profit at RSI level
tpLevel = input(title="Take Profit at RSI Level", defval=75)

// take profit for short at RSI level
tpShortLevel = input(title="Take Profit for Short at RSI Level", defval=25)

// long stop loss type: PERC|ATR|FIB|NONE
longStopLossType = input(title="Long Stop Loss Type", defval=0)

// short stop loss type: PERC|ATR|FIB|NONE
shortStopLossType = input(title="Short Stop Loss Type", defval=0)

// long stop loss value
longStopLossValue = input(title="Long Stop Loss Value", defval=14)

// short stop loss value
shortStopLossValue = input(title="Short Stop Loss Value", defval=5)

// plot bullish signals
plotBullish = input(title="Plot Bullish", defval=true)

// plot bearish signals
plotBearish = input(title="Plot Bearish", defval=true)

// ATR length for trailing stop loss
atrLength = input(title="ATR Length (for Trailing stop loss)", defval=14)

// ATR multiplier for trailing stop loss
atrMultiplier = input(title="ATR Multiplier (for Trailing stop loss)", defval=3.5)
```