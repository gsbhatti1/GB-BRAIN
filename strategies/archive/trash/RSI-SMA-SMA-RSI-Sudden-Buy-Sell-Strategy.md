> Name

SMA-RSI & Sudden Buy and Sell Strategy

> Author

ChaoZhang

> Strategy Description


![IMG](https://www.fmz.com/upload/asset/950d769e62fbc99660.png)
 [trans]

## Overview

This strategy mainly uses the average value of RSI and sudden price changes to identify market trends and reversal points. The core idea is to consider establishing positions when RSI shows overbought or oversold conditions, and look for reversal opportunities when there are sudden price changes. EMA is also used as a filter.

## Principles

1. Calculate the SMA of RSI. When RSI SMA crosses above 60 or falls below 40, it is considered overbought or oversold, and reverse positions will be considered.

2. When the change of RSI exceeds a certain value, it is regarded as a sudden change. Combined with the actual close price verification, it serves as a signal to establish reverse position.

3. Use multiple EMAs for filtering. Only when price crosses above shorter period EMA, long position will be considered. Only when price falls below shorter period EMA, short position will be considered.

4. By combining the use of RSI average, sudden changes and EMA filtering, better entry points can be identified.

## Advantage Analysis

1. Using RSI average can accurately judge overbought or oversold conditions, which is conducive to capturing reversal opportunities.

2. Sudden changes often signify shifts in price trend and direction, using this signal can improve the timeliness of entries.

3. Multi-level EMA filtering can further avoid false signals and reduce unnecessary losses.

4. The combination of multiple parameters as decision criteria can enhance the stability and reliability of the strategy.

## Risks and Mitigations

1. RSI performance may be unstable, and SMA hit rate may be low. RSI parameters can be optimized or other indicators can replace it.

2. Sudden changes could just be short-term fluctuations rather than true reversals. Increase sensing cycle length to improve judgment accuracy.

3. There is lag in EMA direction filtering. Test shorter period EMAs to improve sensitivity.

4. In general, this strategy is quite sensitive to parameter tuning. Careful tests are needed to find optimum parameter combinations. Use stop loss to control risks.

## Optimization Suggestions

1. Test other indicators like ADX, MACD combined with RSI to find better entry points.

2. Increase machine learning algorithms to judge the authenticity and stability of sudden buy/sell signals.

3. Further enhance EMA direction filtering such as using composite judgment of different period EMAs.

4. Add adaptive stop loss strategy to dynamically adjust stop loss range based on market volatility.

5. Continue parameter optimization to find optimum parameter combinations. Evaluation criteria could be Sharpe Ratio etc.


## Conclusion

This strategy firstly uses RSI average to determine overbought or oversold conditions. Reverse positions are then established when sudden changes occur. EMA is also used as an auxiliary filter. With proper parameter settings, this strategy can effectively determine market trend shifts. Overall speaking, it has good stability and practical value. There is still room for further improvement, requiring persistent testing and optimization.

[/trans]

> Strategy Arguments


| Argument | Default | Description |
| --- | --- | --- |
| v_input_1 | 14 | length |
| v_input_2 | 10 | inst_length |
| v_input_3 | 10 | bars |
| v_input_int_1 | 20 | lookbackno2 |
| v_input_int_2 | 20 | input_ema20 |
| v_input_int_3 | 50 | input_ema50 |
| v_input_int_4 | 100 | input_ema100 |
| v_input_int_5 | 200 | input_ema200 |
| v_input_int_6 | 400 | input_ema400 |
| v_input_int_7 | 800 | input_ema800 |
| v_input_4 | 40 | over40 |
| v_input_5 | 60 | over60 |

> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © samwillington

//@version=5
strategy("sma RSI & Sudden Buy and Sell Strategy v1", overlay=true)
price = close
length = input(14)
inst_length = input(10)
var rbc = 0
var float rsiBP = 0.0
var rsc = 0
var float rsiSP = 0.0
bars = input(10)

lookbackno2 = input.int(20)
rsi_buy = 0
rsi_sell = 0

// EMA inputs
input_ema20 = input.int(20)
ema20 = ta.ema(price, input_ema20)
input_ema50 = input.int(50)
ema50 = ta.ema(price, input_ema50)
input_ema100 = input.int(100)
ema100 = ta.ema(price, input_ema100)
input_ema200 = input.int(200)
ema200 = ta.ema(price, input_ema200)
input_ema400 = input.int(400)
ema400 = ta.ema(price, input_ema400)
input_ema800 = input.int(800)
ema800 = ta.ema(price, input_ema800)

vrsi = ta.rsi(price, length)

hi2 = ta.highest(price, lookbackno2)
lo2 = ta.lowest(price, lookbackno2)

buy_diff_rsi = vrsi > over40 ? 1 : 0
sell_diff_rsi = vrsi < over60 ? 1 : 0

// TODO: complete the script
```

Please note that the PineScript is incomplete and requires additional code to fully implement the strategy. The `buy_diff_rsi` and `sell_diff_rsi` variables need further logic for determining buy/sell signals based on RSI changes, EMA crossovers, etc.