> Name

Williams-R-Dynamic-TP-SL-Adjustment-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/693ea875fea3e9b203.png)
[trans]
#### Overview
This strategy is based on the Williams %R indicator and optimizes trading performance by dynamically adjusting take profit and stop loss levels. Buy signals are generated when the Williams %R crosses above the oversold area (-80), and sell signals are generated when it crosses below the overbought area (-20). An Exponential Moving Average (EMA) is used to smooth the Williams %R values and reduce noise. The strategy offers flexible parameter settings, including indicator periods, take profit/stop loss (TP/SL) levels, trading hours, and trade direction choices, to adapt to different market conditions and trader preferences.

#### Strategy Principles
1. Calculate the Williams %R indicator value for a given period.
2. Calculate the Exponential Moving Average (EMA) of the Williams %R.
3. When the Williams %R crosses above the -80 level from below, it triggers a buy signal; when it crosses below the -20 level from above, it triggers a sell signal.
4. After a buy entry, set take profit and stop loss levels. The trade is closed when the TP/SL price levels are reached or when the Williams %R triggers a reverse signal.
5. After a sell entry, set take profit and stop loss levels. The trade is closed when the TP/SL price levels are reached or when the Williams %R triggers a reverse signal.
6. Optionally, trade within a specified time range (e.g., 9:00-11:00) and choose whether to trade near the top of the hour (X minutes before to Y minutes after).
7. Optionally, choose the trade direction as long only, short only, or both.

#### Advantages Analysis
1. Dynamic TP/SL: Dynamically adjust take profit and stop loss levels based on user settings, which can better protect profits and control risks.
2. Flexible parameters: Users can set various parameters according to their preferences, such as indicator periods, TP/SL levels, trading hours, etc., to adapt to different market conditions.
3. Smoothed indicator: Introducing EMA to smooth Williams %R values can effectively reduce indicator noise and improve signal reliability.
4. Restricted trading time: Optionally trade within a specific time range to avoid highly volatile market periods and reduce risk.
5. Customizable trade direction: Choose to go long only, short only, or trade in both directions based on market trends and personal judgment.

#### Risk Analysis
1. Improper parameter settings: If the TP/SL settings are too loose or too strict, it may lead to profit loss or frequent stop-outs.
2. Trend identification errors: The Williams %R indicator performs poorly in choppy markets and may generate false signals.
3. Limited effect of time restrictions: Limiting trading time may cause the strategy to miss some good trading opportunities.
4. Over-optimization: Over-optimizing parameters may lead to poor strategy performance in future actual trading.

#### Optimization Directions
1. Combine with other indicators: Such as trend indicators, volatility indicators, etc., to improve the accuracy of signal confirmation.
2. Dynamic parameter optimization: Adjust parameters in real-time according to market conditions, such as using different parameter settings in trending and ranging markets.
3. Improve TP/SL methods: Such as using trailing stop loss, partial profit-taking, etc., to better protect profits and control risks.
4. Incorporate money management: Dynamically adjust the position size of each trade based on account balance and risk preferences.

#### Summary
The Williams %R Dynamic TP/SL Adjustment Strategy captures overbought and oversold price conditions in a simple and effective way while providing flexible parameter settings to adapt to different market environments and trading styles. The strategy dynamically adjusts take profit and stop loss levels, which can better control risks and protect profits. However, when applying the strategy in practice, attention should still be paid to factors such as parameter settings, signal confirmation, and trading time selection to further improve the robustness and profitability of the strategy.
[/trans]

> Source (PineScript)

```pinescript
//@version=5
strategy("Williams %R Strategy defined buy/sell criteria with TP / SL", overlay=true)

// User inputs for TP and SL levels
tp_level = input.int(defval=60, title="Take Profit Level")
sl_level = input.int(defval=-20, title="Stop Loss Level")

// Williams R indicator calculation
williamsR = ta.willr(14)
ema_williamsR = ta.ema(williamsR, 9)

// Buy and Sell signals
buy_signal = ta.crossover(ema_williamsR, -80)
sell_signal = ta.crossunder(ema_williamsR, -20)

// Trade entry
if (buy_signal)
    strategy.entry("Buy", strategy.long)

if (sell_signal)
    strategy.entry("Sell", strategy.short)

// Set Take Profit and Stop Loss levels
if (strategy.opentrades > 0)
    if (strategy.position_size > 0)
        strategy.exit("Profit Target", "Buy", limit=tp_level, stop=sl_level)
    else
        strategy.exit("Loss Cutoff", "Sell", limit=sl_level, stop=tp_level)

// Optional time and direction settings
[trans]
#### Overview
This script provides an implementation of the Williams %R dynamic TP/SL adjustment strategy with customizable parameters for trade direction and trading hours. It utilizes the Williams %R indicator to identify market conditions and sets take profit and stop loss levels dynamically based on user inputs.

#### Strategy Parameters
1. **Take Profit Level**: User-defined level at which a buy position will be exited.
2. **Stop Loss Level**: User-defined level at which a sell position will be exited.
3. **Trade Direction**: Option to trade only long, only short, or both directions.
4. **Trading Hours**: Optional setting to limit trading to specific hours.

#### Usage
1. Define the take profit and stop loss levels using the `input.int` function.
2. Calculate the Williams %R indicator and its EMA for smoothing.
3. Generate buy and sell signals based on crossing conditions.
4. Enter trades when appropriate, exiting positions upon reaching the TP or SL level.

#### Example Pine Script Code
```pinescript
//@version=5
strategy("Williams %R Dynamic TP/SL Adjustment Strategy", overlay=true)

// User inputs for TP and SL levels
tp_level = input.int(defval=60, title="Take Profit Level")
sl_level = input.int(defval=-20, title="Stop Loss Level")

// Williams R indicator calculation
williamsR = ta.willr(14)
ema_williamsR = ta.ema(williamsR, 9)

// Buy and Sell signals
buy_signal = ta.crossover(ema_williamsR, -80)
sell_signal = ta.crossunder(ema_williamsR, -20)

// Trade entry
if (buy_signal)
    strategy.entry("Buy", strategy.long)

if (sell_signal)
    strategy.entry("Sell", strategy.short)

// Set Take Profit and Stop Loss levels
if (strategy.opentrades > 0)
    if (strategy.position_size > 0)
        strategy.exit("Profit Target", "Buy", limit=tp_level, stop=sl_level)
    else
        strategy.exit("Loss Cutoff", "Sell", limit=sl_level, stop=tp_level)

// Optional time and direction settings

```
[/trans]
```