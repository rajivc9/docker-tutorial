from flask import Flask, render_template, request, redirect, url_for, jsonify
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)

# Redis connection
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

TASKS_KEY = 'tasks'


def get_tasks():
    """Retrieve all tasks from Redis."""
    tasks_json = redis_client.lrange(TASKS_KEY, 0, -1)
    return [json.loads(task) for task in tasks_json]


def add_task(title):
    """Add a new task to Redis."""
    task = {
        'id': datetime.now().timestamp(),
        'title': title,
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    redis_client.rpush(TASKS_KEY, json.dumps(task))
    return task


def toggle_task(task_id):
    """Toggle task completion status."""
    tasks = get_tasks()
    redis_client.delete(TASKS_KEY)
    
    for task in tasks:
        if str(task['id']) == str(task_id):
            task['completed'] = not task['completed']
        redis_client.rpush(TASKS_KEY, json.dumps(task))


def delete_task(task_id):
    """Delete a task from Redis."""
    tasks = get_tasks()
    redis_client.delete(TASKS_KEY)
    
    for task in tasks:
        if str(task['id']) != str(task_id):
            redis_client.rpush(TASKS_KEY, json.dumps(task))


@app.route('/')
def index():
    """Main page showing all tasks."""
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    """Add a new task."""
    title = request.form.get('title', '').strip()
    if title:
        add_task(title)
    return redirect(url_for('index'))


@app.route('/toggle/<task_id>')
def toggle(task_id):
    """Toggle task completion."""
    toggle_task(task_id)
    return redirect(url_for('index'))


@app.route('/delete/<task_id>')
def delete(task_id):
    """Delete a task."""
    delete_task(task_id)
    return redirect(url_for('index'))


@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        redis_client.ping()
        redis_status = 'connected'
    except Exception:
        redis_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'redis': redis_status,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/tasks')
def api_tasks():
    """API endpoint to get all tasks as JSON."""
    return jsonify(get_tasks())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

