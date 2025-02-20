# Todo List Application API Documentation

## Architecture Overview

The Todo List application follows a modular architecture with clear separation of concerns:

### Core Components

#### 1. TodoEngine (`todo_engine.py`)
- Core business logic and data management
- Handles CRUD operations for tasks
- Manages data persistence using JSON storage
- Integrates with TagManager and SearchEngine

#### 2. AIEngine (`ai_engine.py`)
- Provides AI-powered task analysis and insights
- Integrates with Deepseek API for task analysis
- Features include priority determination, categorization, and time estimation

### Helper Modules (`modules/`)

#### 1. TagManager (`tags.py`)
- Handles task tagging functionality
- Extracts hashtags from text
- Manages tag operations (add, remove, list)

#### 2. SearchEngine (`search.py`)
- Provides advanced search capabilities
- Supports text, tag, and status-based filtering
- Implements multi-criteria search

#### 3. ErrorHandler (`error_handler.py`)
- Centralized error handling system
- Custom exception classes for different error types
- Standardized error response formatting

### User Interfaces

#### 1. CLI Interface (`todo_cli.py`)
- Command-line interface for basic operations
- Interactive menu-driven interface
- Suitable for quick task management

#### 2. GUI Interface (`todo_gui.py`)
- Tkinter-based desktop application
- Features a modern, intuitive interface
- Supports drag-and-drop and keyboard shortcuts

#### 3. Web Interface (`todo_web.py`)
- Flask-based web application
- RESTful API endpoints
- Supports CORS for cross-origin requests

## Data Flow

1. User input → Interface Layer (CLI/GUI/Web)
2. Interface Layer → TodoEngine
3. TodoEngine ↔ Helper Modules (TagManager, SearchEngine)
4. TodoEngine ↔ Storage (tasks.json)
5. AIEngine → Task Analysis and Insights

## Data Storage

Tasks are stored in `tasks.json` with the following structure:

```json
{
    "id": 1,
    "title": "Example Task",
    "description": "Task description with #tags",
    "status": "Pending",
    "created_at": "2024-01-01 12:00:00",
    "tags": ["example", "task"]
}
```

## Error Handling

The application uses a hierarchical error system:

1. `TodoError`: Base exception class
2. `TaskNotFoundError`: For missing tasks
3. `ValidationError`: For invalid input data
4. `StorageError`: For storage operation failures

## AI Integration

The AIEngine provides:

1. Task Analysis
   - Priority determination
   - Category suggestion
   - Time estimation
   - Task-specific suggestions

2. Task List Analysis
   - Productivity scoring
   - Completion rate tracking
   - Improvement suggestions

## Best Practices

1. Error Handling
   - Always use appropriate error classes
   - Provide detailed error messages
   - Handle errors at the appropriate level

2. Data Validation
   - Validate input before processing
   - Check for required fields
   - Enforce length limits

3. Code Organization
   - Follow modular architecture
   - Keep interfaces separate
   - Use helper modules for specific functionality

4. Documentation
   - Maintain clear docstrings
   - Document API endpoints
   - Keep README updated

## Future Enhancements

1. Database Integration
   - Replace JSON storage with SQL database
   - Add data migration tools

2. Enhanced AI Features
   - Natural language task parsing
   - Automated task prioritization
   - Smart task scheduling

3. Additional Interfaces
   - Mobile application
   - API authentication
   - Real-time updates