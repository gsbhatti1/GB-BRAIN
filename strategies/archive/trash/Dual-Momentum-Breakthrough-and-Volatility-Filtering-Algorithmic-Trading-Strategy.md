``` pinescript
/*backtest
start: 2023-11-21 00:00:00
end: 2023-12-21 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Qorbanjf

//@version=4
strategy("Dual-Momentum-Breakthrough-and-Volatility-Filtering-Algorithmic-Trading-Strategy", shorttitle="Dual-Momentum Breakthrough", overlay=true)

// DEMA
length = input(10, minval=1, title="DEMA LENGTH")
src = input(close, title="Source")
e1 = ema(src, length)
e2 = ema(e1, length)
dema1 = 2 * e1 - e2
plot(dema1, "DEMA", color=color.yellow)

// EMA
len = input(25, minval=1, title="EMA Length")
srb = input(close, title="Source")
offset = input(title="Offset", type=input.integer, defval=0, minval=-500, maxval=500)
ema1 = ema(srb, len)
plot(ema1, title="EMA", color=color.blue)

// ATR
atr_length = input(14, minval=1, title="ATR Lookback Period")
atr = atr(atr_length)
plot(atr, title="ATR", color=color.red)

// Moving Average
ma_type = input(title="Moving Average Type", type=input.string, defval="EMA", options=["EMA", "SMA"])
ma_len = input(20, minval=1, title="Moving Average Period")
ma = ma_type == "EMA" ? ema(close, ma_len) : sma(close, ma_len)
plot(ma, title="MA", color=color.orange)

// Long Position Rules
trail_stop_loss = input(50, minval=0, title="Trail stop loss (%)")
long_take_profit = input(3000, minval=0, title="Long Take Profit (%)")
from_month = input(true, title="From Month")
from_day = input(true, title="From Day")
from_year = input(2017, minval=1900, title="From Year")
to_month = input(true, title="To Month")
to_day = input(true, title="To Day")
to_year = input(9999, minval=1900, title="To Year")

// Long Position Logic
if (dema1 > ema1 and not na(dema1) and not na(ema1))
    strategy.entry("Long", strategy.long)
    
trail_stop = trail_stop_loss / 100 * close
trail_stop_price = max(low[1], strategy.position_avg_price - trail_stop)
strategy.exit("Trail Stop", "Long", stop=trail_stop_price)

trail_take_profit = long_take_profit / 100 * close
take_profit_price = min(high[1], strategy.position_avg_price + trail_take_profit)
strategy.exit("Take Profit", "Long", limit=take_profit_price)

// Display Settings
show_ma = input(title="Show Moving Average?", type=input.bool, defval=true)
if show_ma
    plot(ma, title="MA", color=color.orange)
```

This Pine Script translates the provided strategy description into a functional trading strategy. It includes the calculation of DEMA and EMA, ATR for volatility filtering, and the logic for entering and exiting long positions based on the conditions specified.