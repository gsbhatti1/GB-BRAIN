> Name

Dynamic-Balancing-Strategy-with-50-Funds-and-50-Positions

> Author

ChaoZhang

### Strategy Overview

This strategy dynamically balances between 50% funds and 50% positions, achieving risk control by constantly adjusting the proportion of positions and funds. It is suitable for investors who cannot monitor the market in real time.

### Strategy Principles

1. The initial capital is set to 1 million yuan, with 50% allocated as funds and 50% as positions.
2. During each trading cycle, if the remaining funds exceed 1.05 times the unrealized profit or loss at the opening of the day, an additional 2.5% of the remaining funds will be used to increase the position size.
3. If the unrealized profit or loss exceeds 1.05 times the remaining funds, part of the positions will be sold to restore balance.
4. Positions are closed at the end of the trading period.

### Strategic Advantages

1. Through dynamic fund and position balancing, risks can be effectively controlled, minimizing huge losses in extreme market conditions.
2. No need for frequent market monitoring; only periodic adjustments of funds and positions are required, making it suitable for busy investors.
3. Adjustable parameters enable different levels of risk tolerance to cater to various investor needs.

### Strategy Risk

1. Inability to capture short-term fluctuations, resulting in limited profit margins.
2. Long-term one-sided markets may result in insufficient position sizes, missing out on full market opportunities.
3. Improper parameter settings can lead to excessive frequent position adjustments or inefficient capital utilization.

### Strategy Optimization

1. Introducing more parameters can achieve finer control over positions and capital ratios.
2. Combining stop-loss and stop-profit principles can appropriately manage risks for larger positions.
3. Testing different trading cycle parameter settings can enhance the adaptability of the strategy.

### Summary

This strategy achieves risk control through dynamic fund and position balancing, making it simple to operate and implement compared to other strategies. Future improvements can be made by introducing more adjustable parameters and integrating with other strategic ideas.

||

### Strategy Overview

This strategy dynamically balances between 50% funds and 50% positions for effective risk management. By continuously adjusting the ratio of funds to positions, it allows investors who cannot monitor the market in real time to manage their risks simply.

### Strategy Logic

1. Initialize capital at 1 million yuan, divided equally into 50% funds and 50% positions.
2. During the trading period, if remaining funds exceed unrealized profit/loss by 1.05 times at each open, use 2.5% of remaining funds to add positions.
3. If unrealized profit/loss exceeds remaining funds by 1.05 times, sell partial positions to restore balance.
4. Close all positions at the end of the trading period.

### Advantages

1. Effective risk control through dynamic fund and position balancing, avoiding huge losses in extreme market conditions.
2. Simple to operate for busy investors, only needing to adjust the fund/position ratios.
3. Customizable parameters to meet varying risk appetites.

### Risks

1. Unable to capitalize on short-term fluctuations, resulting in limited profit potential.
2. Long-term one-sided markets may result in insufficient position sizes.
3. Improper parameter tuning can lead to excessive frequent position adjustments or inefficient capital utilization.

### Enhancement Opportunities

1. Introduce more parameters for finer fund/position control.
2. Incorporate stop loss/profit taking rules for larger positions.
3. Test different trading period parameter settings to improve adaptability of the strategy.

### Conclusion
This strategy achieves risk control through dynamic balancing between funds and positions, making it simple to implement compared to other strategies. Further improvements can be made by introducing more adjustable parameters and combining with other strategic concepts.

```pinescript
/*backtest
start: 2023-12-17 00:00:00
end: 2023-12-18 19:00:00
Period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("00631L Trading Simulation", shorttitle="Sim", overlay=true, initial_capital = 1000000)

// Set the principal
capital=1000000

// Set buy and sell date ranges
start_date = timestamp(2020, 11, 4)
next_date = timestamp(2020, 11, 5)
sell_date = timestamp(2023, 10, 24)
end_date = timestamp(2023, 10, 25) // The end date is changed to October 25, 2023

// Determine whether it is during the trading period
in_trade_period = true
// Realized profit and loss
realized_profit_loss = strategy.netprofit
plot(realized_profit_loss, title="Realized Profit/Loss", color=color.blue)
// Unrealized P&L
open_profit_loss = strategy.position_size * open
plot(open_profit_loss, title="Open Profit/Loss", color=color.red)
// Remaining funds
remaining_funds = capital + realized_profit_loss - (strategy.position_size * strategy.position_avg_price)
plot(remaining_funds, title="Remaining Funds", color=color.yellow)
// Total equity
total_price = remaining_funds + open_profit_loss
plot(total_price, title="Total Equity", color=color.white)

// Buy logic: Buy daily investment amount of products on each trading day during the trading period
first_buy = time >= start_date and time <= next_date
buy_condition = in_trade_period and dayofmonth != dayofmonth[1]
// Selling logic: Sell all items on the closing day of the trading period.
sell_all = time >= sell_date

// Buy 50% of the principal on the first day of the trading period
if first_buy
    strategy.order("First", strategy.long, qty = capital/2/open)
// Buy at the opening of each K-line
```