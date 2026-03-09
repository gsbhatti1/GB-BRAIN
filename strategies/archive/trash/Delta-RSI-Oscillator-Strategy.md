``` pinescript
/*backtest
start: 2022-04-29 00:00:00
end: 2022-05-28 23:59:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tbiktag
//
// Delta-RSI Oscillator Strategy
//
// A strategy that uses Delta-RSI Oscillator (© tbiktag) as a stand-alone indicator:
// https://www.tradingview.com/script/OXQVFTQD-Delta-RSI-Oscillator/
//
// Delta-RSI is a smoothed time derivative of the RSI, plotted as a histogram 
// and serving as a momentum indicator. 
// 
// Input parameters:
// RSI Length: The timeframe of the RSI that serves as an input to D-RSI.
// Length: The length of the lookback frame used for local regression.
// Polynomial Order: The order of the local polynomial function used to interpolate the RSI.
// Signal Length: The length of a EMA of the D-RSI series that is used as a signal line.
// Trade signals are generated based on three optional conditions:
// - Zero-crossing: bullish when D-RSI crosses zero from negative to positive values (bearish otherwise)
// - Signal Line Crossing: bullish when D-RSI crosses from below to above the signal line (bearish otherwise)
// - Direction Change: bullish when D-RSI was negative and starts ascending (bearish otherwise)
//
// Since D-RSI oscillator is based on polynomial fitting of the RSI curve, there is also an option
// to filter trade signal by means of the root mean-square error of the fit (normalized by the sample average).
// 
//@version=4
study(title="Delta-RSI Oscillator Strategy", shorttitle = "D-RSI", overlay = true)

// ---Subroutines---
matrix_get(_A,_i,_j,_nrows) =>
    // Get the value of the element of an implied 2d matrix
    //input: 
    // _A :: array: pseudo 2d matrix _A = [[column_0],[column_1],...,[column_(n-1)]]
    // _i :: integer: row number
    // _j :: integer: column number
    // _nrows :: integer: number of rows in the implied 2d matrix
    array.get(_A,_i+_nrows*_j)

matrix_set(_A,_value,_i,_j,_nrows) =>
    // Set a value to the element of an implied 2d matrix
    //input: 
    // _A :: array, changed on output: pseudo 2d matrix _A = [[column_0],[column_1],...,[column_(n-1)]]
    // _value :: float: the new value to be set
    // _i :: integer: row number
    // _j :: integer: column number
    // _nrows :: integer: number of rows in the implied 2d matrix
    array.set(_A,_i+_nrows*_j,_value)

transpose(_A,_nrows,_ncolumns) =>
    // Transpose an implied 2d matrix
    // input:
    // _A :: array: pseudo 2d matrix _A = [[column_0],[column_1],...,[column_(n-1)]]
    // _nrows :: integer: number of rows in _A
    // _ncolumns :: integer: number of columns in _A
    // output:
    // _AT :: array: pseudo 2d matrix with implied dimensions: _ncolums x _nrows
    var _AT = array.new_float(_nrows*_ncolumns,0)
    for i = 0 to _nrows-1
        for j = 0 to _ncolumns-1
            matrix_set(_AT, matrix_get(_A,i,j,_nrows),j,i,_ncolumns)
    _AT

multiply(_A,_B,_nrowsA,_ncolumnsA,_ncolumnsB) => 
    // Calculate scalar product of two matrices
    // input: 
    // _A :: array: pseudo 2d matrix
    // _B :: array: pseudo 2d matrix
    // _nrowsA :: integer: number of rows in _A
    // _ncolumnsA :: integer: number of columns in _A
    // _ncolumnsB :: integer: number of columns in _B
    // output:
    // _C:: array: pseudo 2d matrix with implied dimensions _nrowsA x _ncolumnsB
    var _C = array.new_float(_nrowsA*_ncolumnsB,0)
    int _nrowsB = _ncolumnsA
    float elementC= 0.0
    for i = 0 to _nrowsA-1
        for j = 0 to _ncolumnsB-1
            elementC := 0
            for k = 0 to _ncolumnsA-1
                elementC := elementC + matrix_get(_A,i,k,_nrowsA)*matrix_get(_B,k,j,_nrowsB)
            matrix_set(_C,elementC,i,j,_nrowsA)
    _C

vnorm(_X,_n) =>
    //Square norm of vector _X with size _n
    float _norm = 0.0
    for i = 0 to _n-1
        _norm := _norm + pow(array.get(_X,i),2)
    sqrt(_norm)

qr_diag(_A,_nrows,_ncolumns) => 
    //QR Decomposition with Modified Gram-Schmidt Algorithm (Column-Oriented)
    // input:
    // _A :: array: pseudo 2d matrix _A = [[column_0],[column_1],...,[column_(n-1)]]
    // _nrows :: integer: number of rows in _A
    // _ncolumns :: integer: number of columns in _A
    // output:
    // _Q: unitary matrix, implied dimenstions
```