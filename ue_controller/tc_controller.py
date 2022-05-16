from flask import Blueprint, request, jsonify
from tc_rules import get, post, delete
from config import if_name
import logging, os

logger = logging.getLogger(__name__)

tc_controller_bp = Blueprint('ai_app', '__name__')

@tc_controller_bp.route('/tc_rules', methods=['GET', 'POST', 'DELETE'])
def handle_uav_data():
    if request.method == 'GET': 
        return jsonify(get())
    if request.method == 'POST': 
        create_rules(request.get_json())
        post(request.get_json())
        return jsonify(get())
    if request.method == 'DELETE': 
        delete_rules()
        delete()
        return jsonify({'result': 'Rules deleted.'})

def create_rules(rules):
    if not rules['apply']: return
    tc_cmd = f"tcset {if_name}"
    tc_cmd_ai = f"tcset {if_name}"
    if 'delay' in rules:
        tc_cmd += f" --delay {rules['delay']} "
    if 'rate' in rules:
        tc_cmd += f" --rate {rules['rate']}"
        tc_cmd_ai += f" --rate {rules['rate']}"
    if 'loss' in rules:
        tc_cmd += f" --loss {rules['loss']}"
    tc_cmd += " --overwrite"
    tc_cmd_ai += " --direction incoming --overwrite"

    # delete_rules()
    # exec_and_log(f"{tc_cmd} --direction incoming")
    # exec_and_log(f"{tc_cmd} --direction outgoing")
    exec_and_log(f"{tc_cmd}")
    exec_and_log(f"sshpass -p 'ffmpeg' ssh root@10.10.21.11 {tc_cmd_ai}")


def delete_rules():
    tc_cmd = f"tcdel {if_name} --all"
    exec_and_log(tc_cmd)

def exec_and_log(cmd):
    logger.info(f"Executing command: \t'{cmd}'")
    logger.debug(os.system(cmd))