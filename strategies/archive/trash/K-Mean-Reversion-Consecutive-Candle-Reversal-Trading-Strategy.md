> Name

Mean-Reversion-Consecutive-Candle-Reversal-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1dae1d30727352e93d1.png)

#### Overview
This is a trading strategy based on the mean reversion principle, designed to capture short-term price reversal opportunities by identifying consecutive bearish and bullish candle patterns. The core logic of the strategy involves entering a long position after three consecutive bearish candles and exiting after three consecutive bullish candles. An optional EMA filter can be added to enhance trade quality.

#### Strategy Principles
The strategy is based on the following core elements:
1. Consecutive Candle Counter: Tracks the number of consecutive bullish and bearish candles.
2. Entry Condition: Triggers a long signal when a specified number (default 3) of consecutive lower closing prices occur.
3. Exit Condition: Triggers an exit signal when a specified number (default 3) of consecutive higher closing prices occur.
4. EMA Filter: Optionally uses a 200-period exponential moving average as a trend filter.
5. Trading Time Window: Can set specific trading start and end times to limit the trading periods.

#### Strategy Advantages
1. Simple and clear logic: The strategy uses a simple candle counting method, making it easy to understand and implement.
2. High adaptability: It can be applied to different timeframes and trading instruments.
3. Flexible parameters: Consecutive candle counts and EMA period parameters can be adjusted as needed.
4. Comprehensive risk control: Multiple mechanisms including time window and trend filter are used to control risks.
5. High computational efficiency: The core logic only requires comparing adjacent candle closing prices, resulting in a low computational load.

#### Strategy Risks
1. Trend market risk: May encounter frequent false breakouts in strong trending markets.
2. Parameter sensitivity: The number of consecutive candles setting significantly impacts strategy performance.
3. Slippage impact: May face significant slippage risks in volatile markets.
4. False signal risk: Consecutive candle patterns may be affected by market noise.
5. Lack of stop loss: The strategy lacks an explicit stop loss mechanism, potentially leading to large drawdowns.

#### Strategy Optimization Directions
1. Add stop loss mechanism: It is recommended to add a fixed or trailing stop loss to control risks.
2. Optimize filter conditions: Can introduce volume and volatility indicators as auxiliary filters.
3. Dynamic parameter adjustment: Consider dynamically adjusting the consecutive candle count requirements based on market conditions.
4. Enhance position management: Design partial position building and reduction mechanisms to improve returns.
5. Improve time management: Set different trading parameters for different times of the day.

#### Summary
This is a well-designed mean reversion strategy that generates returns by capturing short-term oversold bounce opportunities. The main advantages of the strategy are its simple logic and high adaptability, but risk control needs attention in practical application. It is recommended to enhance the stability of the strategy through adding stop loss mechanisms, optimizing filter conditions, and other improvements.

```pinescript
/* backtest
start: 2025-01-19 00:00:00
end: 2025-02-18 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("3 Down, 3 Up Strategy", overlay=true, initial_capital = 1000000, default_qty_value = 200, default_qty_type = strategy.percent_of_equity, process_orders_on_close = true, margin_long = 5, margin_short = 5, calc_on_every_tick = true)


//#region INPUTS SECTION
// ============================================
// Time Settings
// ============================================
startTimeInput = input(timestamp("1 Jan 2014"), "Start Time", group = "Time Settings")
endTimeInput = input(timestamp("1 Jan 2099"), "End Time", group = "Time Settings")
isWithinTradingWindow = true

// ============================================
// Strategy Settings
// ============================================
buyTriggerInput = input.int(3, "Consecutive Down Closes for Entry", minval = 1, group = "Strategy Settings")
sellTriggerInput = input.int(3, "Consecutive Up Closes for Exit", minval = 1, group = "Strategy Settings")

// ============================================
// EMA Filter Settings
// ============================================
useEmaFilter = input.bool(false, "Use EMA Filter", group = "Trend Filter")
emaPeriodInput = input.int(200, "EMA Period", minval = 1, group = "Trend Filter")
//#endregion

//#region INDICATOR CALCULATIONS
// ============================================
// Consecutive Close Counter
// ============================================
var int aboveCount = na
var int belowCount = na

aboveCount := close > close[1] ? (na(aboveCount) ? 1 : aboveCount + 1) : 0
belowCount := close < close[1] ? (na(belowCount) ? 1 : belowCount + 1) : 0

// ============================================