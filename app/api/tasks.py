import os
import subprocess
from flask import Flask, render_template
from app import celery
from app.api import api
from config import work_dir


gyoithon_path = os.path.join(work_dir, 'bin/GyoiThon/gyoithon.py')


@celery.task(bind=True)
def run_gyoithon(self):
    output = []
    process = subprocess.Popen(['python', "bin/GyoiThon/gyoithon.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               bufsize=1, universal_newlines=True)
    for line in process.stdout:
        output.append(line.strip())
        self.update_state(state='PROGRESS', meta={'output': '\n'.join(output)})
    process.wait()
    return {'output': '\n'.join(output), 'code': process.returncode}


@api.route('/run_task/', methods=['GET'])
def run_task():
    print("run tasks!")
    task = run_gyoithon.apply_async()
    return task.id


@api.route('/task_status/<task_id>/', methods=['GET'])
def task_status(task_id):
    task = run_gyoithon.AsyncResult(task_id)
    if task.state == 'PROGRESS':
        return task.info['output']
    elif task.state == 'SUCCESS':
        return 'Task completed with return code: {}\n{}'.format(task.info['code'], task.info['output'])
    else:
        return 'Task failed :('
