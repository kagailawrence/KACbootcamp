class Student:
    def __init__(self, name, age, grade, courses, units):
        self.name = name
        self.age = age
        self.grade = grade
        self.courses = courses
        self.units = units
    
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Grade: {self.grade}")
        print("Courses:", ", ".join(self.courses))
        print("Units:", ", ".join(self.units))
        print("-" * 30)

# Create 3 student objects
students = [
    Student("John Doe", 20, "A", 
            ["Computer Science", "Mathematics"], 
            ["Programming 101", "Calculus"]),
    Student("Jane Smith", 19, "B+",
            ["Business", "Economics"],
            ["Marketing", "Microeconomics"]),
    Student("Mike Johnson", 21, "A-",
            ["Engineering", "Physics"],
            ["Mechanics", "Electromagnetics"])
]

# Print all students' info using a loop
for student in students:
    student.display_info()