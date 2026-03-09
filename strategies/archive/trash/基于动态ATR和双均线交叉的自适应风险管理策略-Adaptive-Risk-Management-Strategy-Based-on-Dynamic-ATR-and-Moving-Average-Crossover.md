> Name

Profitable Moving Average Crossover Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8ca33c79b217af9c3e1.png)
![IMG](https://www.fmz.com/upload/asset/2d871415a5db59099227a.png)


#### Overview
This strategy is a trading system that combines dual moving average crossover signals with dynamic risk management. It generates trading signals through the crossover of short-term and long-term moving averages while using the ATR indicator to dynamically adjust stop-loss and take-profit levels. The strategy also incorporates time filtering and a cooldown period to optimize trade quality, along with risk-reward ratio and per-trade risk percentage management mechanisms.

#### Strategy Principles
The strategy is based on several core components:
1. The signal generation system uses the crossover of short-term (10-period) and long-term (100-period) simple moving averages to trigger trades. A buy signal is generated when the short-term MA crosses above the long-term MA, and vice versa.
2. The risk management system uses a 14-period ATR multiplied by 1.5 to set dynamic stop-loss distances, with the profit target being twice the stop-loss distance (adjustable risk-reward ratio).
3. A time filter allows users to set specific trading hours, executing trades only within the specified time range.
4. A trading cooldown mechanism sets a 10-period waiting time to prevent overtrading.
5. Risk per trade is controlled at 1% of the account (adjustable).

#### Strategy Advantages
1. Dynamic Risk Management: Uses the ATR indicator to adapt to market volatility, automatically adjusting stop-loss and take-profit distances in different market conditions.
2. Comprehensive Risk Control: Achieves systematic money management through set risk-reward ratios and per-trade risk percentages.
3. Flexible Time Management: Can adjust trading hours according to different market characteristics.
4. Overtrading Prevention: Cooldown mechanism effectively prevents excessive trading signals during volatile periods.
5. Visualization: Clearly displays trading signals and moving averages on the chart for analysis and optimization.

#### Strategy Risks
1. Trend Reversal Risk: May generate false breakout signals in ranging markets, leading to consecutive stops.
2. Parameter Sensitivity: The choice of moving average periods, ATR multiplier, and other parameters significantly affects strategy performance.
3. Improper time filter settings may miss important trading opportunities.
4. Fixed risk-reward ratio may not be flexible enough for different market conditions.

#### Strategy Optimization Directions
1. Introduce Trend Strength Filter: Add ADX or similar indicators to assess trend strength, trading only during strong trends.
2. Dynamic Risk-Reward Ratio Adjustment: Automatically adjust risk-reward ratio based on market volatility or trend strength.
3. Add Volume Analysis: Incorporate volume as a supplementary indicator for signal confirmation.
4. Optimize Cooldown Mechanism: Make cooldown period length dynamically adjust based on market volatility.
5. Implement Market Environment Classification: Use different parameter combinations in different market environments.

#### Summary
This strategy builds a complete trading system by combining classical technical analysis methods with modern risk management concepts. Its core advantages lie in dynamic risk management and multiple filtering mechanisms, but parameters still need to be optimized based on specific market characteristics in practical applications. Successful strategy operation requires traders to deeply understand the function of each component and adjust parameters timely according to market changes. Through the suggested optimization directions, the strategy has the potential to achieve more stable performance across different market environments.

```pinescript
/*backtest
start: 2024-09-18 00:00:00
end: 2025-02-19 00:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Profitable Moving Average Crossover Strategy", shorttitle="Profitable MA Crossover", overlay=true)

// Input parameters for the moving averages
shortPeriod = input.int(10, title="Short Period", minval=1)
longPeriod = input.int(100, title="Long Period", minval=1)

// Input parameters for time filter
startHour = input.int(0, title="Start Hour (UTC)", minval=0, maxval=23)
startMinute = input.int(0, title="Start Minute (UTC)", minval=0, maxval=59)
endHour = input.int(23, title="End Hour (UTC)", minval=0, maxval=23)
endMinute = input.int(59, title="End Minute (UTC)", minval=0, maxval=59)

// Cooldown period input (bars)
cooldownBars = input.int(10, title="Cooldown Period (bars)", minval=1)
```