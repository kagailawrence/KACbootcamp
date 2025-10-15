"""
Inheritance  Reusing Code

Inheritance allows one class to borrow attributes and methods from another.
It helps eliminate repetition and promotes reuse.

"""

# Parent class
class Animal:
    def speak(self):
        print("This animal makes a sound.")

# Child class
class Dog(Animal):
    def speak(self):
        print("Woof!")

# Another child class
class Cat(Animal):
    def speak(self):
        print("Meow!")

# Objects
dog = Dog()
cat = Cat()

dog.speak()
cat.speak()

#The child classes Dog and Cat inherit from Animal,
# but can override methods to customize behavior.

# Example 2: Inheriting attributes and methods
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hi, I'm {self.name} and I'm {self.age} years old.")

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)  # Call the parent constructor
        self.student_id = student_id
        self.course = None  # New attribute specific to Student

    def introduce(self):
        super().introduce()  # Call the parent method
        print(f"My student ID is {self.student_id}.")

        
class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)  # Call the parent constructor
        self.subject = subject

    def introduce(self):
        super().introduce()  # Call the parent method
        print(f"I teach {self.subject}.")

# Objects
student = Student("Alice", 20, "S12345")
teacher = Teacher("Mr. Smith", 40, "Math")