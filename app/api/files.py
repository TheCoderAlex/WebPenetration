from flask import Flask, jsonify, send_from_directory, request, send_file
import os
import time
import pandas as pd
from app.api import api

report_dir = "bin/GyoiThon/report"
logs_dir = "bin/GyoiThon/logs"
exclude_files = ['report_template.html', '~$sample_report.xlsx', '.gitignore']


def format_size(size):
    # 将字节大小转换为合适的单位
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def get_file_info(directory, filename):
    file_path = os.path.join(directory, filename)
    file_stats = os.stat(file_path)
    file_info = {
        'filename': filename,
        'size': format_size(file_stats.st_size),
        'modification_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stats.st_mtime)),
        'creation_date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stats.st_ctime)),
        'download_url': request.url_root + 'api/download/' + filename
    }
    return file_info


def get_files(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, directory)
            if filename not in exclude_files and not filename.endswith('.html'):
                file_info = get_file_info(directory, relative_path)
                files_list.append(file_info)
    return files_list


@api.route("/reports", methods=['GET'])
def list_reports():
    try:
        files_list = get_files(report_dir)
        return jsonify(files_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route("/logs", methods=['GET'])
def list_logs():
    try:
        file_list = get_files(logs_dir)
        return jsonify(file_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route("/download/<path:filename>", methods=['GET'])
def download_file(filename):
    try:
        if os.path.exists(os.path.join(report_dir, filename)):
            path = os.path.join(report_dir, filename)
            # Fuuuck
            path = '../' + path
            return send_file(path, as_attachment=True)
        elif os.path.exists(os.path.join(logs_dir, filename)):
            path = os.path.join(logs_dir, filename)
            path = '../' + path
            return send_file(path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@api.route("/get_result/<path:filename>", methods=['GET'])
def get_result(filename):
    try:
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bin/GyoiThon/report'))
        csv_file_path = os.path.join(parent_directory, filename)
        print(csv_file_path)
        if os.path.exists(csv_file_path):

            df = pd.read_csv(csv_file_path)
            data = df.to_dict(orient='records')

            return jsonify(data)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route("/view_exploit_report/<path:filename>", methods=['GET'])
def view_exploit_report(filename):
    try:
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../bin/GyoiThon/report'))
        html_file_path = os.path.join(parent_directory, filename)
        if os.path.exists(html_file_path):
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            return jsonify({'html': html_content})
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
