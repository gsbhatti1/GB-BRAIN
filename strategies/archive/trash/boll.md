Name

boll fool version

Author

sabar

Source (javascript)

``` javascript
function main(){
$.CTA("BTC_USDT", function(st){
var r = st.records; //Get the K-line array
if (r.length < 20) return; // Filter K line length
var close = r[r.length - 2].close; //Get the closing price of the previous K line
var mp = st.position.amount; //Get position information

var boll = TA.BOLL(r, 20, 2); // Calculate Bollinger Bands indicator
var upLine = boll[0];
//Get the upper track array
var midLine = boll[1]; //Get the mid-rail array
var downLine = boll[2];//Get the lower rail array
var upPrice = upLine [upLine.length - 2];
//Get the upper track value of the last K line
var midPrice = midLine[midLine.length - 2];
//Get the middle track value of the last K line
var downPrice = downLine[downLine.length - 2];
//Get the lower track value of the previous K line
if(mp == 1 && (close < midPrice)) return -1; //If you hold a long order and the closing price is less than the mid-rail.Pinduo
if (mp == -1 && (close > midPrice)) return 1; //If you hold a short order and the closing price is greater than the mid-rail.empty
if (mp == 0 && close > midPrice) return 1; //If there is no position, the closing price is greater than the upper track.Open long
if (mp == 0 && close < downPrice) return -1; //If there is no position and the closing price is less than the lower track.Open short
});
}
```

Detail

https://www.fmz.com/strategy/318249

Last Modified

2021-09-23 09:43:52