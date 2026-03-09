> Name

Momentum-Breakout-Trading-Strategy-Based-on-Price-Breakout-and-Mean-Reversion

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1899c7f9f996e07acc5.png)
[trans]

## Overview

This strategy combines price breakout and mean reversion to determine and track trends. It uses multiple indicators for confirmation and filtration, achieving precise trading signals through strict entry and exit mechanisms. The strategy is suitable for short-term and medium-term trading, by locking in small profits through rigorous entry and exit rules.

## Strategy Logic

1. Use HMA as the baseline to determine the price trend direction. Price above HMA indicates an upward trend, price below HMA indicates a downward trend.

2. SSL Channel serves as the confirmation indicator by confirming the trend based on the price relationship with the channel direction.

3. TDFI as the momentum indicator to gauge the strength. Trade entry is allowed only when momentum reaches a certain level.

4. RVI indicator serves as the exit indicator. Trend exhaustion is judged when RVI line shape changes.

5. ATR calculates stop loss and take profit.

6. Entry conditions: Price breaks through baseline, SSL channel direction aligns with price, TDFI reaches threshold.

7. Exit conditions: RVI line shape change, price break back through baseline and SSL channel.

## Advantage Analysis

1. Combining multiple indicators helps filter out false breakouts effectively.

2. Strict entry conditions and stop loss exit control single loss.

3. Take full advantage of price trends to obtain excess returns.

4. Large optimization space for indicator parameters, adaptable to different products and timeframes.

## Risk Analysis

1. Unable to identify trend reversal, risks of overtrading by chasing highs/lows.

2. Short-term operations, risks of overtrading.

3. Subjective influence in stop loss level setting, may be too loose or too tight.

4. Parameter settings不当可能导致交易频繁或不足。

## Optimization Directions

1. Add trend judgment indicators to ensure accuracy in determining trend direction.

2. Incorporate reversal signal indicators to reduce the probability of chasing highs/lows.

3. Consider dynamic adjustment of ATR to ATR Trailing Stop for more dynamic stop loss.

4. Test different MA systems to find parameter optimization directions.

5. Optimize parameters for specific trading products.

## Conclusion

This strategy achieves precision in trading signals through multi-indicator confirmation. Strict stop loss mechanisms control single loss. It suits people familiar with technical analysis operations. Parameters can be adjusted for different market cycles. Overall, the strategy has positive expected benefit and return, but risks of incorrect trend judgment and overtrading should be noted.

||


## Overview

This strategy combines price breakout and mean reversion to determine and track trends. It uses multiple indicators for confirmation and filtration, achieving precise trading signals through strict entry and exit mechanisms. The strategy is suitable for short-term and medium-term trading, by locking in small profits through rigorous entry and exit rules.

## Strategy Logic

1. Use HMA as the baseline to determine the price trend direction. Price above HMA indicates an upward trend, price below HMA indicates a downward trend.

2. SSL Channel serves as the confirmation indicator by confirming the trend based on the price relationship with the channel direction.

3. TDFI as the momentum indicator to gauge the strength. Trade entry is allowed only when momentum reaches a certain level.

4. RVI indicator serves as the exit indicator. Trend exhaustion is judged when RVI line shape changes.

5. ATR calculates stop loss and take profit.

6. Entry conditions: Price breaks through baseline, SSL channel direction aligns with price, TDFI reaches threshold.

7. Exit conditions: RVI line shape change, price break back through baseline and SSL channel.

## Advantage Analysis

1. Combining multiple indicators helps filter out false breakouts effectively.

2. Strict entry conditions and stop loss exit control single loss.

3. Take full advantage of price trends to obtain excess returns.

4. Large optimization space for indicator parameters, adaptable to different products and timeframes.

## Risk Analysis

1. Unable to identify trend reversal, risks of overtrading by chasing highs/lows.

2. Short-term operations, risks of overtrading.

3. Subjective influence in stop loss level setting, may be too loose or too tight.

4. Parameter settings不当可能导致交易频繁或不足。

## Optimization Directions

1. Add trend judgment indicators to ensure accuracy in determining trend direction.

2. Incorporate reversal signal indicators to reduce the probability of chasing highs/lows.

3. Consider dynamic adjustment of ATR to ATR Trailing Stop for more dynamic stop loss.

4. Test different MA systems to find parameter optimization directions.

5. Optimize parameters for specific trading products.

## Conclusion

This strategy achieves precision in trading signals through multi-indicator confirmation. Strict stop loss mechanisms control single loss. It suits people familiar with technical analysis operations. Parameters can be adjusted for different market cycles. Overall, the strategy has positive expected benefit and return, but risks of incorrect trend judgment and overtrading should be noted.

||


## Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|ATR Length|
|v_input_2|1.5|SL|
|v_input_3|true|TP|
|v_input_4|20|hmaslowlength|
|v_input_5_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|10|SSL Period|
|v_input_7|4|TDFI Lookback|
|v_input_8|0.05|Filter High|
|v_input_9|-0.05|Filter Low|
|v_input_10|4|RVI Length|


> Source (PineScript)

``` pinescript
//@version=3
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Designed per No Nonsense Forex VP rules
//Made to be as modular as possible, so we can swap the indicators in and out.
//Originated from causecelebre
//Tried to put in as much VP rules as possible

///////////////////////////////////////////////////
//Rules Implemented:
///////////////////////////////////////////////////
// - SL 1.5 x ATR
// - TP 1 x ATR
//
// - Entry conditions
//// - Entry within 1 candles of baseline + 1 x confirmation + volume
//// - Entry only if baseline is < 1 x ATR
// - Exit conditions
//// - Exit on exit indicator or when baseline or confirmation flip 

///////////////////////////////////////////////////
//Trades entries
///////////////////////////////////////////////////
// - First entry L1 or S1 with standard SL and TP
// - Second entry L2 or S2 with standard SL and exit upon the exit conditions

///////////////////////////////////////////////////
//Included Indicators and settings
///////////////////////////////////////////////////
// - Baseline = HMA 20
// - Confirmtion = SSL 10
// - Volume = TDFI 4
// - Exit = RVI 4

///////////////////////////////////////////////////
//Credits
// Strategy causecelebre https://www.tradingview.com/u/causecelebre/
// TDFI causecelebre https://www.tradingview.com/u/causecelebre/
// SSL Channel ErwinBeckers https://www.tradingview.com/u/ErwinBeckers/
////////////////////////////////////////////////////////////////////
```