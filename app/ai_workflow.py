# Simulates AI/ML workflow
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
from data_collector import uav_data
import paramiko

persons = []

# Starts IA Object Detection
def start_detection(user="root", ip="10.10.21.11", port="22", camera="rtsp://10.10.21.10:8554/compose-rtsp"):
    global persons
    # defines command to start object detection
    # command = f"cd darknet && ./darknet detector demo cfg/coco.data cfg/yolov4-p6.cfg yolov4-p6.weights {camera} -dont_show"
    command = f"cd darknet && ./darknet detector test cfg/coco.data cfg/yolov4-p6.cfg yolov4-p6.weights data/person.jpg -dont_show"
    # start AI throught ssh connection
    try:
        # creates paramiko connection 
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(username=user, hostname=ip, port=port, password="ffmpeg")
        # executes command
        _,stdout,stderr = client.exec_command(command, get_pty=True)
        for line in iter(stdout.readline, ""):
            print(line, end="")
            if 'person:' in line:
                person = {
                    "ap": (line.split(':')[1])[1],
                    "time": datetime.timestamp(datetime.now()),
                    # "bandwidth": uav_data['bandwidth']
                }
                print(f"<------------------------->\n{person}\n<------------------------->")
                persons.append(person)
    except Exception as err:
            print(str(err))
    finally:
        if client: client.close()

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

print("starting detection ...")
start_detection()