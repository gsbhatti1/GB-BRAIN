> Name

ANN-based-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1063f65cfd84e9efd9f.png)
[trans]

## Overview

This strategy utilizes an artificial neural network (ANN) to predict future price changes and generates trading signals based on the predictions. It falls under the category of trend-following strategies. The advantages include its ability to identify complex nonlinear trends, making it suitable for medium-to-long term trading. However, there is a risk that the backtest results may be good but the live performance may not be as favorable.

## Strategy Logic

The strategy uses an ANN model to predict the percentage change of the next trading day.

- **Input Layer**: Contains only one node representing the percentage change of the previous day.
- **Hidden Layers**: Consists of two layers, with 5 nodes in the first layer and 33 nodes in the second layer. Both use hyperbolic tangent (tanh) as the activation function.
- **Output Layer**: Contains a single node that goes through a linear activation function to produce the final prediction.
- If the prediction is greater than the threshold parameter, a long signal is generated; if it's less than the negative of the threshold parameter, a short signal is generated.

## Strategy Advantages

- The ANN model can fit complex nonlinear relationships in data.
- Only requires input from one day prior to make predictions.
- Can identify trends across longer time frames.
- Multiple hidden layers enhance modeling capabilities.
- Optimized activation functions and parameters lead to better performance.

## Risks

- Overfitting risk, which may result in poor live trading performance compared to backtesting.
- Requires a significant amount of historical data for training; unsuitable for recently listed stocks.
- Parameters and structure need optimization, leading to variable results.
- Only predicts one-day changes, making it difficult to determine long-term trends.
- Performance may degrade during periods of market consolidation.

## Improvement Directions

- Add more input variables such as volume information.
- Experiment with different ANN architectures and activation functions.
- Optimize network parameters for improved fit.
- Increase the size of training data to reduce overfitting.
- Predict across multiple time horizons to better identify trends.
- Combine with other models using ensemble learning.
- Incorporate volatility measures and other indicators for enhanced risk management.

## Conclusion

This ANN-based strategy can identify complex nonlinear trends and is well-suited for medium-to-long term trading. However, the black-box nature of ANNs poses significant challenges in live trading scenarios. Optimization across input features, model architecture, parameter tuning, and ensemble learning should be combined with traditional technical analysis to ensure robust real-world performance. Artificial intelligence strategies still need to integrate conventional techniques to maximize their effectiveness.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Threshold|
|v_input_2|1D|Timeframe|


> Source (Pinescript)

```pinescript
//@version=2
strategy("ANN Strategy v2")

threshold = input(title="Threshold", type=float, defval=0.0000, step=0.0001)
timeframe = input(title="Timeframe",  defval='1D' )

getDiff() =>
    yesterday=request.security(syminfo.tickerid, timeframe, ohlc4[1])
    today=ohlc4
    delta=today-yesterday
    percentage=delta/yesterday

PineActivationFunctionLinear(v) => v
PineActivationFunctionTanh(v) => (exp(v) - exp(-v))/(exp(v) + exp(-v))

l0_0 = PineActivationFunctionLinear(getDiff())

l1_0 = PineActivationFunctionTanh(l0_0*0.8446488687)
l1_1 = PineActivationFunctionTanh(l0_0*-0.5674069006)
l1_2 = PineActivationFunctionTanh(l0_0*0.8676766445)
l1_3 = PineActivationFunctionTanh(l0_0*0.5200611473)
l1_4 = PineActivationFunctionTanh(l0_0*-0.2215499554)

l2_0 = PineActivationFunctionTanh(l1_0*0.3341657935 + l1_1*-2.0060003664 + l1_2*0.8606354375 + l1_3*0.9184846912 + l1_4*-0.8531172267)
l2_1 = PineActivationFunctionTanh(l1_0*-0.0394076437 + l1_1*-0.4720374911 + l1_2*0.2900968524 + l1_3*1.0653326022 + l1_4*0.3000188806)
l2_2 = PineActivationFunctionTanh(l1_0*-0.559307785 + l1_1*-0.9353655177 + l1_2*1.2133832962 + l1_3*0.1952686024 + l1_4*0.8552068166)
l2_3 = PineActivationFunctionTanh(l1_0*-0.4293220754 + l1_1*0.8484259409 + l1_2*-0.7154087313 + l1_3*0.1102971055 + l1_4*0.2279392724)
l2_4 = PineActivationFunctionTanh(l1_0*0.9111779155 + l1_1*0.2801691115 + l1_2*0.0039982713 + l1_3*-0.5648257117 + l1_4*0.3281705155)
l2_5 = PineActivationFunctionTanh(l1_0*-0.2963954503 + l1_1*0.4046532178 + l1_2*0.2460580977 + l1_3*0.6608675819 + l1_4*-0.8732022547)
l2_6 = PineActivationFunctionTanh(l1_0*0.8810811932 + l1_1*0.6903706878 + l1_2*-0.5953059103 + l1_3*-0.3084040686 + l1_4*-0.4038498853)
l2_7 = PineActivationFunctionTanh(l1_0*-0.5687101164 + l1_1*0.2736758588 + l1_2*-0.2217360382 + l1_3*0.8742950972 + l1_4*0.2997583987)
l2_8 = PineActivationFunctionTanh(l1_0*0.0708459913 + l1_1*0.8221730616 + l1_2*-0.7213265567 + l1_3*-0.3810462836 + l1_4*0.0503867753)
l2_9 = PineActivationFunctionTanh(l1_0*0.488
```