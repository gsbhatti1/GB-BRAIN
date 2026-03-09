``` javascript
// Signal structure
var Template = {
    Flag: "45M103Buy",     // Identifier, can be freely specified
    Exchange: 1,           // Designated exchange trading pair
    Currency: "BTC_USDT",  // Trading pair
    ContractType: "swap",  // Contract type, swap, quarter, next_quarter, spot for spot trading
    Price: "{{close}}",    // Opening or closing price, -1 for market price
    Action: "buy",         // Trading type [ buy: spot buy, sell: spot sell, long: futures buy, short: futures sell, closesell: futures buy to close, closebuy: futures sell to close ]
    Amount: "0",           // Trading volume
}

var BaseUrl = "https://www.fmz.com/api/v1"   // FMZ extended API interface address 
var RobotId = _G()                           // Current live trading ID
var Success = "#5cb85c"    // Success color
var Danger = "#ff0000"     // Danger color
var Warning = "#f0ad4e"    // Warning color
var buffSignal = []

// Validate signal message format
function DiffObject(object1, object2) {
    const keys1 = Object.keys(object1)
    const keys2 = Object.keys(object2)
    if (keys1.length !== keys2.length) {
        return false
    }
    for (let i = 0; i < keys1.length; i++) {
        if (keys1[i] !== keys2[i]) {
            return false
        }
    }
    return true
}

function CheckSignal(Signal) {
    Signal.Price = parseFloat(Signal.Price)
    Signal.Amount = parseFloat(Signal.Amount)
    if (Signal.Exchange <= 0 || !Number.isInteger(Signal.Exchange)) {
        Log("Exchange minimum number is 1 and must be an integer", Danger)
        return
    }
    if (Signal.Amount <= 0 || typeof(Signal.Amount) != "number") {
        Log("Trading volume cannot be less than 0 and must be a numeric type", typeof(Signal.Amount), Danger)
        return
    }
    if (typeof(Signal.Price) != "number") {
        Log("Price must be numeric", Danger)
        return
    }
    if (Signal.ContractType == "spot" && Signal.Action != "buy" && Signal.Action != "sell") {
        Log("Command is spot trading, Action error, Action:", Signal.Action, Danger)
        return 
    }
    if (Signal.ContractType != "spot" && Signal.Action != "long" && Signal.Action != "short" && Signal.Action != "closesell" && Signal.Action != "closebuy") {
        Log("Command is futures trading, Action error, Action:", Signal.Action, Danger)
        return 
    }
    return true
}

function commandRobot(url, accessKey, secretKey, robotId, cmd) {
    // https://www.fmz.com/api/v1?access_key=xxx&secret_key=xxx&method=CommandRobot&args=[xxx, ""]
    url = url + '?access_key=' + accessKey + '&secret_key=' + secretKey + '&method=CommandRobot&args=[' + robotId + ',+""]'
    var postData = {
        method:'POST', 
        data:cmd
    }
    var headers = "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36\nContent-Type: application/json"
    var ret = HttpQuery(url, postData, "", headers)
    Log("Simulate TradingView webhook request, send test POST request:", url, "body:", cmd, "response:", ret)
}

function createManager() {
    var self = {}
    self.tasks = []
    
    self.process = function() {
        var processed = 0
        if (self.tasks.length > 0) {
            _.each(self.tasks, function(task) {
                if (!task.finished) {
                    processed++
                    self.pollTask(task)
                }
            })
            if (processed == 0) {
                self.tasks = []
            }
        }
    }
    
    self.newTask = function(signal) {
        // {"Flag":"45M103Buy","Exchange":1,"Currency":"BTC_USDT","ContractType":"swap","Price":"10000","Action":"buy","Amount":"0"}
        var task = {}
        task.Flag = signal["Flag"]
        task.Exchange = signal["Exchange"]
        task.Currency = signal["Currency"]
        task.ContractType = signal["ContractType"]
        task.Price = signal["Price"]
        task.Action = signal["Action"]
        task.Amount = signal["Amount"]
        task.exchangeIdx = signal["Exchange"] - 1
        task.pricePrecision = null
        task.amountPrecision = null 
        task.error = null 
        task.exchangeLabel = exchanges[task.exchangeIdx].GetLabel()
        task.finished = false 
        
        Log("Create task:", task)
        self.tasks.push(task)
    }
    
    self.getPrecision = function(n) {
        var precision = null 
        var arr = n.toString().split(".")
        if (arr.length == 1) {
            precision = 0
        } else if (arr.length == 2) {
            precision = arr[1].length
        } 
        return precision
    }
    
    self.pollTask = function(task) {
        var e = exchanges[task.exchangeIdx]
        var name = e.GetName()
        var isFutures = true
        e.SetCurrency(task.Currency)
        if (task.ContractType != "spot" && name.indexOf("Futures_") != -1) {
            // Non-spot, set contract type
            e.SetContractType(task.ContractType)
        } else if (task.ContractType == "spot" && name.indexOf("Futures_") == -1) {
            isFutures = false 
        } else {
            task.error = "The ContractType in the command does not match the configured exchange object type"
            task.finished = true
            return 
        }
        
        var depth = e.GetDepth()
        if (!depth || !depth.Bids || !depth.Asks) {
            task.error = "Depth data abnormal"
            return 
        }
        
        if (depth.Bids.length == 0 && depth.Asks.length == 0) {
            task.error = "No orders in the market"
            return 
        }
        
        _.each([depth.Bids, depth.Asks], function(arr) {
            _.each(arr, function(order) {
                var pricePrecision = self.getPrecision(order.Price)
                var amountPrecision = self.getPrecision(order.Amount)
                task.pricePrecision = pricePrecision
                task.amountPrecision = amountPrecision
            })
        })
    }
}
```