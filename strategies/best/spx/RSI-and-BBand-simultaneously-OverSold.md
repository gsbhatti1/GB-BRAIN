```markdown
---
Name
RSI-and-BBand-simultaneously-OverSold

Author
ChaoZhang

Strategy Description
This indicator is created by combining the standard period RSI indicator with an Oversold limit of 32, an Overbought limit of 70 and a period of 14 (these values can be changed optionally from the entries and settings tabs of the indicator). Additionally, it includes the Bollinger Band indicator with a standard deviation of 2 and a period of 20. The RSI Oversold is indicated by an upward green triangle where the price simultaneously falls below the BB and the lower limit (Low) (i.e., below 32), while the RSI Overbought (i.e., above 70) at the same time the price rises above the BB and the upper limit (Upper) is indicated by a downward red triangle. An alarm condition is established on these conditions.

**Backtest**
![IMG](https://www.fmz.com/upload/asset/1f1cc8bca66e3e9a1fd.png)

> Strategy Arguments

| Argument | Default | Description |
| --- | --- | --- |
| v_input_1_close | 0 | RSI Source: close, high, low, open, hl2, hlc3, hlcc4, ohlc4 |
| v_input_2 | 14 | RSI Periodu |
| v_input_3 | 32 | Enter RSI Base Value |
| v_input_4 | 70 | Enter RSI Top Value |
| v_input_5 | 20 | BBPeriodu |
| v_input_6_close | 0 | Source: close, high, low, open, hl2, hlc3, hlcc4, ohlc4 |
| v_input_7 | 2 | Standard Deviation |

> Source (PineScript)

```pinescript
// backtest
// start: 2022-02-11 00:00:00
// end: 2022-05-11 00:00:00
// period: 10m
// basePeriod: 1m
// exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
```

```pinescript
//@version=4
study(title="RSI & BB'de aynı anda Oversold Yakalama", shorttitle="RSI&BB OS", overlay=true)

// RSI hesabı ile kaynak ve period seçimi için seçki kutusu ve değer giriş kutuları burada yapıldı
rsiKaynagi = input(title="RSI Kaynagi", type=input.source, defval=close)
rsiPeriodu = input(title="RSI Periodu", type=input.integer, defval=14)
rsiDegeri = rsi(rsiKaynagi, rsiPeriodu)
rsiTabanDegeri = input(title="RSI Taban Değerini gir", type=input.integer, defval=32) // defval: default value yani varsayılan değer
rsiTavanDegeri = input(title="RSI Tavan Değerini gir", type=input.integer, defval=70)

// Bollinger Bandı hesabı ve kaynak ve period seçimi için seçki kutusu ve değer giriş kutuları burada yapıldı
bbPeriodu = input(20, minval=1)
bbKaynagi = input(close, title="Source")
standartSapmaDegeri = input(2.0, minval=0.001, maxval=50, title="Standart Sapma")
bandOrtasi = sma(bbKaynagi, bbPeriodu)
sapmaHesabi = standartSapmaDegeri * stdev(bbKaynagi, bbPeriodu)
bbUstSiniri = bandOrtasi + sapmaHesabi
bbAltsiniri = bandOrtasi - sapmaHesabi
bandOrtaCizgisi = plot(bandOrtasi, "Orta Çizgi", color=color.black) 
ustSinirCizgisi = plot(bbUstSiniri, "Üst Sınır Çizgisi", color=color.black)
altSinirCizgisi = plot(bbAltsiniri, "Alt Sınır Çizgisi", color=color.black)
fill(ustSinirCizgisi, altSinirCizgisi, title="Arka Plan", color=color.rgb(33, 150, 243, 95)) // arka plan renkleri RGB cinsinden

// RSI'nin değerinin 20 altındayken aynı anda fiyatın Bollinger Bandının altı sınırının altında olduğu durum için şart oluşturma
bullishkosulu = rsiDegeri<rsiTabanDegeri and low<bbAltsiniri
bearishkosulu = rsiDegeri>rsiTavanDegeri and high>bbUstSiniri

// bu kosulun sağlandığı yerleri belirtilen yazı ve / veya şekille gösterme
plotshape((bullishkosulu)? 1 : 0, style=shape.triangleup, text="Bullish", color=color.green, location=location.belowbar, size=size.small)
plotshape((bearishkosulu)? 1 : 0, style=shape.triangledown, text="Bearish", color=color.red, location=location.abovebar, size=size.small)

//triangleup: yukarı yönlü üçgen
//text: görünmesi istenen yazı 
//color: yazı ve şekil rengi
//location: mumun altında mı üstünde mi görünsün
//belowbar: mumun yani barın altında görünsün
//size : büyüklük küçüklük ölçüsü (burada small ile küçük olsun istendi)

alertcondition(bullishkosulu, title="Bullish koşulu üzerine alarm kur", message="{{interval}} - RSI<33 ve Fiyat<BB Lower - {{ticker}} - En düşük fiyat:{{low}} - {{timenow}}")
alertcondition(bearishkosulu, title="Bearish koşulu üzerine alarm kur", message="{{interval}} - RSI>70 ve Fiyat>BB Upper - {{ticker}} - En yüksek fiyat:{{high}} - {{timenow}}")

if bearishkosulu
    strategy.entry("Enter Long", strategy.long)
else if bullishkosulu
    strategy.entry("Enter Short", strategy.short)
```

> Detail
https://www.fmz.com/strategy/362654

> Last Modified
2022-05-12 17:48:21
```