> Name

Ichimoku-Backtester-with-TP-SL-and-Cloud-Confirmation

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c483369670e6628319.png)
[trans]

### Overview

This is a trend-following strategy based on the Ichimoku cloud. It integrates moving averages, the Ichimoku cloud, and precise entry and exit mechanisms to enhance profitability.

### Strategy Logic

The core of this strategy involves constructing the Ichimoku components using user-defined input parameters—Tenkan-Sen, Kijun-Sen, Senkou Span A & B, and Chikou Span. Bullish (long) and bearish (short) signals are identified when prices cross these equilibrium lines.

Additionally, stop loss and take profit levels are set based on the entry price to manage risk and reward. There is also an option to wait for cloud confirmation, i.e., Senkou Span A > B for longs and Senkou Span A < B for shorts. This helps avoid false breakouts.

### Advantages

The main advantages of this strategy are:

1. The Ichimoku indicator is good at identifying trends and momentum. The equilibrium lines provide strong support and resistance areas.
2. Stop loss and take profit features maximize rewards while minimizing risks, optimizing the risk-reward profile.
3. Cloud confirmation filters out false signals, ensuring high-probability entries, thus enhancing profitability.

### Risks

However, there are also key risks to consider:

1. The Ichimoku indicator can be prone to whipsaws during range-bound markets with no clear trend. Many stop losses may get triggered.
2. The cloud is a lagging indicator; by the time it confirms, much of the move might have already occurred.
3. Optimizing stop loss and take profit levels is challenging and sensitive. Suboptimal parameters can result in more losses.

### Enhancements

Some ways this strategy can be improved:

1. Combine Ichimoku with leading indicators like RSI for additional confirmation and early entry.
2. Adaptively adjust stop loss and take profit based on volatility rather than fixed percentages.
3. Test optimal parameters across various assets and timeframes to identify the best setups for the strategy.
4. Incorporate machine learning to continually optimize parameters and strategy rules based on updated data.

### Conclusion

This is a solid Ichimoku system with good trend capture and risk management features. With some enhancements, it can be an excellent addition to overall trading approaches. It works well across forex, commodities, and cryptocurrency markets, making it a recommended quantified strategy.

||

### Overview

This is an Ichimoku backtesting strategy with take profit, stop loss, and cloud confirmation. It aims to improve profitability by precisely capturing trends using the Ichimoku indicator.

### Strategy Logic

The core of this strategy involves constructing the Ichimoku components based on user input parameters—Tenkan-Sen, Kijun-Sen, Senkou Span A & B, and Chikou Span. Bullish (long) and bearish (short) signals are identified when prices cross these equilibrium lines.

In addition, stop loss and take profit levels are set based on the entry price to manage risk and reward. There is also an option to wait for cloud confirmation, i.e., Senkou Span A > B for longs and Senkou Span A < B for shorts. This helps avoid false breakouts.

### Advantages

The main advantages of this strategy are:

1. Ichimoku is good at identifying trends and momentum. The equilibrium lines provide solid support and resistance areas.
2. Stop loss and take profit features maximize rewards while minimizing risks, optimizing the risk-reward profile.
3. Cloud confirmation filters out false signals, ensuring high-probability entries, thus enhancing profitability.

### Risks

However, there are also key risks to consider:

1. Ichimoku is prone to whipsaws during range-bound markets with no clear trend. Lots of stops may be hit.
2. The cloud is a lagging indicator. By the time there is cloud confirmation, much of the move may have already occurred.
3. Optimizing stop loss and take profit levels is challenging and sensitive. Suboptimal parameters may result in more losses.

### Enhancements

Some ways this strategy can be improved:

1. Combine Ichimoku with leading indicators like RSI for additional confirmation and early entry.
2. Adaptively adjust stop loss and take profit based on volatility instead of using fixed percentages.
3. Test optimal parameters across various assets and timeframes to identify best setups for the strategy.
4. Incorporate machine learning to continually optimize parameters and strategy rules based on updated data.

### Conclusion

This is a solid Ichimoku system with good trend capture and risk management features. With some enhancements, it can be an excellent addition to overall trading approaches. It works well across forex, commodities, and cryptocurrency markets, making it a recommended quantified strategy.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Tenkan-Sen Bars|
|v_input_2|26|Kijun-Sen Bars|
|v_input_3|52|Senkou-Span B Bars|
|v_input_4|26|Chikou-Span Offset|
|v_input_5|26|Senkou-Span Offset|
|v_input_6|true|Long Entry|
|v_input_7|true|Short Entry|
|v_input_8|true|Wait for Cloud Confirmation|
|v_input_9|true|Use Short Stop Loss|
|v_input_10|5|Short Stop Loss (%)|
|v_input_11|true|Use Long Stop Loss|
|v_input_12|5|Long Stop Loss (%)|
|v_input_13|true|Use Short Take Profit|
|v_input_14|20|Short Take Profit (%)|
|v_input_15|true|Use Long Take Profit|
|v_input_16|20|Long Take Profit (%)|
|v_input_17|false|Show Date Range|
|v_input_18|true|From Month|
|v_input_19|true|From Day|
|v_input_20|2020|From Year|
|v_input_21|true|Thru Month|
|v_input_22|true|Thru Day|
|v_input_23|2112|Thru Year|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-11-17 00:00:00
end: 2023-11-23 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

strategy("Ichimoku Backtester with TP and SL", overlay=true, 
     currency = currency.USD, default_qty_type = strategy.percent_of_equity, 
     default_qty_value = 95)
//@version=4

// Inputs
ts_bars = input(9, minval=1, title="Tenkan-Sen Bars")
ks_bars = input(26, minval=1, title="Kijun-Sen Bars")
ssb_bars = input(52, minval=1, title="Senkou-Span B Bars")
cs_offset = input(26, minval=1, title="Chikou-Span Offset")
ss_offset = input(26, minval=1, title="Senkou-Span Offset")
long_entry = input(true, title="Long Entry")
short_entry = input(true, title="Short Entry")

wait_for_cloud = input(true, title="Wait for Cloud Confirmation")

use_short_stop_loss = input(true, title="Use Short Stop Loss")
short_stop_loss = input(title="Short Stop Loss (%)", type=input.float, minval=0.0, step=0.1, 
     defval=5) * 0.01
use_long_stop_loss = input(true, title="Use Long Stop Loss")
long_stop_loss = input(title="Long Stop Loss (%)", type=input.float, minval=0.0, step=0.1, 
     defval=5) * 0.01
     
use_short_take_profit = input(true, title="Use Short Take Profit")
short_take_profit = input(title="Short Take Profit (%)", type=input.float, minval=0.0, step=0.1,
     defval = 20) * .01
use_long_take_profit = input(true, title="Use Long Take Profit")
long_take_profit = input(title="Long Take Profit (%)", type=input.float, minval=0.0, step=0.1,
     defval = 20) * .01

// === INPUTS ===
```