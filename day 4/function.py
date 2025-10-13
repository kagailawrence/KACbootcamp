"""
Functions Definition, Parameters & Return Values
What is a Function?

A function is a block of code that performs a specific task.
Instead of repeating code multiple times, you can write it once and reuse it.

Definition: Declaring the function.

Parameters: Values you pass into the function.

Return: Value the function gives back.

instance where to use functions.
1. Code Reusability: Write once, use multiple times.
2. Modularity: Break down complex problems into smaller, manageable pieces.
3. Readability: Makes code easier to read and understand.
4. Maintainability: Easier to update and maintain code.
5. Abstraction: Hide complex logic behind simple function calls.
6. Testing: Functions can be tested independently.
"""


# Function definition
def greet(name):
    return f"Hello, {name}!"


# Calling the function
message = greet("James")
print(message)  # Output: Hello, James

def log():
    print("error, World!")

log()  # Output: error, World!

def add(a, b):
    return a + b

def Multiply(x, y):
    return x * y

result = add(5, 3)
print("Result:", result) # Output: Result: 8


"""
Parameters vs Return Values
Term	        Meaning	                    Example
Parameter	    Input your function expects	name in greet(name)
Argument	    Actual value you give	"Pamela"
Return value	What comes back	"Hello, Pamela!"
"""