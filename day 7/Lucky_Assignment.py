def add_task(tasks, task):
    """Add a new task to the list"""
    tasks.append(task)
    print(f"Task '{task}' added successfully!")

def view_tasks(tasks):
    """Display all tasks with their indices"""
    if not tasks:
        print("No tasks available.")
        return
    print("\nCurrent Tasks:")
    for index, task in enumerate(tasks, 1):
        print(f"{index}. {task}")

def remove_task(tasks, index):
    """Remove a task by its index"""
    try:
        task = tasks.pop(index - 1)
        print(f"Task '{task}' removed successfully!")
    except IndexError:
        print("Invalid task number!")

def main():
    tasks = []
    while True:
        print("\n=== Task Manager ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Remove Task")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            task = input("Enter task description: ")
            add_task(tasks, task)
        
        elif choice == '2':
            view_tasks(tasks)
        
        elif choice == '3':
            view_tasks(tasks)
            if tasks:
                index = int(input("Enter task number to remove: "))
                remove_task(tasks, index)
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()