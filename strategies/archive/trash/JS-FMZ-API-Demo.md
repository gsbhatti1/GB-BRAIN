> Name

Oak Quantization-JS docking FMZ extension API-Demo

> Author

Oak Quantization

> Source (javascript)

```javascript
var URL = "https://www.fmz.com/api/v1?";
var AK = "b3a53d3XXXXXXXXXXXXXXXXXXX866fe5"; //Replace here with your own AccessKey
var SK = "1d9ddd7XXXXXXXXXXXXXXXXXXX85be17"; //Replace here with your own SecretKey

//Get the object of the basic 5 parameters
function getParam(version, ak, args) {
    return {
        'version': version,
        'access_key': ak,
        'method': 'GetNodeList',
        'args': JSON.stringify(args),
        'nonce': new Date().getTime()
    }
}

//Perform md5 encryption
function md5(param) {
    var paramUrl = param.version + "|" + param.method + "|" + param.args + "|" + param.nonce + "|" + SK
    Log("paramUrl:", paramUrl);
    return Hash("md5", "hex", paramUrl)
}

//Get the final request URL
function getFinalUrl(param) {
    return URL + "access_key=" + AK + "&nonce=" + param.nonce + "&args=" + param.args + "&sign=" + param.sign + "&version=" + param.version + "&method=" + param.method;
}

//The naming method of...args is not supported in js, so use the arguments keyword to obtain the parameter array instead.
function getArgs() {
    return [].slice.call(arguments);
}

function main() {
    //Get 5 basic parameter objects
    var param = getParam("1.0.0", AK, getArgs());
    Log("param:", param);
    //Get the md5 encrypted result of the splicing parameters
    var md5Result = md5(param);
    //Assign the encryption result to the basic parameter object
    param.sign = md5Result;
    //Get the URL of the request api
    var finalUrl = getFinalUrl(param);
    Log("finalUrl:", finalUrl);
    //Execute the request and print the results
    var info = HttpQuery(finalUrl);
    Log("info:", info);
}
```

> Detail

https://www.fmz.com/strategy/208065

> Last Modified

2020-05-16 21:35:13