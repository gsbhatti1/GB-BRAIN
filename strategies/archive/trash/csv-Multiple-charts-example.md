``` javascript
var tradeHistory = {buyData:{amount:0, money:0}, sellData:{amount:0, money:0}, a:0, b:0, c:0, d:0, total:0}
var updateB = 0
var lastNet = 0
var updateD = 0
if(_G('tradeHistory')){
    tradeHistory = _G('tradeHistory')
}
function getDepth(){
    var asks = []
    var bids = []
    var temp = 0
    var depth = JSON.parse(HttpQuery('https://api.binance.com/api/v1/depth?symbol=BTCUSDT'))
    if(!depth){
        return false
    }
    depth.bids.reverse()
    for(i=0;i<depth.bids.length;i++){
        temp += parseFloat(depth.bids[i][1])
    }
    for(i=0;i<depth.bids.length;i++){
        temp -= parseFloat(depth.bids[i][1])
        bids.push([parseFloat(depth.bids[i][0]), temp])
    }
    temp = 0
    for(i=0;i<depth.asks.length;i++){
        temp += parseFloat(depth.asks[i][1])
        asks.push([parseFloat(depth.asks[i][0]), temp])
    }
    return {asks:asks,bids:bids}
    
}
var chartA = {
    __isStock: false,
    extension: {
        layout: 'single',
        col: 6, // Specifies the width unit value, total is 12
        height: 500,
    },
    title: {
        text: 'Volume Distribution Chart'
    },
    xAxis: [{
        title: { text: 'Data' },
        alignTicks: false
    }, {
        title: { text: 'Histogram' },
        alignTicks: false,
        opposite: true
    }],

    yAxis: [{
        title: { text: 'Data' }
    }, {
        title: { text: 'Histogram' },
        opposite: true
    }],

    series: [{
        name: 'Histogram',
        type: 'histogram',
        xAxis: 1,
        yAxis: 1,
        baseSeries: 's1',
        zIndex: -1
    },{
        name: 'Data',
        type: 'scatter',
        data: [],
        id: 's1',
        marker: {
            radius: 1.5
        }
    }]
};
var chartB = {
    extension: {
        layout: 'single', // Not part of the group, displayed separately. Default is grouped 'group'
        col: 6,
        height: 300, // Specifies the height
    },
    credits: {
        enabled: false
    },
    title: {
        text: 'Net Purchase Funds'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: 'Net Purchase',
        type: 'column',
        data: []
    }],
}
var chartC = {
    extension: {
        layout: 'single', // Not part of the group, displayed separately. Default is grouped 'group'
        col: 6,
        height: 300,      // Specifies the height
    },
    title: {
        text: 'Transaction Price'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: 'last',
        data: [],
    }]
}
var chartD = {
    __isStock: false,
    extension: {
        layout: 'single', // Not part of the group, displayed separately. Default is grouped 'group'
        col: 6,
        height: 500,      // Specifies the height
    },
    chart: {
        type: 'area',
        zoomType: 'xy'
    },
    title: {
        text: 'BTC-USDT Depth'
    },
    xAxis: {
        minPadding: 0,
        maxPadding: 0,
        plotLines: [{
            color: '#888',
            value: 0.1523,
            width: 1,
            label: {
                text: 'Actual price',
                rotation: 90
            }
        }],
        title: {
            text: 'Price'
        }
    },
    yAxis: [{
        min:0,
        lineWidth: 1,
        gridLineWidth: 1,
        title: null,
        tickWidth: 1,
        tickLength: 5,
        tickPosition: 'inside',
        labels: {
            align: 'left',
            x: 8
        }
    }, {
        opposite: true,
        linkedTo: 0,
        lineWidth: 1,
        gridLineWidth: 0,
        title: null,
        tickWidth: 1,
        tickLength: 5,
        tickPosition: 'inside',
        labels: {
            align: 'right',
            x: -8
        }
    }],
    plotOptions: {
        area: {
            fillOpacity: 0.2,
            lineWidth: 1,
            step: 'center'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size=10px;">Price: {point.key}</span><br/>',
        valueDecimals: 2
    },
    series: [{
        name: 'Bids',
        data: [],
        color: '#03a7a8'
    }, {
        name: 'Asks',
        data: [],
        color: '#fc5857'
    }]
};
var chartE = {
    __isStock: false,
    extension: {
        layout: 'single', // Not part of the group, displayed separately. Default is grouped 'group'
        col: 6,
        height: 500,      // Specifies the height
    },
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: 'Transaction Quantity<br>Distribution<br>',
        align: 'center',
        verticalAlign: 'middle',
        y: 40
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '110%'
        }
    },
    series: [{
        type: 'pie',
        name: 'Ratio',
        innerSize: '50%',
        data: []
    }]
}
var chartF = {
    extension: {
        layout: 'single', // Not part of the group, displayed separately. Default is grouped 'group'
        col: 6,
        height: 300,      // Specifies the height
    },
    title: {
        text: 'Total Net Purchase'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: 'last',
        data: [],
    }]
}
var chart = Chart([chartB,chartC,chartD,chartA,chartF,chartE]);
//chart.reset()
function main() {
    var client = Dial("wss://stream.binance.com:9443/ws/" + 'btcusdt' + "@trade", 60)
    var updateTime = new Date().getTime()
    while(true){
        var trade = JSON.parse(client.read())
        if(trade.m){
            tradeHistory.sellData.amount += parseFloat
```