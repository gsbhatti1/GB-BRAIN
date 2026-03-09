``` pinescript
/*backtest
start: 2024-01-06 00:00:00
end: 2025-01-04 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI-MACD-Stochastic Strategy", shorttitle = "RMS_V1", overlay=true)

// Inputs
use_macd = input.bool(true, title="Use MACD")
use_rsi = input.bool(true, title="Use RSI")
use_stochastic = input.bool(true, title="Use Stochastic")
threshold_buy = input.float(0.5, title="Buy Threshold (Probability)")
threshold_sell = input.float(-0.5, title="Sell Threshold (Probability)")

// Indicators
// RSI
rsi_period = input.int(14, title="RSI Period")
rsi = ta.rsi(close, rsi_period)

// Stochastic Oscillator
stoch_k = ta.stoch(close, high, low, rsi_period)
stoch_d = ta.sma(stoch_k, 3)

// MACD
[macd_line, signal_line, _] = ta.macd(close, 12, 26, 9)

// Calculate Z-score
lookback = input.int(20, title="Z-score Lookback Period")
mean_close = ta.sma(close, lookback)
stddev_close = ta.stdev(close, lookback)
zscore = (close - mean_close) / stddev_close

// Buy and Sell Conditions
long_condition = (use_rsi and rsi < 30) or (use_stochastic and stoch_k < 20) or (use_macd and macd_line > signal_line)
short_condition = (use_rsi and rsi > 70) or (use_stochastic and stoch_k > 80) or (use_macd and macd_line < signal_line)

buy_signal = long_condition and zscore > threshold_buy
sell_signal = short_condition and zscore < threshold_sell

// Trading Actions
if (buy_signal)
    strategy.entry("Buy", strategy.long)
if (sell_signal)
    strategy.close("Buy")
```

This Pine Script code defines a trading strategy using RSI, MACD, and Stochastic Oscillator indicators. It includes inputs for enabling/disabling the indicators, setting probability thresholds, and calculating Z-scores. The strategy performs buy and sell actions based on the defined conditions and Z-score thresholds.