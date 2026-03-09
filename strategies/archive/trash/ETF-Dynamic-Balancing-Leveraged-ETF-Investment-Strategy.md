> Name

Dynamic Balancing Two-way Tracking Leveraged ETF Investment Strategy Dynamic-Balancing-Leveraged-ETF-Investment-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/e20a71f1a3e9eea3b0.png)
[trans]
### Overview

This strategy uses Hong Kong Hang Seng Index ETF (00631L) as the investment target, and balances the return and risk of the investment portfolio in real time by dynamically adjusting cash positions and position proportions. The strategy is simple and easy to implement, and there is no need to judge market trends. It is suitable for investors who cannot check the market frequently.

### Strategy Principles

1. Initially invest 50% of the total funds to purchase 00631L;
2. Monitor the ratio of unrealized gains and remaining cash;

- When unrealized gains exceed 10% of remaining cash, close 5% of the position;
- When the remaining cash exceeds 10% of unrealized gains, purchase an additional 5% position;

3. Dynamically adjust positions and cash ratios to control portfolio returns and risks.

### Advantage Analysis

1. Simple and easy to operate, no need to judge the market;
2. Dynamically adjust positions and effectively control investment risks;
3. Two-way tracking, timely stop loss and profit;
4. Suitable for investors who cannot check the market frequently.


### Risks and Countermeasures

1. Leveraged ETFs are highly volatile;

- Use gradual position building and invest in batches at intervals.

2. Unable to stop losses in time;

- Set a stop loss line to control the maximum loss.

3. Transaction costs are high;

- Appropriately relax the balance range and reduce position adjustments.

### Optimization Ideas

1. Optimize position and cash ratio;
2. Test the income effects of different ETF varieties;
3. Add trend judgment indicators to improve capital utilization efficiency.

### Summary

This strategy controls investment risks by building a dynamically balanced investment portfolio without judging market trends. It is simple to operate and suitable for investors who cannot frequently check the market. It is a very practical quantitative investment strategy.

||

### Overview

This strategy takes Hong Kong Hang Seng Index ETF (00631L) as the investment target and dynamically adjusts the cash position and position ratio to balance the return and risk of the investment portfolio in real time. The strategy is simple and easy to implement without the need to judge market trends and is suitable for investors who cannot frequently check the market.

### Principles

1. Initially invest 50% of the total funds to purchase 00631L;
2. Monitor the ratio between unrealized profit and remaining cash;

- Sell 5% of position when unrealized profit exceeds remaining cash by 10%;
- Add 5% to position when remaining cash exceeds unrealized profit by 10%;

3. Dynamically adjust position and cash ratio to control portfolio return and risk.

### Advantage Analysis

1. Simple and easy to operate without the need to judge market conditions;
2. Dynamically adjusting positions effectively manages investment risk;
3. Two-way tracking to timely stop loss or take profit;
4. Suitable for investors who cannot frequently check the market.

### Risks and Mitigations

1. Leveraged ETFs have higher volatility;

- Adopt gradual position building and spaced investments.

2. Unable to timely stop loss;

- Set stop loss line to control maximum loss.

3. Higher trading costs;

- Relax balancing range to reduce position adjustments.

### Optimization Ideas

1. Optimize position and cash ratio;
2. Test return effectiveness across different ETF products;
3. Incorporate trend indicators to improve capital utilization efficiency.


### Conclusion

By constructing a dynamic balancing portfolio, this strategy controls investment risks without the need to judge market trends. Simple to operate, it is a highly practical quantitative investment strategy suitable for investors who cannot frequently check the market.

[/trans]

> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-24 23:59:59
Period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("00631L Trading Simulation", shorttitle="Sim", overlay=true, initial_capital = 1000000)

//Set the principal
capital=1000000

//Set buy and sell date ranges
start_date = timestamp(2022, 10, 6)
next_date = timestamp(2022, 10, 7) // Better starting date
//start_date = timestamp(2022, 3, 8)
//next_date = timestamp(2022, 3, 9) // Poor starting date
sell_date = timestamp(2024, 1, 19)
end_date = timestamp(2024, 1, 21) // The end date is January 21, 2024

// Determine whether it is during transaction
in_trade_period = time >= start_date and time <= end_date
// realized profit and loss
realized_profit_loss = strategy.netprofit
plot(realized_profit_loss, title="realized_profit_loss", color=color.blue)
// Unrealized P&L
open_profit_loss = strategy.position_size * open
plot(open_profit_loss, title="open_profit_loss", color=color.red)
// remaining funds
remaining_funds = capital + realized_profit_loss - (strategy.position_size * strategy.position_avg_price)
plot(remaining_funds, title="remaining_funds", color=color.yellow)
// Total equity
total_price = remaining_funds + open_profit_loss
plot(total_price, title="total_price", color=color.white)
// Buy logic: Buy daily_investment amount of products on each trading day during the trading period
first_buy = time >= start_date and time <= next_date
buy_condition = in_trade_period and dayofmonth != dayofmonth[1]
// Selling logic: Sell all items on the closing day of the trading period.
sell_all = time >= sell_date

// Buy 50% of the principal on the first day of the trading period
if (first_buy)
    strategy.order("First", strategy.long, qty=capital/2/open)
//Buy at the opening of each K-line

// Adding logic: Remaining funds > Unrealized profit and loss * 1.05
add_logic = remaining_funds > open_profit_loss * 1.05
if (add_logic)
    // Add more code here to place a new order for additional positions if needed.
```
