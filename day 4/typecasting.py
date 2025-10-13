"""
type casting in Python
Type casting is the process of converting a variable from one data type to another.
In Python, you can use built-in functions to perform type casting.
Here are some common type casting functions:
"""


numberstring = "123"
number = int(numberstring)  # Convert string to integer
print(number)  # Output: 123
print(type(number))  # Output: <class 'int'>


floatstring = "45.67"
floatnumber = float(floatstring)  # Convert string to float
print(floatnumber)  # Output: 45.67
print(type(floatnumber))  # Output: <class 'float'>

num = 10
num_float = float(num)  # Convert integer to float
print(num_float)  # Output: 10.0
print(type(num_float))  # Output: <class 'float'>


num2 = 5.89
num_int = int(num2)  # Convert float to integer (truncates decimal part)
print(num_int)  # Output: 5
print(type(num_int))  # Output: <class 'int'>



"""
Why Type Casting?
1. Data Compatibility: Ensures variables are in the correct format for operations.
2. Prevent Errors: Avoids type-related errors during execution.
3. Data Manipulation: Allows for easier data processing and manipulation.
4. User Input Handling: Converts user input (usually strings) to appropriate types.
5. Interfacing with APIs: Ensures data types match expected formats when
 interacting with external systems.
 """