# -*- coding: utf-8 -*-
from flask import *
import subprocess

app = Flask(__name__)
@app.route('/api/v1/ping', methods=['POST'])
def cal():
    result = {}
    receiver = request.get_json()
    for i in receiver:
        for n in range(len(receiver[i])):
            ip_address = receiver[i][n]
            result[ip_address] = ip_address
            r = subprocess.check_output(['ping', '-c1', receiver[i][n]], stdin=None)
            ping_ms = str(r.splitlines()[1].split()[-2].split('=')[-1])
            mes_ping_ms = "%s ms"%(ping_ms)
            result[ip_address] = mes_ping_ms
        return jsonify(result), 200

app.run(host="0.0.0.0")
