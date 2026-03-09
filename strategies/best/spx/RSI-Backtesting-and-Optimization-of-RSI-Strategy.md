``` pinescript
/*backtest
start: 2023-11-02 00:00:00
end: 2023-11-09 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("rsi超买超卖_回测用", overlay=false, initial_capital=50000, currency=currency.USD, default_qty_type=strategy.cash)
open_pos = input.int(50000, title="每次开单资金(usdt)")
rsi_period = input.int(14, title="rsi周期")
rsi_line      = input.float(20.0,      title='RSI触发线',      step=0.05)
stop_rsi_top_line = input.float(70, title = "顶部rsi止损线")
stop_rsi_bottom_line = input.float(30, title = "底部rsi止损线")
stop_loss_perc = input.float(0.03, title = "止损线")
stop_profit = input.float(0.01, title = "止盈")
loss_stop_trade_k = input.int(24, title="亏损后x根K线不做交易")

// 计算RSI
rsi_value = rsi(close, rsi_period)

// 判断超买超卖状态
long_condition = rsi_value < rsi_line
short_condition = rsi_value > 100 - rsi_line

// 设置止损和止盈价格
stop_loss_price_long = na
stop_loss_price_short = na
take_profit_price_long = na
take_profit_price_short = na

if (long_condition)
    strategy.entry("Long", strategy.long, comment="进入多头")
    
    // 计算止损价
    stop_loss_price_long := security(syminfo.tickerid, "1m", close * (1 - stop_loss_perc))
    
    // 如果之前没有设置止盈价，则计算当前的止盈价
    if (na(take_profit_price_long))
        take_profit_price_long := security(syminfo.tickerid, "1m", close * (1 + stop_profit))

if (short_condition)
    strategy.entry("Short", strategy.short, comment="进入空头")
    
    // 计算止损价
    stop_loss_price_short := security(syminfo.tickerid, "1m", close * (1 + stop_loss_perc))
    
    // 如果之前没有设置止盈价，则计算当前的止盈价
    if (na(take_profit_price_short))
        take_profit_price_short := security(syminfo.tickerid, "1m", close * (1 - stop_profit))

// 设置止损和止盈
if (strategy.opentrades > 0)
    trade_id = strategy.opentrades.id(0)
    
    if (strategy.opentrades.entry_price(trade_id) <= stop_loss_price_long)
        strategy.close("Long", comment="止损出场")
        
    if (strategy.opentrades.entry_price(trade_id) >= take_profit_price_long)
        strategy.close("Long", comment="止盈出场")
        
    if (strategy.opentrades.entry_price(trade_id) >= stop_loss_price_short)
        strategy.close("Short", comment="止损出场")
        
    if (strategy.opentrades.entry_price(trade_id) <= take_profit_price_short)
        strategy.close("Short", comment="止盈出场")

// 暂停交易
if (strategy.equity < 0 and not na(strategy.equity))
    var int count = 1
    while (count <= loss_stop_trade_k)
        strategy.cancel_all()
        count := count + 1
```

This Pine Script code implements the RSI strategy with backtesting features, including setting up long and short positions based on RSI values, calculating stop-loss and take-profit levels, and adding a trading pause mechanism after losses.