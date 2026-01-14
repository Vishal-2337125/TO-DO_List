import json
import os
import datetime

# Constants
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading tasks: {e}")
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=4)
        print("Tasks saved successfully.")
    except IOError as e:
        print(f"Error saving tasks: {e}")

def add_task(tasks):
    """Add a new task to the list."""
    description = input("Enter ask description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    # Optional: Tags
    tags_input = input("Enter tags (comma separated, optional): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []

    # Optional: Due Date
    due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
    
    task_id = 1
    if tasks:
        task_id = max(t['id'] for t in tasks) + 1

    new_task = {
        'id': task_id,
        'description': description,
        'status': 'pending',
        'created_at': datetime.datetime.now().isoformat(),
        'tags': tags,
        'due_date': due_date
    }
    
    tasks.append(new_task)
    print(f"Task '{description}' added with ID {task_id}.")

def view_tasks(tasks):
    """Display all tasks in a formatted table."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- To-Do List ---")
    print(f"{'ID':<5} {'Status':<10} {'Description':<30} {'Due Date':<15} {'Tags'}")
    print("-" * 80)
    for task in tasks:
        status_icon = "[Done]" if task['status'] == 'done' else "[Pending]"
        tags_display = ", ".join(task.get('tags', []))
        due_date = task.get('due_date', '')
        print(f"{task['id']:<5} {status_icon:<10} {task['description']:<30} {due_date:<15} {tags_display}")
    print("-" * 80)

def mark_done(tasks):
    """Mark a task as done by ID."""
    view_tasks(tasks)
    try:
        task_id = int(input("Enter ID of task to mark done: "))
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = 'done'
                print(f"Task {task_id} marked as done.")
                return
        print("Task not found.")
    except ValueError:
        print("Invalid input. Please enter a valid numeric ID.")

def delete_task(tasks):
    """Delete a task by ID."""
    view_tasks(tasks)
    try:
        task_id = int(input("Enter ID of task to delete: "))
        for i, task in enumerate(tasks):
            if task['id'] == task_id:
                removed = tasks.pop(i)
                print(f"Task '{removed['description']}' deleted.")
                return
        print("Task not found.")
    except ValueError:
        print("Invalid input. Please enter a valid numeric ID.")

def print_menu():
    print("\n=== To-Do List Manager ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task Done")
    print("4. Delete Task")
    print("5. Exit")

def main():
    print("Welcome to your To-Do List Manager!")
    tasks = load_tasks()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_task(tasks)
            save_tasks(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_done(tasks)
            save_tasks(tasks)
        elif choice == '4':
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
