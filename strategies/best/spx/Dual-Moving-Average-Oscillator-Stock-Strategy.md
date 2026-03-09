### Overview

This strategy uses the Dual Moving Average Oscillator index to determine the buy and sell points of stocks. The Dual Moving Average Oscillator index consists of two exponential moving averages with different parameters, and measures the momentum of price changes to detect overbought and oversold conditions.

### Strategy Principle  

The core indicator of this strategy is the True Strength Index (TSI). The calculation method is:

1. Calculate the price change `pc = close - preclose`

2. Smooth `pc` twice using both long period of 12 days and short period of 9 days exponential moving average. Obtain double smoothed price change: `double_smoothed_pc`

3. Similarly, double smooth the absolute value `|pc|` to get `double_smoothed_abs_pc`

4. Finally TSI index = 100 * (double_smoothed_pc / double_smoothed_abs_pc)

By comparing the TSI value with its signal line `tsi_signal`, we can determine overbought or oversold zones, thereby deciding buy and sell points.

Buy signal: TSI crosses over its signal upward, indicating reversal of the stock price, marking the start of an overbought zone where we should go long.

Sell signal: TSI crosses below its signal downward, indicating reversal of the stock price, marking the end of an overbought zone where we should close our position and sell out.

### Advantage Analysis  

The biggest advantage of this strategy lies in using the dual moving average indicator to identify cyclical features in stock prices. By simultaneously employing both long and short periods in the dual moving average, it can capture price change trends more sensitively and accurately than a single moving average, and is more effective in determining trading signals.

In addition, this strategy chooses the TSI index rather than other common technical indicators because TSI pays more attention to calculating price change momentum. This can judge overbought/oversold conditions more precisely, resulting in better trading points.

### Risk Analysis  

The biggest risk of this strategy is that the dual moving average itself is quite sensitive to price changes. In case of price fluctuation, it can easily generate false signals. Moreover, the criteria for TSI to judge overbought/oversold zones are still subjective, and improper parameter settings also impact the accuracy.

To control such risks, it is advisable to optimize parameters appropriately by adjusting lengths of the double moving averages. Combining other indicators to verify signals is also necessary to avoid opening positions amid volatility. Furthermore, optimizing stop-loss strategies and setting up risk control measures against emergencies are quite essential.

### Optimization Directions   

The optimization directions of this strategy mainly focus on two aspects:

1. Parameter optimization. The optimal combination of parameters like lengths of long and short moving average and signal line can be backtested to improve the sensitivity.

2. Configure filtering indicators. Such as combining Bollinger Bands, KDJ, and so on to verify buy/sell signals and prevent wrong opening of positions. Trading volume filter can also be applied to open positions only when volume surges.

3. Add stop-loss strategy. Set up moving stop loss, timed exit to limit the loss of single position. Also we can suspend trading temporarily based on market condition to control systematic risk.

4. Optimize position sizing. Set up dynamic size and proportion of positions based on market condition to manage the risk exposure of every trade.

### Summary  

This strategy utilizes the calculation method of Dual Moving Average Oscillator index, integrating both long and short term analysis of price momentum changes, thereby determining overbought and oversold zones to decide entries and exits. Compared to a single moving average, it has the advantage of more accurate and sensitive judgment. Of course, proper parameter optimization is still necessary, coupled with other indicators for signal filtering, so as to enhance the stability and profitability. Overall, this strategy provides an effective technical tool to determine trading points, which is worth live testing and optimizing.

---

### Strategy Arguments

| Argument | Default | Description |
| -------- | ------- | ----------- |
| v_input_1 | 10000   | Initial Capital |
| v_input_2 | true    | Risk Percentage |
| v_input_3 | 12      | Long Length    |
| v_input_4 | 9       | Short Length   |
| v_input_5 | 12      | Signal Length  |

### Source (PineScript)

```pinescript
//@version=5
strategy("Dual Moving Average Oscillator Stock Strategy", overlay=true)

// Input arguments
initial_capital = input(10000, title="Initial Capital")
risk_percentage = input(true, title="Risk Percentage")
long_length = input(12, title="Long Length")
short_length = input(9, title="Short Length")
signal_length = input(12, title="Signal Length")

// Calculate price change
pc = close - open[1]

// Smooth pc twice using both long and short period exponential moving averages
double_smoothed_pc = ta.smooth(ta.ema(pc, long_length), short_length)
double_smoothed_abs_pc = ta.smooth(ta.ema(math.abs(pc), short_length))

// Calculate TSI index
tsi_index = 100 * (double_smoothed_pc / double_smoothed_abs_pc)

// Plot TSI and signal line
plot(tsi_index, title="TSI", color=color.blue)
plot(tsi_signal, title="Signal Line", color=color.red)

// Buy/sell signals
buy_condition = ta.crossover(tsi_index, tsi_signal)
sell_condition = ta.crossunder(tsi_index, tsi_signal)

if (risk_percentage == true)
    // Risk management based on risk percentage
    max_risk_per_trade = initial_capital * 0.01

// Execute trades
if buy_condition
    strategy.entry("Buy", strategy.long)

if sell_condition
    strategy.close("Buy")

```