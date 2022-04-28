from flask import Flask
from dotenv import load_dotenv
from app.errors import errors_bp
from tc_controller import tc_controller_bp
import logging

if __name__ == '__main__':
    # init logs
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s | %(message)s')
    logger = logging.getLogger(__name__)

    # load env file
    load_dotenv(dotenv_path='./config.env')
    
    app = Flask(__name__)
    # endpoints
    app.register_blueprint(errors_bp)
    app.register_blueprint(tc_controller_bp)
    

    app.run(host='0.0.0.0', port=5002)