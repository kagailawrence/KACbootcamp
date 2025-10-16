"""
Writing Clean, Reusable Code with AI Suggestions check the roadmap.sh for system design and architecture
What Does “Clean Code” Mean?

Clean code is:

Readable: easy to understand.

Reusable: avoids repetition (DRY principle).

Maintainable: easy to modify or extend later.
"""

#Example: Without Clean Code

print("Task 1: Wash dishes")
print("Task 2: Do homework")
print("Task 3: Go shopping")


#Example: With Clean Code (Using Functions)
def add_task(task):
    print(f"Task added: {task}")

add_task("Wash dishes")
add_task("Do homework")
add_task("Go shopping")
add_task("Clean room")


def add_tasks(tasks):
    for task in tasks:
        print(f"Task added: {task}")


tasks = ["Wash dishes", "Do homework", "Go shopping", "Clean room"]
add_tasks(tasks)