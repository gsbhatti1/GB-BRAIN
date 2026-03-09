> Name

Triple-Moving-Average-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/823831b8ea37647c22.png)
[trans]

Overview: This strategy is a typical technical analysis strategy that utilizes several common moving average indicators like EMA and auxiliary indicators like RSI, MACD, PSR to form entry and stop loss rules for finding low buy high sell opportunities.

Principle: The core of this strategy is the 5, 9, 21 day moving averages. When the short period MA crosses over the long period one, it signals an uptrend; when the short period MA crosses below the long period one, it signals a downtrend. In addition, RSI is used to determine overbought and oversold levels, MACD to judge the trend, PSR to identify support and resistance for combo trading. The background color shows market sentiment to assist trend judgment. The parameters are customizable for configuring entry rules.

Advantages:  
1. MA indicators give clear trend direction.
2. RSI effectively spots overbought/oversold levels, MACD judges short-long trend, PSR finds key price levels. The indicators are complementary.
3. Flexible entry rules and parameter settings.
4. Many optimizable indicators and parameter combinations adaptable to varying market conditions.

Risks:  
1. Short-term operations may fail to capture major trend and miss reversals.
2. Improper parameter configuration can lead to too many false signals or missing good signals.
3. Pure technical indicators are susceptible to manipulation by arbitrageurs causing losses.
4. Prone to being stopped out in high volatile markets.

Solutions:
1. Capture mid-long term trend appropriately to avoid trading against major trend.
2. Optimize parameters, use stop loss to control risks.
3. Watch out the possibilities of pullback from highs and bounce from lows.

Optimization:
1. Fine tune MA parameters for best combo.
2. Add more indicators to filter signals.
3. Increase machine learning metrics for probability estimate.
4. Combine volume changes to enhance signal accuracy.
5. Add stop loss to restrict loss expansion.

Summary: This strategy integrates multiple auxiliary signals, leverages the strength of MA indicators to identify short-term low buy high sell chances. Parameters and indicators combinations may be optimized continuously to improve strategy efficacy, but operation frequency and risks should be moderated to prevent oversized single trade loss from eroding overall profitability.

[/trans]

||

Overview: This strategy is a typical technical analysis strategy that utilizes several common moving average indicators like EMA and auxiliary indicators like RSI, MACD, PSR to form entry and stop loss rules for finding low buy high sell opportunities.

Principle: The core of this strategy is the 5, 9, 21 day moving averages. When the short period MA crosses over the long period one, it signals an uptrend; when the short period MA crosses below the long period one, it signals a downtrend. In addition, RSI is used to determine overbought and oversold levels, MACD to judge the trend, PSR to identify support and resistance for combo trading. The background color shows market sentiment to assist trend judgment. The parameters are customizable for configuring entry rules.

Advantages:  
1. MA indicators give clear trend direction.
2. RSI effectively spots overbought/oversold levels, MACD judges short-long trend, PSR finds key price levels. The indicators are complementary.
3. Flexible entry rules and parameter settings.
4. Many optimizable indicators and parameter combinations adaptable to varying market conditions.

Risks:  
1. Short-term operations may fail to capture major trend and miss reversals.
2. Improper parameter configuration can lead to too many false signals or missing good signals.
3. Pure technical indicators are susceptible to manipulation by arbitrageurs causing losses.
4. Prone to being stopped out in high volatile markets.

Solutions:
1. Capture mid-long term trend appropriately to avoid trading against major trend.
2. Optimize parameters, use stop loss to control risks.
3. Watch out the possibilities of pullback from highs and bounce from lows.

Optimization:
1. Fine tune MA parameters for best combo.
2. Add more indicators to filter signals.
3. Increase machine learning metrics for probability estimate.
4. Combine volume changes to enhance signal accuracy.
5. Add stop loss to restrict loss expansion.

Summary: This strategy integrates multiple auxiliary signals, leverages the strength of MA indicators to identify short-term low buy high sell chances. Parameters and indicators combinations may be optimized continuously to improve strategy efficacy, but operation frequency and risks should be moderated to prevent oversized single trade loss from eroding overall profitability.

[/trans]

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|0|Strategy: rsi|ema|macd|psr|off|BB|ema5|
|v_input_2|0|background color: rsi|ema|macd|psr|off|exchange|BB|ema5|
|v_input_3|false|Show ema5?|
|v_input_4|true|Show ema9?|
|v_input_5|true|Show ema21?|
|v_input_6|false|Show ema50?|
|v_input_7|false|Show ema100?|
|v_input_8|true|Show ema200|
|v_input_9|true|Color oversold and overbought bars?|
|v_input_10|true|Show Parabolic Sar|
|v_input_11|true|Show Bollinger Bands?|
|v_input_12|false|Show Daily Pivots?|
|v_input_13|true|linewidth|
|v_input_14|true|sar points width|
|v_input_15|40|oversold rsi|
|v_input_16|65|overbought rsi|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-11-17 00:00:00
end: 2023-08-08 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("f.society v7", title="f.society v7", overlay=true)
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
// 4. borrar todo el texo y reemplazar con todo el contenido de este archivo
// 5. Pulse el botón "Añadir a trazar" (Add to graph)
// -----------------------------------------------------
// revisar opciones de on y off segun indicadores deseados
// https://cdn.discordapp.com/attachments/405885820114042883/412115277883506700/unknown.png
// se puede cambiar la estrategia desde este menu desplegable para señales buy/sell

// Options
estrategia = input(defval="rsi", title = "Strategy", options=["ema","rsi","macd","psr","off","BB","ema5"])
in_bkcolor = input(defval="rsi", title = "background color", options=["ema","rsi","macd","psr","off","exchange","BB","ema5"])
e5 = input(title="Show ema5?", type=bool, defval=false)
e9 = input(title="Show ema9?", type=bool, defval=true)
e21 = input(title="Show ema21?", type=bool, defval=true)
e50 = input(title="Show ema50?", type=bool, defval=false)
e100 = input(title="Show ema100?", type=bool, defval=false)
e200 = input(title="Show ema200?", type=bool, defval=true)
...