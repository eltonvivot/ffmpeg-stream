import json, logging
from config import tc_rules

logger = logging.getLogger(__name__)

def get():
    with open(tc_rules, 'r') as cfile:
        return json.load(cfile)

# works as update
def post(data):
    with open(tc_rules, 'w') as cfile:
        json.dump(data, cfile, indent=2)

def delete():
    return post({})