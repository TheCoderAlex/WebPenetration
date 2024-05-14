#!/bin/bash

# 设置环境变量
export FLASK_APP=app
export FLASK_ENV=development

# 启动 Celery worker
celery -A app.celery worker --loglevel=info
