> Name

Multi-indicator-Assisted-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy combines the use of EMA, RSI, MACD, PSAR, Bollinger Bands, and other technical indicators to comprehensively judge price trends from multiple angles, finding optimal entry points. It provides multiple parameter setting options for customizable personalized strategies.

## Strategy Logic

1. Use 3 EMAs (5-period, 9-period, 21-period) to determine the price trend; EMA crossovers indicate trend changes.

2. RSI judges overbought/oversold levels. RSI below the lower level signifies oversold; above the upper level, overbought.

3. MACD checks the moving average difference. DIFF crossing above DEA is a bullish signal, and below is a bearish signal.

4. PSAR indicates the current trend direction for additional context.

5. Bollinger Bands show support and resistance levels. Price breaking the bands suggests a trend change.

6. Take long/short positions when the indicators give aligned signals based on user selection.

## Advantages

1. Multiple indicators avoid misleading signals from a single indicator.

2. Customizable parameters allow users to select optimal combinations.

3. Accurate trend change detection from EMA, MACD, etc.

4. RSI efficiently identifies overbought/oversold opportunities.

5. PSAR and Bollinger Bands reveal turning points.

## Risks

1. Fewer multi-indicator signal occurrences may miss good opportunities.

2. No filtering when a single indicator gives a false signal.

3. Users may choose suboptimal parameter sets leading to over/undertrading.

4. No risk management limits like STOP LOSS.

5. Insufficient backtest data to fully validate the strategy.

Possible solutions:

1. Widen indicator thresholds to provide more signals.

2. Add other indicators to filter out false signals.

3. Provide more indicator options for users to test combinations.

4. Incorporate stop loss and other risk management measures.

5. Backtest on more markets to optimize parameters.

## Optimization Directions

1. Test more indicator combinations to find the best matches.

2. Add machine learning modules for more data-driven improvements.

3. Incorporate trend filtering to determine the trade direction.

4. Optimize money management strategies for various market environments.

5. Develop auto-parameter optimization programs for intelligent improvements.

## Summary

This strategy applies multiple technical indicators for comprehensive trend analysis, avoiding overreliance on a single indicator. It can be further enhanced via parameter tuning, adding validation modules, integrating AI, etc., to provide more quality signals while maintaining robustness.

| Argument | Default | Description |
| --- | --- | --- |
| v_input_1 | 0 | Strategy: rsi | ema | macd | psr | off | BB | ema5 |
| v_input_2 | 0 | Background color: rsi | ema | macd | psr | off | exchange | BB | ema5 |
| v_input_3 | false | Show ema5? |
| v_input_4 | true | Show ema9? |
| v_input_5 | true | Show ema21? |
| v_input_6 | false | Show ema50? |
| v_input_7 | false | Show ema100? |
| v_input_8 | true | Show ema200 |
| v_input_9 | true | Color oversold and overbought bars? |
| v_input_10 | true | Show Parabolic Sar |
| v_input_11 | true | Show Bollinger Bands? |
| v_input_12 | false | Show Daily Pivots? |
| v_input_13 | true | linewidth |
| v_input_14 | true | sar points width |
| v_input_15 | 40 | oversold rsi |
| v_input_16 | 65 | overbought rsi |

> Source (PineScript)

```pinescript
//@version=3
strategy("f.society", title="f.society", overlay=true)
//@Author: rick#1414
// -----------------------------------------------------
// f.society : Pone 3EMA: 5, 9, 21, 50, 100, 200, SAR, 
// velas azules en sobreventa y velas moradas sobre compra 
// SAR 0.02, 0.02, 0.2 , Bandas de Bollinger
// estrategia de compra y venta con rsi, macd o psr
// color de fondo: ema, rsi (color azul sobreventa 35, 25 (mas intenso))
// -----------------------------------------------------
// Como agregar a Trading view:
// 1 Cerrar todos los otros indicadores antes de añadirlo
// 2. Ir a la página de inicio TradingView.com
// 3. En la parte inferior, haga clic en Editor Pine // ver imagen: // https://cdn.discordapp.com/attachments/407267549047422976/407393815112974336/unknown.png
// 4. Borrar todo el texto y reemplazar con todo el contenido de este archivo
// 5. Pulse el botón "Añadir a trazar" (Add to graph)
// -----------------------------------------------------
// revisar opciones de on y off segun indicadores deseados
// https://cdn.discordapp.com/attachments/405885820114042883/412115277883506700/unknown.png
// se puede cambiar la estrategia desde este menu desplegable para señales buy/sell

// Options
estrategia = input(defval="rsi", title = "Strategy", options=["ema","rsi","macd","psr","off","BB","ema5"])
in_bkcolor = input(defval="rsi", title = "background color", options=["ema","rsi","macd","psr","off","exchange","BB","ema5"])
e5 = in
```