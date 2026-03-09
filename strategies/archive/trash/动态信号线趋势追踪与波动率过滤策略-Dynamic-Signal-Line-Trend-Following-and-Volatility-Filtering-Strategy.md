```pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2024-10-31 23:59:59
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © DailyPanda

//@version=5
strategy("DSL Strategy [DailyPanda]",
     initial_capital = 2000,
     commission_value=0.00,
     slippage=3,
     overlay = true)

//--------------------------------------------------------------------------------------------------------------------
// USER INPUTS
//--------------------------------------------------------------------------------------------------------------------

// DSL Indicator Inputs CP
int   len         = input.int(34, "Length", group="CP")      // Length for calculating DSL
int   offset      = input.int(1, "Offset", group="CP")       // Offset for DSL calculation
float atrLen      = input.float(14, "ATR Length", group="Volatility")  // ATR length for volatility bands
float volLevel    = input.float(2.0, "Volatility Level", group="Volatility")  // Volatility level threshold

// Strategy Logic
//@version=5
strategy("DSL Strategy [DailyPanda]",
     initial_capital = 2000,
     commission_value=0.00,
     slippage=3,
     overlay = true)

//--------------------------------------------------------------------------------------------------------------------
// USER INPUTS
//--------------------------------------------------------------------------------------------------------------------

// DSL Indicator Inputs CP
int   len         = input.int(34, "Length", group="CP")      // Length for calculating DSL
int   offset      = input.int(1, "Offset", group="CP")       // Offset for DSL calculation
float atrLen      = input.float(14, "ATR Length", group="Volatility")  // ATR length for volatility bands
float volLevel    = input.float(2.0, "Volatility Level", group="Volatility")  // Volatility level threshold

// Strategy Logic
```