from flask import Flask
from uav_data_collector import uav_data_bp
from ai_data_collector import ai_data_bp
from errors import errors_bp
from config import show_config

if __name__ == '__main__':
    show_config()
    app = Flask(__name__)
    # endpoints
    app.register_bluelogger.debug(uav_data_bp)
    app.register_bluelogger.debug(ai_data_bp)
    app.register_bluelogger.debug(errors_bp)
    app.run(host='0.0.0.0', port=5001, debug=True)