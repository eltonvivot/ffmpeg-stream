from flask import Blueprint, jsonify
import traceback, logging

logger = logging.getLogger(__name__)

errors_bp = Blueprint('errors', '__name__')

@errors_bp.app_errorhandler(Exception)
def handle_errors(error):
    logger.debug(traceback.format_exc())
    return jsonify({'error': str(error) }), 500