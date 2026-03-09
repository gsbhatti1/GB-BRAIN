Name

Trading Pair Accuracy Calibration

Author

Spartan plays with quantification


Source (javascript)

```javascript
/*
-- After the strategy references the template, it directly calls this method using $.Test()
-- The main function will not be triggered in the strategy and is only used as an entry point for template debugging.

-- The precision calibration of the GetExPrecision function only supports single digits, and does not currently support cases where the trading pair precision is tens/hundreds/thousands of digits...
-- [Warning] If the handicap depth is too low to accurately express the true accuracy, the function may lose accuracy.
*/

let gCache = {};

let scientificToNumber = function(num) {
    if (/\d+\.?\d*e[\+\-]*\d+/i.test(num)) { // Regularly matches numbers in scientific notation
        var zero = '0', //
        parts = String(num).toLowerCase().split('e'), // Split into coefficients and indices
        e = parts.pop(), // Store index
        l = Math.abs(e), // Take the absolute value, l-1 is the number of 0s
        sign = e / l, // Judge positive or negative
        coeff_array = parts[0].split('.'); // Split the coefficient according to decimal points
        if (sign === -1) { // If it is a decimal
            num = zero + '.' + new Array(l).join(zero) + coeff_array.join(''); // Splice strings, if it is a decimal, splice 0 and decimal point
        } else {
            var dec = coeff_array[1];
            if (dec) l = l - dec.length; // If it is an integer, count the non-zero digits except the first digit in the integer and reduce the number of 0s accordingly.
            num = coeff_array.join('') + new Array(l + 1).join(zero); // Join strings. If it is an integer, no decimal point is required.
        }
    }
    return num;
}

$.GetPrecision = function(depth) {
    let maxLenAmt = 0;
    let maxLenPrice = 0;
    depth.Asks.forEach(function(ask) {
        let price = scientificToNumber(ask["Price"]).toString();
        if (price.indexOf('.') > -1) {
            let priceP = price.split(".")[1].length;
            if (priceP > maxLenPrice) {
                maxLenPrice = priceP;
            }
        }
        let amt = scientificToNumber(ask["Amount"]).toString();
        if (amt.indexOf('.') > -1) {
            let amtP = amt.split(".")[1].length;
            if (amtP > maxLenAmt) {
                maxLenAmt = amtP;
            }
        }
    })
    return [maxLenPrice, maxLenAmt];
}

// Return array [precision of price, precision of quantity]
$.GetExPrecision = function(ex, force) {
    if (IsVirtual()) {
        return null;
    }
    let key = ex.GetName() + '_ex_precision_' + ex.GetCurrency();
    let cache = gCache[key];
    if (!force && cache) {
        return cache;
    }
    let r = $.GetPrecision(_C(ex.GetDepth));
    gCache[key] = r;
    Log("Cache precision information to local", key, r);
    return r;
}

function main() {
    $.GetExPrecision(exchange, false);
}
```


Detail

https://www.fmz.com/strategy/372101

Last Modified

2022-09-23 16:16:20