``` pinescript
/*backtest
start: 2023-10-04 00:00:00
end: 2023-10-08 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Ichimoku-Based Trend Tracking Strategy", pyramiding=0, calc_on_every_tick = true, initial_capital = 50000, commission_type = strategy.commission.cash_per_order, commission_value = 10.00)

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////Ichimoku Clouds////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////(Version 40.0)//////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

periodoLinhaDeConversao = input(defval=9, title="Conversion Line (Tenkan-sen)",  minval=1)
periodoLinhaBase = input(defval=26, title="Base Line (Kijun-sen)",  minval=1)
periodoNivelAdiantadoB = input(defval=52, title="Leading Span B (Senkou Span B)",  minval=1)
deslocamento = input(defval=26, title="Shift",  minval=1)

linhaDeConversao = (high[periodoLinhaDeConversao] + low[-periodoLinhaDeConversao]) / 2
linhaBase = (high[periodoLinhaBase] + low[-periodoLinhaBase]) / 2
nivelAdiantadoA = (linhaDeConversao + linhaBase) / 2
nivelAdiantadoB = (high[periodoNivelAdiantadoB] + low[-periodoNivelAdiantadoB]) / 2

雲頂 = nivelAdiantadoA + deslocamento
雲底 = nivelAdiantadoA - deslocamento

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
strategy.entry("Buy", strategy.long, when = close > 雲頂)
strategy.entry("Sell", strategy.short, when = close < 雲底)

// 设置止盈止损
目标利润比例 = input(5, title="Profit Goal (%)", minval=0)
止损比例 = input(0.5, title="Stop Loss (%)", minval=0)

目标利润 = capitalInicial * (目标利润比例 / 100)
止损水平 = capitalInicial * (止损比例 / 100)

// 根据价格突破云顶或云底平仓
strategy.exit("Profit Target", from_entry="Buy", profit_target=目标利润)
strategy.exit("Loss Cut", from_entry="Buy", stop=止损水平)
strategy.exit("Profit Target", from_entry="Sell", profit_target=目标利润)
strategy.exit("Loss Cut", from_entry="Sell", stop=止损水平)
```

This is the translated and adjusted Pine Script code, keeping the original code blocks, numbers, and formatting intact, with the translated human-readable text as specified.