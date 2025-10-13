
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Select operation: +, -, *, /")
operator = input("Enter operator: ")

if operator == '+':
    print("Result:", num1 + num2)
elif operator == '-':
    print("Result:", num1 - num2)
elif operator == '*':
    print("Result:", num1 * num2)
elif operator == '/':
    print("Result:", num1 / num2)
else:
    print("Invalid operator!")
