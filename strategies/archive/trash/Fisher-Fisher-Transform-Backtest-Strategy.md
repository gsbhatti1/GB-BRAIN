> Name

Fisher Transform Indicator Backtest Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1c4cdd0aa8c4bf7accf.png)
[trans]


### Overview

The Fisher Transform Indicator backtest strategy calculates the Fisher transform of prices to identify price reversal points and generate trading signals. The strategy processes prices using the Fisher transform formula to remove non-Gaussian features of price distributions, resulting in a standardized indicator with an approximate Gaussian distribution. The strategy determines price reversals based on inflection points of the Fisher transform curve and produces long and short signals.

### Strategy Principle

The core of this strategy is to process prices using the Fisher transform formula to eliminate non-Gaussian features of natural price distributions. The Fisher transform formula is:  

\[ y = 0.5 \times \ln\left(\frac{1 + x}{1 - x}\right) \]

Here \( x \) is the processed price, obtained by first finding the highest and lowest prices over the most recent Length periods using the `highest` and `lowest` functions, and then normalizing as follows:

\[ x = \frac{\text{price} - \text{minimum}}{\text{maximum} - \text{minimum}} - 0.5 \]

Prices processed this way approximate a Gaussian distribution. \( x \) is then substituted into the Fisher transform formula to obtain the Fisher transform curve. Inflection points in the Fisher transform curve signal price reversals.

When the Fisher transform curve turns from positive to negative, a sell signal is generated. When it turns from negative to positive, a buy signal is generated.

### Advantage Analysis

1. The Fisher transform removes non-Gaussian features from prices, resulting in more well-behaved, standardized prices and fewer false signals
2. Captures price reversal points, avoiding chasing tops and bottoms
3. Flexible parameter adjustment for tuning reversal sensitivity  
4. Customizable directionality, adapts to various market environments
5. Simple logic easy to understand and implement

### Risk Analysis   

1. Improper parameter settings may miss turns or generate false signals
2. Slippage in live trading may prevent perfect signal execution 
3. Hard to identify turns when prices are volatile

Solutions:  

1. Optimize parameters by adjusting Length 
2. Relax entry criteria appropriately to ensure fills
3. Filter false signals combining other indicators  
4. Strictly follow rules and manage risks

### Optimization Directions

1. Optimize Length parameter to find best combination
2. Add filters to avoid false signals e.g. moving averages, volatility indicators etc.  
3. Incorporate stop loss to control loss per trade
4. Add re-entry mechanism to track continuing trends  

### Conclusion

The Fisher Transform Indicator backtest strategy identifies price reversal points by removing non-Gaussian price features. It is an easily implemented mean reversion strategy. Its advantages lie in flexible parameters for catching turns while its main weakness is the difficulty of live implementation with the need for strict entry rules. Various methods can be used to optimize this strategy for practical applicability.

||

### Overview

The Fisher Transform backtest strategy calculates the Fisher transform of prices to identify price reversal points and generate trading signals accordingly. The strategy processes prices using the Fisher transform formula to remove non-Gaussian features of price distributions, resulting in a standardized indicator with an approximate Gaussian distribution. The strategy determines price reversals based on inflection points of the Fisher transform curve and produces long and short signals.

### Strategy Principle

The core of this strategy is to process prices using the Fisher transform formula to eliminate non-Gaussian features of natural price distributions. The Fisher transform formula is:  

\[ y = 0.5 \times \ln\left(\frac{1 + x}{1 - x}\right) \]

Here \( x \) is the processed price, obtained by first finding the highest and lowest prices over the most recent Length periods using the `highest` and `lowest` functions, and then normalizing as follows:

\[ x = \frac{\text{price} - \text{minimum}}{\text{maximum} - \text{minimum}} - 0.5 \]

Prices processed this way approximate a Gaussian distribution. \( x \) is then substituted into the Fisher transform formula to obtain the Fisher transform curve. Inflection points in the Fisher transform curve signal price reversals.

When the Fisher transform curve turns from positive to negative, a sell signal is generated. When it turns from negative to positive, a buy signal is generated.

### Advantage Analysis

1. The Fisher transform removes non-Gaussian features from prices, resulting in more well-behaved, standardized prices and fewer false signals
2. Captures price reversal points, avoiding chasing tops and bottoms
3. Flexible parameter adjustment for tuning reversal sensitivity  
4. Customizable directionality, adapts to various market environments
5. Simple logic easy to understand and implement

### Risk Analysis   

1. Improper parameter settings may miss turns or generate false signals
2. Slippage in live trading may prevent perfect signal execution 
3. Hard to identify turns when prices are volatile

Solutions:  

1. Optimize parameters by adjusting Length 
2. Relax entry criteria appropriately to ensure fills
3. Filter false signals combining other indicators  
4. Strictly follow rules and manage risks

### Optimization Directions

1. Optimize Length parameter to find best combination
2. Add filters to avoid false signals e.g. moving averages, volatility indicators etc.  
3. Incorporate stop loss to control loss per trade
4. Add re-entry mechanism to track continuing trends  

### Conclusion

The Fisher Transform backtest strategy identifies price reversal points by removing non-Gaussian price features. It is an easily implemented mean reversion strategy. Its advantages lie in flexible parameters for catching turns while its main weakness is the difficulty of live implementation with the need for strict entry rules. Various methods can be used to optimize this strategy for practical applicability.

||

### Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|Length|
|v_input_2|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v2.0 22/12/2016
//  Market prices do not have a Gaussian probability density function
//  as many traders think. Their probability curve is not bell-shaped.
//  But trader can create a nearly Gaussian PDF for prices by normalizing
//  them or creating a normalized indicator such as the relative strength
//  index and applying the Fisher transform. Such a transformed output 
//  creates the peak swings as relatively rare events.
//  Fisher transform formula is: y = 0.5 * ln ((1+x)/(1-x))
//  The sharp turning points of these peak swings clearly and unambiguously
//  identify price reversals in a timely manner.
//
//  For signal used zero.
// You can change long to short in the Input Settings
// Please, use it only for learning or paper trading. Do not for real trading.
////////////////////////////////////////////////////////////
strategy(title="Fisher Transform Indicator by Ehlers Backtest", shorttitle="Fisher Transform Indicator by Ehlers")
Length = input(10, minval=1)
reverse = input(false, title="Trade reverse")
hline(0, color=color.blue)
xHL2 = hl2
xMaxH = highest(xHL2, Length)
xMinL = lowest(xHL2, Length)
nValue1 = 0.33 * 2 * ((xHL2 - xMinL) / (xMaxH - xMinL) - 0.5) + 0.67 * nz(nValue1[1])
nValue2 = iff(nValue1 > 0, nValue1, nValue2)
plot(nValue2, color=color.red)

// Implement the rest of the strategy logic here
```