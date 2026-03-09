> Name

Low-Pyramid-Risk-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/190799ca3c70c5fb0ef.png)
[trans]

This strategy identifies potential low points in price movement through a combination of different indicators and gradually builds positions through pyramiding to reduce risk. The strategy also incorporates functions such as stop loss, take profit, and trailing stop loss to effectively control risk.

## Strategy Overview

The strategy first uses the difference between RSI and EMA RSI to identify potential price lows. To filter out false signals, the strategy also combines moving average and multi-timeframe stochastic indicator for confirmation. Once the low point signal is confirmed, long positions will be gradually built at slightly lower prices from that point through pyramiding. The strategy allows up to 12 tracking orders to be opened, with the size of each order increasing in sequence, which can effectively diversify risks. All orders will follow an overall stop loss to exit, while allowing to set take profit separately for each order. To further control risks, the strategy also sets an overall stop loss based on equity percentage.

## Strategy Principle

The strategy consists of three main modules: low point identification, pyramid tracking, and risk control.

The **low point identification module** uses the difference between RSI and its EMA to identify potential price lows. To improve accuracy, moving average indicator and multi-timeframe stochastic indicators are introduced for signal filtering. Only when the price is below the moving average and the stochastic K line is below 30, the validity of the low point signal will be confirmed.

The **pyramid tracking module** is the core of this strategy. Once the low point signal is confirmed, the strategy will open the first position at 0.1% below that low point. Afterwards, as long as the price keeps falling and is below a certain percentage of the average entry price, more long orders will be added. The size of new orders will increase in sequence, for example, the third order is 3 times the first order size. This pyramid tracking approach helps in averaging risks. The strategy allows up to 12 tracking orders.

The **risk control module** includes three aspects. First is the overall stop loss based on the highest price in recent periods. All orders will follow this stop loss. Second is independent take profit setting for each order, which allows to close the order based on a certain percentage of the entry price. Third is an overall stop loss based on the percentage of account equity, which is the strongest risk control method.

## Strategy Advantages

- Pyramid tracking reduces the risk of individual orders while diversifying overall risk.
- The combination of multiple indicators improves the accuracy of low point identification.
- Overall stop loss, take profit, and trailing stop functions effectively control risk.
- Equity stop loss mechanism protects the account from significant losses.
- Parameters can be tuned to balance risk vs reward.

## Strategy Risks

- Low point identification still has some limitations, which may miss the best entry point or enter false signals.
- Adding orders when facing adverse market conditions may increase losses.
- The strategy needs a relatively long period to reflect its advantages.
- Inappropriate parameter setting may lead to insufficient risk control.

To reduce these risks, the following aspects can be optimized:

1. Change or add indicators to improve low point identification accuracy.
2. Optimize the number of orders, intervals, and take profit percentage, etc., to reduce the risk per order.
3. Moderately tighten the stop loss level to protect profits.
4. Test different products with good liquidity and large fluctuations.

## Strategy Optimization

There is still room for further optimization of this strategy:

1. Try introducing more advanced techniques like machine learning for low point identification.
2. Dynamically adjust the order quantity, stop loss level, etc., based on market conditions.
3. Add a box stop loss mechanism to avoid expanding losses.
4. Add a re-entry mechanism.
5. Optimize parameters for stocks and cryptocurrency products.

## Summary

This strategy effectively reduces the risk of individual orders through the pyramid tracking approach. The overall stop loss, take profit, and trailing stop functions also play a very good role in risk control. However, there is still room for improvement in low point identification and other aspects. If more advanced techniques can be introduced, dynamic adjustment of parameters can be added, combined with parameter optimization, the risk/reward ratio of this strategy will significantly improve.