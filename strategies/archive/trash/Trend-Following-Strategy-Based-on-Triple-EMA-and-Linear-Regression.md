``` pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-02-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Wunderbit Trading

//@version=4
strategy("Automated Bitcoin (BTC) Investment Strategy", overlay=true, initial_capital=5000, pyramiding = 0, currency="USD", default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.1)

////////////  Functions

Atr(p) =>
    atr = 0.
    Tr = max(high - low, max(abs(high - close[1]), abs(low - close[1])))
    atr := nz(atr[1] + (Tr - atr[1])/p, Tr)

//TEMA
TEMA(series, length) =>
    if (length > 0)
        ema1 = ema(series, length)
        ema2 = ema(ema1, length)
        ema3 = ema(ema2, length)
        (3 * ema1) - (3 * ema2) + ema3
    else
        na

tradeType = input("LONG", title="What trades should be taken : ", options=["LONG", "SHORT", "BOTH", "NONE"])

///////////////////////////////////////////////////
/// INDICATORS
source=close

/// TREND
trend_type1 = input("TEMA", title="First Trend Line : ", options=["LSMA", "TEMA", "EMA", "SMA"])
trend_type2 = input("LSMA", title="First Trend Line : ", options=["LSMA", "TEMA", "EMA", "SMA"])

trend_type1_length=input(25, "Length of the First Trend Line")
trend_type2_length=input(100, "Length of the Second Trend Line")

leadLine1 = if trend_type1=="LSMA"
    linreg(close, trend_type1_length, 0)
else if trend_type1=="TEMA"
    TEMA(close, trend_type1_length)
else if trend_type1 =="EMA"
    ema(close, trend_type1_length)
else
    sma(close, trend_type1_length)

leadLine2 = if trend_type2=="LSMA"
    linreg(close, trend_type2_length, 0)
else if trend_type2=="TEMA"
    TEMA(close, trend_type2_length)
else if trend_type2 =="EMA"
    ema(close, trend_type2_length)
else
    sma(close, trend_type2_length)

p3 = plot(leadLine1, color=#53b987, title="EMA", transp=50, linewidth=1)
p4 = plot(leadLine2, color=#eb4d5c, title="SMA", transp=50, linewidth=1)
fill(p3, p4, transp=60, color=leadLine1 > leadLine2 ? #53b987 : #eb4d5c)

//Upward Trend
UT=crossover(leadLine1,leadLine2)
DT=crossunder(leadLine1,leadLine2)

// TP/ SL/  FOR LONG
// TAKE PROFIT AND STOP LOSS
long_tp1_inp = input(15, title='Long Take Profit 1 %', step=0.1)/100
long_tp1_qty = input(20, title="Long Take Profit 1 Qty", step=1)

long_tp2_inp = input(30, title='Long Take Profit 2%', step=0.1)/100
long_tp2_qty = input(20, title="Long Take Profit 2 Qty", step=1)

long_take_level_1 = strategy.position_avg_price * (1 + long_tp1_inp)
long_take_level_2 = strategy.position_avg_price * (1 + long_tp2_inp)

long_sl_input = input(5, title='stop loss in %', step=0.1)/100
long_sl_input_level = strategy.position_avg_price * (1 - long_sl_input)

// Stop Loss
multiplier = input(3.5, "SL Mutiplier", minval=1, step=0.1)
ATR_period=input(8,"ATR period", minval=1, step=1)

// Strategy
// LONG STRATEGY CONDITION
if UT
    if tradeType == "LONG" or tradeType == "BOTH"
        strategy.entry("Long Entry", strategy.long)
    
    if tradeType == "SHORT" or tradeType == "BOTH"
        strategy.entry("Short Entry", strategy.short)
    
// STOP LOSS
if strategy.position_size > 0
    stopLossPrice = long_sl_input_level
    strategy.exit("Long Exit", from_entry="Long Entry", stop=stopLossPrice)

// TAKE PROFIT
if strategy.position_size > 0
    takeProfit1 = long_take_level_1
    takeProfit2 = long_take_level_2
    strategy.exit("Long Take Profit 1", from_entry="Long Entry", limit=takeProfit1)
    strategy.exit("Long Take Profit 2", from_entry="Long Entry", limit=takeProfit2)
```