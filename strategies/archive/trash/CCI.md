Name

Based on CCI cyclical range trading strategy

Author

dark blue


Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|Diff|40|Period Range|
|Length|100|Cycle length|
|AvgLength|10|CCI average|
|Name|rb1810|Contract code|


Source (javascript)

``` javascript
/*backtest
start: 2015-01-01 09:00:00
end: 2018-04-22 15:00:00
Period: 1h
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES","minfee":0,"fee":[0,0]}]
*/


// Syntax fixed format, call main function
function main() {
    // Call the CTA framework in the commodity futures trading library
    $.CTA(Name, function(st) {
        // Get K-line array
        var j = st.records;
        // The maximum number of K lines referenced by the indicator operation
        if (j.length < Length) {
            return;
        }
        // Get the closing price of the previous K line
        var c1 = j[j.length - 2].Close;
        // Get the closing price of the previous K line
        var c2 = j[j.length - 3].Close;
        // Get CCI indicator array
        var cci = talib.CCI(j, Length);
        // Calculate the CCI average of the last K line
        var sum1 = 0;
        for (var i = cci.length - 1 - 1; i >= cci.length - AvgLength - 1; i--) {
            sum1 += cci[i];
        }
        var ccima1 = sum1 / AvgLength;
        // Calculate the CCI average of the previous K-line
        var sum2 = 0;
        for (var k = cci.length - 1 - 2; k >= cci.length - AvgLength - 2; k--) {
            sum2 += cci[k];
        }
        var ccima2 = sum2 / AvgLength;
        // Get the current position number, a positive number means long position, a negative number means short position, 0 means no position
        var mp = st.position.amount;
        // If there is currently no position, and the closing price of the previous K line is greater than the MA value of the previous K line, and the K value of the previous K line is greater than the D value of the previous K line, open a long order
        if (mp === 0 && ccima2 < Diff && ccima1 > Diff) {
            return 1; // If there is currently no position, specify the return value as N, which means opening N long orders.
        }
        // If there is currently no position, and the closing price of the previous K line is less than the MA value of the previous K line, and the K value of the previous K line is less than the D value of the previous K line, open a short order
        if (mp === 0 && ccima2 > -Diff && ccima1 < -Diff) {
            return -1; // If there is currently no position, specify the return value as -N, which means opening N short orders.
        }
        // If you currently hold a long order and the K value of the previous K line is less than the D value of the previous K line, close the long order
        if (mp > 0 && ccima2 > Diff && ccima1 < Diff) {
            return -1; // If there are currently multiple orders, specify the return value to be -N, which means N lots of long orders.
        }
        // If you currently hold a short order and the K value of the previous K line is greater than the D value of the previous K line, close the short order
        if (mp < 0 && ccima2 < -Diff && ccima1 > -Diff) {
            return 1; // If there is currently a short order, specify the return value as N, which means closing N short orders.
        }
    });
}
```


Detail

https://www.fmz.com/strategy/60287

Last Modified

2018-04-23 17:42:32