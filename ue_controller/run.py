from flask import Flask, jsonify
from dotenv import load_dotenv
from tc_controller import tc_controller_bp
from cam_controller import cam_controller_bp
import logging, traceback

if __name__ == '__main__':
    # init logs
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s | %(message)s')
    logger = logging.getLogger(__name__)

    # load env file
    load_dotenv(dotenv_path='./config.env')
    
    app = Flask(__name__)
    # endpoints
    app.register_blueprint(tc_controller_bp)
    app.register_blueprint(cam_controller_bp)

    @app.errorhandler(Exception)
    def handle_errors(error):
        logger.debug(traceback.format_exc())
        return jsonify({'error': str(error) }), 500

    app.run(host='0.0.0.0', port=5002)