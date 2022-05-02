# Simulates AI/ML workflow
from datetime import datetime
from flask import g
from config import ai_user, ai_passwd, ai_host, ai_port, ai_dtime, uav_cam, od_output, od_results, tc_control
import paramiko, logging, time, os, threading, requests

logger = logging.getLogger(__name__)
logging.getLogger("paramiko").setLevel(logging.WARNING)
client = None

# Connects to AI Object Detection
def connect():
    global client
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(username=ai_user, hostname=ai_host, port=ai_port, password=ai_passwd)
        transport = client.get_transport()
        transport.set_keepalive(1)
    except Exception as err:
            logger.error(str(err))
            raise

# Disconnects of AI Object Detection
def disconnect():
    global client
    if not client: logger.warning("Invalid connection.")
    else: client.close()
    client = None

# Starts AI Object Detection
def start_detection():
    global client
    # Check if already have connections
    if client: logger.warning("Object Detection is already running.") 
    else: connect()
    # Write to output and results file
    string = f"\n##### OBJECT DETECTION : {int(datetime.timestamp(datetime.now()))} #####" 
    log_to_file(string, od_output)
    log_to_file(string, od_results)
    # defines command to start object detection
    command = f"cd darknet && ./darknet detector demo cfg/coco.data cfg/yolov4-p6.cfg yolov4-p6.weights {uav_cam} -dont_show"
    # command = f"cd darknet && ./darknet detector test cfg/coco.data cfg/yolov4-p6.cfg yolov4-p6.weights data/person.jpg -dont_show"
    try:
        triggered_stop = False
        stime = 0.0
        count_time = 0.0
        g.results = []
        # executes command
        _,stdout,stderr = client.exec_command(command, get_pty=True)
        for line in iter(stdout.readline, ""):
            log_to_file(line.rstrip("\n"), od_output)
            if 'Done!' in line and not triggered_stop:
                threading.Thread(target=stop_detection, args=(ai_dtime,)).start()
                stime = datetime.timestamp(datetime.now())
                count_time = datetime.timestamp(datetime.now())
            # if (datetime.timestamp(datetime.now()) - count_time) >= 5.0:
            #     pass
            if 'person:' in line:
                result={}
                tc_rules = (requests.get(url=tc_control)).json()
                dtime = datetime.timestamp(datetime.now()) - stime
                ap = (line.split(': ')[1])[:2]
                logp = "Time: {:.2f}".format(dtime) + f" | AP:{ap}%"
                result['time'] = dtime
                result['ap'] = ap
                for k, v in tc_rules.items():
                    result[k] = v
                    logp+= f" | {k}:{v}"
                g.results.append(result)
                log_to_file(logp, od_results)
        return g.results
    except Exception:
            raise
    finally:
        disconnect()

# Stops AI Object Detection after given seconds
def stop_detection(seconds=0):
    time.sleep(seconds)
    disconnect()

def log_to_file(string, file):
    os.system(f"echo '{string}' >> {file}")

# # Simulates a request for more bandwidth
# def require_bandwidth(message = ''):
#     print(f"More bandwith needed! {message}")

# # Checks camera resolution to increase bandwidth  if needed
# def manage_bandwidth():
#     min_wid = 1920
#     min_hgt = 1080
#     min_bdwt = 70
#     from rapp import stream_res
#     while True:
#         if min_wid < stream_res['wid'] and min_hgt < stream_res['hgt']: 
#             require_bandwidth('Stream resolution is not 4K')
#         if min_bdwt < uav_data['bandwidth']: 
#             require_bandwidth('Insufficient current bandwidth')

# # Check if UAV camera is streaming
# def is_stream_on():
#     # Opens the inbuilt camera to capture video.
#     cap = cv2.VideoCapture(path)

#     # Return True if stream is open or False if not
#     if cap.isOpened():
#         ret, _ = cap.read()
#         cap.release()
#         return ret

# # Check UAV stream resolution
# def get_stream_res(path=stream_path):
#     global stream_res
#     image = 'stream_frame.jpg'
#     # Opens the inbuilt camera to capture video.
#     cap = cv2.VideoCapture(path)
#     while(cap.isOpened()):
#         ret, frame = cap.read()
#         # If video ends.
#         if ret == False: break

#         # cv2.imwrite(image, frame)
#         # img = cv2.imread(image)
  
#         # fetching the dimensions
#         stream_res['wid'] = frame.shape[1]
#         stream_res['hgt'] = frame.shape[0]
    
#     cap.release()


# print("starting detection ...")
# start_detection()