from turtle import delay
from flask import Blueprint, jsonify
from config import uav_cname, ffmpeg_cmd, uav_cfile
import logging, os, time

logger = logging.getLogger(__name__)

cam_controller_bp = Blueprint('uav_cam', '__name__', url_prefix='/uav_cam')

@cam_controller_bp.route('/start', methods=['GET'])
def handle_start_cam():
    return jsonify({'result': start_cam()})

@cam_controller_bp.route('/stop', methods=['GET'])
def handle_stop_cam():
    return jsonify({'result': stop_cam()})

@cam_controller_bp.route('/status', methods=['GET'])
def handle_status_cam():
    status = 'stopped'
    if is_cam_on(): status = 'running'
    return jsonify({'result':f'Object Detection is {status}.'})

def is_cam_on():
    ps = exec_cmd(f"docker ps | grep '{uav_cname}'")
    return uav_cname in ps

def start_cam(ffmpeg_cmd=ffmpeg_cmd):
    if is_cam_on(): return 'UAV CAM is already ON.'
    # exec_cmd(f"export FFMPEG_CMD={ffmpeg_cmd}")
    logger.info(f"Running UAV CAM with FFMPEG_CMD:\n\t{os.system('echo $FFMPEG_CMD')}")
    res = exec_cmd(f"docker-compose -f {uav_cfile} up --build {uav_cname}")
    time.sleep(3)
    if is_cam_on(): return 'UAV CAM started.'
    else: raise Exception(f"Failed to start UAV CAM.\nOutput: {res}")

def stop_cam():
    if not is_cam_on(): return 'UAV CAM is already OFF.'
    res = exec_cmd(f"docker stop {uav_cname}")
    time.sleep(3)
    if not is_cam_on(): return 'UAV CAM stopped.'
    else: raise Exception(f"Failed to stop UAV CAM.\nOutput: {res}")

def exec_cmd(cmd):
    logger.debug(f"cmd: {cmd}")
    res = os.system(cmd)
    logger.debug(res)
    return res