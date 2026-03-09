> Name

Adaptive Range Trading System Based on Dual RSI Indicators

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ac6a3f823407eb811a.png)

[trans]
#### Overview
This strategy is an adaptive trading system based on dual RSI (Relative Strength Index) indicators. It combines RSI indicators from different timeframes to identify market trends and trading opportunities, while optimizing trading performance through money management and risk control mechanisms. The core strength of the strategy lies in the synergy between multi-period RSIs to enhance profitability while maintaining trading safety.

#### Strategy Principles
The strategy uses a 7-period RSI indicator as the primary trading signal, combined with a daily RSI as a trend filter. A long position is initiated when the short-period RSI breaks above 40 and the daily RSI is above 55. If the price drops below the initial entry price during a position, the system automatically adds to the position to lower the average cost. Positions are closed when RSI breaks below from above 60. A 5% stop-loss is implemented for risk control. The strategy also includes a money management module that automatically calculates position sizes based on total capital and preset risk ratios.

#### Strategy Advantages
1. Multi-period RSI combination improves signal reliability.
2. Adaptive position averaging mechanism effectively reduces holding costs.
3. Comprehensive money management system adjusts positions based on risk preference.
4. Fixed stop-loss protection strictly controls risk per trade.
5. Considers trading costs for more realistic trading conditions.

#### Strategy Risks
1. RSI indicators may generate false signals in volatile markets.
2. Position averaging mechanism may lead to significant losses in continuous downtrends.
3. Fixed percentage stop-loss may be too conservative in high volatility periods.
4. Trading costs can significantly impact returns during frequent trading.
5. Strategy execution requires sufficient liquidity.

#### Optimization Directions
1. Incorporate volatility indicators (like ATR) for dynamic stop-loss adjustment.
2. Add trend strength filters to reduce false signals in ranging markets.
3. Optimize position averaging logic with dynamic adjustments based on market volatility.
4. Include RSI confirmations from additional timeframes.
5. Develop adaptive position sizing system.

#### Summary
This is a complete trading system combining technical analysis and risk management. It generates trading signals through multi-period RSI coordination while controlling risk through money management and stop-loss mechanisms. The strategy is suitable for trending markets but requires parameter optimization based on actual market conditions. The system's good extensibility leaves room for further optimization.

#### Source (PineScript)

```pinescript
/*backtest
start: 2024-11-12 00:00:00
end: 2024-12-11 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Dual RSI with Rebuy Logic + Capital, Commission, and Stop Loss", overlay=true)

// Parameters
rsi_length = input.int(7, title="RSI Length")
daily_rsi_length = input.int(7, title="Daily RSI Length")
capital = input.float(10000, title="Initial Capital", minval=0)  // Initial capital
risk_per_trade = input.float(0.01, title="Risk per Trade (%)", minval=0.01, maxval=1.0)  // Risk per trade in percentage
commission = input.float(0.1, title="Commission (%)", minval=0, maxval=100)  // Commission in percentage
stop_loss_pct = input.float(5, title="Stop Loss (%)", minval=0.1, maxval=100)  // Stop loss percentage

// Order size calculation
risk_amount = capital * risk_per_trade
order_size = risk_amount / close  // Order size based on risk amount and price

// Daily RSI
day_rsi = request.security(syminfo.tickerid, "D", ta.rsi(close, daily_rsi_length), lookahead=barmerge.lookahead_on)

// RSI on current timeframe
rsi = ta.rsi(close, rsi_length)

// Buy and sell conditions
buy_condition = rsi[1] < 40 and rsi > rsi[1] and day_rsi > 55
sell_condition = rsi[1] > 60 and rsi < rsi[1]

// Variables to store the price of the first buy
var float first_buy_price = na
var bool is_position_open = false

// Buy logic
if buy_condition
    if not is_position_open
        // Initial buy signal
        strategy.entry("Buy", strategy.long, qty=1)
        first_buy_price := close
        is_position_open := true
    else if close < first_buy_price
        // Rebuy signal, only when price lower than the initial buy price
        strategy.entry("Rebuy", strategy.long, qty=1)

// Sell logic
if sell_condition and is_position_open
    strategy.close("Buy")
    strategy.close("Rebuy")
    first_buy_price := na  // Reset the buy price
    is_position_open := false

// Stop loss condition
if is_position_open
    // Calculate stop loss price (5% below entry price)
    stop_loss_price = first_buy_price * (1 - stop_loss_pct / 100)
    
    // Stop loss for "Buy" and "Rebuy"
```