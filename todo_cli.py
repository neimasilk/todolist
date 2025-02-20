from todo_engine import TodoList
from datetime import datetime

def display_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    
    print("\nID | Title | Description | Status | Tags | Created At")
    print("-" * 80)
    for task in tasks:
        tags = ', '.join(task['tags']) if task['tags'] else 'No tags'
        print(f"{task['id']} | {task['title']} | {task['description']} | {task['status']} | {tags} | {task['created_at']}")

def main():
    todo = TodoList()
    
    while True:
        print("\nTodo List Application")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. View Tags")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            task = todo.add_task(title, description)
            print(f"Task added successfully with ID: {task['id']}")
        
        elif choice == '2':
            # Sort tasks: Pending first, then by date (newest first)
            sorted_tasks = sorted(todo.tasks, 
                                key=lambda x: (x['status'] == 'Completed', 
                                            datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S').timestamp() * -1))
            display_tasks(sorted_tasks)
        
        elif choice == '3':
            task_id = int(input("Enter task ID to mark as complete: "))
            try:
                task = todo.update_task(task_id, "Completed")
                print(f"Task {task_id} marked as complete.")
            except Exception as e:
                print(f"Error: {str(e)}")
        
        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            try:
                todo.delete_task(task_id)
                print(f"Task {task_id} deleted successfully.")
            except Exception as e:
                print(f"Error: {str(e)}")
        
        elif choice == '5':
            print("\nSearch Options:")
            query = input("Enter search text (or press Enter to skip): ")
            tags = input("Enter tags to filter (comma-separated, or press Enter to skip): ")
            status = input("Enter status to filter (Pending/Completed, or press Enter to skip): ")
            
            # Process search parameters
            tags = tags.split(',') if tags else None
            status = status if status in ['Pending', 'Completed'] else None
            
            try:
                results = todo.search_tasks(query=query if query else None, 
                                          tags=tags,
                                          status=status)
                print("\nSearch Results:")
                display_tasks(results)
            except Exception as e:
                print(f"Error: {str(e)}")
        
        elif choice == '6':
            try:
                tags = todo.get_all_tags()
                if tags:
                    print("\nAvailable Tags:")
                    print(", ".join(sorted(tags)))
                else:
                    print("No tags found.")
            except Exception as e:
                print(f"Error: {str(e)}")
        
        elif choice == '7':
            print("Thank you for using Todo List Application!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()