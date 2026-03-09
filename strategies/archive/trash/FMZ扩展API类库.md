> Name

FMZ extension API class library

> Author

ChaoZhang

> Strategy Description

Article from Mr. Ao <<Ok teaches you step by step how to use JS to connect to the FMZ extension API>>
https://www.fmz.com/digest-topic/5631

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|AccessKey|AccessKey|AccessKey|
|SecretKey|SecretKey|SecretKey|


> Source (javascript)

``` javascript
var URL = "https://www.fmz.com/api/v1?";
function GetUrl(method, dateInfo) {
    var param = getParam("1.0.0", AccessKey, method, dateInfo);
    //Log("param:",param);
    //Get the md5 encrypted result of the splicing parameters
    var md5Result = md5(param);
    //Assign the encryption result to the basic parameter object
    param.sign = md5Result;
    //Get the URL of the request api
    return getFinalUrl(param);
}
//Get API information through parameters
$.getAPIInfo = function (method, dateInfo) {
    var info;
    while (true) {
        try {
            info = HttpQuery(GetUrl(method, dateInfo));
            if (!info || info.indexOf("result") == -1) {
                Log("info error", info, method, dateInfo);
                Sleep(2000);
            } else {
                break;
            }
        } catch (error) {
            Log(error.message)
        }
    }
    return JSON.parse(info);
}

//Get the object of the basic 5 parameters
function getParam(version, ak, method, args) {
    return {
        version: version,
        access_key: ak,
        method: method,
        args: JSON.stringify(args),
        nonce: new Date().getTime(),
    };
}

//Perform md5 encryption
function md5(param) {
    var paramUrl = param.version + "|" + param.method + "|" + param.args + "|" + param.nonce + "|" + SecretKey;
    //Log("paramUrl:",paramUrl);
    return Hash("md5", "hex", paramUrl);
}

//Get the final request URL
function getFinalUrl(param) {
    //Log(param)
    return URL + "access_key=" + AccessKey + "&nonce=" + param.nonce + "&args=" + escape(param.args) + "&sign=" + param.sign + "&version=" + param.version + "&method=" + param.method;
}

//The naming method of...args is not supported in js, so use the arguments keyword to obtain the parameter array instead.
$.getArgs = function () {
    return [].slice.call(arguments);
}
function init(){
    //Log("mode")
    if (AccessKey == "" || SecretKey == "") {
        throw "AccessKey or SecretKey cannot be empty";
    }

    //let robotId = _G();
    //$.getAPIInfo("CommandRobot", $.getArgs(robotId, "coverAll"))
}
$.AccessKey = AccessKey;
$.SecretKey = SecretKey;
```


> Detail

https://www.fmz.com/strategy/318271

> Last Modified

2024-06-01 18:40:01