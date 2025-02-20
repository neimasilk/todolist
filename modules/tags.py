"""Task Tagging System

This module provides functionality for managing tags in the Todo List application.
It handles tag extraction, addition, removal, and retrieval operations.

Typical usage example:
    tags = TagManager.extract_tags("Task with #project #priority")
    task = TagManager.add_tags_to_task(task, "Add #important feature")
"""

from typing import List, Set, Dict, Any
import re

class TagManager:
    @staticmethod
    def extract_tags(text: str) -> Set[str]:
        """Extract hashtags from text.
        
        Args:
            text: The text to extract tags from.
            
        Returns:
            Set of unique tags found in the text.
        """
        """Extract hashtags from text."""
        # Find all words starting with # and containing word characters
        tags = re.findall(r'#(\w+)', text)
        return set(tags)
    
    @staticmethod
    def add_tags_to_task(task: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Extract tags from text and add them to the task.
        
        Args:
            task: The task dictionary to add tags to.
            text: The text to extract tags from.
            
        Returns:
            Updated task dictionary with new tags added.
        """
        """Extract tags from text and add them to the task."""
        tags = TagManager.extract_tags(text)
        if 'tags' not in task:
            task['tags'] = list(tags)
        else:
            task['tags'].extend(list(tags))
            task['tags'] = list(set(task['tags']))  # Remove duplicates
        return task
    
    @staticmethod
    def remove_tags_from_task(task: Dict[str, Any], tags_to_remove: List[str]) -> Dict[str, Any]:
        """Remove specified tags from a task.
        
        Args:
            task: The task dictionary to remove tags from.
            tags_to_remove: List of tags to remove.
            
        Returns:
            Updated task dictionary with specified tags removed.
        """
        """Remove specified tags from a task."""
        if 'tags' in task:
            task['tags'] = [tag for tag in task['tags'] if tag not in tags_to_remove]
        return task
    
    @staticmethod
    def get_all_tags(tasks: List[Dict[str, Any]]) -> Set[str]:
        """Get all unique tags from all tasks.
        
        Args:
            tasks: List of task dictionaries to extract tags from.
            
        Returns:
            Set of all unique tags found across all tasks.
        """
        """Get all unique tags from all tasks."""
        all_tags = set()
        for task in tasks:
            if 'tags' in task:
                all_tags.update(task['tags'])
        return all_tags