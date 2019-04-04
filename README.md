# ForExLang
Statically typed imperative language

## Overview
Implemented in Python. Main use case - simulation of operations on the foreign exchange market.

Basic features:

* Primitive (`integer`, `string`, `float`, `boolean`) and complex types (like structures)
* Embeded `rate`, `direction`, `pair`, `trend`, `trader` types
* some basic operators (`+`, `-`, `/`, `*`, `%`)
* builtin functions `output`, `numtoa`, `toUSD` 
* Small standard library with basic functions like print, type conversion and currency convertion
* `if` and `while` control statements

## Usage
1) Clone this repository.
2) Create `.py` file and import the `SemanticAnalyzer`.
3) Create instance of `SemanticAnalyzer` and run `analyze_file` method.

## Language overview
### Supported types
**Numbers** are represented with 2 possible types: integer and float with support of +, -, /, *, % operators between all of them. 
**Strings** are like in most other languages
```
"String example"
```
**Character** is the one unicode character in single quotes
```
'c'
```

**Boolean** 
```
ugu, net // istead true and false
```

**Functions** are declared with `func` keyword followed by it's type.
```
func boolean isPositive(d direction) {...}
```
> NOTE: function parameters has format `identifier, type`.


There is 3 **builtin functions**:
* `output`(takes string as an argument and prints it),
* `numtoa` (takes 1 argument (`integer` or `float`), returns string)
* `toUSD` (takes 1 argument (with type `rate`), returns `rate` with right pair leg equal to USD).

## Control flow
#### Assignment
Nothing unusual for primitive types.
Complex types can be assigned with block or by accessing some specific property
```
let pair testPair;
testPair.left = "EUR";
testPair.right = "USD";

```
or
```
let pair testPair;
testPair = {
	left = "EUR";
	right = "USD";
}
```

#### If statement
Conditional expression must evaluate to boolean type, else block is optional
```
if (r1.rateValue < r2.rateValue) {
    return ->;
}
else {
    return <-;
}
```

#### While statement
Conditional expression must evaluate to boolean type. 
```
let integer counter;
counter = 3;

while (counter < 5) {
    output(numtoa(counter));
    counter = counter + 1;
}
```

## How does it work
First step is parsing syntax to lexemes. Next is building and validating AST tree against semantic rules.
Language is statically typed so static analysis is performed by semantic analyzer.

## Features
This language is designed to simplify the presentation of processes in the foreign exchange market and their simulation.

#### Specific types
* `pair` - currency pair. Has two fields: `left` and `right`. (Price of pair always in the right currency). For example: if left = "EUR" and right = "USD" this is similar to the EURUSD currency.
* `rate` - currency rate (price of particular currency pair). Has two fields: `ratePair` and `rateValue`. `ratePair` has type `pair`, `rateValue` - price of currency pair.
* `direction` - can be `->` (direction up) and `<-` (direction down). 
* `trend` - trend of particular rate line. Has two fields: `trDirection` and `trendSize`. `trDirection` has type `direction` and means the price rises or drops, `trendSize` is greater or equal to 0. 

#### Specific functions
* `toUSD` - converts currency rate to USD. Takes 1 argument (with type `rate`), returns `rate` with right pair leg equal to USD (`right = 'USD'`).  This funtion is VERY useful if you need to compare currency pairs with different right leg currency. 

See `example2.txt` with example of using this types.