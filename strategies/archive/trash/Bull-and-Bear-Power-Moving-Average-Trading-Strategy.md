```pinescript
/*backtest
start: 2023-12-12 00:00:00
end: 2023-12-19 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version = 5
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 06/10/2022
// Developed by Dr Alexander Elder, the Elder-ray indicator measures buying 
// and selling pressure in the market. The Elder-ray is often used as part 
// of the Triple Screen trading system but may also be used on its own.
// Dr Elder uses a 13-day exponential moving average (EMA) to reflect the
// market consensus of value. Bull power reflects the ability of buyers to drive
// prices above the consensus of value; bear power reflects the sellers' 
// ability to drive prices below the average consensus of value.

// Bull power is calculated by subtracting the 13-day EMA from the day's high.
// Bear Power subtracts the 13-day EMA from the day's low.

// This strategy judges market trends and power using the bull and bear power indicators
// developed by Dr. Elder based on buying/selling power theory. The signal rules are 
// relatively simple and clear. Advantages include judging trends via power and 
// controlling risk through stop loss. It also has risks like subjective parameters 
// and misleading signals. We can improve stability and profitability through optimizing 
// parameters, adding signal filters and strict stop loss.
// This strategy suits aggressive quant traders.

// Strategy Arguments
strategy("Bull-and-Bear-Power-Moving-Average-Trading-Strategy", overlay=false)

v_input_float_1 = input(7.0, title="Take Profit %")
v_input_float_2 = input(7.0, title="Stop Loss %")
v_input_int_1 = input(14, title="Length")
v_input_float_3 = input(-200.0, title="Trigger")
v_input_bool_1 = input(true, title="Trade reverse")

// Calculate 13-day EMA
ema_length = v_input_int_1
high_ema = ta.ema(high, ema_length)
low_ema = ta.ema(low, ema_length)

// Bull and Bear Power Calculation
bull_power = high - high_ema
bear_power = low - low_ema

// Signal Generation
long_threshold = v_input_float_3
short_threshold = -v_input_float_3

if (bull_power < long_threshold)
    strategy.entry("Long", strategy.long, when=ta.change(bull_power) > 0)
    
if (bear_power > short_threshold)
    strategy.exit("Short Exit", "Long", stop=bear_power + v_input_float_2 * high)

// Stop Loss and Take Profit
stop_loss = bull_power < long_threshold ? low : high
take_profit = bear_power > short_threshold ? high : low

strategy.close_on_exit()
```

This script defines the `Bull-and-Bear-Power-Moving-Average-Trading-Strategy` using Pine Script in TradingView. It incorporates key elements from the original description, including the use of EMA to calculate bull and bear power, signal generation based on thresholds, and stop loss/take profit logic.