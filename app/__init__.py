import logging

# init logs
f='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s | %(message)s'
log_level=logging.DEBUG
logging.basicConfig()
logging.basicConfig(level=log_level, format=f)