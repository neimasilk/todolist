import json
import os
from datetime import datetime

class TodoList:
    def __init__(self):
        self.tasks = []
        self.filename = 'tasks.json'
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.tasks = json.load(file)
            except json.JSONDecodeError:
                self.tasks = []

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, description=""):
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'status': 'Pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{title}' added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found!")
            return

        print("\nYour Todo List:")
        print("-" * 50)
        for task in self.tasks:
            print(f"ID: {task['id']}")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print(f"Created: {task['created_at']}")
            print("-" * 50)

    def update_task(self, task_id, status):
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
                self.save_tasks()
                print(f"Task {task_id} updated successfully!")
                return
        print(f"Task with ID {task_id} not found!")

    def delete_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print(f"Task {task_id} deleted successfully!")
                return
        print(f"Task with ID {task_id} not found!")

def main():
    todo = TodoList()
    
    while True:
        print("\nTodo List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            todo.add_task(title, description)
        
        elif choice == '2':
            todo.view_tasks()
        
        elif choice == '3':
            task_id = int(input("Enter task ID to mark as complete: "))
            todo.update_task(task_id, "Completed")
        
        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            todo.delete_task(task_id)
        
        elif choice == '5':
            print("Thank you for using Todo List Application!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()