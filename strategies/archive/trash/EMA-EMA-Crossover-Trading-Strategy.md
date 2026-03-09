> Name

EMA Crossover Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/9555b98989b968a618.png)
[trans]
### Overview
The EMA Crossover trading strategy generates buy and sell signals by calculating EMA lines of different periods and detecting their crossover situations. When the faster EMA crosses above the slower EMA, a buy signal is generated. When the faster EMA crosses below the slower EMA, a sell signal is generated.

### Strategy Logic

The core of this strategy is to compute two EMA lines with different periods, including a faster EMA with a default period of 9, and a slower EMA with a default period of 20. The code calculates these two lines by calling the built-in `ema` function in Pine Script. It then generates trading signals by detecting if the two EMA lines cross. Specifically, if the faster EMA crosses above the slower EMA, a buy signal is triggered. If the faster EMA crosses below the slower EMA, a sell signal is triggered.

The crossover situations are detected using the `crossover` and `crossunder` built-in functions in Pine Script. The `crossover` function checks if the faster EMA crosses above the slower EMA and returns a boolean value. The `crossunder` function checks if the faster EMA crosses below the slower EMA and returns a boolean value. Based on the return values of these two functions, the code submits corresponding buy or sell orders.

In addition, the code provides some auxiliary conditions such as setting start/end dates, restricting only long or short trades, etc. These features help conduct more sophisticated backtests or optimizations.

### Advantage Analysis

The biggest advantage of this strategy is that it is very simple and straightforward, easy to understand and implement, making it suitable for beginners to learn. Also, as a trend following indicator, moving averages can effectively track market trends and generate additional profits by exploiting the momentum. Lastly, this strategy has few parameters, which makes it easy to tune and optimize.

### Risk Analysis

The main risks this strategy faces are whipsaw trades and trend reversals. EMA lines are susceptible to short-term market fluctuations, which may generate false signals and trigger unnecessary trades, increasing trading frequency and costs. On the other hand, when crossover signals trigger, the trend may be nearing its reversal point, making trades riskier. Inappropriate parameter settings can also impact strategy performance.

Methods like adjusting EMA periods, adding filters can help reduce whipsaws. Stop loss orders control single trade loss. Parameter optimization improves robustness. However, no trading strategies can completely avoid losses, so one must be ready to take on risks.

### Optimization Opportunities

This strategy can be improved in the following aspects:

1. Optimize EMA periods to find best parameter sets
2. Add indicators like MACD, RSI as filters to reduce false signals  
3. Incorporate trend metrics to avoid trend reversals
4. Select stocks based on fundamentals 
5. Adjust position sizing, set stops based on ATR

### Conclusion

The EMA crossover is a simple yet effective trend following strategy. It uses EMA crosses to generate trading signals, automatically capturing price trends. This easy to understand and adjustable strategy is perfect for beginners to learn. It can also be integrated into more complex strategies. However, all strategies bear risks and need prudent management. Continued enhancements in terms of optimization and enriching market conditions can make this strategy more robust.
[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Fast EMA|
|v_input_2|20|Slow EMA|
|v_input_3|0|Trade Direction: Both|Short|Long|
|v_input_4|timestamp(01 Jan 1970 00:00)|Start Date|
|v_input_5|timestamp(31 Dec 2170 23:59)|End Date|


> Source (PineScript)

```pinescript
//@version=4
strategy(
    "EMA Cross Strategy",
    overlay=true,
    calc_on_every_tick=true,
    currency=currency.USD
)

// INPUT:
emaFast = input(title="Fast EMA", type=input.integer, defval=9, minval=1, maxval=9999)
emaSlow = input(title="Slow EMA", type=input.integer, defval=20)
```