"""
Definition

OOP (Object-Oriented Programming) is a programming paradigm that organizes code into objects
real-world entities that contain both data (attributes) and behavior (methods).
Instead of writing one long script, OOP helps you structure your code to be:
    -Reusable
    -Modular
    -Scalable
    -Easier to maintain


example:
Think of a class as a blueprint, and objects as the buildings made from that blueprint.

Example:
Class: Car blueprint (defines color, brand, speed)
Object: A specific car (red Toyota moving at 120 km/h)



| Concept         | Description                                     | Example                   |
| --------------- | ----------------------------------------------- | ------------------------- |
| **Class**       | Blueprint for creating objects                  | `class Car:`              |
| **Object**      | Instance of a class                             | `my_car = Car()`          |
| **Attribute**   | Variable inside a class                         | `self.color`              |
| **Method**      | Function inside a class                         | `def start_engine(self):` |
| **Inheritance** | Reuse attributes and methods from another class | `class ElectricCar(Car):` |

"""

# Define a class
class Car:
    # Constructor (initializes attributes)
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color
    
    # Method
    def start_engine(self):
        print(f"The {self.color} {self.brand}'s engine has started.")

    def stop_engine(self):
        print(f"The {self.color} {self.brand}'s engine has stopped.")



# Create objects
car1 = Car("Toyota", "Red")
car2 = Car("BMW", "Blue")

# Use methods
car1.start_engine()
car2.start_engine()
car3 = Car("Honda", "Green")
car3.start_engine()
car1.stop_engine()
car2.stop_engine()
car3.stop_engine()

list_of_cars = [car1, car2, car3]


"""
Understanding __init__ / Constructor

A constructor is a special method that automatically runs when you create a new object.
It sets up the initial values (attributes) of the object.
"""

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def get_balance(self):
        return self.balance
    
    def get_owner(self):
        return self.owner
    
    def set_owner(self, new_owner):
        self.owner = new_owner
        print(f"Owner updated to {self.owner}")

    def set_balance(self, new_balance):
        self.balance = new_balance
        print(f"Balance updated to {self.balance}")

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. Remaining balance: {self.balance}")

# Create an object
Alice_account = BankAccount("Alice", 1000)
Alice_account.deposit(500)
Alice_account.withdraw(200)
Alice_account.withdraw(2000)  # Should show insufficient funds
