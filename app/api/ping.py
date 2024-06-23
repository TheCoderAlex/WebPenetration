from flask import request, jsonify
import subprocess
import re
from ping3 import ping, verbose_ping
from app.api import api


@api.route('/ping', methods=['GET'])
def ping_ip():
    try:
        with open('bin/GyoiThon/host.txt', 'r') as file:
            data = file.read()
        hosts_list = data.splitlines()
        res = []
        for hosts in hosts_list:
            print(hosts)
            server = hosts.split(' ')[1]
            port = hosts.split(' ')[2]
            ping_output = subprocess.run(['ping', '-c', '3', server], capture_output=True, text=True).stdout

            # 正则判断是否收到全部的包
            transmitted_regex = re.search(r'(\d+) packets transmitted', ping_output)
            received_regex = re.search(r'(\d+) received', ping_output)
            if transmitted_regex and received_regex:
                transmitted_packets = int(transmitted_regex.group(1))
                received_packets = int(received_regex.group(1))
                if transmitted_packets == received_packets:
                    continue
            # 没收到所有的包
            res.append(server)

        if len(res) == 0:
            return jsonify({'status': 'true'})
        else:
            return jsonify({'status': 'false', 'result': res})
    except Exception as e:
        return jsonify({'status': 'false', 'result': 'Fail to read the hosts.'})
