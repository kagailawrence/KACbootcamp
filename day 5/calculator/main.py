from math_operations import add, subtract, multiply, divide, power, sqrt, factorial
from utils import get_numbers

print("Choose operation: + or -")
op = input("Enter operator: ")
a, b = get_numbers()

if op == '+':
    print("Result:", add(a, b))
elif op == '-':
    print("Result:", subtract(a, b))
elif op == '*':
    print("Result:", multiply(a, b))
elif op == '/':
    try:
        print("Result:", divide(a, b))
    except ValueError as e:
        print("Error:", e)
elif op == '^':
    print("Result:", power(a, b))
elif op == 'sqrt':
    try:
        print("Result:", sqrt(a))
    except ValueError as e:
        print("Error:", e)
elif op == 'factorial':
    try:
        print("Result:", factorial(a))
    except ValueError as e:
        print("Error:", e)
else:
    print("Invalid operator.")

    