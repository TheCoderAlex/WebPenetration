from app.api import api
from flask import jsonify, request


@api.route('/write_hosts', methods=['POST'])
def write_hosts():
    # {
    #     "hosts_content": [
    #         "http 192.168.220.132 80 /MCIR/splash/index.php",
    #         "http 192.168.220.132 80 /bodgeit/"
    #     ]
    # }
    data = request.json

    if not data or 'hosts_content' not in data:
        return jsonify({'error': 'No valid hosts content provided!'}), 400

    with open('bin/GyoiThon/host.txt', 'w') as f:
        f.truncate(0)
        for line in data['hosts_content']:
            f.write(line + '\n')

    return jsonify({'message': 'Hosts file has been updated successfully!'})
