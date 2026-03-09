``` javascript
/*
- Interactive Command String Format:
  action:amount
  action: buy , sell , long , short , cover_long , cover_short, spk , bpk
- Exchange Type:
  eType variable value: 0 spot , 1 futures

- TradingView Documentation Link:
  https://www.tradingview.com/pine-script-docs/en/v4/Quickstart_guide.html
  https://cn.tradingview.com/chart/8xfTuX7F/

- TradingView Webhook Request
  https://www.fmz.com/api/v1?access_key=xxx&secret_key=yyyy&method=CommandRobot&args=[186515,"action:amount"]

- Library References:
  Reference cryptocurrency trading library.
*/

// Parameters
//var IsMarketOrder = true 
var QuotePrecision = 3
var BasePrecision = 3

// Futures parameters
var Ct = "swap"
//exchange.SetContractType("swap")        // Set as perpetual contract
//exchange.SetCurrency("BTC_USDT")

// Global variables
var BUY = "buy"
var SELL = "sell"
var LONG = "long"
var SHORT = "short"
var COVER_LONG = "cover_long"
var COVER_SHORT = "cover_short"
var SPK = "spk"
var BPK = "bpk"

//------------------- Add
const accountInformation = { //Account information
    type: 'table',
    title: 'Account Information',
    cols: ['Initial Balance', 'Wallet Balance ', 'Margin Balance', 'Free Margin', 'Used Margin', 'Total Revenue', 'Yield'], //Table headers
    rows: null //Table array   
};

const binanceFundingRate = { //Position array
    type: 'table',
    title: 'Binance U-coin Position',
    cols: ['Symbol', 'Direction ', 'Opening Volume', 'Opening Price', 'Holding Value', 'Leverage', 'Used Margin', 'Profit'], //Table headers
    rows: null //Table array
};

initialPrincipalUsdt = null //Initial principal in USDT
revenueUsdt = 0 //Revenue


//--------------------------------------
//Account Information
//--------------------------------------
function accountInformationFunction() {
    exchange.SetContractType("swap"); // Set as perpetual contract swap / quarter/
    var Currency = exchange.GetCurrency()
    exchange.SetCurrency(Currency) // Switch product to access the U-coin account information
    var account = _C(exchange.GetAccount)

    _CDelay(2000 * 60)
    if (!account) {
        Log("Failed to get asset")
        return
    }
    
    if (initialPrincipalUsdt == null ) {
        initialPrincipalUsdt = account.Info.totalWalletBalance // Get the total wallet balance as the initial balance when loading
        _G("initialPrincipalUsdt", initialPrincipalUsdt) // Retrieve saved data
        if (initialPrincipalUsdt == 0) {
            Log("No assets in USDT contract")
            return
        }
    }

    InitialBalance = Number(initialPrincipalUsdt)
    WalletBalance = account.Info.totalWalletBalance
    marginBalance = account.Info.totalCrossWalletBalance
    FreeMargin = account.Info.availableBalance
    UsedMargin = account.Info.totalMaintMargin
   
    TotalRevenue = Number(WalletBalance) - Number(InitialBalance)
    Yield1 = TotalRevenue / InitialBalance
    yield1 = Number(Yield1)
    Yield = (yield1 * 100).toFixed(2) + "%"
    //Pack in array
    revenueUsdt = Number(TotalRevenue)

    accountInformation.rows = [] // Clear the rows
    accountInformation.rows[0] = [InitialBalance, WalletBalance, marginBalance, FreeMargin, UsedMargin, TotalRevenue, Yield]

}

//--------------------------------------
//Position Array
//--------------------------------------
function binanceFundingRateFunction() { //Position array
    binanceFundingRate.rows = []
    exchange.SetContractType("swap"); // Set as perpetual contract, note that both U-coin and USDT-based futures exist
    var y = 0 // Check if there is no such product

    for (var i = 0; i < exchanges.length; i++) {
        exchange.SetCurrency(exchanges[i].GetCurrency()) // Switch product
        //-------------------------------------------------------
        var position = _C(exchange.GetPosition) // Get account position information
       // Log("position", position)
        _CDelay(1000 * 2 * 60)
        // The U-coin has different quarterly contracts in a separate array. This is different from perpetuals.
        if (position) {
            for (var iii = 0; iii < position.length; iii++) {
                if (exchange.GetContractType() == position[iii].ContractType) { // Why check, because positions of quarterly contracts are all together
                    binanceFundingRate.rows[y] = [position[iii].Info.symbol, position[iii].Type == 0 ? "BUY" : "SELL", position[iii].Amount,
                        position[iii].Price, position[iii].Amount * position[iii].Price,
                        position[iii].MarginLevel, position[iii].Margin, position[iii].Profit
                    ]
                    y++
                }
            }
        }

    }

}


//--------------------------------------
//Main Function
//--------------------------------------

function main() {
    // Clear log if not needed, can be deleted
    //LogReset(1)

    // Set precision
    exchange.SetPrecision(QuotePrecision, BasePrecision)

    // Identify futures or spot market
    var eType = 0
    var eName = exchange.GetName() // Name of the exchange, like: Futures_Binance
    var patt = /Futures_/
    if (patt.test(eName)) { // Check if it contains Futures_
        Log("Added exchange is a futures exchange:", eName, "#FF0000")
        eType = 1
        if (Ct == "") {
            throw "Ct contract set to empty"
        } else {
            Log(exchange.SetContractType(Ct), "Set contract: ", Ct, "#FF0000")
        }
    } else {
        Log("Added exchange is a spot market:", eName, "#32CD32")
    }

    // Test position function
    var position3 = exchange.GetPosition()
    if (position3.length == 0) {
        Log("Robot first startup, performing comprehensive check on the exchange", "#33CD33"
```