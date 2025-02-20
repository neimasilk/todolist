from datetime import datetime

# Sample tasks for testing sorting
sample_tasks = [
    {
        "id": 1,
        "title": "Task 1",
        "description": "Pending task from yesterday",
        "status": "Pending",
        "created_at": "2024-02-19 10:00:00",
        "tags": ["test"]
    },
    {
        "id": 2,
        "title": "Task 2",
        "description": "Completed task from today",
        "status": "Completed",
        "created_at": "2024-02-20 15:00:00",
        "tags": ["test"]
    },
    {
        "id": 3,
        "title": "Task 3",
        "description": "Pending task from today",
        "status": "Pending",
        "created_at": "2024-02-20 09:00:00",
        "tags": ["test"]
    },
    {
        "id": 4,
        "title": "Task 4",
        "description": "Completed task from yesterday",
        "status": "Completed",
        "created_at": "2024-02-19 16:00:00",
        "tags": ["test"]
    }
]

def sort_by_status_and_date(tasks):
    """Sort tasks by status (Pending first) and then by creation date (newest first)"""
    return sorted(
        sorted(tasks, key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S'), reverse=True),
        key=lambda x: x['status'] == 'Completed'
    )

def print_tasks(tasks, title):
    """Print tasks in a formatted way"""
    print(f"\n{title}:")
    print("-" * 80)
    for task in tasks:
        print(f"ID: {task['id']} | Status: {task['status']} | Created: {task['created_at']} | Title: {task['title']}")
    print("-" * 80)

# Test different sorting approaches
print_tasks(sample_tasks, "Original Task List")

# Sort by status and date
sorted_tasks = sort_by_status_and_date(sample_tasks)
print_tasks(sorted_tasks, "Sorted by Status (Pending First) and Date (Newest First)")

# Sort by date only
date_sorted = sorted(sample_tasks, key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S'), reverse=True)
print_tasks(date_sorted, "Sorted by Date Only (Newest First)")

# Sort by status only
status_sorted = sorted(sample_tasks, key=lambda x: x['status'] == 'Completed')
print_tasks(status_sorted, "Sorted by Status Only (Pending First)")