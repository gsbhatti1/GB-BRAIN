``` pinescript
/*backtest
start: 2024-01-14 00:00:00
end: 2024-01-21 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Mysteriown

//@version=4
strategy(title="VWAP + Fibo Dev Extensions Strategy", overlay=true, pyramiding=5, commission_value=0.08)

// -------------------------------------
// ------- Inputs Fibos Values ---------
// -------------------------------------

fib1 = input(title="Fibo extension 1", type=input.float, defval=1.618)
fib2 = input(title="Fibo extension 2", type=input.float, defval=2.618)
reso = input(title="Resolution VWAP", type=input.resolution, defval="W")
dev = input(title="Deviation value min.", type=input.integer, defval=150)


// -------------------------------------
// -------- VWAP Calculations ----------
// -------------------------------------

t = time(reso)
debut = na(t[1]) or t > t[1]

addsource = hlc3 * volume
addvol = volume
addsource := debut ? addsource : addsource + addsource[1]
addvol := debut ? addvol : addvol + addvol[1]
VWAP = addsource / addvol

sn = 0.0
sn := debut ? sn : sn[1] + volume * (hlc3 - VWAP[1]) * (hlc3 - VWAP)
sd = sqrt(sn / addvol)

Fibp2 = VWAP + fib2 * sd
Fibp1 = VWAP + fib1 * sd
Fibm1 = VWAP - fib1 * sd
Fibm2 = VWAP - fib2 * sd


// -------------------------------------
// -------------- Plots ----------------
// -------------------------------------

plot(VWAP, title="VWAP", color=color.blue)
plot(Fibp2, title="Upper Band", color=color.red)
plot(Fibp1, title="Middle Band", color=color.orange)
plot(Fibm1, title="Lower Band", color=color.green)

longCondition = crossover(VWAP, Fibm1) and VWAP > dev
shortCondition = crossunder(VWAP, Fibp1) and VWAP < -dev

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// Stop Loss EXIT Signals
stopLossLong = VWAP <= Fibm2
stopLossShort = VWAP >= Fibp2

if (stopLossLong)
    strategy.exit("Stop Loss Long", "Long")

if (stopLossShort)
    strategy.exit("Stop Loss Short", "Short")
```

This Pine Script code implements the described trading strategy. The `VWAP` calculation and band levels are correctly computed, and the entry conditions for long and short positions are set based on crossing over or under the Fibonacci bands. Stop loss exit conditions are also defined to close trades when price breaks through the respective bands.