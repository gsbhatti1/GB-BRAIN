``` javascript
/*
- Command String Format
  action:amount
  action: buy , sell , long , short , cover_long , cover_short, spk , bpk
- Exchange Type
  eType variable value: 0 spot , 1 futures

- TradingView Documentation Link
  https://www.tradingview.com/pine-script-docs/en/v4/Quickstart_guide.html
  https://cn.tradingview.com/chart/8xfTuX7F/

- TV Webhook Request
  https://www.fmz.com/api/v1?access_key=xxx&secret_key=yyyy&method=CommandRobot&args=[186515,"action:amount"]

- Library References
  Refer to cryptocurrency trading library
*/

// Parameters
//var IsMarketOrder = true 
var QuotePrecision = 3
var BasePrecision = 3

// Futures parameters
var Ct = "swap"
//exchange.SetContractType("swap")        // Set to perpetual swap
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

//------------------- Added
const accountInformation = { // Account Information
    type: 'table',
    title: 'Account Information',
    cols: ['Initial Balance', 'Wallet Balance', 'Margin Balance', 'Free Margin', 'Used Margin', 'Total Revenue', 'Yield'], // Column headers
    rows: null // Row data
};

const binanceFundingRate = { // Funding Rate Table
    type: 'table',
    title: 'Binance U-Indexed Position',
    cols: ['Symbol', 'Direction', 'Amount', 'Price', 'Position Value', 'Leverage', 'Margin Used', 'Profit'], // Column headers
    rows: null // Row data
};

initialPrincipalUsdt = null // Initial principal in USDT
revenueUsdt = 0 // Total revenue


//--------------------------------------
// Account Information
//--------------------------------------
function accountInformationfunction() {
    exchange.SetContractType("swap"); // Set to perpetual swap
    var Currency = exchange.GetCurrency()
    exchange.SetCurrency(Currency) // Switch to access the U-Indexed account
    var account = _C(exchange.GetAccount)

    _CDelay(2000 * 60)
    if (!account) {
        Log("Failed to get asset information")
        return
    }
    
    if (initialPrincipalUsdt == null) {
        initialPrincipalUsdt = account.Info.totalWalletBalance // Record the initial balance
        _G("initialPrincipalUsdt", initialPrincipalUsdt) // Get saved data
        if (initialPrincipalUsdt == 0) {
            Log("No assets in USDT contract")
            return
        }
    }
    /*API 
    "totalInitialMargin": "0.00000000",  // Required initial margin in USD
    "totalMaintMargin": "0.00000000",  // Maintained margin in USD
    "totalWalletBalance": "126.72469206",   // Total wallet balance in USD
    "totalUnrealizedProfit": "0.00000000",  // Unrealized profit in USD
    "totalMarginBalance": "126.72469206",  // Total margin balance in USD
    "totalPositionInitialMargin": "0.00000000",  // Required initial margin based on the latest mark price in USD
    "totalOpenOrderInitialMargin": "0.00000000",  // Required initial margin for current open orders based on the latest mark price in USD
    "totalCrossWalletBalance": "126.72469206",  // Cross-margin total wallet balance in USD
    "totalCrossUnPnl": "0.00000000",    // Cross-margin total unrealized profit in USD
    "availableBalance": "126.72469206",       // Available balance in USD
    "maxWithdrawAmount": "126.72469206"     // Maximum withdrawable balance in USD
    */

    InitialBalance = Number(initialPrincipalUsdt)
    WalletBalance = account.Info.totalWalletBalance
    marginBalance = account.Info.totalCrossWalletBalance
    FreeMargin = account.Info.availableBalance
    UsedMargin = account.Info.totalMaintMargin
   
    TotalRevenue = Number(WalletBalance) - Number(InitialBalance)
    Yield1 = TotalRevenue / InitialBalance
    yield1 = Number(Yield1)
    Yield = (yield1 * 100).toFixed(2) + "%"
    // Pack in array
    revenueUsdt = Number(TotalRevenue)

    accountInformation.rows = [] // Clear array
    // 'Initial Balance',  'Wallet Balance ',  'Margin Balance', 'Free Margin', 'Used Margin', 'Total Revenue', 'Yield'
    accountInformation.rows[0] = [InitialBalance, WalletBalance, marginBalance, FreeMargin, UsedMargin, TotalRevenue, Yield]

}

//--------------------------------------
// Position Table
//--------------------------------------
function binanceFundingRatefunction() { // Position Table
    binanceFundingRate.rows = []
    exchange.SetContractType("swap"); // Set to perpetual swap, note that both U-Indexed and USDT-Indexed have perpetual swaps
    var y = 0 // Flag to check if there is no such product

    for (var i = 0; i < exchanges.length; i++) {
        exchange.SetCurrency(exchanges[i].GetCurrency()) // Switch product
        //-------------------------------------------------------
        var position = _C(exchange.GetPosition) // Get account position
       // Log("position", position)
        _CDelay(1000 * 2 * 60)
        // U-Indexed contracts are in a separate array from the futures. Perpetual and futures are different.
        if (position) {
            for (var iii = 0; iii < position.length; iii++) {
                if (exchange.GetContractType() == position[iii].ContractType) { // Why check, because all futures positions are grouped together
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
// Main Function
//--------------------------------------
function main() {
    // Clear logs, can be deleted if not needed
    //LogReset(1)

    // Set precision
    exchange.SetPrecision(QuotePrecision, BasePrecision)

    // Identify futures or spot
    var eType = 0
    var eName = exchange.GetName() // Exchange name, e.g. Futures_Binance
    var patt = /Futures_/
    if (patt.test(eName)) { // Check if it contains Futures_
        Log("Added exchange is a futures exchange:", eName, "#FF0000")
        eType = 1
        if (Ct == "") {
            throw "Ct contract setting is empty"
        } else {
            Log(exchange.SetContractType(Ct), "Set contract to:", Ct, "#FF0000")
        }
    } else {
        Log("Added exchange is a spot exchange:", eName, "#32CD32")
    }

    // Test position function
    var position3 = exchange.GetPosition()
    if (position3.length == 0) {
        Log("Robot is starting for the first time, performing a comprehensive check of the exchange", "#33CD33"
```