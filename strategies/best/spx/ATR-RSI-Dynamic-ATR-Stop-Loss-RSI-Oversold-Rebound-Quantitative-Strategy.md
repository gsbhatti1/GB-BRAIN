> Name

Dynamic ATR Stop-Loss RSI Oversold Rebound Quantitative Strategy - Dynamic-ATR-Stop-Loss-RSI-Oversold-Rebound-Quantitative-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1aa84010a36b301b8fe.png)

[trans]
#### Overview
This strategy is a quantitative trading system based on RSI oversold signals and dynamic ATR stop-loss. Using daily timeframe data, it combines RSI oversold signals with a 200-day moving average trend filter to capture rebound opportunities in oversold market conditions. The strategy employs both dynamic ATR stop-loss and static percentage stop-loss mechanisms, along with triple profit targets implemented through staged position reduction.

#### Strategy Principles
The core logic includes the following key elements:
1. Entry Signal: System generates long signals when RSI(5) falls below the oversold level of 30 and price is above the 200-day moving average.
2. Stop-Loss Mechanism: Combines 1.5x ATR(20) dynamic stop-loss with a 25% fixed stop-loss.
3. Profit Targets: Sets three targets at 5%, 10%, and 15%, reducing position by 33%, 66%, and 100% respectively.
4. Position Management: Recommends using Kelly Criterion calculated 59.13% position size or conservative 75% position size.

#### Strategy Advantages
1. Dual Trend Confirmation: Validates trades through both RSI oversold and moving average trend, improving win rate.
2. Flexible Risk Control: Dynamic ATR stop-loss adapts to market volatility while fixed stop-loss provides ultimate protection.
3. Intelligent Profit Management: Triple targets with staged position reduction secures profits while maintaining upside potential.
4. Scientific Capital Management: Optimizes position sizing using Kelly Criterion, balancing risk and reward.

#### Strategy Risks
1. Trend Dependency: Strategy may trigger frequent stops in ranging markets.
Suggestion: Add oscillator filters to reduce false signals.

2. Wide Stop-Loss: 25% fixed stop-loss may result in large single-trade losses.
Suggestion: Adjust stop-loss percentage based on personal risk tolerance.

3. Drawdown Risk: Staged profit-taking may reduce positions too early in strong trends.
Suggestion: Consider dynamic profit targets or retain portion for trend following.

#### Strategy Optimization Directions
1. Signal Optimization:
- Add volume confirmation
- Incorporate trend indicators like MACD
- Implement volatility filters

2. Stop-Loss Optimization:
- Implement dynamic stop-loss percentages
- Add time-based stops
- Include risk-reward filters

3. Profit-Taking Optimization:
- Set dynamic targets based on ATR
- Implement trailing stops
- Optimize position reduction ratios

#### Summary
This strategy constructs a complete trading system by combining RSI oversold signals with moving average trend filtering, complemented by dynamic ATR stop-loss and triple profit targets. Its strengths lie in flexible risk control and rational profit management, though optimization based on market conditions and personal risk preference is necessary. Through continuous improvement of the signal system, stop-loss mechanism, and profit-taking strategy, the system shows potential for better performance in live trading.

||

#### Source (PineScript)

```pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA/4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/
// © wielkieef

//@version=5
strategy("Simple RSI Stock Strategy [1D]", overlay=true, pyramiding=1, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=75, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.03)

// Rsi
oversoldLevel = input(30, title="Oversold Level")
overboughtLevel = input(70, title="Overbought Level")
rsi = ta.rsi(close, 5)
rsi_overbought = rsi > overboughtLevel  
rsi_oversold = rsi < oversoldLevel

// Sma 200
lenghtSMA = input(200, title="SMA Length")
sma200 = ta.sma(close, lenghtSMA)

// ATR stop-loss
atrLength = input.int(20, title="ATR Length")
atrMultiplier = input.float(1.5, title="ATR Multiplier")
atrValue = ta.atr(atrLength)
var float long_stop_level = na
var float short_stop_level = na
var float tp1_level = na
var float tp2_level = na
var float tp3_level = na

// Strategy entry
long = (rsi_oversold) and close > sma200 

// Take Profit levels
tp_1 = input.float(5.0, "TP 1", minval=0.1, step=0.1)
tp_2 = input.float(10.0, "TP 2", minval=0.2, step=0.1)
tp_3 = input.float(15.0, "TP 3", minval=0.3, step=0.1)

if long
    strategy.entry("Long", strategy.long)
    long_stop_level := close - atrMultiplier * atrValue
    tp1_level := strategy.position_avg_price * (1 + tp_1 / 100)
    tp2_level := strategy.position_avg_price * (1 + tp_2 / 100)
```