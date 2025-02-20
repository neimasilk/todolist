from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from todo_engine import TodoList
from modules.error_handler import TodoError, ErrorHandler
from datetime import datetime

app = Flask(__name__)
CORS(app)

todo = TodoList()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        # Sort tasks: Pending first, then by date (newest first)
        sorted_tasks = sorted(todo.tasks, 
                             key=lambda x: (x['status'] == 'Completed', 
                                         datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S').timestamp() * -1))
        return jsonify(sorted_tasks)
    except TodoError as e:
        return jsonify(ErrorHandler.format_error_response(e)), 400

@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        title = data.get('title')
        description = data.get('description', '')
        task = todo.add_task(title, description)
        return jsonify(task), 201
    except TodoError as e:
        return jsonify(ErrorHandler.format_error_response(e)), 400

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = todo.update_task(task_id, 'Completed')
        return jsonify(task)
    except TodoError as e:
        return jsonify(ErrorHandler.format_error_response(e)), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = todo.delete_task(task_id)
        return jsonify(task)
    except TodoError as e:
        return jsonify(ErrorHandler.format_error_response(e)), 404

@app.route('/tasks/search', methods=['GET'])
def search_tasks():
    try:
        query = request.args.get('q')
        tags = request.args.get('tags')
        status = request.args.get('status')
        
        # Convert tags string to list if present
        if tags:
            tags = tags.split(',')
        
        results = todo.search_tasks(query=query, tags=tags, status=status)
        return jsonify(results)
    except TodoError as e:
        return jsonify(ErrorHandler.format_error_response(e)), 400

@app.route('/tags', methods=['GET'])
def get_tags():
    try:
        tags = list(todo.get_all_tags())  # Convert set to list before jsonifying
        return jsonify(tags)
    except TodoError as e:
        return jsonify(ErrorHandler.format_error_response(e)), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)