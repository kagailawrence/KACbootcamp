#Lists (Python) and Arrays (JavaScript) hold multiple values in one variable.

fruits = ["apple", "banana", "cherry"] 
print(fruits[2])  # Access first item
fruits.append("orange")  # Add item
fruits.append("something else")  # Add item
print(fruits)
fruits.remove("banana")  # Remove item
print(fruits)
print(len(fruits))  # Length of list
fruits.sort()  # Sort list
print(fruits)

db=[]
student1 = {
    "name": "James",
    "age": 20,
    "grade": "A",
    "courses": ["Math", "Science"]
}
student2 = {
    "name": "Alice",
    "age": 22,
    "grade": "B",
    "courses": ["English", "History"]
}
db.append(student1)
db.append(student2)
print(db)
