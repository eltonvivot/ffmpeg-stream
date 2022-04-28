# Simulates Object Detection rApp
from flask import Blueprint, request, jsonify
from context import get, post
from ai_workflow import start_detection, stop_detection
from config import ai_dtime
import threading

ai_app_bp = Blueprint('ai_app', '__name__')
cdata = "ai_data"

@ai_app_bp.route('/ai_data', methods=['GET', 'POST'])
def handle_uav_data():
    if request.method == 'GET': 
        return jsonify(get(cdata))
    if request.method == 'POST': 
        post(cdata, request.get_json())
        return jsonify(get(cdata))

@ai_app_bp.route('/ai_detection/start', methods=['GET'])
def handle_start_detection():
    threading.Thread(target=start_detection).start()
    threading.Thread(target=stop_detection, args=(ai_dtime,)).start()
    return jsonify({'result':'Object Detection Started.'})

@ai_app_bp.route('/ai_detection/stop', methods=['GET'])
def handle_stop_detection():
    stop_detection()
    return jsonify({'result':'Object Detection Stopped.'})