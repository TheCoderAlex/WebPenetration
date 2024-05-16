from app.api import api
from flask import Flask, request, redirect, url_for
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('bin/GyoiThon/config.ini')


@api.route('/update', methods=['POST'])
def update_config():
    if request.method == 'POST':
        try:
            for section in config.sections():
                for key in request.form:
                    if key.startswith(section):
                        escaped_value = request.form[key].replace('%', '%%')
                        config.set(section, key.split('_', 1)[1], escaped_value)

            with open('bin/GyoiThon/config.ini', 'w') as configfile:
                config.write(configfile)

            return redirect(url_for('views.config', success=True))
        except Exception as e:
            return redirect(url_for('views.config', success=False, error=str(e)))
