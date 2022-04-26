# Simulates Data management and exposure
from datetime import datetime
import json

# context vars
uav_data = {}

# simulates O1 data collector
def o1_collect_uav_data():
    global uav_data
    rapp_collection = json.loads("/app/o_data_collection.json")
    for data in rapp_collection['uav_data']:
        if data['time'] >= datetime.timestamp(datetime.now()): uav_data = data