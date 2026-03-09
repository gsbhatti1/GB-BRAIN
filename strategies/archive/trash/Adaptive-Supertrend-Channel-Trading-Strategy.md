> Name

Adaptive-Supertrend-Channel-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy generates trading signals by building double-layer supertrend channels and utilizing price breaks to cross these channels. It adjusts channel width based on price volatility for an adaptive effect, making it a trend-following strategy.

## Strategy Logic

1. Calculate the standard deviation and average true range (ATR) of prices, using ATR to adjust the channel width.
2. Construct double-layer supertrend channels with the inner layer more sensitive and the outer layer more stable.
3. Generate buy/sell signals when price breaks through the inner or outer channel.
4. The dual-channel structure helps filter out some false breakouts.
5. ATR volatility adjusts the channel width, widening it when volatility surges for adaptive effect.

## Advantages

1. Supertrend channels are simple and effective in tracking trends.
2. The double-channel structure improves signal quality by filtering false breakouts.
3. Volatility-adaptive adjustments make the channels more suitable for different market environments.
4. Easy to implement with straightforward parameter tuning.
5. Visualized channels and breakouts form clear trading signals.

## Risks

1. Breakout signals may produce false signals, leading to unnecessary losses.
2. Inability to determine trend direction poses risks of counter-trend trading.
3. Adaptive adjustments may be overly sensitive, causing excessive volatility in the channel width.
4. Improper parameter optimization can lead to overfitting.
5. As a trend-following strategy, it struggles in range-bound markets.

## Optimization Directions

1. Test different parameters' impacts on adaptive effectiveness.
2. Incorporate moving averages (MA) to determine major trends.
3. Optimize breakout confirmation mechanisms to avoid false breakouts.
4. Add stop-loss strategies to limit per-trade losses.
5. Evaluate the impact of channel parameter tuning on trading frequency.
6. Use machine learning algorithms for dynamic parameter optimization.

## Conclusion

This strategy uses adaptive double supertrend channels to capture price trends. Its advantages include simplicity and effectiveness in trend tracking, but it also faces risks such as false breakouts and incorrect trend direction. Through further parameter tuning and supplementary mechanisms, the strategy can be improved, becoming a robust trend-following system.

||


## Overview

This strategy builds double-layer supertrend channels and generates trading signals when price breaks through these channels. It adjusts channel width based on price volatility for an adaptive effect, making it belong to trend following strategies.

## Strategy Logic

1. Calculate the standard deviation and average true range (ATR) of prices, using ATR to adjust the channel width.
2. Construct double-layer supertrend channels with the inner layer more sensitive and the outer layer more stable.
3. Generate buy/sell signals when price breaks through the inner or outer channel.
4. The dual-channel structure helps filter out some false breakouts.
5. ATR volatility adjusts the channel width, widening it during increased volatility for adaptive effect.

## Advantages

1. Supertrend channels are simple and effective in tracking trends.
2. The double-channel structure improves signal quality by filtering false breakouts.
3. Volatility-adaptive adjustments make the channels more suitable for different market environments.
4. Easy to implement with straightforward parameter tuning.
5. Visualized channels and breakouts form clear trading signals.

## Risks

1. Breakout signals may produce false signals, leading to unnecessary losses.
2. Inability to determine trend direction poses risks of counter-trend trading.
3. Adaptive adjustments may be overly sensitive, causing excessive volatility in the channel width.
4. Improper parameter optimization can lead to overfitting.
5. As a trend-following strategy, it struggles in range-bound markets.

## Enhancement

1. Test different parameters' impacts on adaptive effectiveness.
2. Incorporate moving averages (MA) to determine major trends.
3. Optimize breakout confirmation mechanisms to avoid false breakouts.
4. Add stop-loss strategies to limit per-trade losses.
5. Evaluate the impact of channel parameter tuning on trading frequency.
6. Use machine learning algorithms for dynamic parameter optimization.

## Conclusion

This strategy uses adaptive double supertrend channels to capture price trends. Its advantages include simplicity and effectiveness in trend tracking, but it also faces risks such as false breakouts and incorrect trend direction. Through further parameter tuning and supplementary mechanisms, the strategy can be improved, becoming a robust trend-following system.

||


> Strategy Arguments

| Argument        | Default  | Description                    |
|-----------------|----------|--------------------------------|
| v_input_1       | 3        | Multiplier                     |
| v_input_2       | 10       | Period                         |
| v_input_3       | false    | Self-Adjusting                 |
| v_input_4       | true     | From Day                       |
| v_input_5       | true     | From Month                     |
| v_input_6       | 2019     | From Year                      |
| v_input_7       | true     | To Day                         |
| v_input_8       | true     | To Month                       |
| v_input_9       | 2020     | To Year                        |

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-08-20 00:00:00
end: 2023-09-19 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("SuperTrend Cloud Strategy", shorttitle="SuperTrend Cloud Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital = 1000)

// Inputs
multi = input(title="Multiplier", type=input.float, step=0.1, defval=3, minval=1)
period = input(title="Period", type=input.integer, step=1, defval=10, minval=1)
SelfAdjust = input(title="Self-Adjusting", type=input.bool, defval=false)

////////////////////////////////////////////////////////////////////////////////
// BACKTESTING RANGE
 
// From Date Inputs
fromDay = input(defval=1, title="From Day", minval=1, maxval=31)
fromMonth = input(defval=1, title="From Month", minval=1, maxval=12)
fromYear = input(defval=2019, title="From Year", minval=1970)

// To Date Inputs
toDay = input(defval=1, title="To Day", minval=1, maxval=31)
toMonth = input(defval=1, title="To Month", minval=1, maxval=12)
toYear = input(defval=2020, title="To Year", minval=1970)

// Calculate start/end date and time condition
startDate = timestamp(fromYear, fromMonth, fromDay, 00, 00)
finishDate = timestamp(toYear, toMonth, toDay, 00, 00)
time_cond = true

////////////////////////////////////////////////////////////////////////////////

dev = stdev(close, period)
stdDev = (dev / close) * 100 + 1
MultDev = SelfAdjust ? multi * stdDev : multi

up_lev1 = hl2 - MultDev * atr(period)
dn_lev1 = hl2 + MultDev * atr(period)
up_lev2 = hl2 - (MultDev * 2 * atr(period))
dn_lev2 = hl2 + (MultDev * 2 * atr(period))

up_trend1 = 0.0
up_trend1 := close[1] > up_trend1[1] ? max(up_lev1, up_trend1[1]) : up_lev1
up_trend2 = 0.0
up_trend2 := close[1] > up_trend2[1] ? max(up_lev2, up_trend2[1]) : up_lev2

down_trend1 = 0.0
down_trend1 := close[1] < down_trend1[1] ? min(dn_lev1, down_trend1[1]) : dn_lev1
down_trend2 = 0.0
down_trend2 := close[1] < down_trend2[1] ? min(dn_lev2, down_trend2[1]) : dn_lev2

trend1 = 0
trend1 := close > down_trend1[1] ? 1 : close < up_trend1[1] ? -1 : nz(trend1[1], 1)
trend2 = 0
trend2 := close > down_trend2[1] ? 1 : close < up_trend2[1] ? -1 : nz(trend2[1], 1)

st_line1 = trend1 == 1 ? up_trend1 : down_trend1
st_line2 = trend2 == 1 ? up_trend2 : down_trend2

// Plotting
plot1 = plot(st_line1, color=trend1 == 1 ? color.green : color.red, style=plot.style_line, linewidth=1, title="SuperTrend 1")
plot2 =