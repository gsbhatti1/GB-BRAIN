```pinescript
/*backtest
start: 2024-01-26 00:00:00
end: 2024-02-25 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Elliott Wave Strategy with 200 SMA", overlay=true)

// Elliott Wave Strategy
wave1High = high[1]
wave1Low = low[1]
wave2High = high[2]
wave2Low = low[2]
wave3High = high[3]
wave3Low = low[3]
wave4High = high[4]
wave4Low = low[4]
wave5High = high[5]
wave5Low = low[5]

bullishWavePattern = wave3High > wave1High and wave4Low > wave2Low and wave5High > wave3High
bearishWavePattern = wave3Low < wave1Low and wave4High < wave2High and wave5Low < wave3Low

enterLong = bullishWavePattern and close > sma(close, 200)
exitLong = bearishWavePattern
enterShort = bearishWavePattern and close < sma(close, 200)
exitShort = bullishWavePattern

// Plotting 200 SMA
sma200 = sma(close, 200)
plot(sma200, color=color.blue, title="Moving Average 200")

// Displaying "Razer Moving 200" message on chart
if (enterLong)
    label.new(bar_index, low, "Long on Moving 200", color=color.green, textcolor=color.white)
if (enterShort)
    label.new(bar_index, high, "Short on Moving 200", color=color.red, textcolor=color.white)

if (enterLong)
    strategy.entry("Long", strategy.long)
if (exitLong)
    strategy.close("Long")
if (enterShort)
    strategy.entry("Short", strategy.short)
if (exitShort)
    strategy.close("Short")
```

> Detailed
The provided Pine Script code implements the trading strategy described in the Chinese document. The script identifies Elliott Wave patterns and uses a 200-day Simple Moving Average (SMA) to generate buy and sell signals.

1. **Elliott Wave Patterns**: 
   - `bullishWavePattern` checks for an upward wave pattern by comparing high points of waves.
   - `bearishWavePattern` checks for a downward wave pattern similarly.
   
2. **Trading Signals**:
   - Long entry occurs when the bullish wave pattern is identified and the closing price exceeds the 200-day SMA.
   - Short entry occurs when the bearish wave pattern is identified and the closing price falls below the 200-day SMA.

3. **Visualization**:
   - The script plots a 200-day SMA on the chart for reference.
   - Buy (`Long`) signals are marked with green labels at the low of the bar.
   - Sell (`Short`) signals are marked with red labels at the high of the bar.

4. **Strategy Execution**:
   - `strategy.entry` and `strategy.close` functions handle the entry and exit of trades based on the defined conditions.

This implementation effectively translates the Chinese strategy description into a fully operational Pine Script for backtesting and live trading in TradingView.