import subprocess
from flask import jsonify, request
from app import celery
from app.api import api
from app.utils.html_color import convert_ansi_to_html

task_ids = []
succeeded_task_ids = []
failed_task_ids = []
terminated_task_ids = []
non_progress_count = {}

progress_id = {}

STOP_THRESHOLD = 10

# 输出缓存的最大行数
MAX_OUTPUT_LINES = 10


@celery.task(bind=True)
def run_gyoithon(self, parameters, ID):
    output = []
    command = ['python', "-u", "bin/GyoiThon/gyoithon.py", "-r", ID]
    for key, value in parameters.items():
        if value == True:
            if key == 'no_update_vulndb':
                command.append('--no-update-vulndb')
            else:
                command.append('-' + key)
    # print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               bufsize=1,
                               universal_newlines=True)
    for line in process.stdout:
        output.append(convert_ansi_to_html(line))
        if len(output) > MAX_OUTPUT_LINES:
            del output[:-MAX_OUTPUT_LINES]
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


@api.route('/success_task_ids', methods=['GET'])
def success_task():
    return jsonify({'task_ids': succeeded_task_ids})


@api.route('/failed_task_ids', methods=['GET'])
def failed_task():
    return jsonify({'task_ids': failed_task_ids})


@api.route('/terminated_task_ids', methods=['GET'])
def terminated_task():
    return jsonify({'task_ids': terminated_task_ids})


@api.route('/terminate_task', methods=['POST'])
def terminate_task():
    data = request.json
    task_id = data.get('task_id')
    if task_id in task_ids:
        celery.control.revoke(task_id, terminate=True)
        task_ids.remove(task_id)
        terminated_task_ids.append(task_id)
        return jsonify({'task_id': task_id, 'status': 'Task terminated'})
    else:
        return jsonify({'task_id': task_id, 'status': 'Task ID not found'})


@api.route('/start_task', methods=['POST'])
def run_task():
    parameters = request.json
    task_id = request.json.get('task_id')
    progress_id[task_id] = 0
    task = run_gyoithon.apply_async(kwargs={'parameters': parameters, 'ID': task_id}, task_id=task_id)
    task_ids.append(task.id)
    return jsonify({'task_id': task.id})

@api.route('/get_progress/<task_id>/', methods=['GET'])
def get_progress(task_id):
    return jsonify({'progress': progress_id[task_id]})

@api.route('/task_status/<task_id>/', methods=['GET'])
def task_status(task_id):
    task = run_gyoithon.AsyncResult(task_id)

    text = task.info['output'][0]
    if 'scrapy' in text or 'Scrapy' in text or ('check' in text and 'using' in text):
        progress_id[task_id] = 1
    elif 'exploit' in text:
        progress_id[task_id] = 2

    if task.state == 'PROGRESS':
        if task_id in non_progress_count:
            non_progress_count[task_id] = 0
        return task.info['output']
    elif task.state == 'SUCCESS':
        progress_id[task_id] = 3
        if task_id in non_progress_count:
            del non_progress_count[task_id]
        celery.control.revoke(task_id, terminate=True)
        if task_id in task_ids:
            task_ids.remove(task_id)
            succeeded_task_ids.append(task_id)
        return 'Task completed with return code: {}\n{}'.format(task.info['code'], task.info['output'])
    else:
        if task_id in task_ids:
            if task_id in non_progress_count:
                non_progress_count[task_id] += 1
                if non_progress_count[task_id] >= STOP_THRESHOLD:
                    celery.control.revoke(task_id, terminate=True)
                    task_ids.remove(task_id)
                    failed_task_ids.append(task_id)
                    return 'Task terminated due to inactivity.'
            else:
                non_progress_count[task_id] = 1
        else:
            return 'Task is not running or does not exist.'
