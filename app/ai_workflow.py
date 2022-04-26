# Simulates AI/ML workflow
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
from data_collector import uav_data

persons = []

# Starts IA Object Detection
def start_detection(user="root", ip="10.10.21.11", port="22", camera="rtsp://10.10.21.10:8554/compose-rtsp"):
    global persons
    # defines command to start object detection
    command = f"cd darknet && ./darknet detector demo cfg/coco.data cfg/yolov4-p6.cfg yolov4-p6.weights {camera}"
    # start throught ssh connection
    p = Popen(f"ssh {user}@{ip} -p {port} '{command}", stdout = PIPE, stderr = STDOUT, shell = True)
    # monitor stdout (using while variant to skip bugs)
    while True:
        line = p.stdout.readline()
        print(line)
        if not line: break
        if 'person:' in line:
            person_qnt = (line.split(':')[1])[1]
            if person_qnt > 0:
                person = {
                    "qnt": person_qnt,
                    "time": datetime.timestamp(datetime.now()),
                    "bandwidth": uav_data['bandwidth']
                }
                persons.append(person)

# Simulates a request for more bandwidth
def require_bandwidth(message = ''):
    print(f"More bandwith needed! {message}")

# Checks camera resolution to increase bandwidth  if needed
def manage_bandwidth():
    min_wid = 1920
    min_hgt = 1080
    min_bdwt = 70
    from rapp import stream_res
    while True:
        if min_wid < stream_res['wid'] and min_hgt < stream_res['hgt']: 
            require_bandwidth('Stream resolution is not 4K')
        if min_bdwt < uav_data['bandwidth']: 
            require_bandwidth('Insufficient current bandwidth')

start_detection()