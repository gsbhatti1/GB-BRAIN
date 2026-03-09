> Name

K Line Consecutive Number Bull Bear Judgment Strategy - K-Consecutive-Candles-Bull-Bear-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1e0f433500bd65b3cc4.png)

[trans]
#### Overview
This strategy determines bull or bear markets based on the number of consecutive up or down candles and makes trades accordingly. When the closing price is consecutively higher than the previous candle's close for a specified number of times, it enters a long position; when the closing price is consecutively lower than the previous candle's close for a specified number of times, it enters a short position. Stop loss and take profit are set, and a trailing stop mechanism is introduced to protect profits.

#### Strategy Principle
1. Record the number of times the consecutive bullish and bearish conditions are met. If the close is higher than the previous candle, the bullish count increases by 1 and the bearish count resets to 0; if the close is lower, the bearish count increases by 1 and the bullish count resets to 0; otherwise, both counts reset to 0.
2. When the bullish count reaches the specified number k, enter a long position with stop loss and take profit.
3. For long positions, record the highest price after entry. When the highest price exceeds the entry price by iTGT minimum price variation units and the close pulls back below the highest price by iPcnt%, close the position.
4. When the bearish count reaches the specified number k2, enter a short position with stop loss and take profit.
5. For short positions, record the lowest price after entry. When the lowest price is lower than the entry price by iTGT minimum price variation units and the close rebounds above the lowest price by iPcnt%, close the position.

#### Strategy Advantages
1. Simple and easy to understand, making trading decisions based on the continuity of candles with clear logic.
2. Introduces a trailing stop mechanism to actively protect profits after the price moves a certain distance in the favorable direction.
3. Setting stop loss and take profit can effectively control risks and lock in profits.
4. Adjustable parameters to suit different markets and trading styles.

#### Strategy Risks
1. In choppy markets, frequent opening and closing of positions may lead to large slippage costs.
2. The judgment of consecutive candle numbers is affected by market noise, which may result in frequent signals.
3. Fixed stop loss and take profit levels may not adapt to changes in market volatility.

#### Strategy Optimization Directions
1. Introduce more technical indicators, such as moving averages and volatility, to assist in judging the strength and direction of trends.
2. Optimize the trigger conditions for the trailing stop, such as adjusting the pullback percentage based on ATR.
3. Adopt more dynamic stop loss and take profit methods, such as trailing stops and stepped take profits.
4. Optimize parameters to find the optimal combination for different markets and instruments.

#### Summary
This strategy captures bull and bear trends through the continuity of candles while setting stop loss and take profit to control risks. The introduction of a trailing stop can better protect profits. However, it may generate frequent signals in choppy markets, requiring further optimization of signal reliability. In addition, the setting of stop loss and take profit can be more flexible to adapt to dynamic market changes. Overall, the strategy has a simple and clear idea, suitable for trending markets, but there is still room for optimization.

||

#### Overview
This strategy determines bull or bear markets based on the number of consecutive up or down candles and makes trades accordingly. When the closing price is consecutively higher than the previous candle's close for a specified number of times, it enters a long position; when the closing price is consecutively lower than the previous candle's close for a specified number of times, it enters a short position. Stop loss and take profit are set, and a trailing stop mechanism is introduced to protect profits.

#### Strategy Principle
1. Record the number of times the consecutive bullish and bearish conditions are met. If the close is higher than the previous candle, the bullish count increases by 1 and the bearish count resets to 0; if the close is lower, the bearish count increases by 1 and the bullish count resets to 0; otherwise, both counts reset to 0.
2. When the bullish count reaches the specified number k, enter a long position with stop loss and take profit.
3. For long positions, record the highest price after entry. When the highest price exceeds the entry price by iTGT minimum price variation units and the close pulls back below the highest price by iPcnt%, close the position.
4. When the bearish count reaches the specified number k2, enter a short position with stop loss and take profit.
5. For short positions, record the lowest price after entry. When the lowest price is lower than the entry price by iTGT minimum price variation units and the close rebounds above the lowest price by iPcnt%, close the position.

#### Strategy Advantages
1. Simple and easy to understand, making trading decisions based on the continuity of candles with clear logic.
2. Introduces a trailing stop mechanism to actively protect profits after the price moves a certain distance in the favorable direction.
3. Setting stop loss and take profit can effectively control risks and lock in profits.
4. Adjustable parameters to suit different markets and trading styles.

#### Strategy Risks
1. In choppy markets, frequent opening and closing of positions may lead to large slippage costs.
2. The judgment of consecutive candle numbers is affected by market noise, which may result in frequent signals.
3. Fixed stop loss and take profit levels may not adapt to changes in market volatility.

#### Strategy Optimization Directions
1. Introduce more technical indicators, such as moving averages and volatility, to assist in judging the strength and direction of trends.
2. Optimize the trigger conditions for the trailing stop, such as adjusting the pullback percentage based on ATR.
3. Adopt more dynamic stop loss and take profit methods, such as trailing stops and stepped take profits.
4. Optimize parameters to find the optimal combination for different markets and instruments.

#### Summary
This strategy captures bull and bear trends through the continuity of candles while setting stop loss and take profit to control risks. The introduction of a trailing stop can better protect profits. However, it may generate frequent signals in choppy markets, requiring further optimization of signal reliability. In addition, the setting of stop loss and take profit can be more flexible to adapt to dynamic market changes. Overall, the strategy has a simple and clear idea, suitable for trending markets, but there is still room for optimization.

||

```pinescript
//@version=5
strategy("K Consecutive Candles 數來寶V2", max_bars_back=300, overlay=true)

// Define user inputs
k = input.int(3, title="Number of Consecutive Candles for Long", minval=1)
k2 = input.int(3, title="Number of Consecutive Candles for Short", minval=1)
stopLossTicks = input.int(500, title="Stop Loss (Ticks)")
takeProfitTicks = input.int(500, title="Take Profit (Ticks)")
iTGT = input.int(200, "iTGT")  // Trailing Stop Distance
iPcnt = input.int(50, "iPcnt")  // Trailing Stop Percentage

var float TrailValue = 0
var float TrailExit = 0
var float vMP = 0

BarsSinceEntry = ta.barssince(strategy.position_size == 0)

vMP := strategy.position_size

// Create an array to hold key-value pairs
addArrayData(type, value) =>
    alert_array = array.new_string()
    array.push(alert_array, '"timenow": ' + str.tostring(timenow))
    array.push(alert_array, '"seqNum": ' + str.tostring(value))
    array.push(alert_array, '"type": "' + type + '"')
    alertstring = '{' + array.join(alert_array, ', ') + '}'

// Define condition variables
var int countLong = 0  // Record the number of consecutive bullish conditions met
var int countShort = 0 // Record the number of consecutive bearish conditions met

// Calculate the number of consecutive greater or less than the previous close price
if close > close[1]
    countLong += 1
    countShort := 0  // Reset bearish count
else if close < close[1]
    countShort += 1
    countLong := 0  // Reset