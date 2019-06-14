# -*- coding: utf-8 -*-
from flask import *
import psutil as ps

app = Flask(__name__)
@app.route('/api/v1/vms', methods=['GET'])
def vms():
    return usage()

@app.route('/api/v1/vms/usages', methods=['GET'])
def usage():
    dict_usage ={}
    dict_usage['CPU_usage'] = get_cpu()
    dict_usage['DISK_usage'] = get_disk()
    dict_usage['MEM_usage'] = get_mem()
    return jsonify(dict_usage), 200

@app.route('/api/v1/vms/usages/cpu', methods=['GET'])
def get_cpu():
    return str(ps.cpu_percent())


@app.route('/api/v1/vms/usages/disk', methods=['GET'])
def get_disk():
    return str(ps.disk_usage('/').percent)


@app.route('/api/v1/vms/usages/mem', methods=['GET'])
def get_mem():
    return str(((ps.virtual_memory().used*1.0))/(1024**3))

app.run(host="0.0.0.0")