from flask import Flask, request, jsonify, redirect, url_for
import configparser
from app.api import api

# 读取配置文件
config = configparser.ConfigParser()
config.read('bin/GyoiThon/config.ini')


@api.route('/config', methods=['GET'])
def get_config():
    config_data = {}
    for section in config.sections():
        for key, value in config.items(section):
            config_data[f"{section}_{key}"] = value
    return jsonify(config_data)


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

            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
