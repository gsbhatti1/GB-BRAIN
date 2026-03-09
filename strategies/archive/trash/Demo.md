Name

How Demo uses strategy interaction to dynamically adjust strategy parameters

Author

momox

Strategy Description

The strategy requires constant testing and adjustment, and the parameters are often changed. Stopping and restarting every time is laborious and laborious, and the original profit progress will be lost (although it can also be restored through global parameters). In fact, botvs has provided a way to dynamically adjust parameters—“Strategy Interaction”

Strategy Arguments



|Button|Default|Description|
|----|----|----|
|A3|999|AAA parameters|
|B3|Botvs|BBB parameters|


Source (javascript)

``` javascript
varInterval=2000;

// AAA, BBB are the parameters that you want to dynamically adjust in the strategy
varAAA=0;
var BBB="hello world";

function main() {
while(true){
onTick();
Sleep(Interval);
}
}

function onTick(){
set_command();
Log("AAA="+AAA," BBB="+BBB);
}

// Get dynamic parameters (strategy interaction content)
function set_command() {

var get_command = GetCommand(); // The GetCommand method is a method for obtaining parameters. The obtained parameters are in the form of strings. The format is "parameter name: parameter value". See BotVS API documentation.
if (get_command != null) {
if (get_command.indexOf("A3:") == 0) { // If the incoming parameter name is A3 (starting with "A3:", it means it is an A3 parameter)

AAA = (get_command.replace("A3:", "")); // Assign the value to AAA in the policy (replace the leading string with empty, and the rest is our parameter value)

Log("AAA becomes:" + AAA);
}

if (get_command.indexOf("B3:") == 0) { // If the parameter name passed in is B3 (it starts with "B3:", it means it is a B3 parameter)

BBB = (get_command.replace("B3:", "")); // Assign value to BBB in the strategy (replace the leading string with empty, and the rest is our parameter value)

Log("BBB becomes:" + BBB);
}

}
}
```

Detail

https://www.fmz.com/strategy/8379

Last Modified

2016-01-09 21:18:07