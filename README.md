# ForExLang
Statically typed imperative language

## Overview
Implemented in Python. Main use case - simulation of operations on the foreign exchange market.

Basic features:

* Primitive (`integer`, `string`, `float`, `boolean`) and complex types (like structures)
* Embeded `rate`, `direction`, `pair`, `trend`, `trader` types
* some basic operators (`+`, `-`, `/`, `*`, `%`)
* builtin functions `output`, `numtoa`, `toUSD` 
* Small standard library with basic functions like print, type conversion and data validation for embeded types
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
ugu, net // istead true and 
```

**Functions** are declared with `func` keyword followed by it's type.
```
func boolean isPositive(num direction) {...}
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
