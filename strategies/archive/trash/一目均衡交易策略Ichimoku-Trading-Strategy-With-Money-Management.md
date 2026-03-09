``` pinescript
/*backtest
start: 2022-12-05 00:00:00
end: 2023-12-11 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Author Obarut
//@version=5
strategy("İchimoku Strategy With Money Management",overlay=true)

//Inputs
ts_period = input.int(9, minval=1, title="Tenkan-Sen Period")
ks_period = input.int(26, minval=1, title="Kijun-Sen Period")
ssb_period = input.int(52, minval=1, title="Senkou-Span B Period")
cs_offset = input.int(26, minval=1, title="Chikou-Span Offset")
ss_offset = input.int(26, minval=1, title="Senkou-Span Offset")


// Back Testing Period

fromday = input.int(defval=1,title="Start Date",minval=1,maxval=31) 
frommonth = input.int(defval=1,title="Start Month",minval=1,maxval=12)
fromyear = input.int(defval=1980,title="Start Year",minval=1800, maxval=2100)
today = input.int(defval=1,title="End Date",minval=1,maxval=31)
tomonth = input.int(defval=1,title="End Month",minval=1,maxval=12)
toyear =input.int(defval=2100,title="End Year",minval=1800,maxval=2200)


start=timestamp(fromyear,frommonth,fromday,00,00)
finish=timestamp(toyear,tomonth,today,00,00)
timewindow= time>=start and time<=finish

middle(len) => math.avg(ta.lowest(len), ta.highest(len))

// Ichimoku Components

tenkan = middle(ts_period)
kijun = middle(ks_period)
senkouA = math.avg(tenkan, kijun)
senkouB = middle(ssb_period)


atr = ta.atr(14)
ss_above = math.max(senkouA[ss_offset-1], senkouB[ss_offset-1])
ss_below = math.min(senkouA[ss_offset-1], senkouB[ss_offset-1])

// Price Distance From Tenkan

distance = close - tenkan

// Price Distance from Kijun

distancek = close - kijun

// Entry/Exit Signals

tk_cross_kijun_bull = tenkan >= kijun
tk_cross_kijun_bear = tenkan <= kijun
cs_cross_bull = ta.mom(close, cs_offset-1) > 0
cs_cross_bear = ta.mom(close, cs_offset-1) < 0
price_above_kumo = close > ss_above
pbsenkA = close < ss_above
pasenkB = close > ss_below
price_below_kumo = close < ss_above
future_kumo_bull = senkouA > senkouB
future_kumo_bear = senkouA < senkouB

// Price Distance From Tenkan
disbull = distance < 2*atr
//Price Distance From Kijun
disbullk = distancek < 3*atr
//Price ATR Condition for Chasing Strategy
chase_condition = disbull and disbullk and price_above_kumo and future_kumo_bull

// Long Entry Conditions
long_entry = tk_cross_kijun_bull and cs_cross_bull and chase_condition

// Exit Conditions
exit_long = tk_cross_kijun_bear or price_below_kumo or (profit > 30) or (loss > 3)

if (timewindow and long_entry)
    strategy.entry("Long", strategy.long)

if (timewindow and exit_long)
    strategy.close("Long")

// Risk Management
max_profit = input.float(1.2, title="Max Profit Factor")
max_loss = input.float(0.85, title="Max Loss Factor")

profit_target = close * max_profit
stop_loss = close * max_loss

if (strategy.opentrades > 0)
    if (strategy.equity < stop_loss or strategy.profit_factor > max_profit)
        strategy.close("Long", force=True)

```