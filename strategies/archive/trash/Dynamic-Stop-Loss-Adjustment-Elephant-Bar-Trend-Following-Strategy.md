``` pinescript
/*backtest
start: 2024-12-17 00:00:00
end: 2025-01-16 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

//@version=6
strategy("Dynamic Stop Loss Adjustment Elephant Bar Trend Following Strategy", overlay=true)

// Configurable Parameters
num_barras = input.int(15, title="Number of Bars for Average", minval=1, maxval=100)
percentual_fechamento_valido = input.float(10, title="Valid Close Percentage Range (%)", minval=1, maxval=100)
percentual_condicao_tamanho = input.float(1.8, title="Size Multiplier of Average Bar", minval=0.1, step=0.1)
percentual_lucro = input.float(1.8, title="% Profit Target Referring to Bar Size", minval=0.1, step=0.1)

var bool executou_entrada = false

// Calculate the size of each bar
barra_tamanho = math.abs(close - open)

// Calculate the average size of the last 'num_barras' bars
media_tamanho = ta.sma(barra_tamanho, num_barras)

// Define variables for candle body, upper shadow and lower shadow
corpo = barra_tamanho
sombra_superior = high - math.max(close, open)
sombra_inferior = math.min(close, open) - low

// Conditions to check if the shadow is at least 2x larger than the body
sombra_sup_maior = sombra_superior >= 2 * corpo
sombra_inf_maior = sombra_inferior >= 2 * corpo

// Define minimum ratio between shadow and body
relacao_minima = 2.0

fechamento_valido = (close >= high - (percentual_fechamento_valido / 100) * (high - low)) or (close <= low + (percentual_fechamento_valido / 100) * (high - low))

// Condition to identify "elephant bars"
elefante_bar = sombra_sup_maior and (sombra_inferior <= relacao_minima * corpo)
elefante_bar_down = sombra_inf_maior and (sombra_superior <= relacao_minima * corpo)

// Define the entry direction based on elephant bar direction
dir_trade = na
if (bar_index == 1)
    if (elefante_bar or elefante_bar_down)
        if close > open
            dir_trade := 1
        else if close < open
            dir_trade := -1

// Set initial stop-loss and profit target
stop_loss = na
profit_target = na
if (dir_trade == 1)
    stop_loss := low[2]
    profit_target := high * (1 + percentual_lucro / 100)
else if (dir_trade == -1)
    stop_loss := high[2]
    profit_target := low * (1 - percentual_lucro / 100)

// Adjust stop-loss dynamically based on price movement
if (dir_trade == 1 and close > stop_loss)
    if (close >= profit_target * 0.6)
        stop_loss := ta.valuewhen(close >= profit_target * 0.6, high[2], 0)
    else if (close >= profit_target * 0.8)
        stop_loss := ta.valuewhen(close >= profit_target * 0.8, low[1], 0)
    else if (close >= profit_target * 0.9)
        stop_loss := ta.valuewhen(close >= profit_target * 0.9, high, 0)

// Entry and exit logic
if (dir_trade == 1 and close > stop_loss) or (dir_trade == -1 and close < stop_loss)
    if not executou_entrada
        strategy.entry("Buy", strategy.long, when=dir_trade == 1)
        strategy.exit("Close Long", "Buy", stop=stop_loss, limit=profit_target)
        executou_entrada := true

// Plotting
plotshape(series=elefante_bar or elefante_bar_down, title="Elephant Bar", location=location.belowbar, color=color.green, style=shape.labelup, text="ELEPHANT BAR")
plotchar(stop_loss != na, "Stop Loss", char="$", color=color.red)
plotchar(profit_target != na, "Profit Target", char="%", color=color.blue)

```

This Pine Script code implements the described dynamic stop-loss adjustment elephant bar trend-following strategy. It includes all the necessary components and logic as per the original script.