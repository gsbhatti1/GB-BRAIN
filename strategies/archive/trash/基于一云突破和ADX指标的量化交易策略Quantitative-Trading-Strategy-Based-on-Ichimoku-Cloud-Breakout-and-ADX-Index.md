``` pinescript
/*backtest
start: 2023-01-26 00:00:00
end: 2024-02-01 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Coinrule

//@version=5
strategy('Ichimoku Cloud with ADX (By Coinrule)',
         overlay=true,
         initial_capital=1000,
         process_orders_on_close=true,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=30,
         commission_type=strategy.commission.percent,
         commission_value=0.1)

showDate = input(defval=true, title='Show Date Range')
timePeriod = time >= timestamp(syminfo.timezone, 2022, 1, 1, 0, 0)

// Stop Loss and Take Profit for Shorting
Stop_loss = input(1) / 100
Take_profit = input(5) / 100
longStopPrice = strategy.position_avg_price * (1 - Stop_loss)
longTakeProfit = strategy.position_avg_price * (1 + Take_profit)

// Inputs
ts_bars = input.int(9, minval=1, title='Tenkan-Sen Bars')
ks_bars = input.int(26, minval=1, title='Kijun-Sen Bars')
ssb_bars = input.int(52, minval=1, title='Senkou-Span B Bars')
cs_offset = input.int(26, minval=1, title='Chikou-Span Offset')
ss_offset = input.int(26, minval=1, title='Senkou-Span Offset')
long_entry = input(true, title='Long Entry')
short_entry = input(true, title='Short Entry')

middle(len) => math.avg(ta.lowest(len), ta.highest(len))

// Ichimoku Components
tenkan = middle(ts_bars)
kijun = middle(ks_bars)
senkouA = math.avg(tenkan, kijun)
senkouB = middle(ssb_bars)

// Plot Ichimoku Kinko Hyo
plot(tenkan, color=color.new(#0496ff, 0), title='Tenkan-Sen')
plot(kijun, color=color.new(#999999, 0), title='Kijun-Sen')
plot(senkouA, color=color.new(#009900, 0), title='Senkou Span A')
plot(senkouB, color=color.new(#ff9900, 0), title='Senkou Span B')
plot(tenkan, style=plot.style_line, color=color.new(#0496ff, 0), title='Tenkan-Sen')
plot(kijun, style=plot.style_line, color=color.new(#999999, 0), title='Kijun-Sen')
plot(senkouA, style=plot.style_line, color=color.new(#009900, 0), title='Senkou Span A')
plot(senkouB, style=plot.style_line, color=color.new(#ff9900, 0), title='Senkou Span B')
plot(tenkan, style=plot.style_histogram, color=color.new(#0496ff, 0), title='Tenkan-Sen')
plot(kijun, style=plot.style_histogram, color=color.new(#999999, 0), title='Kijun-Sen')
plot(senkouA, style=plot.style_histogram, color=color.new(#009900, 0), title='Senkou Span A')
plot(senkouB, style=plot.style_histogram, color=color.new(#ff9900, 0), title='Senkou Span B')

// Chikou Span
plot(cs_offset, title='Chikou Span', color=color.new(#ff0000, 0), style=plot.style_histogram, location=location.belowbar)

// Plot ADX
adx = ta.adx(14)
plot(adx, title='ADX', color=color.new(#0000ff, 0), style=plot.style_histogram)

// Long Entry Signal
long_signal = ta.crossover(tenkan, kijun) and ta.crossover(tenkan, 0) and close > senkouB and adx < 45 and ta.plus_di(14) > ta.minus_di(14) and long_entry
if (long_signal)
    strategy.entry('Long', strategy.long)

// Short Entry Signal
short_signal = ta.crossunder(tenkan, kijun) and ta.crossunder(tenkan, 0) and close < senkouB and adx > 45 and ta.plus_di(14) < ta.minus_di(14) and short_entry
if (short_signal)
    strategy.entry('Short', strategy.short)

// Stop Loss and Take Profit
strategy.exit('Long Exit', from_entry='Long', stop=longStopPrice, limit=longTakeProfit)
strategy.exit('Short Exit', from_entry='Short', stop=strategy.position_avg_price * (1 + Stop_loss), limit=strategy.position_avg_price * (1 - Take_profit))
```

This script implements the trading strategy described. It includes the Ichimoku Cloud components, ADX calculation, and the specific trading rules for long and short positions.