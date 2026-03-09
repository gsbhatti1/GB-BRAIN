``` pinescript
/*backtest
start: 2023-11-01 00:00:00
end: 2023-11-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy(title='[STRATEGY][RS]Dual-EMA-Golden-Cross-Breakthrough-Strategy', shorttitle='S', overlay=true, pyramiding=0, initial_capital=100000)
USE_TRADESESSION = input(title='Use Trading Session?', type=bool, defval=true)
USE_TRAILINGSTOP = input(title='Use Trailing Stop?', type=bool, defval=true)
trade_session = input(title='Trade Session:', defval='0400-1500', confirm=false)
istradingsession = not USE_TRADESESSION ? false : not na(time('1', trade_session))
bgcolor(istradingsession?gray:na)
trade_size = input(title='Trade Size:', type=float, defval=1)
tp = input(title='Take profit in pips:', type=float, defval=55.0) * (syminfo.mintick*10)
sl = input(title='Stop loss in pips:', type=float, defval=22.0) * (syminfo.mintick*10)
ma_length00 = input(title='EMA length:',  defval=5)
ma_length01 = input(title='DEMA length:',  defval=34)
price = input(title='Price source:',  defval=open)

//  ||--- NO LAG EMA, Credit LazyBear:  ---||
f_LB_zlema(_src, _length)=>
    _ema1=ema(_src, _length)
    _ema2=ema(_ema1, _length)
    _d=_ema1-_ema2
    _zlema=_ema1+_d
//  ||-------------------------------------||

ma00 = f_LB_zlema(price, ma_length00)
ma01 = f_LB_zlema(price, ma_length01)
plot(title='M0', series=ma00, color=black)
plot(title='M1', series=ma01, color=black)

isnewbuy = change(strategy.position_size)>0 and change(strategy.opentrades)>0
isnewsel = change(strategy.position_size)<0 and change(strategy.opentrades)>0

buy_entry_price = isnewbuy ? price : buy_entry_price[1]
sel_entry_price = isnewsel ? price : sel_entry_price[1]
plot(title='BE', series=buy_entry_price, style=circles, color=strategy.position_size <= 0 ? na : aqua)
plot(title='SE', series=sel_entry_price, style=circles, color=strategy.position_size >= 0 ? na : aqua)
buy_appex = na(buy_appex[1]) ? price : isnewbuy ? high : high >= buy_appex[1] ? high : buy_appex[1]
sel_appex = na(sel_appex[1]) ? price : isnewsel ? low : low <= sel_appex[1] ? low : sel_appex[1]
plot(title='BA', series=buy_appex, style=circles, color=strategy.position_size <= 0 ? na : teal)
plot(title='SA', series=sel_appex, style=circles, color=strategy.position_size >= 0 ? na : teal)
buy_ts = buy_appex - sl
sel_ts = sel_appex + sl
plot(title='Bts', series=buy_ts, style=circles, color=strategy.position_size <= 0 ? na : red)
plot(title='Sts', series=sel_ts, style=circles, color=strategy.position_size >= 0 ? na : red)

buy_cond1 = crossover(ma00, ma01) and (USE_TRADESESSION ? istradingsession : true)
buy_cond2 = not crossunder(ma00, ma01) and (USE_TRADESESSION ? istradingsession : true)
sel_cond1 = crossunder(ma00, ma01) and (USE_TRADESESSION ? istradingsession : true)
sel_cond2 = not crossover(ma00, ma01) and (USE_TRADESESSION ? istradingsession : true)

if (buy_cond1 or buy_cond2)
    strategy.entry("Buy", strategy.long, size=trade_size)
if (sel_cond1 or sel_cond2)
    strategy.entry("Sell", strategy.short, size=trade_size)

```

```