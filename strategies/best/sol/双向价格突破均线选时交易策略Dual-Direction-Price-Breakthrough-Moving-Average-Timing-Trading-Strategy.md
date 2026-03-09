> Name

Dual-Direction-Price-Breakthrough-Moving-Average-Timing-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/151515d2c8e2d28ddd8.png)
[trans]

## Overview

The Dual-Direction-Price-Breakthrough-Moving-Average-Timing-Trading-Strategy (Dual-Direction-Price-Breakthrough-Moving-Average-Timing-Trading-Strategy) is a quantitative trading strategy that uses price breakthrough of moving averages to determine trading signals. It compares the closing price with a moving average of a specified period and generates trading signals when the price breaks through the moving average.

## Strategy Logic

The core logic of this strategy is:

1. Calculate the moving average (EMA) of a specified period (e.g., 200 days) using the EMA function.
2. Compare the closing price with the EMA to determine if the price breaks through the EMA. Specifically, when the closing price is above the EMA, it is considered that the price has broken through the EMA upwards; when the closing price is below the EMA, it is considered that the price has broken through the EMA downwards.
3. Determine long and short signals based on the breakthroughs. When the price breaks through the EMA upwards, a long signal is generated; when the price breaks through the EMA downwards, a short signal is generated.
4. When a signal is triggered, place an order with a certain percentage (e.g., 100%) and set stop loss and take profit prices.
5. When the stop loss or take profit price is touched, close the position.
6. Repeat the process to profit from the timing of the price breaking through the moving average.

The strategy is simple and straightforward to understand and implement. It aims to capture short-term momentum by signals of breaking through moving averages. However, it also has certain lagging and whipsaw risks.

## Advantages

- Simple and clear logic, easy to understand and validate.
- Smooth tracking ability utilizing characteristics of moving averages.
- High trading frequency, suitable for short-term trading.
- Quick response to price changes, catching good timing.

## Risks

- Certain level of lagging, may miss initial breakthroughs of price.
- Frequent trading when whipsawed multiple times.
- Risk of being stopped out on sharp reversals.

Optimization methods include parameter tuning, using more effective indicators, reducing trading frequency, etc. Adaptive stops and filtering conditions can also control risks.

## Optimization Directions

- Test different types and parameters of moving averages for better solutions, e.g., EMA, SMA, LWMA.
- Add filtering conditions to avoid whipsaw trades, e.g., volume, Bollinger Bands, ATR, etc.
- Optimize and test stop loss and take profit strategies to lower risks.
- Combine trend following, mean reversion, and other strategies for a robust trading system.
- Add parametrization for wider adaptability.

## Conclusion

The strategy has a relatively simple logic of tracking moving averages to capture short-term momentum. Advantages include responsiveness and ease of use; disadvantages include lagging and inertia. Further optimizations can be done on indicator selection, stop loss mechanisms, filtering techniques to make the strategy more solid and comprehensive.

||

## Overview

The Dual Direction Price Breakthrough Moving Average Timing Trading Strategy is a quantitative trading strategy that uses price breakthrough of moving averages to determine trading signals. It compares the closing price with a moving average of a specified period and generates trading signals when the price breaks through the moving average.

## Strategy Logic

The core logic of this strategy is:

1. Calculate the moving average (EMA) of a specified period (e.g., 200 days) using the EMA function.
2. Compare the closing price with the EMA to determine if the price breaks through the EMA. Specifically, when the closing price is above the EMA, it is considered that the price has broken through the EMA upwards; when the closing price is below the EMA, it is considered that the price has broken through the EMA downwards.
3. Determine long and short signals based on the breakthroughs. When the price breaks through the EMA upwards, a long signal is generated; when the price breaks through the EMA downwards, a short signal is generated.
4. When a signal is triggered, place an order with a certain percentage (e.g., 100%) and set stop loss and take profit prices.
5. When the stop loss or take profit price is touched, close the position.
6. Repeat the process to profit from the timing of the price breaking through the moving average.

The strategy is simple and straightforward to understand and implement. It aims to capture short-term momentum by signals of breaking through moving averages. However, it also has certain lagging and whipsaw risks.

## Advantages

- Simple and clear logic, easy to understand and validate.
- Smooth tracking ability utilizing characteristics of moving averages.
- High trading frequency, suitable for short-term trading.
- Quick response to price changes, catching good timing.

## Risks

- Certain level of lagging, may miss initial breakthroughs of price.
- Frequent trading when whipsawed multiple times.
- Risk of being stopped out on sharp reversals.

Optimization methods include parameter tuning, using more effective indicators, reducing trading frequency, etc. Adaptive stops and filtering conditions can also control risks.

## Optimization Directions

- Test different types and parameters of moving averages for better solutions, e.g., EMA, SMA, LWMA.
- Add filtering conditions to avoid whipsaw trades, e.g., volume, Bollinger Bands, ATR, etc.
- Optimize and test stop loss and take profit strategies to lower risks.
- Combine trend following, mean reversion, and other strategies for a robust trading system.
- Add parametrization for wider adaptability.

## Conclusion

The strategy has a relatively simple logic of tracking moving averages to capture short-term momentum. Advantages include responsiveness and ease of use; disadvantages include lagging and inertia. Further optimizations can be done on indicator selection, stop loss mechanisms, filtering techniques to make the strategy more solid and comprehensive.

---

## Strategy Arguments

|Argument|Default|Description|
|---|---|---|
|v_input_1|timestamp(01 Jan 2020 12:00 +0000)|Backtest Start|
|v_input_2|timestamp(01 Jan 2024 12:00 +0000)|Backtest End|
|v_input_float_1|true|Long Stop Loss (%)|
|v_input_float_2|true|Short Stop Loss (%)|
|v_input_float_3|true|Long Take(%)|
|v_input_float_4|true|Short Take (%)|
|v_input_int_1|200|EMA Length|
|v_input_3_close|0|Swing Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_2|20|Swing Period|
|v_input_float_5|3.5|Swing Multiplier|
|v_input_4|false|Bar Colors On/Off|


## Source (PineScript)

```pinescript
/*backtest
start: 2022-12-08 00:00:00
end: 2023-12-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/

// Credits to the original Script - Range Filter DonovanWall https://www.tradingview.com/script/lut7sBgG-Range-Filter-DW/
// This version is the old version of the Range Filter with less settings to tinker with

//@version=5
strategy(title='Range Filter - B&S Signals', shorttitle='RF - B&S Signals', initial_capital=1000, currency=currency.GBP, default_qty_value=100, default_qty_type=strategy.percent_of_equity, commission_type=strategy.commission.percent, commission_value=0.075, overlay=true)


i_startTime = input(defval=timestamp('01 Jan 2020 12:00 +0000'), title='Backtest Start')
i_endTime = input(defval=timestamp('01 Jan 2024 12:00 +0000'), title='Backtest End')

inDateRange     = true
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------
//Functions
//-----------------------------------------------------------------------------------------------------------------------------