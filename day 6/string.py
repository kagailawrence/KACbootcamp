"""
A string is a sequence of characters enclosed in quotes (' ' or " ").
Strings are used to represent text such as names, messages, or paragraphs.
"""

name = "Lawrence"
message = "Welcome to Vibe Coding Bootcamp!"
print(name)
print(message)


"""" Common String Operations
| Action       | Python                       | JavaScript                   |
| ------------ | ---------------------------- | ---------------------------- |
| Get length   | len(text)                    | text.length                  |
| Uppercase    | text.upper()                 | text.toUpperCase()           |
| Lowercase    | text.lower()                 | text.toLowerCase()           |
| Replace text | text.replace("old", "new")   | text.replace("old", "new")   |
| Split text   | text.split(" ")              | text.split(" ")              |
| Join text    | ' '.join(list)               | array.join(" ")               |
"""
# Example usage of string operations
text = "Hello, World!"
print(len(text))               # Get length
print(text.upper())           # Uppercase
print(text.lower())           # Lowercase
print(text.replace("World", "Python"))  # Replace text
print(text.split(", "))       # Split text  ['Hello', 'Python!']
words = ["Hello", "Python"]
print(' '.join(words))        # Join text # "Hello Python"


# String Formatting
name = "Alice"
age = 30
print("My name is {} and I am {} years old.".format(name, age))


"""
Why It Matters:
String formatting is critical for generating user messages, logs, and dynamic outputs.
"""