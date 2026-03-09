> Name

Donchian Channel Breakout Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1ffec01b3fe02e651eb.png)

---

## Overview

The Donchian Channel Breakout Trading Strategy uses the calculation of the highest and lowest prices over a certain period to determine the current price trend and conducts long and short trades based on channel breakouts. This strategy is suitable for highly volatile stocks and cryptocurrencies.

## Strategy Logic

This strategy constructs a channel by calculating the highest price `pcmax` and the lowest price `pcmin` over the last `history` periods. The calculation methods for the upper and lower rail of the channel are:

- Upper rail `yh = pcmax - (pcmax - pcmin) * (100 - percentDev)/100`
- Lower rail `yl = pcmin + (pcmax - pcmin) * percentDev/100`

where `percentDev` defaults to 13.

A long signal is generated when the price breaks through the upper rail. A short signal is generated when the price breaks through the lower rail.

The specific logic to generate trading signals is:

1. `boundup = high > yh` to determine if the upper rail is broken
2. `bounddn = low < yl` to determine if the lower rail is broken
3. `upsign = sma(bounddn, 2) == 1` uses the SMA of `bounddn` to determine a persistent breakout of the lower rail
4. `dnsign = sma(boundup, 2) == 1` uses the SMA of `boundup` to determine a persistent breakout of the upper rail
5. `exitup = dnsign` a breakout of the upper rail generates an exit signal
6. `exitdn = upsign` a breakout of the lower rail generates an exit signal
7. `if upsign` a breakout of the lower rail generates a long signal
8. `if dnsign` a breakout of the upper rail generates a short signal

The strategy also sets start and end trading times to avoid unnecessary overnight positions.

## Advantages of the Strategy

1. Uses the Donchian channel to determine trends, good backtest results
2. Has both long and short signals, allowing two-way trading
3. Uses SMA to filter signals and avoid bad trades
4. Optional stop loss to control risks
5. Sets start and end trading times to avoid overnight risks

## Risks of the Strategy

1. The Donchian channel is sensitive to `history` and `percentDev` parameters, needs optimization for different products
2. May generate false signals in range-bound markets
3. Does not consider order management, may impact profitability in live trading
4. Does not consider position sizing, risks of oversized positions
5. Does not consider money management, needs reasonable trading capital

## Enhancement Ideas

1. Optimize the `history` and `percentDev` parameters for different products
2. Add filters to avoid false signals in ranging markets
3. Add position sizing to control single position size
4. Add money management to limit total position size
5. Add order management for optimal order execution

## Conclusion

The Donchian Channel Breakout Strategy uses channel breakouts to determine trends and trading signals, with good backtest results and the ability to trade both long and short. However, risks exist regarding parameter optimization, filters, position sizing, money management, and order management. Proper enhancements in these areas are needed before stable live trading. Overall, it is a traditional trend-following strategy, and with optimizations can become a reliable quantitative trading strategy.

---

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|20|history|
|v_input_2|13|percentDev|
|v_input_3|100|capital|
|v_input_4|true|Long|
|v_input_5|true|Short|
|v_input_6|true|Stop Loss|
|v_input_7|3.8|Stop loss multiplicator|
|v_input_8|2018|From Year|
|v_input_9|2100|To Year|
|v_input_10|true|From Month|
|v_input_11|12|To Month|
|v_input_12|true|From day|
|v_input_13|31|To day|


## Source (PineScript)

```pinescript
/*backtest
start: 2023-10-31 00:00:00
end: 2023-11-07 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

////////////////////////////////////////////////////////////
//  Copyright by ChaoZhang v1.0 2023
// Donchian Channel Breakout Trading Strategy
// If you find this script helpful, you can also help me by sending donation to 
// BTC: 16d9vgFvCmXpLf8FiKY6zsy6pauaCyFnzS
// LTC: LQ5emyqNRjdRMqHPHEqREgryUJqmvYhffM
////////////////////////////////////////////////////////////
//@version=3
strategy("Donchian Channel Breakout Trading Strategy", overlay=false)
history = input(20)
percentDev = input(13)
capital = input(100)

needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
usestoploss = input(true, defval = true, title = "Stop Loss")
stoplossmult = input(3.8, defval = 3.8, minval = 1, maxval = 10, title = "Stop Loss Multiplicator")
```