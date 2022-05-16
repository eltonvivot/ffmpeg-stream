# Simulates Object Detection rApp
from asyncio.log import logger
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
    logger.info("Received Start Detection")
    g.results = {}
    g.inc_time = {}
    g.dec_time = {}
    first_name = 'first'
    second_name = 'second'
    logger.info(f"Starting Detection '{first_name}' ...")
    start_detection(first_name, True, False, False)
    logger.debug(f"Waiting 40s ...")
    time.sleep(40)
    logger.info(f"Starting Detection '{second_name}' ...")
    start_detection(second_name, False, True, False)
    # new plot
    logger.info(f"Plotting Figures ...")
    plot_figures(True, False, first_name, second_name)
    return jsonify({'result': "Ok."})

@ai_app_bp.route('/ai_detection/stop', methods=['GET'])
def handle_stop_detection():
    stop_detection()
    return jsonify({'result':'Object Detection Stopped.'})

@ai_app_bp.route('/ai_detection/plot', methods=['GET'])
def handle_plot():
    g.results = {}
    g.inc_time = {}
    g.dec_time = {}
    first_name = 'first'
    second_name = 'second'
    plot_figures(True, False, first_name, second_name, from_files=True)
    return jsonify({'result': "Ok."})