> Name

The-Momentum-Tracking-and-Trend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1351b3dcd32a5335df2.png)
[trans]
### Overview

The core idea of this strategy is to combine the Super Trend indicator and the Average Directional Movement Index (ADX) to judge and track trends. The Super Trend indicator is used to identify the current price trend direction, and the ADX is used to determine the trend strength. Trades are only made under strong trend conditions. Additionally, the strategy uses candlestick body color, trading volume, and other indicators for confirmation, forming a relatively complete set of trading rules.

Overall, this strategy belongs to the trend tracking strategy, aiming to capture medium and long-term clear trends while avoiding interference from consolidation and oscillation periods.

### Strategy Principles

1. Use the Super Trend indicator to determine the price trend direction. When the price stands above the Super Trend, it is a long signal; when it stands below the Super Trend, it is a short signal.

2. Use the ADX to judge the strength of the trend. Trading signals are generated only when the ADX is greater than the threshold, so that periods with unclear consolidation can be filtered out.

3. The candlestick body color is used to judge whether it is currently in an upward or downward pattern, combined with the Super Trend indicator to form confirmation.

4. Expanding trading volume serves as a confirmation signal. Positions are only established when trading volume rises.

5. Set stop loss and take profit to lock in profits and control risks.

6. Close all positions before the set end of the day time.

### Advantages of the Strategy

1. Track medium and long-term clear trends, avoid oscillation, and achieve high profitability.

2. The strategy has few parameters and is easy to understand and implement.

3. Risks are well controlled with stop loss and take profit in place.

4. The use of multiple indicators for confirmation can reduce false signals.

### Risks of the Strategy

1. May suffer large losses during major market-wide corrections.

2. Individual stocks may have sharp reversals due to changes in fundamentals.

3. Black swan events from major policy changes.

Solutions:

1. Appropriately adjust ADX parameters to ensure trading only under strong trends.

2. Increase stop loss percentage to control single loss amount.

3. Closely monitor policies and important events, actively cut loss if necessary.

### Directions for Optimization

1. Test different combinations of Super Trend parameters to find the one that generates the most stable signals.

2. Test different ADX parameter combinations to determine the optimal settings.

3. Add other confirmation indicators like volatility and Bollinger Bands to further reduce false signals.

4. Combine with breakout strategies to cut losses in a timely manner when trends break down.

### Summary

The overall logic of this strategy is clear, using the Super Trend to judge price trend direction, the ADX to determine trend strength, and trading along strong trends. Stop loss and take profit are set to control risks. The strategy has few parameters and is easy to optimize. It can serve as a good example for learning simple and effective trend tracking strategies. Further improvements can be made through parameter optimization, signal filtering, etc.

||

### Overview

The core idea of this strategy is to combine the Super Trend indicator and the Average Directional Movement Index (ADX) to judge and track trends. The Super Trend indicator is used to identify the current price trend direction, and the ADX is used to determine the trend strength. Trades are only made under strong trend conditions. Additionally, the strategy uses candlestick body color, trading volume, and other indicators for confirmation, forming a relatively complete set of trading rules.

Overall, this strategy belongs to the trend tracking strategy, aiming to capture medium and long-term clear trends while avoiding interference from consolidation and oscillation periods.

### Strategy Principles

1. Use the Super Trend indicator to determine the price trend direction. When the price stands above the Super Trend, it is a long signal; when it stands below the Super Trend, it is a short signal.

2. Use the ADX to judge the strength of the trend. Trading signals are generated only when the ADX is greater than the threshold, so that periods with unclear consolidation can be filtered out.

3. The candlestick body color is used to judge whether it is currently in an upward or downward pattern, combined with the Super Trend indicator to form confirmation.

4. Expanding trading volume serves as a confirmation signal. Positions are only established when trading volume rises.

5. Set stop loss and take profit to lock in profits and control risks.

6. Close all positions before the set end of the day time.

### Advantages of the Strategy

1. Track medium and long-term clear trends, avoid oscillation, and achieve high profitability.

2. The strategy has few parameters and is easy to understand and implement.

3. Risks are well controlled with stop loss and take profit in place.

4. The use of multiple indicators for confirmation can reduce false signals.

### Risks of the Strategy

1. May suffer large losses during major market-wide corrections.

2. Individual stocks may have sharp reversals due to changes in fundamentals.

3. Black swan events from major policy changes.

Solutions:

1. Appropriately adjust ADX parameters to ensure trading only under strong trends.

2. Increase stop loss percentage to control single loss amount.

3. Closely monitor policies and important events, actively cut loss if necessary.

### Directions for Optimization

1. Test different combinations of Super Trend parameters to find the one that generates the most stable signals.

2. Test different ADX parameter combinations to determine the optimal settings.

3. Add other confirmation indicators like volatility and Bollinger Bands to further reduce false signals.

4. Combine with breakout strategies to cut losses in a timely manner when trends break down.

### Summary

The overall logic of this strategy is clear, using the Super Trend to judge price trend direction, the ADX to determine trend strength, and trading along strong trends. Stop loss and take profit are set to control risks. The strategy has few parameters and is easy to optimize. It can serve as a good example for learning simple and effective trend tracking strategies. Further improvements can be made through parameter optimization, signal filtering, etc.

---

### Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|0915-1455|Market session|
|v_input_2|true|Long Take Profit (%)|
|v_input_3|true|Short Take Profit (%)|
|v_input_4|0.5|Long Stop Loss (%)|
|v_input_5|0.5|Short Stop Loss (%)|
|v_input_6|2|ST Multiplier|
|v_input_7|10|ST ATR Period|
|v_input_8|14|ADX Length|
|v_input_9|20|ADX Threshold|
|v_input_10|25|ADX Momentum Value|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-02-15 00:00:00
end: 2024-02-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Intraday Strategy Template

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © vikris

//@version=4
strategy("[VJ]Hulk Smash Intra", overlay=true, calc_on_every_tick = false, pyramiding=0,default_qty_type=strategy.percent_of_equity, default_qty_value=100,initial_capital=2000)

// ********** Strategy inputs - Start **********

// Used for intraday handling
// Session value should be from market start to the time you want to square-off 
// your intraday strategy
// Important: The end time should be at least 2 minutes before the intraday
// square-off time set by your broker
var i_marketSession = input(title="Market session", type=input.session, 
     defval="0915-1455", confirm=true)

// Make inputs that set the take profit % (optional)
longProfitPerc = input(title="Long Take Profit (%)",
     type=input.float, minval=0.0, 
```