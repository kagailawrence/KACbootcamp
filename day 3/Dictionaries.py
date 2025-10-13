#Dictionaries (Python) store key-value pairs great for structured data.

student = {
    "name": "James",
    "age": 20,
    "grade": "A",
    "courses": ["Math", "Science"]
}


print(student["name"]) 
print(student["age"])
student["grade"] = "B"
student["city"] = "New York"  # Add new key-value pair
print(student)
student.pop("age")  # Remove key-value pair
student={}
student.clear()  

print(student)  # Print empty dictionary


"""
Store user profiles, settings, or structured data.
Easy to update and retrieve by name (key)
"""