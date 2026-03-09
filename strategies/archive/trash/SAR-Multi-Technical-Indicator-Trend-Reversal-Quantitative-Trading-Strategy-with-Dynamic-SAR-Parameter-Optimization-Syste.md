``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2025-02-18 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("ZigZag + Fractals + SAR Crossover Stratégiia", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Parametre ZigZag
zigzag_depth = input.int(5, title="ZigZag Hĺbka")
zigzag_deviation = input.float(5.0, title="ZigZag Odchýlka (%)") / 100

// Výpočet ZigZag
var float last_pivot = na
var bool is_uptrend = false  // Inicializované na false
zigzag_high = ta.pivothigh(high, zigzag_depth, zigzag_depth)
zigzag_low = ta.pivotlow(low, zigzag_depth, zigzag_depth)

if not na(zigzag_high)
    last_pivot := zigzag_high
    is_uptrend := false
if not na(zigzag_low)
    last_pivot := zigzag_low
    is_uptrend := true

// Fraktály
fractal_up = ta.pivothigh(high, 2, 2)
fractal_down = ta.pivotlow(low, 2, 2)

// Parabolic SAR
sar = ta.sar(0.02, 0.2, 0.02)

// Prechody Parabolic SAR a Cena
sar_cross_up = ta.crossover(sar, close)  // SAR prechádza nad cenu
sar_cross_down = ta.crossunder(sar, close)  // SAR prechádza pod cenu

// Obchodné podmienky založené na
```