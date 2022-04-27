import logging

# init logs
logger = logging.getLogger(__name__)
f='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s | %(message)s'
log_level=logging.DEBUG
logging.basicConfig(level=log_level, format=f)