import subprocess
from flask import jsonify, request
from app import celery
from app.api import api
from app.utils.html_color import convert_ansi_to_html

task_ids = []
non_progress_count = {}
STOP_THRESHOLD = 10


@celery.task(bind=True)
def run_gyoithon(self):
    output = []
    process = subprocess.Popen(['python', "-u", "bin/GyoiThon/gyoithon.py"], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               bufsize=1,
                               universal_newlines=True)
    for line in process.stdout:
        output.append(convert_ansi_to_html(line))
        self.update_state(state='PROGRESS', meta={'output': output})
    process.wait()
    return {'output': output, 'code': process.returncode}


@api.route('/total_tasks', methods=['GET'])
def total_tasks():
    total = len(task_ids)
    return jsonify({'total_tasks': total})


@api.route('/all_task_ids', methods=['GET'])
def all_task_ids():
    return jsonify({'task_ids': task_ids})


@api.route('/terminate_task', methods=['POST'])
def terminate_task():
    data = request.json
    task_id = data.get('task_id')
    if task_id in task_ids:
        celery.control.revoke(task_id, terminate=True)
        task_ids.remove(task_id)
        return jsonify({'task_id': task_id, 'status': 'Task terminated'})
    else:
        return jsonify({'task_id': task_id, 'status': 'Task ID not found'})


@api.route('/start_task/', methods=['POST'])
def run_task():
    task = run_gyoithon.apply_async()
    task_ids.append(task.id)
    return task.id


@api.route('/task_status/<task_id>/', methods=['GET'])
def task_status(task_id):
    task = run_gyoithon.AsyncResult(task_id)
    if task.state == 'PROGRESS':
        return task.info['output']
    elif task.state == 'SUCCESS':
        return 'Task completed with return code: {}\n{}'.format(task.info['code'], task.info['output'])
    else:
        return 'Task is not running or does not exist.'

# TODO: Add a check for the number of tasks not running, and if it exceeds a threshold, stop the task.
