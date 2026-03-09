> Name

Momentum Breakout Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1bbb73a5550072804dc.png)
[trans]
### Overview

This strategy calculates EMA, MACD, and single-day gains to comprehensively determine market breakout signals, achieving a momentum trading strategy of buying low and selling high.

### Strategy Principle

When the fast EMA line crosses over the slow EMA line, it indicates an upward market trend and generates a buy signal. When the MACD difference crosses above the 0 axis, it also generates a buy signal, allowing for long positions to be opened.

Additionally, if the closing price of a single day increases by more than 10% compared to the opening price, a buy signal is also generated to chase the breakout trend.

After opening positions, if the price drops by more than 10%, a stop loss is triggered. If the profit reaches 45%, a take profit is triggered.

### Advantage Analysis

This is a typical trend-following strategy that can capture the uptrend after a strong momentum breakout, with significant profit potential. The main advantages are:

1. EMA lines are used to determine trends, avoiding incorrect entry in consolidation markets.
2. MACD ensures more reliable buy signals.
3. Single-day gain condition can capture trend outbreaks.
4. Reasonable stop loss and take profit settings effectively control risks.

### Risk Analysis

Despite a well-designed strategy, certain risks still need to be managed:

1. Improper breakout signal judgment may result in short losses.
2. Market rebound may also generate false signals.
3. Oversized stop loss setting increases the risk of loss.
4. Insufficient follow-up trend after the breakout may result in insufficient profit.

To mitigate these risks, consider optimizing the moving stop loss strategy or incorporating other indicators like volume for signal filtering.

### Optimization Directions

There is still room for further optimization:

1. Add volume indicators to ensure sufficient trading volume supporting the trend.
2. Optimize MACD parameters to improve indicator sensitivity.
3. Test different combinations of EMA periods.
4. Implement an adaptive stop loss mechanism.
5. Optimize take profit points for more efficient cash management.

By fine-tuning parameters and combining indicators, the stability and profitability of this strategy can be significantly improved.

### Conclusion

In summary, this strategy is simple and practical with significant profit potential. By judging market breakout points, it can effectively capture uptrends, and the drawdown control is also reasonable. In future optimization, continuously improving parameter adjustments and stop loss/take profit design can make it a worthwhile long-term quantitative trading strategy.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|5|fastLength|
|v_input_2|12|slowLength|
|v_input_3|50|baseLength|
|v_input_4|9|MACDLength|
|v_input_5|12|MACDfast|
|v_input_6|26|MACDslow|
|v_input_7|10|Gain %|
|v_input_8|10|Stop Loss %|
|v_input_9|45|Profit %|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-11 00:00:00
end: 2024-01-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Alt Coins", overlay=true)

// Simple Alt Coin Trading Strategy //
// by @ShanghaiCrypto //

////EMA////
fastLength = input(5)
slowLength = input(12)
baseLength = input(50)
price = close

emafast = ema(price, fastLength)
emaslow = ema(price, slowLength)
emabase = ema(price, baseLength)

///MACD////
MACDLength = input(9)
MACDfast = input(12)
MACDslow = input(26)
MACD = ema(close, MACDfast) - ema(close, MACDslow)
aMACD = ema(MACD, MACDLength)
delta = MACD - aMACD

////PUMP////
OneCandleIncrease = input(10, title='Gain %')
pump = OneCandleIncrease/100

////Profit Capture and Stop Loss//////
stop = input(10.0, title='Stop Loss %', type=float)/100
profit = input(45.0, title='Profit %', type=float)/100
stop_level = strategy.position_avg_price * (1 - stop)
take_level = strategy.position_avg_price * (1 + profit)

////Entries/////
if crossover(emafast, emaslow)
    strategy.entry("Cross", strategy.long, comment="BUY")

if (crossover(delta, 0))
    strategy.entry("MACD", strategy.long, comment="BUY")
    
if close > (open + open*pump)
    strategy.entry("Pump", strategy.long, comment="BUY")

/////Exits/////
strategy.exit("SELL","Cross", stop=stop_level, limit=take_level)
strategy.exit("SELL","MACD", stop=stop_level, limit=take_level)
strategy.exit("SELL","Pump", stop=stop_level, limit=take_level)

////Plots////
plot(emafast, color=green)
plot(emaslow, color=red)
plot(emabase, color=yellow)
plot(take_level, color=blue)
plot(stop_level, color=orange)
```

> Detail

https://www.fmz.com/strategy/439229

> Last Modified

2024-01-18 15:17:11