> Name

Historical Breakout Trend System with Moving Average Filter (HBTS)

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1566a8474aeecdb43c4.png)

[trans]
#### Overview
This strategy is a trend-following system based on historical price breakouts and moving average filters. It combines multi-period price breakout signals with moving averages to identify market trends, using strict entry and exit rules to capture medium to long-term market movements. The strategy uses 55-day price breakouts for long signals, 20-day price breakouts for exits, and incorporates a 200-day moving average as a trend filter to effectively reduce false breakout risks.

#### Strategy Principles
The core logic is built on price breakouts and trend following. Specifically:
1. Entry Signal: System generates a long signal when price makes a 55-day high and closes above the 200-day moving average.
2. Exit Signal: System closes positions when price breaks below the 20-day low.
3. Trend Filter: Uses 200-day moving average as a major trend indicator, only entering longs above the average.
4. Position Management: Uses 10% of account equity for each trade.
5. Moving Average Options: Supports SMA, EMA, WMA, and VWMA, allowing flexibility based on market characteristics.

#### Strategy Advantages
1. Clear Logic: Strategy uses classic price breakout and moving average indicators, easy to understand and execute.
2. Robust Risk Control: Has clear stop-loss conditions, manages risk through moving average filters and position control.
3. High Adaptability: Can be adjusted through parameters to suit different market environments.
4. Strong Trend Capturing: Uses multiple timeframe price breakouts to confirm trend direction.
5. High Automation: Clear strategy rules facilitate programmatic implementation.

#### Strategy Risks
1. Choppy Market Risk: Prone to false breakouts during consolidation phases.
2. Slippage Risk: May experience significant slippage in less liquid markets.
3. Trend Reversal Risk: Potential for large drawdowns near major trend turning points.
4. Parameter Sensitivity: Optimal parameters may vary significantly across different market environments.
5. Money Management Risk: Fixed proportion positioning may be too risky in certain situations.

#### Optimization Directions
1. Signal Confirmation: Can add volume breakout and other auxiliary indicators to filter false breakouts.
2. Dynamic Stop Loss: Incorporate ATR and other volatility indicators for dynamic stop loss.
3. Position Management: Dynamically adjust position size based on market volatility.
4. Multi-timeframe Analysis: Add more timeframe analysis to improve signal reliability.
5. Market Environment Recognition: Add trend strength indicators to judge current market conditions.

#### Summary
This is a strategic system that combines classic turtle trading rules with modern technical analysis tools. It captures trends through price breakouts, confirms direction using moving averages, and controls risk with reasonable position management. The strategy logic is clear, practical, and has good scalability. While it may underperform in choppy markets, through proper parameter optimization and risk control, it can still achieve stable returns in trending markets. Traders are advised to adjust parameters based on specific market characteristics and establish comprehensive money management systems when applying to live trading.

#### Source (PineScript)

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-04 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Turtle Traders - Andrei", overlay=true, 
     default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// ====== Inputs ======
// Period for the buy high
lookback_buy = input.int(title="Period for Buy High", defval=55, minval=1)

// Period for the sell low
lookback_sell = input.int(title="Period for Sell Low", defval=20, minval=1)

// Moving average length
ma_length = input.int(title="Moving Average Length", defval=200, minval=1)

// Moving average type
ma_type = input.string(title="Moving Average Type", defval="SMA", options=["SMA", "EMA", "WMA", "VWMA"])

// ====== Calculations ======
// Calculation of the moving average based on selected type
ma = switch ma_type
    "SMA" => ta.sma(close, ma_length)
    "EMA" => ta.ema(close, ma_length)
    "WMA" => ta.wma(close, ma_length)
    "VWMA" => ta.vwma(close, ma_length)

// Calculation of the highest high in the last 'lookback_buy' candles
highest_buy = ta.highest(high, lookback_buy)

// Calculation of the lowest low in the last 'lookback_sell' candles
lowest_sell = ta.lowest(low, lookback_sell)

// ====== Trading Conditions ======
// Entry condition: closing above the highest high in the last 'lookback_buy' candles.
```