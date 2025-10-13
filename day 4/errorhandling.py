"""
Error Handling Basics
Why Handle Errors?
Errors can break your program.
Handling them properly allows your app to keep running smoothly
even when something goes wrong.
Common Error Types
1. SyntaxError: Mistakes in the code structure.
2. TypeError: Mismatched data types.
3. ValueError: Invalid value for a function.
4. IndexError: Accessing out-of-range list elements.
5. KeyError: Accessing non-existent dictionary keys.
"""

try:
    num = int(input("Enter a number: "))
    print(10 / num)
except ValueError:
    print("Invalid input! Please enter a number.")
except ZeroDivisionError:
    print("Cannot divide by zero.")


"""
why important to handle errors
1. User Experience: Prevents crashes, provides feedback.
2. Debugging: Helps identify and fix issues.
3. Data Integrity: Avoids corrupting data.
4. Security: Prevents exploitation of vulnerabilities.
5. Reliability: Ensures consistent application behavior.
6. Graceful Degradation: Allows partial functionality when errors occur.


"""

