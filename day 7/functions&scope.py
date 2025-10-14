"""
Recap: What is a Function?
A function is a reusable block of code that performs a specific task.
Functions prevent repetition, make code modular, and improve readability.
"""

def greet_user(name):
    print(f"Hello, {name}! Welcome to Vibe Coding Bootcamp.")

greet_user("Alice") # prints: Hello, Alice! Welcome to Vibe Coding Bootcamp.
greet_user("Bob")   # prints: Hello, Bob! Welcome to Vibe Coding Bootcamp.
greet_user("Charlie") # prints: Hello, Charlie! Welcome to Vibe Coding Bootcamp.

"""
What is Scope?

Scope defines where a variable can be accessed in your program.
There are two main types of scope in Python: Local Scope and Global Scope.
"""


"""
->Local Scope
Variables created inside a function.
Can only be used within that function.
"""

def add_numbers():
    result = 10 + 5  # local variable
    print(result)

add_numbers()
# print(result)  Error: result is not defined outside function


"""
->Global Scope
Variables created outside any function.
Can be accessed from anywhere in the code.
"""
count = 0  # global variable

def increment():
    global count  # tell Python we’re modifying the global variable
    count += 1
    print("Count:", count)

increment()
increment()
print("Final Count:", count)  # Accessing global variable outside function



"""
Best Practice:
Avoid overusing global variables. Keep your code modular by passing data via function parameters.
"""