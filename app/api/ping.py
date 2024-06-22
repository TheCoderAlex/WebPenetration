from flask import request, jsonify
from ping3 import ping, verbose_ping
from app.api import api


@api.route('/ping', methods=['POST'])
def ping_ip():
    ip = request.args.get('ip')
    if ip is None:
        return jsonify({'status': False, 'result': 'No IP address provided'})
    try:
        delay = ping(ip)
        if delay is None:
            return jsonify({'code': False, 'result': 'Ping failed'})
        else:
            return jsonify({'code': True, 'result': f'Response in {delay} seconds'})
    except Exception as e:
        return jsonify({'code': False, 'result': 'An error occurred', 'error': str(e)})
