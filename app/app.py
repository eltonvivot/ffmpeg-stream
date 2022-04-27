from flask import Flask
from uav_data_collector import uav_data_bp
from ai_data_collector import ai_data_bp
from errors import errors_bp
from config import show_config
import logging

# init logs
f='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s | %(message)s'
log_level=logging.DEBUG
logging.basicConfig()
logging.basicConfig(level=log_level, format=f)

if __name__ == '__main__':
    show_config()
    app = Flask(__name__)
    # endpoints
    app.register_blueprint(uav_data_bp)
    app.register_blueprint(ai_data_bp)
    app.register_blueprint(errors_bp)
    app.run(host='0.0.0.0', port=5001)