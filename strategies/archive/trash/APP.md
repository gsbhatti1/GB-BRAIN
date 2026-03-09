``` javascript
var cfgA = {
    extension: {
        layout: 'single',
        height: 300,      
        col: 4
    },
    title: {
        text: 'line'
    },
    xAxis: {
        type: 'datetime'
    },
    series: [{
        name: 'sin',
        data: []
    }, {
        name: 'cos',
        data: []
    }]
}

var cfgB = {
    __isStock: false,
    extension: {
        layout: 'single',
        height: 300, 
        col: 4
    },    
    title: {
        text: 'Pie chart'
    },
    series: [{
        type: 'pie',
        name: 'one',
        // data set after initialization does not need to be updated using the add function; direct modification of the chart configuration will update the series
        data: [                    
            ["BTC_USDT", 25],
            ["LTC_USDT", 25],
            ["ETH_USDT", 25],
            ["EOS_USDT", 25]
        ]                
    }]
}

var cfgC = {
    __isStock: false,
    extension: {
        layout: 'single',
        col: 4,
        height: '300px'
    },
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Bar with negative stack'
    },
    plotOptions: {
        series: {
            stacking: 'normal'
        }
    },
    xAxis: [{
        categories: ['BTC_USDT', 'ETH_USDT', 'EOS_USDT', 'LTC_USDT'],
        reversed: false,
        labels: {
            step: 1
        },
        accessibility: {
            description: 'A'
        }
    }, { // mirror axis on right side
        opposite: true,
        reversed: false,
        categories: ['BTC_USDT', 'ETH_USDT', 'EOS_US_DT', 'LTC_US_DT'],
        linkedTo: 0,
        labels: {
            step: 1
        },
        accessibility: {
            description: 'B'
        }
    }],
    series: [{
        name: 'A',
        data: [
            -6, -4.3, -8, -2.4
        ]
    }, {
        name: 'B',
        data: [
            2.2, 2.1, 2.2, 2.4
        ]
    }]
}

var cfgD = {
    extension: {
        col: 12,
        height: '600px'
    },
    title: {
        text: 'K Line'
    },
    rangeSelector: {
        selected: 1
    },
    yAxis: [{
        labels: {
            align: 'right',
            x: -3
        },
        title: {
            text: 'OHLC'
        },
        height: '50%',
        lineWidth: 2,
        resize: {
            enabled: true
        }
    }, {
        labels: {
            align: 'right',
            x: -3
        },
        title: {
            text: 'Volume'
        },
        top: '55%',
        height: '25%',
        offset: 0,
        lineWidth: 2
    }],        
    tooltip: {
        split: true
    },
    series: [{
        type: 'candlestick',
        name: 'K',
        id: "k",
        data: []
    }, {
        type: 'column',
        name: 'Volume',
        data: [],
        yAxis: 1
    }, {
        type: 'line',
        data: [],
        id: 'line1'
    }, {
        type: 'flags',
        onSeries: 'k',
        data: []
    }]
}

var cfgE = {
    __isStock: false,
    extension: {
        col: 12,
        height: '300px'
    },
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'pie'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
        }
    },
    series: [{
        name: 'Brands',
        colorByPoint: true,
        data: [{
            name: 'BTC_USDT',
            y: 61.41,
            sliced: true,
            selected: true
        }, {
            name: 'ETH_USDT',
            y: 11.84
        }, {
            name: 'LTC_USDT',
            y: 10.85
        }]
    }]
}

var cfgF = {
    __isStock: false,
    extension: {
        layout: 'single',
        col: 6,
        height: '300px'
    },
    chart: {
        type: 'area',
        zoomType: 'xy'
    },
    title: {
        text: 'ETH_USDT Market Depth'
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
    legend: {
        enabled: false
    },
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
        data: [[99, 0.562], [89, 1.856]],
        color: '#03a7a8'
    }, {
        name: 'Asks',
        data: [[100, 0.12], [120, 0.52]],
        color: '#fc5857'
    }]
}

var cfgG = {
    __isStock: false,
    extension: {
        layout: 'single',
        col: 6,
        height: '300px'
    },    
    data: {
        table: 'dat
```