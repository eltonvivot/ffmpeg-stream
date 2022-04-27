import json, logging
from config import cdata

logger = logging.getLogger(__name__)

def get_all():
    with open(cdata, 'r') as cfile:
        return json.load(cfile)

def get(data_name):
    logger.debug(f"...")
    data = get_all()
    if data_name not in data: raise Exception(f"Context do not have '{data_name}'.")
    return data[data_name]

# works as update
def post(data_name, data):
    logger.debug(f"...")
    context = get_all()
    context[data_name] = data
    with open(cdata, 'w') as cfile:
        json.dump(context, cfile, indent=2)