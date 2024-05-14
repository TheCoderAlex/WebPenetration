from flask import request, jsonify
from ping3 import ping, verbose_ping
from app.api import api


@api.route('/ping/', methods=['GET'])
def ping_ip():
    ip = request.args.get('ip')
    if ip is None:
        return jsonify({'code': '2', 'result': 'No IP address provided'}), 400
    try:
        delay = ping(ip)
        if delay is None:
            return jsonify({'code': '1', 'result': 'Ping failed'}), 400
        else:
            return jsonify({'code': '0', 'result': f'Response in {delay} seconds'}), 200
    except Exception as e:
        return jsonify({'code': '1', 'result': 'An error occurred', 'error': str(e)}), 400
