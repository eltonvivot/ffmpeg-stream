# Simulates Data management and exposure
from flask import Blueprint, request, jsonify
from context import get, post
from ai_workflow import start_detection, stop_detection
from config import ai_dtime
import logging, threading

logger = logging.getLogger(__name__)

uav_data_bp = Blueprint('uav', '__name__')
cdata = "uav_data"

@uav_data_bp.route('/uav_data', methods=['GET', 'POST'])
def handle_uav_data():
    logger.debug(f"{request.path} | {request.method}")
    try:
        if request.method == 'GET': 
            return jsonify(get(cdata)), 200
        if request.method == 'POST': 
            post(cdata, request.get_json())
            data = get(cdata)
            if data['cam_status'] == 'on': 
                threading.Thread(target=start_detection).start()
                threading.Thread(target=stop_detection, args=(ai_dtime,)).start()
            if data['cam_status'] == 'off': stop_detection()
            return jsonify(get(cdata)), 200
    except Exception as err:
        logger.error(f"{err.__class__.__name__}: {err}")
        raise
