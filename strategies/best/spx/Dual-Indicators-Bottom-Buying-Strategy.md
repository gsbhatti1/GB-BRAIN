``` pinescript
/*backtest
start: 2023-12-27 00:00:00
end: 2024-01-03 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © wielkieef

//@version=5

strategy(title='BTFD strategy [3min]', overlay=true, pyramiding=5, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.03)


// Volume

vol_sma_length = input.int(70, title='Volume length')
rsi_length = input.int(20, title='RSI length')
tp1 = input.float(0.4, title='% TP 1')
tp2 = input.float(0.6, title='% TP 2')
tp3 = input.float(0.8, title='% TP 3')
tp4 = input.bool(true, title='TP 4')
tp5 = input.float(1.2, title='% TP 5')
tp1_q = input.int(20, title='% TP 1 Q')
tp2_q = input.int(40, title='% TP 2 Q')
tp3_q = input.int(60, title='% TP 3 Q')
tp4_q = input.int(80, title='% TP 4 Q')
tp5_q = input.int(100, title='% TP 5 Q')
stop_loss_pct = input.float(5.0, title='% Stop Loss')

// Functions

long_condition = ta.volume > ta.sma(ta.volume, vol_sma_length) * 2.5 and ta.rsi(close, rsi_length) < 30
short_condition = false // Not implemented in this strategy

// On condition met, enter long position
if (long_condition)
    strategy.entry("Long", strategy.long)

// Take Profit Logic
total_qty = strategy.opentrades_qty()
tp1_qty = total_qty * tp1_q / 100
tp2_qty = total_qty * tp2_q / 100
tp3_qty = total_qty * tp3_q / 100
tp4_qty = total_qty * tp4_q / 100
tp5_qty = total_qty * tp5_q / 100

// Exit on TP levels
if (strategy.opentrades.exists("Long"))
    strategy.exit(id="TP1", from_entry="Long", limit=close + close * tp1/100, quantity_percent=tp1_qty)
    strategy.exit(id="TP2", from_entry="Long", limit=close + close * tp2/100, quantity_percent=tp2_qty)
    strategy.exit(id="TP3", from_entry="Long", limit=close + close * tp3/100, quantity_percent=tp3_qty)
    if (tp4)
        strategy.exit(id="TP4", from_entry="Long", limit=close + close * tp4/100, quantity_percent=tp4_qty)
    strategy.exit(id="TP5", from_entry="Long", limit=close + close * tp5/100, quantity_percent=tp5_qty)

// Stop Loss Logic
if (strategy.opentrades.exists("Long"))
    strategy.exit(id="StopLoss", from_entry="Long", stop=close - close * stop_loss_pct / 100)
```

This translation keeps the code blocks and formatting exactly as provided while translating the human-readable text.