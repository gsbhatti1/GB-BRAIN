``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-04-30 23:59:59
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Gelişmiş Al-Sat Sinyalleri", overlay=true, process_orders_on_close=true)

// 15 dakikalık grafik verileri
fifteen_minute_close = request.security(syminfo.tickerid, "15", close)

// Stop loss ve take profit seviyelerini hesaplamak için kullanılacak oranlar
stop_loss_ratio = input.float(0.01, title="Stop Loss Oranı")
take_profit_ratio = input.float(0.02, title="Take Profit Oranı")

// Bollinger Bantları göstergesi
length = input.int(20, title="BB Dönemi")
mult = input.float(2.0, title="BB Çarpanı")
basis = ta.sma(fifteen_minute_close, length)
dev = mult * ta.stdev(fifteen_minute_close, length)
upper = basis + dev
lower = basis - dev

// Moving Averages (Hareketli Ortalamalar)
fast_ma = ta.sma(fifteen_minute_close, 10)
slow_ma = ta.sma(fifteen_minute_close, 50)

// MACD göstergesi
macd_line = ta.macd(fifteen_minute_close)[0]
signal_line = ta.macd(fifteen_minute_close)[1]
histogram = ta.macd(fifteen_minute_close)[2]

// RSI göstergesi
rsi_length = input.int(14, title="RSI Dönemi")
rsi = ta.rsi(fifteen_minute_close, rsi_length)

// Stochastik Oscillator göstergesi
k_line = ta.stoch(fifteen_minute_close)[0]
d_line = ta.stoch(fifteen_minute_close)[1]

// VWAP göstergesi
vwap_period = input.int(34, title="VWAP Dönemi")
vwap = ta.vwma(fifteen_minute_close, vwap_period)

// Al-Sat Sinyalleri
buy_condition = fast_ma > slow_ma and macd_line > signal_line and rsi > 50 and fifteen_minute_close > upper and k_line > d_line
sell_condition = fast_ma < slow_ma and macd_line < signal_line and rsi < 50 and fifteen_minute_close < lower and k_line < d_line

// İşlem Yönetimi
if (buy_condition)
    strategy.entry("Buy", strategy.long, stop=fifteen_minute_close - stop_loss_ratio * abs(fifteen_minute_close), limit=fifteen_minute_close + take_profit_ratio * abs(fifteen_minute_close))

if (sell_condition)
    strategy.entry("Sell", strategy.short, stop=fifteen_minute_close + stop_loss_ratio * abs(fifteen_minute_close), limit=fifteen_minute_close - take_profit_ratio * abs(fifteen_minute_close))
```

This Pine Script code implements the advanced trading signals strategy described in your document. The script uses 15-minute chart data to generate buy and sell signals based on multiple technical indicators, including Bollinger Bands, moving averages, MACD, RSI, Stochastic Oscillator, and VWAP. It also sets stop-loss and take-profit levels for risk management.