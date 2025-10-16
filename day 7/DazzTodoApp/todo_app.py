import json
import os

TASKS_FILE = "tasks.json"

def save_tasks(tasks):
    """Save tasks to a JSON file.
    
    Args:
        tasks (list): The list of tasks to save
    """
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

def load_tasks():
    """Load tasks from the JSON file.
    
    Returns:
        list: The loaded tasks, or an empty list if file doesn't exist
    """
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def display_menu():
    """Display the main menu options."""
    print("\n=== Todo List Application ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Exit")

def add_task(tasks):
    """Add a new task to the list and save it.
    
    Args:
        tasks (list): The list of current tasks
    """
    task = input("Enter task description: ")
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")

def view_tasks(tasks):
    """Display all current tasks.
    
    Args:
        tasks (list): The list of current tasks
    """
    if not tasks:
        print("No tasks found!")
        return
    
    print("\nCurrent Tasks:")
    for index, task in enumerate(tasks, 1):
        print(f"{index}. {task}")

def remove_task(tasks):
    """Remove a task from the list and save changes.
    
    Args:
        tasks (list): The list of current tasks
    """
    if not tasks:
        print("No tasks to remove!")
        return
    
    view_tasks(tasks)
    try:
        task_num = int(input("Enter task number to remove: "))
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f"Removed task: {removed_task}")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def main():
    """Main function to run the todo application."""
    tasks = load_tasks()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            print("Thank you for using the Todo App!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()