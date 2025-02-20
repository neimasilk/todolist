\"""Task Search Engine

This module provides advanced search functionality for tasks in the Todo List application.
It supports searching by text, tags, status, and combinations of these criteria.

Typical usage example:
    results = SearchEngine.search_by_text(tasks, "project")
    tagged_tasks = SearchEngine.search_by_tag(tasks, "important")
    filtered = SearchEngine.advanced_search(tasks, {"text": "meeting", "status": "pending"})
"""

from typing import List, Dict, Any
from .tags import TagManager

class SearchEngine:
    @staticmethod
    def search_by_text(tasks: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Search tasks by title or description.
        
        Args:
            tasks: List of task dictionaries to search through.
            query: Text string to search for in titles and descriptions.
            
        Returns:
            List of tasks that match the search query.
        """
        """Search tasks by title or description."""
        query = query.lower()
        return [
            task for task in tasks
            if query in task['title'].lower() or
               query in task.get('description', '').lower()
        ]
    
    @staticmethod
    def search_by_tag(tasks: List[Dict[str, Any]], tag: str) -> List[Dict[str, Any]]:
        """Search tasks by tag.
        
        Args:
            tasks: List of task dictionaries to search through.
            tag: Tag to search for (with or without # prefix).
            
        Returns:
            List of tasks that contain the specified tag.
        """
        """Search tasks by tag."""
        # Remove # if present at the start of the tag
        tag = tag.lstrip('#')
        return [
            task for task in tasks
            if 'tags' in task and tag in task['tags']
        ]
    
    @staticmethod
    def search_by_status(tasks: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
        """Search tasks by status.
        
        Args:
            tasks: List of task dictionaries to search through.
            status: Status to filter by (case-insensitive).
            
        Returns:
            List of tasks with the specified status.
        """
        """Search tasks by status."""
        status = status.lower()
        return [
            task for task in tasks
            if task['status'].lower() == status
        ]
    
    @staticmethod
    def advanced_search(tasks: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search tasks with multiple filters.
        
        Args:
            tasks: List of task dictionaries to search through.
            filters: Dictionary of filters to apply. Can include:
                    - text: search in title and description
                    - tags: list of tags to match
                    - status: task status
            
        Returns:
            List of tasks that match all specified filters.
        """
        """Search tasks with multiple filters.
        
        filters can include:
        - text: search in title and description
        - tags: list of tags to match
        - status: task status
        """
        result = tasks
        
        if 'text' in filters:
            result = SearchEngine.search_by_text(result, filters['text'])
        
        if 'tags' in filters:
            for tag in filters['tags']:
                result = SearchEngine.search_by_tag(result, tag)
        
        if 'status' in filters:
            result = SearchEngine.search_by_status(result, filters['status'])
        
        return result