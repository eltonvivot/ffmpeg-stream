import json
from config import cdata

def get_all():
    return json.loads(cdata)

def get(data_name):
    data = json.loads(cdata)[data_name]
    if data_name not in data: print(f"Context do not have '{data_name}'.")
    return data[data_name]

# works as update
def post(data_name, data):
    context = get_all()
    context[data_name] = data
    with open(cdata, "w") as cfile:
        json.dump(context, cfile, indent=4)