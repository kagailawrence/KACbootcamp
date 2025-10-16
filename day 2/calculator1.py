# calculator.py

def calculator():
    print("🧮 Simple Python Calculator")
    print("-" * 30)

    try:
        # Step 1: Get inputs
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        # Step 2: Display options
        print("\nSelect operation:")
        print(" +  Addition")
        print(" -  Subtraction")
        print(" *  Multiplication")
        print(" /  Division")

        operator = input("\nEnter operator: ").strip()

        # Step 3: Perform calculation
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                print("⚠️  Error: Division by zero is not allowed.")
                return
            result = num1 / num2
        else:
            print("❌ Invalid operator! Please choose +, -, *, or /.")
            return

        # Step 4: Output result
        print(f"\n✅ Result: {num1} {operator} {num2} = {result}")

    except ValueError:
        print("⚠️  Invalid input. Please enter numbers only.")

# Run program
if __name__ == "__main__":
    calculator()
