> Name

Low-Volatility-Directional-Buy-with-Profit-Taking-and-Stop-Loss

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/18ef8c3c3cbc7688a6e.png)
[trans]

### Overview

This strategy is named "Low-Volatility-Directional-Buy-with-Profit-Taking-and-Stop-Loss." It uses moving average crossovers as buy signals and combines profit taking and stop loss to lock in profits. It is suitable for low-volatility coins.

### Strategy Logic

The strategy uses three different-period moving averages: 50-period, 100-period, and 200-period. The buying logic is: when the 50-period MA crosses over the 100-period MA, and the 100-period MA crosses over the 200-period MA, go long.

This signals a breakout from low-volatility ranges and the start of a trend. The rapid rise of the 50-period MA indicates an enhancement of short-term momentum; the upward movement of the 100-period MA signifies mid-term force joining in to stabilize the uptrend.

After entry, the strategy uses profit taking and stop loss to lock in gains. Take profit is set at 8% of the entry price. Stop loss is set at 4% of the entry price. With a higher take profit over stop loss, it ensures overall profitability of the strategy.

### Advantage Analysis

The advantages of this strategy include:

1. Accurately capturing trend opportunities from low-volatility breakouts.
2. Simple and clear logic with moving averages that are easy to calculate and backtest.
3. Reasonable profit taking and stop loss settings ensure stable gains.
4. Flexible configurable parameters allow for easy optimization.

### Risk Analysis

This strategy also has some risks:

1. Incorrect breakout signals may cause losses.
2. It is difficult to close positions when markets reverse.
3. Improper take profit and stop loss parameter settings can affect profitability.

Solutions:

1. Add other indicators to filter signals and ensure the validity of breakouts.
2. Shorten the stop loss period to reduce losses from reversals.
3. Test different take profit and stop loss ratios to find the optimal parameters.

### Optimization Directions

Optimization can be made in the following areas:

1. Test different moving average periods to find the best combination.
2. Add volume indicators to confirm trend breakouts.
3. Dynamically adjust take profit and stop loss percentages.
4. Incorporate machine learning techniques to predict breakout success rates.
5. Adjust parameters based on different market conditions and coins.

In summary, this strategy has a clear overall logic, obtaining low-risk profits by configuring moving average periods and take profit/stop loss percentages. It can be flexibly applied in quantitative trading. Further optimizations can be made in areas such as entry signals and stop loss methods, combined with parameter tuning to achieve the best results.

||

### Overview  

The strategy is named "Low-Volatility-Directional-Buy-with-Profit-Taking-and-Stop-Loss." It utilizes moving average crossovers as buy signals and combines profit taking and stop loss to lock in profits. It is suitable for low-volatility coins.  

### Strategy Logic  

The strategy uses three different-period moving averages: 50-period, 100-period, and 200-period. The buying logic is: when the 50-period MA crosses over the 100-period MA, and the 100-period MA crosses over the 200-period MA, go long.  

This signals a breakout from low-volatility ranges and the start of a trend. The rapid rise of the 50-period MA indicates an enhancement of short-term momentum; the upward movement of the 100-period MA signifies mid-term force joining in to stabilize the uptrend.

After entry, the strategy uses profit taking and stop loss to lock in gains. Take profit is set at 8% of the entry price. Stop loss is set at 4% of the entry price. With a higher take profit over stop loss, it ensures overall profitability of the strategy.  

### Advantage Analysis  

The advantages of this strategy include:

1. Accurately capturing trend opportunities from low-volatility breakouts.
2. Simple and clear logic with moving averages that are easy to calculate and backtest.
3. Reasonable profit taking and stop loss settings ensure stable gains.
4. Flexible configurable parameters allow for easy optimization.

### Risk Analysis  

This strategy also has some risks:

1. Incorrect breakout signals may cause losses.
2. It is difficult to close positions when markets reverse.
3. Improper take profit and stop loss parameter settings can affect profitability.

Solutions:

1. Add other indicators to filter signals and ensure the validity of breakouts.
2. Shorten the stop loss period to reduce losses from reversals.
3. Test different take profit and stop loss ratios to find the optimal parameters.

### Optimization Directions  

Optimization can be made in the following areas:  

1. Test different moving average periods to find the best combination.
2. Add volume indicators to confirm trend breakouts.
3. Dynamically adjust take profit and stop loss percentages.
4. Incorporate machine learning techniques to predict breakout success rates.
5. Adjust parameters based on different market conditions and coins.

In summary, this strategy has a clear overall logic, obtaining low-risk profits by configuring moving average periods and take profit/stop loss percentages. It can be flexibly applied in quantitative trading. Further optimizations can be made in areas such as entry signals and stop loss methods, combined with parameter tuning to achieve the best results.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Month|
|v_input_2|10|From Day|
|v_input_3|2019|From Year|
|v_input_4|true|Thru Month|
|v_input_5|true|Thru Day|
|v_input_6|2112|Thru Year|
|v_input_7|true|Show Date Range|
|v_input_8|50|v_input_8|
|v_input_9|200|v_input_9|
|v_input_10|100|v_input_10|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-10 00:00:00
end: 2023-12-17 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(shorttitle='Low Volatility Buy w/ TP & SL (by Coinrule)', title='Low Volatility Buy w/ TP & SL', overlay=true, initial_capital = 1000, process_orders_on_close=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

// Backtest dates
fromMonth = input(defval=1, title="From Month", type=input.integer, minval=1, maxval=12)
fromDay   = input(defval=10, title="From Day", type=input.integer, minval=1, maxval=31)
fromYear  = input(defval=2019, title="From Year", type=input.integer, minval=1970)
thruMonth = input(defval=1, title="Thru Month", type=input.integer, minval=1, maxval=12)
thruDay   = input(defval=1, title="Thru Day", type=input.integer, minval=1, maxval=31)
thruYear  = input(defval=2112, title="Thru Year", type=input.integer, minval=1970)

showDate  = input(defval=true, title="Show Date Range", type=input.bool)

start     = timestamp(fromYear, fromMonth, fromDay, 00, 00)        // backtest start window
finish    = timestamp(thruYear, thruMonth, thruDay, 23, 59)        // backtest finish window
window()  => time >= start and time <= finish ? true : false       // create function "within window of time"

// MA inputs and calculations
movingaverage_fast = sma(close, input(50))
movingaverage_slow = sma(close, input(200))
movingaverage_normal= sma(close, input(100))

// Entry 
strategy.entry(id="long", long=true, when=movingaverage_slow > movingaverage_normal and movingaverage_fast > movingaverage_normal)

// Exit
longStopPrice  = strategy.position_avg_price * (1 - 0.04)
longTakeProfit = strategy.position_avg_price * (1 + 0.08)

strategy.close("long", when=close < longStopPrice or close > longTakeProfit and window())
```