[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html) [![zai](https://circleci.com/gh/sehnsucht13/zai-pl.svg?style=shield)](https://app.circleci.com/pipelines/github/sehnsucht13/zai-pl) [![PyPI version fury.io](https://badge.fury.io/py/zai-pl.svg)](https://pypi.python.org/pypi/zai-pl/) [![PyPI status](https://img.shields.io/pypi/status/zai-pl.svg)](https://pypi.python.org/pypi/zai-pl/)

# Zai

Zai is a small programming language which I wrote for fun. The language:

- Is Dynamically typed
- Is Entirely written in Python
- Supports classes
- Supports first-class functions
- Supports writing and importing modules

**NOTE:** This is a project made for both learning and fun. It is not meant to be used in serious projects.

# Installation
## Git
```bash
git clone https://github.com/sehnsucht13/zai-pl.git
cd zai-pl
# Start a REPL
python3 -m zai
# Run a file called FILENAME.zai
python3 -m zai FILENAME.zai
```
## Pip
```bash
# Install from pip
pip install --user zai-pl

# Start a REPL
zai-pl

# Run a file called FILENAME.zai
zai-pl FILENAME.zai
```
# Examples
## Data Types
Zai supports:
- Strings
- Integers
- Booleans
- Arrays
## Printing
To print a variable you can use the print keyword. Note: For now, `print` can only print one variable at a time.
```
let myVar = 14; // Assign a variable
print myVar; // Print it to STDOUT
```
## Basic Operations
```
print 4 + 4; // 8
print 4 - 4; // 0
print 4 * 4; // 16
print 4 / 4; // 1
print 3 + 2 - (14 + 4) + 3; // -10

print true && false; // False
print true || false; // True
print !true; // False
print -(4 + 4); // -8

print 4 < 3; // False
print 4 <= 3; // False
print 4 > 3; // True
print 4 >= 3; // True

let myArr = [1,2,3]; // Assign to a variable
print myArr[1];  // 2
myArr[1] = 50;
print myArr[1];  // 50

```
## Variables
To initialize a variable, the `let` keyword is used. All variables must be initialized with a value!
```
let myVar = 14;
```
Once a variable is initaialized, it can be reassigned using:
```
myVar = 41;
```
Variables can also be reassigned using a shorthand
```
let myVar = 0;
myVar += 3; // myVar is now 3
myVar -= 3; // myVar is now 0
```
## Conditionals
### If Statements
```
let a = 13;
if (a == 12){
	print "a is 12";
}elif (a == 13){
	print "a is 13";
}
else{
	print "a has an unknown value";
}
// Prints "a is 13"
```
### Switch Statements
All switch statements in zai must have a `default` branch.
```
let b = 33;
switch(b){
	case 1:
	  print "1";
	  break;
	case 33:
	  print "33";
	  break;
	case 22:
	  print "22";
	  break;
	default:
	  print "unknown";
}
// Prints 33
```
If a case omits the `break` keywords, zai will keep evaluating all cases after it until either a  `break` keyword is found or the `default` case is reached.
```
let b = 33;
switch(b){
	case 1:
	  print "1";
	  break;
	case 33:
	  print "33";
	case 22:
	  print "22";
    case 44:
      print "44";
      break;
	default:
	  print "unknown";
}
// Prints:
// 33
// 22
// 44
```
## Loops
### While Loops
```
let counter = 0;
while (counter <= 5){
	counter += 1;
	print "Ran the loop";
}
// Prints:
// Ran the loop
// Ran the loop
// Ran the loop
// Ran the loop
// Ran the loop
// Ran the loop
```
### Do-While Loops
```
do{
	print "Ran the loop";
	counter += 1;
}while(counter <= 3);
// Prints:
// Ran the loop
// Ran the loop
// Ran the loop
// Ran the loop
```
## Blocks
`zai` supports creating nested blocks similar to those in rust.
```
let myVar = 1;
print myVar; // Prints 1
{
    let myVar = 2;
    print myVar; // Prints 2
}
// Scope ends here
print myVar; // Prints 1
```

## Functions
### Declaring a function
Functions can be declared as follows:
```
func myFunc(a,b){
    print a;
    print b;
    return a + b;
}
```
### Invoking a function
Functions are invoked like most other languages.
```
func myFunc(a,b){
    print a;
    print b;
    return a + b;
}

myFunc(1,2);
```

`zai` has support for first class functions.
```
func f1(a){
    print a;
}

func f2(callback){
    print "Do stuff here";
    callback("Done");
}

f2(f1);
// This will result in
// Do stuff here
// Done


func outer(){
    let innerVar = "a";
    func inner(){
        print innerVar;
    }
    return inner;
}

let retVal = outer();
retVal();
// This will print "a" to the output.



func toBeAssigned(a1, a2){
	print a1 + a2;
}

let addFunc = toBeAssigned;
addFunc(1,1); // Prints 2

```
## Classes
Classes can define a `constructor` function which takes care of initializing class variables. All class instance variables must be prepended with the keyword `this` which refers to the class instance itself. To access the variables, use `this.VAR_NAME`. Class instance variables can also be reassigned as usual.
```
class myClass{
	func constructor(a,b){
		let this.a = a;
		let this.b = b;
	}

	func printVals(){
		print this.a;
		print this.b;
	}

	func addToA(val){
		print this.a + val;
	}

	func reassignA(newVal){
		this.a = newVal;
	}
}


let myClassInstance = myClass(1,2); // Init class
myClassInstance.printVals(); // Print 1 and then 2
myClassInstance.addToA(4); // Print 5

print myClassInstance.a; // Prints 1
myClassInstance.reassignA(4); // Assign a to 4
print myClassInstance.a; // Prints 4
```

Classes in zai do not need to have constructors.
```
class noConstructorClass{
	func initA(val){
		let this.a = val;
	}

	func addToA(val){
		print this.a + val;
	}
}
let myClassInstance2 = noConstructorClass(); // init class
myClassInstance2.initA(1); // Set a to 1
myClassInstance2.addToA(4); // Add 4 to a and print. Prints 5
let myClassInstance2.newVar = 14; // Create a new variable called newVar
print myClassInstance2.newVar; // Print newVar
```
## Imports
zai supports importing modules using the `import` keyword. Imported modules can either be in the same folder that zai was invoked from or they can be somewhere on zai's path. zai's path is set using the environment variable called `ZAI_PATH`.

Modules are imported using the following precedence:
1. Look into the current folder. If the module exists, import it from there.
2. Look into all folder in the `ZAI_PATH` environment variable(if it exists). Folders are evaluated in the order they are declared in.

Example:
If `ZAI_PATH` contains `$HOME/test_modules/:$HOME/` then zai will first look in the current folder(where zai is ran from), the `test_modules` within the user's home directory and finally the users home directory.

All modules should have a file name which ends with `.zai`. If they do not then zai will never find them.

Example:
1. `myModule.zai`: Will be found if on zai's path.
2. `myModule` or `myModule.txt`:  Will never be found.

### Example of importing a module
Content of main file
```
import myModule

myModule.sayHello(); // Prints "Hello from myModule"
```

Content of a file called `myModule.zai` located in a folder somewhere on the paths pointed to by the `ZAI_PATH` environment variable or in the current folder where zai was ran from.
```
func sayHello(){
	print "Hello from myModule";
}

```
### Importing modules using a custom name
Borrowing from the example above:

Content of a file called `myModule.zai`.
```
func sayHello(){
	print "Hello from myModule";
}

```

```
import myModule as newMod

newMod.sayHello(); // Prints "Hello from myModule"
```

Note: modules are represented as plain objects in zai. Therefore, they can be stored as normal variables.
```
import myModule as newMod

let reassignedModule = newMod;
reassignedModule.sayHello(); // Prints "Hello from myModule"
```
# Missing Features and Future Improvements
Here is a list of the features which are currently missing but will be implemented in the future
- [ ] Basic class inheritance
- [ ] Make lexer ignore comments
- [ ] Printing more than one variable at a time.
- [ ] Floating Point Numbers
- [ ] Prefix/Postfix increment and decrement operators
- [ ] Better test suite
- [ ] Importing and calling native python functions(Maybe...)

# Internals and Documentation
- The language grammar can be found within the [docs/grammar file](https://github.com/sehnsucht13/zai-pl/blob/master/docs/grammar)
- Some more in-depth details about the implementation(how objects are represented internally, environment...) can be found within [docs/architecture.md file](https://github.com/sehnsucht13/zai-pl/blob/master/docs/architecture.md)

# Resources
Below are some of the resources which I found helpful while making this.
- [Crafting Interpreters](https://craftinginterpreters.com/ "Crafting Interpreters Homepage")
- [Modern Compiler Design](https://dickgrune.com/Books/MCD_2nd_Edition/ "Modern Compiler Design")
- [Max Bernstein's Blog](https://bernsteinbear.com/blog/ "bernsteinbear")
