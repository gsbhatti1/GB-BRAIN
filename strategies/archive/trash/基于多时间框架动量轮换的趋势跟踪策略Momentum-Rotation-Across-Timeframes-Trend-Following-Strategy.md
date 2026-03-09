> Name

Momentum-Rotation-Across-Timeframes-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/380af997631d45e706.png)
[trans]

## Overview

This strategy uses a combination of moving averages across timeframes to identify trend rotations on the hourly, daily, and weekly charts. It enables low-risk trend following trading. The strategy is flexible, simple to implement, and highly capital efficient, making it suitable for medium to long-term trend traders.

## Trading Logic

The strategy employs 5-day, 20-day, and 40-day moving averages to determine the alignment of trends across different timeframes. Based on the consistency between larger and smaller timeframes, it identifies bullish and bearish cycles.

Specifically, the crossing of the 5-day fast MA above the 20-day medium MA indicates a short-term uptrend. The crossing of the 20-day medium MA above the 40-day slow MA signals a medium-term uptrend. When the fast, medium, and slow MAs are positively aligned (5-day > 20-day > 40-day), it is a bull cycle. When they are negatively aligned (5-day < 20-day < 40-day), it is a bear cycle.

By determining direction from the larger cycles and confirming strength on the smaller cycles, this strategy opens positions only when the major trend and minor momentum align. This effectively avoids false breakouts and achieves high win rate.

The strategy also utilizes ATR trailing stops to control single trade risks and further improve profitability.

## Advantages

- Flexible configurations to suit different instruments and trading styles

- Simple to implement even for beginner traders

- High capital efficiency to maximize leverage

- Effective risk control to avoid significant losses

- Strong trend following ability for sustained profits

- High win rate due to robust signals and fewer whipsaws

## Risks and Improvements

- MA crossovers may lag and cause late trend detection

- Single candle strength detection could trigger premature entry, relax condition

- Fixed ATR stop loss, optimize to dynamic stops

- Consider adding supplementary filters like volume

- Explore different MA parameters for optimization

## Conclusion

This strategy integrates multiple timeframe analysis and risk management for low-risk trend following trading. By adjusting parameters, it can be adapted to different instruments to suit trend traders. Compared to single timeframe systems, it makes more robust trading decisions and generates higher efficiency signals. In conclusion, this strategy has good market adaptiveness and development potential.


## Overview

This strategy uses a combination of moving averages across timeframes to identify trend rotations on the hourly, daily, and weekly charts. It enables low-risk trend following trading. The strategy is flexible, simple to implement, and highly capital efficient, making it suitable for medium to long-term trend traders.

## Trading Logic

The strategy employs 5-day, 20-day, and 40-day moving averages to determine the alignment of trends across different timeframes. Based on the consistency between larger and smaller timeframes, it identifies bullish and bearish cycles.

Specifically, the crossing of the 5-day fast MA above the 20-day medium MA indicates a short-term uptrend. The crossing of the 20-day medium MA above the 40-day slow MA signals a medium-term uptrend. When the fast, medium, and slow MAs are positively aligned (5-day > 20-day > 40-day), it is a bull cycle. When they are negatively aligned (5-day < 20-day < 40-day), it is a bear cycle.

By determining direction from the larger cycles and confirming strength on the smaller cycles, this strategy opens positions only when the major trend and minor momentum align. This effectively avoids false breakouts and achieves high win rate.

The strategy also utilizes ATR trailing stops to control single trade risks and further improve profitability.

## Advantages

- Flexible configurations to suit different instruments and trading styles

- Simple to implement even for beginner traders

- High capital efficiency to maximize leverage

- Effective risk control to avoid significant losses

- Strong trend following ability for sustained profits

- High win rate due to robust signals and fewer whipsaws

## Risks and Improvements

- MA crossovers may lag and cause late trend detection

- Single candle strength detection could trigger premature entry, relax condition

- Fixed ATR stop loss, optimize to dynamic stops

- Consider adding supplementary filters like volume

- Explore different MA parameters for optimization

## Conclusion

This strategy integrates multiple timeframe analysis and risk management for low-risk trend following trading. By adjusting parameters, it can be adapted to different instruments to suit trend traders. Compared to single timeframe systems, it makes more robust trading decisions and generates higher efficiency signals. In conclusion, this strategy has good market adaptiveness and development potential.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|2|Key Vaule. 'This changes the sensitivity'|
|v_input_2|7|ATR Period|
|v_input_int_1|25|atr_length|
|v_input_bool_1|true|(?Performance - credits: @QuantNomad)Show Monthly Performance ?|
|v_input_3|2|Return Precision|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-17 00:00:00
end: 2023-11-16 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © kgynofomo

//@version=5
strategy(title="[Salavi] | Andy Advance Pro Strategy [BTC|M15]", overlay=true, pyramiding=1, initial_capital=10000, default_qty_type=strategy.cash, default_qty_value=10000)

ema_short = ta.ema(close, 5)
ema_middle = ta.ema(close, 20)
ema_long = ta.ema(close, 40)

cycle_1 = ema_short > ema_middle and ema_middle > ema_long
cycle_2 = ema_middle > ema_short and ema_short > ema_long
cycle_3 = ema_middle > ema_long and ema_long > ema_short
cycle_4 = ema_long > ema_middle and ema_middle > ema_short
cycle_5 = ema_long > ema_short and ema_short > ema_middle
cycle_6 = ema_short > ema_long and ema_long > ema_middle

bull_cycle = cycle_1 or cycle_2 or cycle_3
bear_cycle = cycle_4 or cycle_5 or cycle_6

// Inputs
a = input(2, title='Key Vaule. \'This changes the sensitivity\'')
c = input(7, title='ATR Period')
h = false

xATR = ta.atr(c)
nLoss = a * xATR

src = h ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close, lookahead=barmerge.lookahead_off) : close

xATRTrailingStop = 0.0
iff_1 = src > nz(xATRTrailingStop[1], 0) ? src - nLoss : src + nLoss
iff_2 = src < nz(xATRTrailingStop[1], 0) and src[1] < nz(xATRTrailingStop[1], 0) ? math.min(nz(xATRTrailingStop[1]), src + nLoss) : iff_1
xATRTrailingStop := src > nz(xATRTrailingStop[1], 0) and src[1] > nz(xATRTrailingStop[1], 0) ? math.max(nz(xATRTrailingStop[1]), src - nLoss) : iff_2

pos = 0
iff_3 = src[1] > nz(xATRTrailingStop[1], 0) and src < nz(xATRTrailingStop[1], 0) ? -1 : nz(pos[1], 0)
pos := src[1] < nz(xATRTrailingStop[1], 0) and pos == 0 ? 1 : pos
```