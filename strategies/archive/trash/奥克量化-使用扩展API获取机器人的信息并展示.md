> Name

Oak Quantification-Use extended API to obtain robot information and display

> Author

Oak Quantization



> Source (javascript)

```javascript
var URL = "https://www.fmz.com/api/v1?";
var AK = "b3a53d3XXXXXXXXXXXXXXXXXXX866fe5"; //Replace here with your own AccessKey
var SK = "1d9ddd7XXXXXXXXXXXXXXXXXXX85be17"; //Replace here with your own SecretKey
var OFF_SET = 0; //query page number subscript
var PAGE_LENGTH = 5; //Query the data length of the page

function main() {
    LogReset();
    while (true) {
        //Get robot list information
        var robotListJson = getAPIInfo('GetRobotList', getArgs(OFF_SET, PAGE_LENGTH, -1));
        //Get the robot list information
        var robotList = robotListJson.data.result.robots;
        //Create an array to display robot information
        var infoArr = new Array();
        var infoArr_index = 0;
        for (index = 0; index < robotList.length; index++) {
            var robot = robotList[index];
            //Get the robot ID currently looped to
            var robotId = robot.id;
            //Get robot details
            var robotDetailJson = getAPIInfo('GetRobotDetail', getArgs(robotId));
            var robotDetail = robotDetailJson.data.result.robot;
            //Convert details to array object
            var arr = getLogPrientItem(robotDetail);
            infoArr[infoArr_index] = arr;
            infoArr_index++;
        }
        Log("infoArr:", infoArr);
        LogStatus(JSON.stringify(getLogPrient(infoArr)));
        Sleep(30000);
    }
}

function getLogPrient(infoArr) {
    return {
        type: 'table',
        title: 'Oak\'s quantified robot display',
        cols: ['Robot ID', 'Robot name', 'Strategy name', 'Next deduction time', 'Consumption time ms', 'Consumption amount CNY', 'Last active time', 'Whether it is public'],
        rows: infoArr
    };
}

//Get API information through parameters
function getAPIInfo(method, dateInfo) {
    //Get 5 basic parameter objects
    var param = getParam("1.0.0", AK, method, dateInfo);
    //Log("param:", param);
    //Get the md5 encrypted result of the splicing parameters
    var md5Result = md5(param);
    //Assign the encryption result to the basic parameter object
    param.sign = md5Result;
    //Get the URL of the request api
    var finalUrl = getFinalUrl(param);
    //Log("finalUrl:", finalUrl);
    //Execute the request and print the results
    var info = HttpQuery(finalUrl);
    //Log("info:", info);
    return JSON.parse(info);
}

//Get the object of the basic 5 parameters
function getParam(version, ak, method, args) {
    return {
        version: version,
        access_key: ak,
        method: method,
        args: JSON.stringify(args),
        nonce: new Date().getTime()
    };
}

//Perform md5 encryption
function md5(param) {
    var paramUrl = param.version + "|" + param.method + "|" + param.args + "|" + param.nonce + "|" + SK
    //Log("paramUrl:", paramUrl);
    return Hash("md5", "hex", paramUrl);
}

//Get the final request URL
function getFinalUrl(param) {
    return URL + "access_key=" + AK + "&nonce=" + param.nonce + "&args=" + param.args + "&sign=" + param.sign + "&version=" + param.version + "&method=" + param.method;
}

//The naming method of...args is not supported in js, so use the arguments keyword to obtain the parameter array instead.
function getArgs() {
    return [].slice.call(arguments);
}

//Get the display details object 'robot ID', 'robot name', 'strategy name', 'next deduction time', 'time consumed ms', 'amount CNY consumed', 'latest active time', 'whether it is public'],
function getLogPrientItem(robotDetail) {
    var itemArr = new Array();
    var iteArr_index = 0;
    itemArr[iteArr_index++] = robotDetail.id;
    itemArr[iteArr_index++] = robotDetail.name;
    itemArr[iteArr_index++] = robotDetail.strategy_name;
    itemArr[iteArr_index++] = robotDetail.charge_time;
    itemArr[iteArr_index++] = robotDetail.charged;
    itemArr[iteArr_index++] = robotDetail.consumed / 1e8;
    itemArr[iteArr_index++] = robotDetail.refresh;
    itemArr[iteArr_index++] = robotDetail.public == 0 ? "Public" : "Unpublished";
    return itemArr;
}
```


> Detail

https://www.fmz.com/strategy/208526

> Last Modified

2020-05-18 21:28:05