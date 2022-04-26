import json
from config import cdata

def get_all():
    with open(cdata, 'r') as cfile:
        return json.load(cfile)

def get(data_name):
    print(f"debug - get({data_name})")
    data = get_all()
    if data_name not in data: print(f"Context do not have '{data_name}'.")
    return data[data_name]

# works as update
def post(data_name, data):
    print(f"debug - post({data_name})")
    context = get_all()
    context[data_name] = data
    with open(cdata, 'w') as cfile:
        json.dump(context, cfile, indent=2)