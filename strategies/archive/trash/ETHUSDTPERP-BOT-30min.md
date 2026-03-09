``` pinescript
//@version=4
strategy("ETHUSDTPERP BOT 30min", overlay=false, pyramiding=1, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.075)

//Source
source = input(close, title="Source")

//ADX -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Act_ADX             = input(true,       title = "AVERAGE DIRECTIONAL INDEX",            type=input.bool)
ADX_options         = input("MASANAKAMURA",  title = "  ADX OPTION",                                                                                 options=["CLASSIC", "MASANAKAMURA"])
ADX_len             = input(16,         title = "  ADX LENGTH",                         type=input.integer,   minval=1)
th                  = input(13.5,         title = "  ADX THRESHOLD",                      type=input.float,     minval=0, step=0.5)

calcADX(_len) =>
    up              = change(high)
    down            = -change(low)
    plusDM          = na(up)   ? na : (up > down and up > 0   ? up   : 0)
    minusDM         = na(down) ? na : (down > up and down > 0 ? down : 0)
    tr              = rma(tr, _len)
    _plus           = fixnan(100 * rma(plusDM, _len)  / tr)
    _minus          = fixnan(100 * rma(minusDM, _len) / tr)
    sum             = _plus + _minus
    _adx            = 100 * rma(abs(_plus - _minus) / (sum == 0 ? 1 : sum), _len)
    [_plus,_minus,_adx]

calcADX_Masanakamura(_len) =>
    SmoothedTrueRange                   = 0.0
    SmoothedDirectionalMovementPlus     = 0.0
    SmoothedDirectionalMovementMinus    = 0.0
    TrueRange                           = max(max(high - low, abs(high - nz(close[1]))), abs(low - nz(close[1])))
    DirectionalMovementPlus             = high - nz(high[1]) > nz(low[1]) - low ? max(high - nz(high[1]), 0) : 0
    DirectionalMovementMinus            = nz(low[1]) - low > high - nz(high[1]) ? max(nz(low[1]) - low, 0)   : 0
    SmoothedTrueRange                   := nz(SmoothedTrueRange[1]) - (nz(SmoothedTrueRange[1]) / _len) + TrueRange
    SmoothedDirectionalMovementPlus     := nz(SmoothedDirectionalMovementPlus[1])  - (nz(SmoothedDirectionalMovementPlus[1])  / _len) + DirectionalMovementPlus
    SmoothedDirectionalMovementMinus    := nz(SmoothedDirectionalMovementMinus[1]) - (nz(SmoothedDirectionalMovementMinus[1]) / _len) + DirectionalMovementMinus
    DIP                                 = SmoothedDirectionalMovementPlus  / SmoothedTrueRange * 100
    DIM                                 = SmoothedDirectionalMovementMinus / SmoothedTrueRange * 100
    DX                                  = abs(DIP-DIM) / (DIP+DIM)*100
    adx                                 = sma(DX, _len)
    [DIP,DIM,adx]

[DIPlusC,DIMinusC,ADXC] = calcADX(ADX_len) 
[DIPlusM,DIMinusM,ADXM] = calcADX_Masanakamura(ADX_len)
DIPlus                  = ADX_options == "CLASSIC" ? DIPlusC    : DIPlusM
DIMinus                 = ADX_options == "CLASSIC" ? DIMinusC   : DIMinusM
ADX                     = ADX_options == "CLASSIC" ? ADXC       : ADXM

ADX_color = DIPlus > DIMinus and ADX > th ? color.green : DIPlus < DIMinus and ADX > th ? color.red : color.orange
barcolor(color = Act_ADX ? ADX_color : na, title = "ADX")

//RSI---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

len_3 = input(30, minval=1, title="RSI length")
src_3 = input(hl2, "Source")
up_3 = rma(max(change(src_3), 0), len_3)
down_3 = rma(-min(change(src_3), 0), len_3)
rsi_3 = down_3 == 0 ? 100 : up_3 == 0 ? 0 : 100 - (100 / (1 + up_3 / down_3))

//VOLUME-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

maLength = input(title="MA Length", type=input.integer, defval=31, minval=1)
maType = input(title="MA Type", type=input.string, defval="SMA", options=["EMA", "SMA", "HMA", "WMA", "DEMA"])
rvolTrigger = input(title="RVOL To Trigger Signal", type=input.float, defval=1.2)

getMA(length) =>
    maPrice = ema(volume, length)
    if maType == "SMA"
        maPrice := sma(volume, length)
    if maType == "HMA"
        maPrice := hma(volume, length)
    if maType == "WMA"
        maPrice := wma(volume, length)
    if maType == "DEMA"
        e1 = ema(volume, length)
        e2 = ema(e1, length)
        maPrice := 2 * e1 - e2
    maPrice

ma = getMA(maLength)
rvol = volume / ma

//MOMENTUM-------------------------------------------------------------------------
```