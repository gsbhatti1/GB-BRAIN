> Name

RSI/WMA Trend Tracking Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1334ca2ef7f1a4f65bf.png)
 [trans]
## Overview

This strategy is named "RSI/WMA Trend Tracking Strategy." It integrates the advantages of the Relative Strength Index (RSI) and the Weighted Moving Average (WMA) indicators to determine overbought and oversold conditions and price trend direction, achieving effective tracking of price trends.

## Strategy Principle

The core idea is using RSI to identify overbought and oversold conditions. When RSI falls below the oversold line, it indicates oversold status, and long positions can be opened. When RSI rises above the overbought line while long positions are open, it presents a good opportunity to close long positions. Additionally, WMA is used to measure price trend. An upward crossover of price and WMA indicates an uptrend, while a downward crossover indicates a downtrend. By combining the judgment of overbought/oversold and price trend, price trends can be effectively tracked—buy at relative lows and sell at relative highs.

Specifically, the trading logic is:
1. Enter long when RSI falls below the oversold line and set a take profit order.
2. Close long when RSI rises above the overbought line while holding long positions.
3. Cancel the take profit order when price crosses above WMA.
4. Close long when price crosses below WMA while holding long positions.

This logic allows you to track the uptrend at relative lows and the downtrend at relative highs, capturing part of the price move.

## Advantages

The main advantages are:
1. Utilize both RSI and WMA for better trend and overbought/oversold analysis.
2. Enter at relatively high/low levels by tracking overbought/oversold areas.
3. Take profits quickly by setting exit orders, capturing parts of the price move.
4. Simple and easy-to-understand logic, easy to adjust parameters.
5. Allow both long and short, adaptable to all market conditions.

## Risks

There are some risks to note:
1. Lagging issues of RSI and WMA may lead to delayed signals.
2. Take profit orders may get stopped out prematurely.
3. Parameters require constant optimization and tuning, such as overbought/oversold levels.
4. Significant whipsaw may cause large losses.

The risks can be mitigated by incorporating stop loss, parameter tuning through optimization, etc.

## Improvement Areas

The strategy can be further improved in the following areas:
1. Incorporate stop loss alongside take profits.
2. Optimize parameters like RSI/WMA periods through backtesting and paper trading.
3. Introduce position sizing for better risk management.
4. Combine more indicators like MACD, KD to form indicator combos.
5. Utilize machine learning to auto-tune parameters for better performance.

## Conclusion

This strategy combines RSI and WMA to identify overbought and oversold levels and spot trend reversals, automatically tracking price trends and capturing part of the profits. There is good room for improvement by introducing more features, position sizing, machine learning, etc. Overall, it is a simple trend tracking strategy worth exploring.

||

## Overview

The strategy is named "RSI/WMA Trend Tracking Strategy". It leverages the advantages of both Relative Strength Index (RSI) and Weighted Moving Average (WMA) to determine overbought and oversold conditions and price trend direction, thus effectively tracking price trends.

## Strategy Principle

The core idea is using RSI to identify overbought and oversold conditions. When RSI falls below the oversold line, it indicates oversold status, and long positions can be opened. When RSI rises above the overbought line while long positions are open, it presents a good opportunity to close long positions. Additionally, WMA is used to measure price trend. An upward crossover of price and WMA indicates an uptrend, while a downward crossover indicates a downtrend. By combining the judgment of overbought/oversold and price trend, price trends can be effectively tracked—buy at relative lows and sell at relative highs.

Specifically, the trading logic is:
1. Enter long when RSI falls below the oversold line and set a take profit order.
2. Close long when RSI rises above the overbought line while holding long positions.
3. Cancel the take profit order when price crosses above WMA.
4. Close long when price crosses below WMA while holding long positions.

This logic allows you to track the uptrend at relative lows and the downtrend at relative highs, capturing part of the price move.

## Advantages

The main advantages are:
1. Utilize both RSI and WMA for better trend and overbought/oversold analysis.
2. Enter at relatively high/low levels by tracking overbought/oversold areas.
3. Take profits quickly by setting exit orders, capturing parts of the price move.
4. Simple and easy-to-understand logic, easy to adjust parameters.
5. Allow both long and short, adaptable to all market conditions.

## Risks

There are some risks to note:
1. Lagging issues of RSI and WMA may lead to delayed signals.
2. Take profit orders may get stopped out prematurely.
3. Parameters require constant optimization and tuning, such as overbought/oversold levels.
4. Significant whipsaw may cause large losses.

The risks can be mitigated by incorporating stop loss, parameter tuning through optimization, etc.

## Improvement Areas

The strategy can be further improved in the following areas:
1. Incorporate stop loss alongside take profits.
2. Optimize parameters like RSI/WMA periods through backtesting and paper trading.
3. Introduce position sizing for better risk management.
4. Combine more indicators like MACD, KD to form indicator combos.
5. Utilize machine learning to auto-tune parameters for better performance.

## Conclusion

This strategy combines RSI and WMA to identify overbought and oversold levels and spot trend reversals, automatically tracking price trends and capturing part of the profits. There is good room for improvement by introducing more features, position sizing, machine learning, etc. Overall, it is a simple trend tracking strategy worth exploring.

||

## Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2|length|
|v_input_2|10|overSold|
|v_input_3|90|overBought|
|v_input_4|50|WMA Length|
|v_input_5|true|Enable Long Trades|
|v_input_6|true|Enable Long Exit|
|v_input_7|false|Enable Short Trades|
|v_input_8|false|Enable Short Exit|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-11 06:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//Lets connect on LinkedIn (https://www.linkedin.com/in/lets-grow-with-quality/)
//
//I use my indicator it in real life with a zero commision broker on S&P500 Daily.
//Best performance when used with S&P500, long only and pyramiding on daily timeframe.
//
//Please.. still use your brain for entries and exits: higher timeframes, market structure, trend ... 
//If you obviously can see, like when corona started, that cubic tons of selling volume is going to punch the markets, wait until selling climax is over and so on..

strategy("RSI/WMA Strategy", overlay=true)

length = input(2)
overSold = input(10)
overBought = input(90)
wmaLength = input(50, title="WMA Length")

enableLongTrades = input(true, title="Enable Long Trades")
longExit = input(true, title="Enable Long Exit")
shortTrades = input(false, title="Enable Short Trades")
shortExit = input(false, title="Enable Short Exit")

// Calculate RSI
rsi = ta.rsi(close, length)

// Calculate WMA
wma = ta.wma(close, wmaLength)

// Determine long entry
longEntry = ta.crossover(rsi, overSold)

// Determine long exit
longExitCondition = ta.crossunder(rsi, overBought)

// Determine short entry and exit
shortEntry = ta.crossunder(rsi, overBought)
shortExitCondition = ta.crossunder(rsi, overSold)

// Plot RSI and WMA
plot(rsi, color=color.blue, title="RSI")
plot(wma, color=color.red, title="WMA")

// Handle long trades
if (longEntry and enableLongTrades)
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longExitCondition)

// Handle short trades
if (shortEntry and shortTrades)
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortExitCondition)

// Handle long exit
if (longExit and strategy.opentrades > 0)
    strategy.close("Long", stop=longExitCondition)

// Handle short exit
if (shortExit and strategy.opentrades > 0)
    strategy.close("Short", stop=shortExitCondition)
```