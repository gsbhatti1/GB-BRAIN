> Name

Welcome-to-the-BEARMARKET-30MIN

> Author

ChaoZhang

> Strategy Description


Hello everyone,

This is my first concept of bear market movement bot for near future.
The bot is optimized for --->>> BINANCE:BTCUSDT.

The core of this bot is using ATR trend to define trends, and uses RSI value to open new swing shorts (RSI-VWAP) or find a perfect close place (RSI oversold).

This bot is only a short bot designed to maximize profit from every move down in Bitcoin.
I recommend using 1-3x leverage for this bot because of the high amount of wrong trades or closes with minimal profit.
The stop loss is around: 6% (just for best performance in all backtesting time period).

So, short conditions are open by:

1) Both ADX and S_ATR only if RSI is not oversold
a) ADX is one of the most powerful and accurate trend indicators. ADX measures how strong a trend is and can provide valuable information on whether there is a potential trading opportunity.
b) The average true range (ATR) is a technical analysis indicator, introduced by market technician J. Welles Wilder Jr., in his book New Concepts in Technical Trading Systems, that measures market volatility by decomposing the entire range of an asset price for that period.

2) RSI VWAP - VWAP is calculated by adding up the dollars traded for every transaction (price multiplied by the number of shares traded) and then dividing by the total shares traded.
RSI VWAP opens a new position only if there is no bullish signal from Cloud, ADX, ATR indicators

**Backtest**

![IMG](https://www.fmz.com/upload/asset/10b6726f9fa1eb5447c.jpg)

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|2|PP period|
|v_input_2|10|ATR Factor|
|v_input_3|14|ATR Period|
|v_input_4|2|Cloud Length|
|v_input_10|22|Rsi vwap length|
|v_input_11|6|stop loss|
|v_input_12|100|qty percent|
|v_input_5|0|(?ADX_options)ADX_options OPTION: CLASSIC|MASANAKAMURA|
|v_input_6|17|ADX_options LENGTH|
|v_input_7|14|ADX_options THRESHOLD|
|v_input_8|51|(?Relative Strenght Indeks)RSI length|
|v_input_9_high|0|RSI Source: high|close|low|open|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-04-15 00:00:00
end: 2022-05-14 23:59:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © wielkieef


//@version=4

src = close

//strategy("Welcome to the BEARMARKET [30MIN]", overlay=true, initial_capital = 10000, pyramiding = 1, currency = "USD", calc_on_order_fills = false, calc_on_every_tick = false, default_qty_type = strategy.fixed, default_qty_value = 1, commission_value = 0.04)

//Inputs  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

prd                     =               input(2,                                title="PP period")
Factor                  =               input(10,                               title = "ATR Factor")
Pd                      =               input(14,                               title = "ATR Period")
len                     =               input(2,                                title="Cloud Length")
ADX_options             =               input("CLASSIC",                        title="ADX OPTION",                                       options = ["CLASSIC", "MASANAKAMURA"],                                            group = "ADX")
ADX_len                 =               input(17,                               title="ADX LENGTH",                                       type = input.integer, minval = 1,                                                 group = "ADX")
th                      =               input(14,                               title="ADX THRESHOLD",                                    type = input.float, minval = 0, step = 0.5,                                       group = "ADX")
len_3                   =               input(51,                               title="RSI length",                                                                                                                         group = "Relative Strenght Indeks")
src_3                   =               input(high,                             title="RSI Source",                                                                                                                         group = "Relative Strenght Indeks")
RSI_VWAP_length         =               input(22,                               title="Rsi vwap length")

//INDICATORS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

//Cloud -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PI =                                                                                                                                        2 * asin(1)
hilbertTransform(src) =>
    0.0962 * src + 0.5769 * nz(src[2]) - 0.5769 * nz(src[4]) - 0.0962 * nz(src[6])
computeComponent(src, mesaPeriodMult) =>
    hilbertTransform(src) * mesaPeriodMult
computeAlpha(src, fastLimit, slowLimit) =>
    mesaPeriod =                                                                                                                            0.0
    mesaPeriodMult =                                                              
```