> Name

Dynamic-Balancing-Strategy-with-50-Funds-and-50-Positions

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/198847a3568ae2ba0ec.png)
[trans]
### Strategy Overview

This strategy dynamically balances between 50% funds and 50% positions to control risk. By continuously adjusting the ratio between funds and positions, it manages risk for investors who cannot monitor the market in real time.

### Strategy Logic

1. Initialize capital at 1 million, divided equally into 50% funds and 50% positions.

2. During the trading period, if remaining funds exceed unrealized profit/loss by 1.05 times at each open, use 2.5% of remaining funds to add positions.

3. If unrealized profit/loss exceeds remaining funds by 1.05 times, sell partial positions to restore balance.

4. Close all positions at the end of the trading period.

### Advantages

1. Effective risk control through dynamic balancing of funds and positions, avoiding huge losses in extreme market conditions.

2. Simple to operate for busy investors, only need to adjust fund/position ratios.

3. Customizable parameters to meet varying risk appetites.

### Risks

1. Unable to capitalize on short-term fluctuations, profit potential limited.

2. Long one-sided run may result in insufficient position size.

3. Improper parameter tuning leads to excess position flipping or low capital utilization.

### Enhancement Opportunities

1. Introduce more parameters for finer fund/position control.

2. Incorporate stop loss/profit taking for larger positions.

3. Test different trading period parameters to improve adaptability.

### Summary
This strategy achieves risk control by dynamically balancing between funds and positions. Simple to implement compared to other strategies. Can be further improved by introducing more adjustable parameters and combining with other strategy concepts.

||

### Strategy Overview

This strategy dynamically balances between 50% funds and 50% positions to control risk. By continuously adjusting the ratio between funds and positions, it manages risk for investors who cannot monitor the market in real time.

### Strategy Logic

1. Initialize capital at 1 million, divided equally into 50% funds and 50% positions.

2. During the trading period, if remaining funds exceed unrealized profit/loss by 1.05 times at each open, use 2.5% of remaining funds to add positions.

3. If unrealized profit/loss exceeds remaining funds by 1.05 times, sell partial positions to restore balance.

4. Close all positions at the end of the trading period.

### Advantages

1. Effective risk control through dynamic balancing of funds and positions, avoiding huge losses in extreme market conditions.

2. Simple to operate for busy investors, only need to adjust fund/position ratios.

3. Customizable parameters to meet varying risk appetites.

### Risks

1. Unable to capitalize on short-term fluctuations, profit potential limited.

2. Long one-sided run may result in insufficient position size.

3. Improper parameter tuning leads to excess position flipping or low capital utilization.

### Enhancement Opportunities

1. Introduce more parameters for finer fund/position control.

2. Incorporate stop loss/profit taking for larger positions.

3. Test different trading period parameters to improve adaptability.

### Conclusion
This strategy achieves risk control by dynamically balancing between funds and positions. Simple to implement compared to other strategies. Can be further improved by introducing more adjustable parameters and combining with other strategy concepts.

[/trans]

```pinescript
//@version=4
strategy("00631L Trading Simulation", shorttitle="Sim", overlay=true, initial_capital = 1000000)

//Set the principal
capital = 1000000

//Set buy and sell date ranges
start_date = timestamp(2020, 11, 4)
next_date = timestamp(2020, 11, 5)
sell_date = timestamp(2023, 10, 24)
end_date = timestamp(2023, 10, 25) //The end date is changed to October 25, 2023

// Determine whether it is during transaction
in_trade_period = true
// realized profit and loss
realized_profit_loss = strategy.netprofit
plot(realized_profit_loss, title="realized_profit_loss", color=color.blue)
// Unrealized P&L
open_profit_loss = strategy.position_size * open
plot(open_profit_loss, title="open_profit_loss", color=color.red)
//remaining funds
remaining_funds = capital + realized_profit_loss - (strategy.position_size * strategy.position_avg_price)
plot(remaining_funds, title="remaining_funds", color=color.yellow)
//Total equity
total_price = remaining_funds + open_profit_loss
plot(total_price, title="total_price", color=color.white)

//Buy logic: Buy daily_investment amount of products on each trading day during the trading period
first_buy = time >= start_date and time <= next_date
buy_condition = in_trade_period and dayofmonth != dayofmonth[1]
// Selling logic: Sell all items on the closing day of the trading period.
sell_all = time >= sell_date

// Buy 50% of the principal on the first day of the trading period
if (first_buy)
    strategy.order("First", strategy.long, qty = capital / 2 / open)

// Add logic: If remaining funds exceed unrealized profit/loss by 1.05 times at each open, use 2.5% of remaining funds to add positions.
add_positions = not sell_all and realized_profit_loss < remaining_funds * 1.05
if (add_positions)
    strategy.order("Add", strategy.long, qty = remaining_funds * 0.025 / open)

// Sell logic: If unrealized profit/loss exceeds remaining funds by 1.05 times, sell partial positions to restore balance.
sell_partially = not sell_all and realized_profit_loss > remaining_funds * 1.05
if (sell_partially)
    strategy.close("First", qty = strategy.position_size / 2)

// Close all positions at the end of the trading period
if (time >= end_date)
    strategy.close_all()
```