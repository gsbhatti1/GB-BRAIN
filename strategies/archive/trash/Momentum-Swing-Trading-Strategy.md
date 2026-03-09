> Name

Momentum-Swing-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/10e3464b94e8c9296b2.png)
[trans]
## Overview

This is a daily interval swing trading strategy based on momentum techniques using ATR Stops. It was created by Kory Hoang from Stably.

The strategy identifies trend direction using momentum indicators and sets stop loss lines based on ATR to implement low-buy-high-sell swing trading.

## Strategy Logic

The code first sets the backtesting time range.

Then in the indicator section, the following indicators are calculated:

- `atr()`: calculate ATR for stop loss;
- `max_/min_`: highest/lowest price of the previous bar;
- `is_uptrend`: judge if it's in an uptrend;
- `vstop`: stop loss line;

The main logic to judge trend is:

If `close` is higher than the previous downside stop loss line `vstop`, it's judged as an uptrend; if `close` is lower than the previous upside stop loss line `vstop`, it's judged as a downtrend.

When trend changes, adjust the stop loss line position.

Specifically, in an uptrend, the stop loss line is set to the highest price of the previous bar minus the ATR value; in a downtrend, the stop loss line is set to the lowest price of the previous bar plus the ATR value.

This realizes trend following stop loss.

In the trading rules section, open long/short positions when price breaks the stop loss line.

## Advantage Analysis

The advantages of this strategy:

1. Judge trend direction using momentum techniques, timely catch turning points and avoid false breakouts.
2. ATR stop loss traces highest/lowest price, can control risk well.
3. Simple and clear strategy logic, easy to understand and implement.
4. Can make low-buy-high-sell trades between swings.

## Risk Analysis

There are also some risks:

1. Improper ATR parameter may cause stop loss to be too loose or too tight.
2. Fierce whipsaws may happen in ranging trends, causing consecutive stop loss.
3. High trading frequency, higher commissions.

Some optimizations:

1. Test different ATR parameters to find the optimal.
2. Optimize stop loss combining volatility metrics on top of ATR.
3. Add trend filter to avoid unnecessary trades during choppy markets.

## Optimization Directions

Some directions to optimize this strategy:

1. Test different ATR parameters to find the optimal. Backtest multiple parameter sets and evaluate return/risk ratio.
2. Optimize stop loss combining volatility metrics on top of ATR. Add volatility metrics, relax stop loss properly during periods of increasing volatility.
3. Add trend filter to avoid trades during choppy market. Add trend judgment indicators, only trade when trend is clear.
4. Add position sizing mechanism. Adjust position size based on account utilization ratio, consecutive stop loss times etc.
5. Add overnight gap risk control. Actively cut loss before market close to avoid overnight gap risk.

## Conclusion

As a basic daily swing trading strategy, the overall logic is clear. It judges trend with momentum techniques and utilizes ATR for trailing stop loss, effectively controlling risk.

Still large room for optimization, can improve from aspects like trend judgment, stop loss method, position sizing etc. to make the strategy more practical. Overall this strategy provides a solid framework for quantitative trading.

[/trans]

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Month|
|v_input_2|true|From Day|
|v_input_3|2010|From Year|
|v_input_4|12|To Month|
|v_input_5|31|To Day|
|v_input_6|2020|To Year|
|v_input_7|3|length|
|v_input_8|true|mult|
|v_input_9|true|Strategy Direction|

> Source (PineScript)

```pinescript
//@version=2
strategy("BTC Swinger", overlay=true, commission_value=0.25, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

/////////////////////////////////////////////////////////////
//START - SET DATE RANGE

// === BACKTEST RANGE ===
FromMonth = input(defval=1, title="From Month", minval=1)
FromDay   = input(defval=1, title="From Day", minval=1)
FromYear  = input(defval=2010, title="From Year")
ToMonth   = input(defval=12, title="To Month", minval=1)
ToDay     = input(defval=31, title="To Day", minval=1)
ToYear    = input(defval=2020, title="To Year")

startDate = time > timestamp(FromYear, FromMonth, FromDay, 1, 1)
endDate = time < timestamp(ToYear, ToMonth, ToDay, 23, 59)
withinTimeRange = true

/////////////////////////////////////////////////////////////
//END - SET DATE RANGE

/////////////////////
```