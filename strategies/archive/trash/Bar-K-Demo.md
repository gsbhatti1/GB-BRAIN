Name

How to find the previous high and low points of the K-line with a certain number of Bars and the Demo program

Author

Inventor Quantification-Little Dream

Source (javascript)

```javascript
function FindLastHighestPoint(Records, NumOfBars){
    var RecordsLen = Records.length
    if(RecordsLen < 2){
        return false
    }
    if(typeof(NumOfBars) == "undefined"){
        NumOfBars = 0
    }
    var highPrice = TA.Highest(Records, NumOfBars, "High")
    // find the bar
    var bar = null
    for(var i = 0; i < RecordsLen; i++){
        if(Records[i].High == highPrice){
            bar = {}
            bar.record = Records[i]
            bar.index = i
            bar.range = NumOfBars
            break
        }
    }

    // compare current bar
    if(bar && Records[RecordsLen - 1].High >= bar.record.High){
        bar.record = Records[RecordsLen - 1]
        bar.index = RecordsLen - 1
        bar.range = NumOfBars
    }

    if(!bar || !Records[bar.index - 1]){
        return false
    }

    return bar
}

function FindLastLowestPoint(Records, NumOfBars){
    var RecordsLen = Records.length
    if(RecordsLen < 2){
        return false
    }
    if(typeof(NumOfBars) == "undefined"){
        NumOfBars = 0
    }
    var lowPrice = TA.Lowest(Records, NumOfBars, "Low")
    // find the bar
    var bar = null
    for(var i = 0; i < RecordsLen; i++){
        if(Records[i].Low == lowPrice){
            bar = {}
            bar.record = Records[i]
            bar.index = i
            bar.range = NumOfBars
            break
        }
    }

    // compare current bar
    if(bar && Records[RecordsLen - 1].Low <= bar.record.Low){
        bar.record = Records[RecordsLen - 1]
        bar.index = RecordsLen - 1
        bar.range = NumOfBars
    }

    if(!bar || !Records[bar.index - 1]){
        return false
    }

    return bar
}

function main(){
    LogReset(1)
    var chart_obj = Chart({})
    chart_obj.reset()
    while(true){
        var records = exchange.GetRecords()
        if(!records){
            continue
        }
        var bar = FindLastHighestPoint(records)
        var bar2 = FindLastLowestPoint(records)
        $.PlotRecords(records)
        if(bar){
            $.PlotHLine(bar.record.High, "high point", "red")
        }else{
            Log("Insufficient K-line data, the highest point is the initial K-line bar!")
        }
        if(bar2){
            $.PlotHLine(bar2.record.Low, "low", "green")
        }else{
            Log("Insufficient K-line data, the lowest point is the initial K-line bar!")
        }
        LogStatus(_D(), '\n', bar, '\n', bar2)
        Sleep(1000)
    }
}
```

Detail

https://www.fmz.com/strategy/58179

Last Modified

2017-10-28 15:16:43