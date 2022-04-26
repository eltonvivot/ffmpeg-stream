from flask import Flask, request
from uav_data_collector import uav_data_bp
from ai_data_collector import ai_data_bp
from config import show_config

if __name__ == '__main__':
    show_config()
    app = Flask(__name__)
    # endpoints
    app.register_blueprint(uav_data_bp)
    app.register_blueprint(ai_data_bp)
    app.run(host='0.0.0.0', port=5001, debug=True)