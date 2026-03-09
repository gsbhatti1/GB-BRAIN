> Name

ADX Intelligent Trend Tracking Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1045022a6c7c839ea8c.png)
[trans]


## Overview  

The ADX Intelligent Trend Tracking Strategy utilizes the Average Directional Index (ADX) to assess the strength of trends. It captures trends when they are weak and follows strong trends for profit. The strategy generates trading signals by combining trend strength judgment with price breakout, making it a type of trend tracking strategy.

## Strategy Principle  

This strategy primarily relies on the Average Directional Index (ADX) to evaluate current trend strength. ADX calculates the average value of DIRECTIONAL INDICATOR over a certain period to indicate the strength of the trend. When the ADX value is below a set threshold, it indicates consolidation in the market. At this point, a box range is determined. If the price breaks through the upper and lower rails of the box, trading signals are generated.

Specifically, the strategy first calculates the 14-cycle ADX value. When it is lower than 18, it considers the trend weaker. It then calculates the range of the box formed by the highest and lowest prices of the past 20 K-lines. When the price breaks through this box, buy and sell signals are generated. The stop loss distance is set at 50% of the box size, while the take profit distance is set at 100% of the box size.

This strategy integrates trend strength judgment with breakout signals to capture trends when they are weaker and in consolidation phases, avoiding frequent trading during disorderly markets. When strong trends appear, a larger take profit range can yield more profits.

## Advantages of the Strategy  

1. Combining trend strength judgment helps avoid frequent trading during disorderly markets.
2. Box breakouts add filtering to prevent trapping in volatile markets.
3. In trend markets, greater profit targets can be achieved.
4. Customizable ADX parameters, box parameters, and stop loss and take profit coefficients for adapting to different products.

## Risks of the Strategy  

1. Improperly set ADX parameters may result in missing trends or making incorrect judgments.
2. Excessively large or small box ranges can affect performance.
3. Incorrect stop loss and take profit coefficients might cause inadequate stop loss or premature profit taking.

Adjusting parameters like ADX, box range, and stop loss and take profit coefficients can optimize the strategy for different products and market conditions. Strict money management is also crucial to control single trade risk and avoid significant losses.

## Directions for Strategy Optimization  

1. Test different cycles for ADX parameters.
2. Experiment with different lengths of box parameters to determine optimal ranges.
3. Fine-tune stop loss and take profit coefficients to optimize risk-reward ratios.
4. Test unilateral long or short trading only.
5. Incorporate other indicators for combinations, such as volume indicators.

## Summary  

The ADX Intelligent Trend Tracking Strategy is generally a relatively stable trend tracking strategy. It combines trend strength judgment with price breakout signals to avoid common issues like chasing highs and selling lows found in typical trend following strategies. Through parameter optimization and strict money management, the strategy can achieve steady profits.

||

## Overview  

The ADX Intelligent Trend Tracking Strategy uses the Average Directional Index (ADX) to judge the strength of trends, capturing trends when they are weak and tracking strong trends for profit. The strategy generates trading signals by combining trend strength judgment with price breakout, making it a type of trend tracking strategy.

## Strategy Principle  

The core of this strategy is based on the Average Directional Index (ADX) to assess current trend strength. ADX calculates the average value of DIRECTIONAL INDICATOR over a certain period to represent the strength of the trend. When the ADX value is below the set threshold, it indicates consolidation in the market. At this point, the box range is determined. If the price breaks through the upper and lower rails of the box, trading signals are generated.

Specifically, the strategy first calculates the 14-cycle ADX value. When it is lower than 18, a weaker trend is considered. It then calculates the range of the box formed by the highest and lowest prices of the past 20 K-lines. When the price breaks through this box, buy and sell signals are generated. The stop loss distance is set at 50% of the box size, while the take profit distance is set at 100% of the box size.

This strategy integrates trend strength judgment with breakout signals to capture trends when they are weaker and in consolidation phases, avoiding frequent trading during disorderly markets. When strong trends appear, a wider take profit range can yield more profits.

## Advantages of the Strategy  

1. Combining trend strength judgment helps avoid frequent trading during disorderly markets.
2. Box breakouts add filtering to prevent trapping in volatile markets.
3. In trend markets, greater profit targets can be achieved.
4. Customizable ADX parameters, box parameters, and stop loss and take profit coefficients for adapting to different products.

## Risks of the Strategy  

1. Improperly set ADX parameters may result in missing trends or making incorrect judgments.
2. Excessively large or small box ranges can affect performance.
3. Incorrect stop loss and take profit coefficients might cause inadequate stop loss or premature profit taking.

Adjusting parameters like ADX, box range, and stop loss and take profit coefficients can optimize the strategy for different products and market conditions. Strict money management is also crucial to control single trade risk and avoid significant losses.

## Directions for Strategy Optimization  

1. Test different cycles for ADX parameters.
2. Experiment with different lengths of box parameters to determine optimal ranges.
3. Fine-tune stop loss and take profit coefficients to optimize risk-reward ratios.
4. Test unilateral long or short trading only.
5. Incorporate other indicators for combinations, such as volume indicators.

## Summary  

The ADX Intelligent Trend Tracking Strategy is generally a relatively stable trend tracking strategy. It combines trend strength judgment with price breakout signals to avoid common issues like chasing highs and selling lows found in typical trend following strategies. Through parameter optimization and strict money management, the strategy can achieve steady profits.

---

| Argument | Default | Description |
| --- | --- | --- |
| v_input_1 | 14 | (ADX Settings) ADX Smoothing Period |
| v_input_2 | 14 | ADX Period |
| v_input_3 | 18 | ADX Lower Level |
| v_input_4 | 20 | (BreakoutBox) BreakoutBox Lookback Period |
| v_input_5 | true | (Take Profit and Stop Loss) Profit Target Box Width Multiple |
| v_input_6 | 0.5 | Stop Loss Box Width Multiple |
| v_input_7 | false | (Trade Direction) Both(0), Long(1), Short(-1) |

---

## Source (PineScript)

```pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-11-27 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Developer: Andrew Palladino.
//Creator: Rob Booker.
//Date: 9/29/2017
//@version=5
//Date: 08/10/2022
//Updated to V5 from V1, default cash settings added and indicators made more easily visible by:
// @ Powerscooter

strategy("Rob Booker - ADX Breakout", shorttitle="ADX Breakout V5", overlay=true, default_qty_type = strategy.cash, default_qty_value = 100000, initial_capital = 100000)

adxSmoothPeriod = input(14, title="ADX Smoothing Period", group = "ADX Settings")
adxPeriod = input(14, title="ADX Period", group = "ADX Settings")
adxLowerLevel = input(18, title="ADX Lower Level", group = "ADX Settings")
boxLookBack = input(20, title="BreakoutBox Lookback Period", group = "BreakoutBox")
profitTargetMultiple = input(1.0, title="Profit Target Box Width Multiple", group = "Take Profit and Stop Loss")
stopLossMultiple = input(0.5, title="Stop Loss Box Width Multiple", group = "Take Profit and Stop Loss")

plot(adxSmoothPeriod, color=color.blue, title="ADX Smoothing Period")
plot(adxPeriod, color=color.red, title="ADX Period")
plot(adxLowerLevel, color=color.green, title="ADX Lower Level")
```