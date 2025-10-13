"""
Why Learn File Handling?

File handling allows your programs to store, read, and 
manipulate data from external files (e.g., text, JSON, logs, reports).
This is the foundation of all data-driven applications.
"""

# Writing to a file
with open("notes.txt", "w") as file:
    file.write("Welcome to Vibe Coding Bootcamp!\n")
    file.write("This is our first file handling example.")

# Reading from a file
with open("notes.txt", "r") as file:
    content = file.read()
    print("File Content:\n", content)

# Appending to a file
with open("notes.txt", "a") as file:
    file.write("\nLet's append a new line to this file.")   

with open("notes.txt", "r+") as file:
    file.write("\nThis line is added using r+ mode.")
    updated_content = file.read()
    print("Updated File Content:\n", updated_content)
    



"""
File Modes:
| Mode | Description                     |
|------|---------------------------------|
| 'r'  | Read (default)                  |
| 'w'  | Write (creates or overwrites)   |
| 'a'  | Append (adds to the end)        |  
| 'r+' | Read and Write                  |
| 'b'  | Binary mode (for non-text files)|

"""