``` javascript
/* Parameters
stochRSI Indicator Parameters   Array     [14,14,3,3]
Use the spot cryptocurrency trading library
*/
var stochRSI_P_arr = "[14,14,3,3]";


var Interval = 500;

var long = 1;
var free = 0;
var state = free; // Each time a position is opened, closed, or reset
var buyInfo = null; // Reset on each close
var sellInfo = null; // Reset on each open
var initAccount = null; // Reset on each close
var beginAccount = null; // Not reset
var Profit = 0; // Realized Profit and Loss
var prefloatProfit = 0; // Last floating Profit and Loss for trailing stop updates
var openBalance = 0; // Opening position volume
var isCover = false;

var NowPositionInfo = { // Position information, updated on each close
    avgPrice: 0,
    amount: 0,
    floatProfit: 0
};

function openUpdate(){// After opening
    state = long;
    sellInfo = null;
}
function closeUpdate(){// After closing
    state = free;
    addLevel = 0;
    buyInfo = null;
    initAccount = _C(exchange.GetAccount);
    NowPositionInfo.avgPrice = 0;
    NowPositionInfo.amount = 0;
    NowPositionInfo.floatProfit = 0;
    isCover = true;
}

function Calculate(nowAccount,nowDepth){// Calculate and update profit and loss, average price, and position volume
    if(typeof(nowAccount) === 'undefined' ){
        nowAccount = _C(exchange.GetAccount);
        nowDepth = _C(exchange.GetDepth);
    }
    var diff_stocks = nowAccount.Stocks - initAccount.Stocks;// Difference in coins
    var diff_balance = nowAccount.Balance - initAccount.Balance;// Difference in balance
    NowPositionInfo.avgPrice = Math.abs(diff_balance) / Math.abs(diff_stocks);
    NowPositionInfo.amount = Math.abs(diff_stocks);
    NowPositionInfo.floatProfit = diff_balance + diff_stocks * nowDepth.Bids[0].Price; // Floating profit and loss for the current transaction
    Profit = (initAccount.Stocks - beginAccount.Stocks) * nowDepth.Bids[0].Price + (initAccount.Balance - beginAccount.Balance); // Realized profit and loss

    // Update UI
}

function LLV(array,period){
    if(!array || array.length - period < 0){
        throw "error:" + array;
    }
    var min = array[array.length - period];
    for(var i = array.length - period; i < array.length; i++){
        if( array[i] < min ){
            min = array[i];
        }
    }
    return min;
}

function HHV(array,period){
    if(!array || array.length - period < 0){
        throw "error:" + array;
    }
    var max = array[array.length - period];
    for(var i = array.length - period; i < array.length; i++){
        if( array[i] > max){
            max = array[i];
        }
    }
    return max;
}

function DeleteNullEle(initArr){
    var dealArr = [];
    var initArrLen = initArr.length;
    for(var i = 0,j = 0 ; i < initArrLen ; i++,j++){
        if(initArr[i] === null || isNaN(initArr[i]) ){
            j--;
            continue;
        }
        dealArr[j] = initArr[i];
    }
    return dealArr;
}

/*
LC := REF(CLOSE,1); // REF(C,1) previous close price
RSI:=SMA(MAX(CLOSE-LC,0),N,1)/SMA(ABS(CLOSE-LC),N,1) *100;
％K:     MA(RSI-LLV(RSI,M),P1)/MA(HHV(RSI,M)-LLV(RSI,M),P1)*100;  LLV（l,60）表示：检索60天内的最低价，可适应于检索任何股票
％D:MA(％K,P2);

LC := REF(CLOSE,1);
RSI:=SMA(MAX(CLOSE-LC,0),N,1)/SMA(ABS(CLOSE-LC),N,1) *100;
STOCHRSI:MA(RSI-LLV(RSI,M),P1)/MA(HHV(RSI,M)-LLV(RSI,M),P1)*100;
*/
function FstochRSI(records,n,m,p1,p2){
    var len = records.length;
    //var LC = records[len-2];// previous close price
    //var rsi = TA.RSI(records,n);// RSI array
    var rsi = talib.RSI(records,n);
    rsi = DeleteNullEle(rsi);// test
    //Log("rsi:",rsi) // test
    //Log("rsi:",rsi);// test
    //throw "stop";// test
    table.e5 = "rsi :" + rsi[rsi.length-1] + " rsi[-1]:" + rsi[rsi.length-2];// test

    var arr1 = [];
    var arr2 = [];
    var arr3 = [];
    var arr4 = [];
    var rsi_a = [];
    var rsi_b = [];
    var k = [];
    var d = null;

    /* Without current bar
    for(var a = 0 ;a < rsi.length ; a++ ){//改造 不用 LLV
        for(var aa = 0 ; aa <= a; aa++ ){
            rsi_a.push(rsi[aa]);
        }
        arr1.push(rsi[a] - TA.Lowest(rsi_a,m));
    }
    for(var b = 0 ;b < rsi.length ; b++ ){//改造 不用 HHV
        for(var bb = 0 ; bb <= b; bb++ ){
            rsi_b.push(rsi[bb]);
        }
        arr2.push(TA.Highest(rsi_b,m) - TA.Lowest(rsi_b,m));
    }
    */
    for(var a = 0 ;a < rsi.length ; a++ ){//改造 不用 LLV
        if(a < m){
            continue;
        }
        for(var aa = 0 ; aa <= a; aa++ ){
            rsi_a.push(rsi[aa]);
        }
        arr1.push(rsi[a] - LLV(rsi_a,m));
    }
    for(var b = 0 ;b < rsi.length ; b++ ){//改造 不用 HHV
        if(b < m){
            continue;
        }
        for(var bb = 0 ; bb <= b; bb++ ){
            rsi_b.push(rsi[bb]);
        }
        arr2.push(HHV(rsi_b,m) - LLV(rsi_b,m));
    }

    arr1 = DeleteNullEle(arr1);
    arr2 = DeleteNullEle(arr2);
    //Log("arr1:",arr1.length,"-",arr1);// test
    //Log("arr2:",arr2.length,"-",arr2);// test

    arr3 = talib.MA(arr1,p1);
    arr4 = talib.MA(arr2,p1);

    arr3 = DeleteNullEle(arr3);
    arr4 = DeleteNullEle(arr4);

    //Log("ceshi");// test
    var c = 0;
    var diff = 0;
    if(arr3.length !== arr4.length){// test
        throw "error: ！=" + arr3.length + "----" + arr4.length;
        diff = arr4.length - arr3.length; // example   diff  =   10  -   6
    }else{
        //throw "error:" + arr3.length + "----" + arr4.length;
    }

    for( ;c < arr3.length ; c++ ){
        k.push(arr3[c] / arr4[c + diff] * 100);
    }
    
    d = talib.MA(k,p2);

    return [k,d,rsi];
}

function Loop(){// Main loop
    /*
    var go_account = exchange.Go("GetAccount");
    var go_records = exchange.Go("GetRecords");
    var go_depth = exchange.Go("GetDepth");

    var account = go_account.wait(1000);
    var records = go_records.wait(1000);
    var depth = go_depth.wait(1000);
    
    if(account === null || records === null || depth === null){
        // Show error
        return;
    }
    */
    //
    var account = _C(exchange.GetAccount);
    var records = _C(exchange.GetRecords);
    var depth = _C(exchange.GetDepth);
    // Test

    var len = records.length - 1;

    if(records.length < stochRSI_P_arr[0] || records.length < stochRSI_P_arr[1] || records.length < stochRSI_P_arr[2] || records.length < stochRSI_P_arr
```