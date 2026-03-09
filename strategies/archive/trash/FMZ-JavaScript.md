> Name

FMZ Tutorial - JavaScript Quick Start Guide

> Author

TradeMan Author



> Source (javascript)

``` javascript
// The `console.log` in the text can be replaced with Log functions during FMZ debugging.
// Comments are similar to C; this is a single-line comment.
/* This is a multi-line 
   comment */

// Statements can end with a semicolon
doStuff();

// ...but semicolons can also be omitted, and will be inserted automatically at the beginning of a new line (except in certain special cases).
doStuff()

// Because these special cases can result in unexpected results, we keep the semicolon here.

///////////////////////////////////
// 1. Numbers, Strings, and Operators

// JavaScript has only one number type (i.e., 64-bit IEEE 754 double-precision floating point). 
// Doubles have 52 bits for the mantissa, which can precisely represent integers up to 9✕10¹⁵.
3; // = 3
1.5; // = 1.5

// All basic arithmetic operations behave as expected.
1 + 1; // = 2
0.1 + 0.2; // = 0.30000000000000004
8 - 1; // = 7
10 * 2; // = 20
35 / 5; // = 7

// Including division that does not result in an integer.
5 / 2; // = 2.5

// Bitwise operations are the same as in other languages; when bitwise operations are performed on floating-point numbers,
// they will be converted to *at most* a 32-bit unsigned integer.
1 << 2; // = 4

// Parentheses can determine precedence.
(1 + 3) * 2; // = 8

// There are three non-numeric number types
Infinity; // Result of 1/0
-Infinity; // Result of -1/0
NaN; // Result of 0/0

// And there are boolean values.
true;
false;

// Strings can be constructed using single or double quotes.
'abc';
"Hello, world";

// The `!` operator is used for negation.
!true; // = false
!false; // = true

// Equality ===
1 === 1; // = true
2 === 1; // = false

// Inequality !=
1 !== 1; // = false
2 !== 1; // = true

// More comparison operators 
1 < 10; // = true
1 > 10; // = false
2 <= 2; // = true
2 >= 2; // = true

// Strings can be concatenated using +
"Hello " + "world!"; // = "Hello world!"

// Strings can also be compared with < and >
"a" < "b"; // = true

// When using `==` for comparison, type coercion occurs...
"5" == 5; // = true
null == undefined; // = true

// ...unless you use ===
"5" === 5; // = false
null === undefined; // = false 

// ...which can lead to strange behavior.
13 + !0; // 14
"13" + !0; // '13true'

// You can use `charAt` to get a character from a string.
"This is a string".charAt(0);  // = 'T'

// ...or use `substring` to get larger portions.
"Hello world".substring(0, 5); // = "Hello"

// `length` is a property, so do not use ().
"Hello".length; // = 5

// There are two special values: `null` and `undefined`.
null;      // Used to represent deliberately empty values
undefined; // Used to represent values that have not been set (though undefined itself is actually a value)

// false, null, undefined, NaN, 0, and "" are considered falsy; all others are truthy.
// Note that 0 is logically false while "0" is logically true, even though 0 == "0".

///////////////////////////////////
// 2. Variables, Arrays, and Objects

// Variables need to be declared using the `var` keyword. JavaScript is a dynamically typed language,
// so you do not have to specify types. Assignments use `=`.
var someVar = 5;

// If you declare a variable without the `var` keyword, no error will occur...
someOtherVar = 10;

// ...but this will create the variable in the global scope rather than your defined current scope.

// Uninitialized variables are set to undefined.
var someThirdVar; // = undefined

// Arithmetic operations on variables have shorthand:
someVar += 5; // Equivalent to `someVar = someVar + 5`, now someVar is 10
someVar *= 10; // Now someVar is 100

// Increment and decrement also have shorthand.
someVar++; // Now someVar is 101
someVar--; // Back to 100

// Arrays are ordered lists of arbitrary types.
var myArray = ["Hello", 45, true];

// Array elements can be accessed using square bracket indexing.
// Array indices start from 0.
myArray[1]; // = 45

// Arrays are mutable and have a `length` property.
myArray.push("World");
myArray.length; // = 4

// You can add/modify at specific indices
myArray[3] = "Hello";

// JavaScript objects are equivalent to other languages' “dictionaries” or “maps”: unordered collections of key-value pairs.
var myObj = {key1: "Hello", key2: "World"};

// Keys are strings, but if the key itself is a valid JS identifier, quotes are not required.
// Values can be of any type.
var myObj = {myKey: "myValue", "my other key": 4};

// Object property access can be done using square brackets
myObj["my other key"]; // = 4

// ...or you can use `.` if the property is a valid identifier
myObj.myKey; // = "myValue"

// Objects are mutable; values can also be changed or new keys added.
myObj.myThirdKey = true;

// If you try to access an undefined value, it will return undefined.
myObj.myFourthKey; // = undefined

///////////////////////////////////
// 3. Logic and Control Structures

// The syntax in this section is almost identical to Java's.

// `if` statements work the same as in other languages.
1 + 1; // = 2
0.1 + 0.2; // = 0.30000000000000004

// Parentheses can determine precedence.
(1 + 3) * 2; // = 8

// The `setTimeout` function is asynchronous, so the `sayHelloInFiveSeconds` function will exit immediately,
// and `setTimeout` will call `inner` later.
function sayHelloInFiveSeconds(name){
    var prompt = "Hello, " + name + "!";
    // Inner functions default to local scope
    // like `var` declarations.
    function inner(){
        alert(prompt);
    }
    setTimeout(inner, 5000);
}

// The `setTimeout` function is asynchronous; the `sayHelloInFiveSeconds` function will exit immediately,
// and `setTimeout` will call `inner` later.
// Because `inner` is "closed over" by `sayHelloInFiveSeconds`,
// it can still access the `prompt` variable when called, even after `sayHelloInFiveSeconds` has exited.

sayHelloInFiveSeconds("Adam"); // Will alert "Hello, Adam!" in 5 seconds

///////////////////////////////////
// 4. Objects, Constructors, and Prototypes

// Objects can contain methods.
var myObj = {
    myFunc: function(){
        return "Hello world!";
    }
};
myObj.myFunc(); // = "Hello world!"

// When an object's method is called, the `this` keyword refers to its containing object at runtime.
myObj = {
    myString: "Hello world!",
    myFunc: function(){
        return this.myString;
    }
};
myObj.myFunc(); // = "Hello world!"

// But when a function accesses `this`, it accesses its execution context rather than its definition context.
```