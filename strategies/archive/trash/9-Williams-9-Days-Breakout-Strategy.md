> Name

Williams 9-Day Breakout Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1e3de40bcbcc0bf8ddd.png)

[trans]


### Overview

This strategy is based on Larry Williams' 9-day breakout concept, by monitoring the direction of the 9-day moving average to determine the trend, and taking positions at breakout points to follow the trend.

### Strategy Logic

- Use 9-day Exponential Moving Average (EMA) as an indicator to judge the trend
- When the price breaks out above the EMA from below, it is judged as bullish, and a long position is taken
- When the price breaks out below the EMA from above, it is judged as bearish, and a short position is taken
- Buy signal: Opening price is lower than the 9-day EMA, closing price is higher than the 9-day EMA
- Sell signal: Opening price is higher than the 9-day EMA, closing price is lower than the 9-day EMA

Specifically:

1. Calculate the 9-day EMA
2. Check if the candle of the day satisfies the buy condition, i.e. opening price is lower than the 9-day EMA, closing price is higher than the 9-day EMA
3. If satisfied, take a long position at the closing price, with stop loss set at the previous high
4. Check if the candle of the day satisfies the sell condition, i.e. opening price is higher than the 9-day EMA, closing price is lower than the 9-day EMA
5. If satisfied, exit the previous long position, with take profit set at the previous low

The above constitutes the complete logic of buy and sell.

### Advantage Analysis

This is a relatively simple trend-following strategy with the following strengths:

1. Using EMA to judge trend direction can effectively filter out price noise
2. Taking positions at EMA breakout can timely capture trend reversals
3. Adopting previous high as stop loss and previous low as take profit can lock in trend profits
4. The trading rules are clear and simple, easy to understand and implement, suitable for beginners
5. High capital usage efficiency, no need to hold positions all the time, only short-term positions at trend breakouts

### Risks and Optimization

The strategy also has some risks and deficiencies, which can be further optimized from the following aspects:

1. The 9-day EMA period setting may not be flexible enough for different products and market conditions, adaptive EMA period can be introduced
2. Using only 9-day EMA to judge trend may be too simple, multiple time frame EMAs or other indicators can be combined
3. Transaction costs and slippage are not considered, which can significantly affect PnL in live trading
4. No stop loss and take profit ratios are set, unable to control risk reward of individual trades
5. Entry signals may oscillate multiple times, generating unnecessary small orders, filters can be added

In summary, the strategy can be improved through dynamic parameter optimization, multifactor judgement, transaction cost management, risk-reward control etc., to make the strategy more robust across different market conditions.

### Conclusion

The Williams 9-day breakout strategy is a relatively classic short-term trend-following strategy. The core idea is simple and clear, using EMA to determine trend direction, taking positions at breakout points, following the trend and managing risks. The strategy is easy to understand and implement, with high capital usage efficiency, but also has some deficiencies. We can optimize it from multiple perspectives to make the parameters more dynamic, judgement rules more rigorous, risk control more complete, thereby adapting to a wider range of market conditions and improving the stability and profitability.

||


### Overview

This strategy is based on the 9-day breakout concept of Larry Williams, by monitoring the direction of the 9-day moving average to determine the trend, and taking positions at breakout points to follow the trend.

### Strategy Logic

- Use 9-day EMA as an indicator to judge the trend
- When price breaks out above EMA from below, it is judged as bullish, and long position is taken
- When price breaks out below EMA from above, it is judged as bearish, and short position is taken
- Buy signal: Opening price is lower than 9-day EMA, closing price is higher than 9-day EMA
- Sell signal: Opening price is higher than 9-day EMA, closing price is lower than 9-day EMA

Specifically:

1. Calculate the 9-day EMA
2. Check if the candle of the day satisfies the buy condition, i.e. opening price is lower than 9-day EMA, closing price is higher than 9-day EMA
3. If satisfied, take long position at closing price, with stop loss set at previous high
4. Check if the candle of the day satisfies the sell condition, i.e. opening price is higher than 9-day EMA, closing price is lower than 9-day EMA
5. If satisfied, exit the previous long position, with take profit set at previous low

The above constitutes the complete logic of buy and sell.

### Advantage Analysis

This is a relatively simple trend-following strategy with the following strengths:

1. Using EMA to judge trend direction can effectively filter out price noise
2. Taking positions at EMA breakout can timely capture trend reversals
3. Adopting previous high as stop loss and previous low as take profit can lock in trend profits
4. The trading rules are clear and simple, easy to understand and implement, suitable for beginners
5. High capital usage efficiency, no need to hold positions all the time, only short-term positions at trend breakouts

### Risks and Optimization

The strategy also has some risks and deficiencies, which can be further optimized from the following aspects:

1. EMA period setting as 9 days may not be flexible enough for different products and market conditions, adaptive EMA period can be introduced
2. Using only 9-day EMA to judge trend may be too simple, multiple time frame EMAs or other indicators can be combined
3. Transaction costs and slippage are not considered, which can significantly affect PnL in live trading
4. No stop loss and take profit ratios are set, unable to control risk reward of individual trades
5. Entry signals may oscillate multiple times, generating unnecessary small orders, filters can be added

In summary, the strategy can be improved through dynamic parameter optimization, multifactor judgement, transaction cost management, risk-reward control etc., to make the strategy more robust across different market conditions.

### Conclusion

The Williams 9-day breakout strategy is a relatively classic short-term trend-following strategy, with a simple and clear core idea. It uses EMA to determine trend direction, takes positions at breakout points, follows the trend, and manages risks. The strategy is easy to understand and implement, with high capital usage efficiency, but also has some deficiencies. We can optimize it from multiple perspectives to make the parameters more dynamic, judgement rules more rigorous, risk control more complete, thereby adapting to a wider range of market conditions and improving the stability and profitability.

||


### Source (PineScript)

```pinescript
/*backtest
start: 2023-09-16 00:00:00
end: 2023-10-16 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Larry Williams Teste2", overlay=true)

// Window of time
start     = timestamp(2019, 00, 00, 00, 00)  // backtest start window
finish    = timestamp(2019, 12, 31, 23, 59)  // backtest finish window
window()  => true  // create function "within window of time"

ema9 = ema(close, 9)  // 9-period EMA

// Buy conditions
c1 = (open < ema9 and close > ema9)  // open below EMA9 and close above EMA9

if (window())
    if (c1)
        strategy.entry("Compra", true, stop=high)  // Place stop-buy order at the previous high
    else
        strategy.cancel("Compra")  // Cancel order if the next candle does not "hit"

// Sell conditions
v1 = (open > ema9 and close < ema9)  // open above EMA9 and close below EMA9

if (window())
    if (v1)
        strategy.exit("Venda", from_entry="Compra", stop=low)  // Exit from entry with stop-loss at previous low
    else
        strategy.cancel("Venda")  // Cancel order if the next candle does not "hit"
```

> Detail

https://www.fmz.com/strategy/429463

> Last Modified

2023-10-17 13:51:15