# Simulates Object Detection rApp
from flask import Blueprint, request, jsonify
from context import get, post

ai_data_bp = Blueprint('ai_data', '__name__', url_prefix='/ai_data')
cdata = "uav_data"

@ai_data_bp.route('', methods=['GET, POST'])
def handle_uav_data():
    if request.method == 'GET': 
        return jsonify(get(cdata))
    if request.method == 'POST': 
        post(cdata, request.get_json())
        return jsonify(get(cdata))