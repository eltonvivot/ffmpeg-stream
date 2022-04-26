from flask import Blueprint, jsonify
import traceback

errors_bp = Blueprint('errors', '__name__')

@errors_bp.app_errorhandler(Exception)
def handle_errors(error):
    print(traceback.format_exc())
    return jsonify({'error': str(error) }), 500