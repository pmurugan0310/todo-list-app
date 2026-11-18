from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f)

@app.route('/')
def index():
    todos = load_tasks()
    # Calculate how many tasks are not completed yet
    remaining = sum(1 for task in todos if not task['done'])
    return render_template('index.html', todos=todos, remaining=remaining)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('task')
    if task_text:
        todos = load_tasks()
        # Add as a dictionary this time
        todos.append({"text": task_text, "done": False})
        save_tasks(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    todos = load_tasks()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_tasks(todos)
    return redirect(url_for('index'))

# NEW ROUTE: Toggle task completion
@app.route('/toggle/<int:index>')
def toggle(index):
    todos = load_tasks()
    if 0 <= index < len(todos):
        todos[index]['done'] = not todos[index]['done'] # Flip True/False
        save_tasks(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)