# Simulates Data management and exposure
from flask import Blueprint, request, jsonify
from context import get, post
from ai_workflow import start_detection, disconnect

uav_data_bp = Blueprint('uav', '__name__')
cdata = "uav_data"

@uav_data_bp.route('/uav_data', methods=['GET', 'POST'])
def handle_uav_data():
    print(f"{request.path} | {request.method}")
    if request.method == 'GET': 
        return jsonify(get(cdata))
    if request.method == 'POST': 
        post(cdata, request.get_json())
        data = get(cdata)
        if data['cam_status'] == 'on': start_detection()
        if data['cam_status'] == 'off': disconnect()
        return jsonify(get(cdata))
