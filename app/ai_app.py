# Simulates Object Detection rApp
from flask import Blueprint, request, jsonify, g
from context import get, post
from ai_workflow import start_detection, stop_detection, plot_figures
import threading, time

ai_app_bp = Blueprint('ai_app', '__name__')
cdata = "ai_data"

@ai_app_bp.route('/ai_data', methods=['GET', 'POST'])
def handle_uav_data():
    if request.method == 'GET': 
        return jsonify(get(cdata))
    if request.method == 'POST': 
        post(cdata, request.get_json())
        return jsonify(get(cdata))

@ai_app_bp.route('/ai_detection/start', methods=['POST'])
def handle_start_detection():
    g.results = {}
    g.inc_time = {}
    g.dec_time = {}
    g.detection_name = 'first'
    start_detection(request.get_json(), True, False)
    first_name = g.detection_name
    g.detection_name = 'second'
    time.sleep(20)
    start_detection(request.get_json(), False, True)
    # new plot
    plot_figures(True, False, first_name, g.detection_name)
    return jsonify({'result': "Ok."})

@ai_app_bp.route('/ai_detection/stop', methods=['GET'])
def handle_stop_detection():
    stop_detection()
    return jsonify({'result':'Object Detection Stopped.'})