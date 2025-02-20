"""Todo List Application Core Engine

This module provides the core functionality for the Todo List application.
It handles all task-related operations including CRUD operations, data persistence,
and integration with helper modules for tagging and searching.

Typical usage example:
    todo = TodoList()
    task = todo.add_task("Complete project", "Finish documentation and testing")
    todo.update_task(task['id'], "Completed")
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
from modules import TagManager, SearchEngine
from modules.error_handler import TaskNotFoundError, ValidationError, StorageError, ErrorHandler

class TodoList:
    """Initialize TodoList with empty task list and load existing tasks."""
    def __init__(self):
        self.tasks = []
        self.filename = 'tasks.json'
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load tasks from JSON file.
        
        Raises:
            StorageError: If there are issues reading the tasks file.
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.tasks = json.load(file)
            except json.JSONDecodeError as e:
                raise StorageError('read', {'error': str(e)})
            except IOError as e:
                raise StorageError('read', {'error': str(e)})

    def save_tasks(self) -> None:
        """Save tasks to JSON file.
        
        Raises:
            StorageError: If there are issues writing to the tasks file.
        """
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.tasks, file, indent=4)
        except IOError as e:
            raise StorageError('write', {'error': str(e)})

    def add_task(self, title: str, description: str = "") -> Dict[str, Any]:
        """Add a new task to the list.
        
        Args:
            title: The title of the task.
            description: Optional detailed description of the task.
            
        Returns:
            Dict containing the created task data.
            
        Raises:
            ValidationError: If title is empty or too long.
            StorageError: If task cannot be saved.
        """
        # Validate input data
        ErrorHandler.handle_validation(title, description)

        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'status': 'Pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tags': []
        }
        # Extract tags from title and description
        task = TagManager.add_tags_to_task(task, title)
        if description:
            task = TagManager.add_tags_to_task(task, description)
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_task_by_id(self, task_id: int) -> Dict[str, Any]:
        """Retrieve a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve.
            
        Returns:
            Dict containing the task data.
            
        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        raise TaskNotFoundError(task_id)

    def update_task(self, task_id: int, status: str) -> Dict[str, Any]:
        """Update the status of a task.
        
        Args:
            task_id: The ID of the task to update.
            status: The new status for the task.
            
        Returns:
            Dict containing the updated task data.
            
        Raises:
            TaskNotFoundError: If no task exists with the given ID.
            StorageError: If task cannot be saved.
        """
        task = self.get_task_by_id(task_id)
        task['status'] = status
        self.save_tasks()
        return task

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task from the list.
        
        Args:
            task_id: The ID of the task to delete.
            
        Returns:
            Dict containing the deleted task data.
            
        Raises:
            TaskNotFoundError: If no task exists with the given ID.
            StorageError: If task cannot be saved.
        """
        task = self.get_task_by_id(task_id)
        self.tasks.remove(task)
        self.save_tasks()
        return task
    
    def search_tasks(self, query=None, tags=None, status=None):
        """Search tasks using various filters."""
        filters = {}
        if query:
            filters['text'] = query
        if tags:
            filters['tags'] = tags if isinstance(tags, list) else [tags]
        if status:
            filters['status'] = status
        
        return SearchEngine.advanced_search(self.tasks, filters)
    
    def get_all_tags(self):
        """Get all unique tags from all tasks."""
        return TagManager.get_all_tags(self.tasks)