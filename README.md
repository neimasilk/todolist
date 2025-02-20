# Todo List Application

A modern, feature-rich Todo List application with multiple interfaces and AI-powered task management capabilities.

## Version

Current version: v1.1.0-beta

## Features

### Multiple Interfaces
- Command Line Interface (CLI) for quick task management
- Graphical User Interface (GUI) for desktop users
- Web Interface for browser-based access
- RESTful API for programmatic access

### Core Functionality
- Task Management
  - Create tasks with titles and descriptions
  - View tasks in a customizable list format
  - Mark tasks as complete
  - Delete tasks
  - Automatic task sorting and prioritization

### Advanced Features
- Smart tag system for task categorization
- Advanced search with text and tag filters
- Task metadata tracking (creation date, status)
- Data persistence using JSON storage
- Modular architecture for easy extensibility

## Architecture

The application follows a modular architecture:
- `todo_engine.py`: Core business logic and data management
- `modules/`: Helper modules for tags and search functionality
- Interface implementations:
  - `todo_cli.py`: Command-line interface
  - `todo_gui.py`: Tkinter-based desktop GUI
  - `todo_web.py`: Flask-based web interface

## Prerequisites

- Python 3.x
- Tkinter (included in standard Python installation)
- Flask (for web interface)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/todolist.git

# Navigate to project directory
cd todolist

# Optional: Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
python todo_cli.py
```

Follow the on-screen menu to:
- Add new tasks
- View all tasks
- Mark tasks as complete
- Delete tasks
- Search tasks

### Desktop GUI

```bash
python todo_gui.py
```

Features:
- Intuitive graphical interface
- Task list with sortable columns
- Add tasks through a dialog window
- Mark tasks complete with a single click
- Delete tasks with confirmation

### Web Interface

```bash
python todo_web.py
```

Access the web interface at `http://localhost:5000`
- RESTful API endpoints for task management
- Browser-based task management
- Mobile-friendly interface

## Data Storage

All tasks are stored in `tasks.json` in the project root directory. The file is automatically created when you add your first task.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.