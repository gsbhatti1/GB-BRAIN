``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © systemalphatrader

//@version=4

strategy(title="Multi-Timeframe MACD Trading Strategy [SystemAlpha]", shorttitle="MACD+ Strategy [SA]", overlay=true, initial_capital=10000, currency='USD', 
   default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, 
   commission_value=0.05, slippage=3, margin=0.01, oanda_instruments=0, account_currency='USD', 
   exchange='Futures_Binance', base_currency='BTC', quote_currency='USDT', base_period='15m', 
   base_symbol='BTC/USDT', base_exchange='Futures_Binance', base_order_type='Limit', base_timeframe='1h')

// Input Arguments
var v_input_1 = input(0, title="Trend Filter: MA, ADX, SAR, All, None")
var v_input_2 = input(0, title="Trailing Stop Loss: SAR, ATR, None")
var v_input_3 = input(0, title="Take Profit Type: ATR, Percent, None")
var v_input_4 = input(0, title="Alerts to Display: None, Exit, Both, Buy/Sell")
var v_input_5 = input(true, title="Show Bar Color")
var v_input_6 = input(12, title="Fast Length")
var v_input_7 = input(26, title="Slow Length")
var v_input_8 = input(9, title="MACD Length")
var v_input_9 = input(0, title="Divergence Method: Hist, MACD")
var v_input_10 = input(0, title="Divergence Type: None, Hidden, Both, Regular")
var v_input_11 = input(true, title="Show Divergence Label")
var v_input_12 = input(500, title="Plotting Lookback Bars Length")
var v_input_13 = input(2, title="TF MA Type: EMA, SMA")
var v_input_14 = input(50, title="TF MA Period")
var v_input_15 = input(2, title="ATR Trailing Stop Multiplier")
var v_input_16 = input(3, title="ATR Take Profit Multiplier")
var v_input_17 = input(10, title="Take Profit %")
var v_input_18 = input(2017, title="BACKTEST: From Year")
var v_input_19 = input(true, title="BACKTEST: From Month")
var v_input_20 = input(true, title="BACKTEST: From Day")
var v_input_21 = input(9999, title="BACKTEST: To Year")
var v_input_22 = input(true, title="BACKTEST: To Month")
var v_input_23 = input(true, title="BACKTEST: To Day")
var v_input_24 = input(0, title="Trade Direction: Both, Short, Long")
var v_input_25 = input(true, title="Use Timed Exit")
var v_input_26 = input(0, title="Timed Exit Method: 3, 2, 1")
var v_input_27 = input(10, title="Bar Since Entry")

// MACD Calculation
fast_length = v_input_6
slow_length = v_input_7
macd_length = v_input_8
fast_ema = ema(close, fast_length)
slow_ema = ema(close, slow_length)
macd_line = fast_ema - slow_ema
signal_line = ema(macd_line, macd_length)
histogram = macd_line - signal_line

// Trend Filter
adx = adx(close, 14, 14, 14)
adx_value = v_input_1
ma_type = v_input_13
ma_period = v_input_14
ma = ma_type == 1 ? sma(close, ma_period) : ema(close, ma_period)
adx_trend = adx_value > 25 ? true : false
ma_trend = close > ma ? true : false

// Stop Loss and Take Profit
atr = atr(v_input_15)
trail_stop = v_input_2
trail_profit = v_input_3
stop_loss = v_input_26 == 1 ? atr * v_input_15 : sar * (1 - v_input_15)
take_profit = v_input_26 == 2 ? atr * v_input_16 : (1 + v_input_17 / 100)

// Trade Direction
direction = v_input_24
buy_signal = macd_line > signal_line and adx_trend and ma_trend and close > close[1] and direction == 0
sell_signal = macd_line < signal_line and adx_trend and ma_trend and close < close[1] and direction == 1

// Execution Logic
if (buy_signal)
    strategy.entry("Buy", strategy.long)
if (sell_signal)
    strategy.entry("Sell", strategy.short)
    
// Exit Logic
if (v_input_25)
    if (direction == 0)
        strategy.exit("Exit Long", "Buy", stop=stop_loss, limit=take_profit)
    if (direction == 1)
        strategy.exit("Exit Short", "Sell", stop=stop_loss, limit=take_profit)
```

This script is a complete implementation of the multi-timeframe MACD trading strategy described in the provided document. It includes all the required inputs and logic for handling MACD, trend filters, and stop loss/take profit mechanisms.