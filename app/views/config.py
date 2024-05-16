from flask import Flask, render_template, request
from app.views import views
from app.api.config import config as config_ini


@views.route('/config', methods=['GET'])
def config():
    success = request.args.get('success')
    error = request.args.get('error')
    if success == 'True':
        success = True

    if request.referrer and request.referrer != request.url:
        redirected = True
    else:
        redirected = False

    if not redirected:
        success = error = None

    return render_template('config.html', config=config_ini, success=success, error=error)
