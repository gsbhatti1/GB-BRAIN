``` pinescript
/*backtest
start: 2023-11-29 00:00:00
end: 2023-12-06 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Description:
//This strategy is a refactored version of an EMA cross strategy with a normalized ATR filter and ADX control. 
//It aims to provide traders with signals for long positions based on market conditions defined by various indicators.

//How it Works:
//1. EMA: Uses short (8 periods) and long (20 periods) EMAs to identify crossovers.
//2. ATR: Uses a 14-period ATR, normalized to its 20-period historical range, to filter out noise.
//3. ADX: Uses a 14-period RMA to identify strong trends.
//4. Volume: Filters trades based on a 14-period SMA of volume.
//5. Super Trend: Uses a Super Trend indicator to identify the market direction.

//How to Use:
//- Buy Signal: Generated when EMA short crosses above EMA long, and other conditions like ATR and market direction are met.
//- Sell Signal: Generated based on EMA crossunder and high ADX value.

//Originality and Usefulness:
//This script combines EMA, ATR, ADX, and Super Trend indicators to filter out false signals and identify more reliable trading opportunities. 
//USD Strength is not working, just simulated it as PSEUDO CODE: [close>EMA(50)]

//Strategy Results:
//- Account Size: $1000
//- Commission: Not considered
//- Slippage: Not considered
//- Risk: Less than 5% per trade
//- Dataset: Aim for more than 100 trades for sufficient sample size

//Note: This script should be used for educational purposes and should not be considered as financial advice.

//Chart:
//- The script's output is plotted as Buy and Sell signals on the chart.
//- No other scripts are included for clarity.
//- Have tested with 30mins period
//- You are encouraged to play with parameters, let me know if you 

//@version=5
strategy("Advanced EMA Cross with Normalized ATR Filter, Controlling ADX", shorttitle="ALP V5", overlay=true )

// Initialize variables
var bool hasBought = false
var int barCountSinceBuy = 0

// Define EMA periods
emaShort = ta.ema(close, 8)
emaLong = ta.ema(close, 20)

```