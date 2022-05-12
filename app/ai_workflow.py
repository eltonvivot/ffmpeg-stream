# Simulates AI/ML workflow
from datetime import datetime
from re import T
from flask import g
from numpy import rate
from config import ai_user, ai_passwd, ai_host, ai_port, ai_dtime, uav_cam, od_output, od_results, tc_control, gc_folder
import paramiko, logging, time, os, threading, requests
import matplotlib.pylab as plt 
 
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
def start_detection(tc_new_rules):
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
        added_new_rule = False
        added_best_rule = False
        stime = 0.0
        last_rule = {}
        g.results = []
        # executes command
        _,stdout,stderr = client.exec_command(command, get_pty=True)
        for line in iter(stdout.readline, ""):
            log_to_file(line.rstrip("\n"), od_output)
            # if 'Done!' in line and not triggered_stop:
            #     threading.Thread(target=stop_detection, args=(ai_dtime,)).start()
            #     stime = datetime.timestamp(datetime.now())
            #     count_time = datetime.timestamp(datetime.now())
            if (datetime.timestamp(datetime.now()) - stime) >= 7.0 and triggered_stop and not added_new_rule:
                added_new_rule = True
                update_uav_tc_rules(tc_new_rules)
                if 'delay' in tc_new_rules: tc_new_rules['delay'] = tc_new_rules['delay'][:-2]
                if 'rate' in tc_new_rules: tc_new_rules['rate'] = tc_new_rules['rate'][:-4]
                if 'loss' in tc_new_rules: tc_new_rules['loss'] = tc_new_rules['loss'][:-1]
                tc_new_rules['time'] = datetime.timestamp(datetime.now()) - stime
                g.results.append(tc_new_rules)
            if (datetime.timestamp(datetime.now()) - stime) >= 14.0 and triggered_stop and not added_best_rule:
                added_best_rule = True
                tc_best_rules = {"delay": 0.05, "loss": 0.0, "rate": 500.0}
                update_uav_tc_rules(tc_best_rules)
                tc_best_rules['time'] = datetime.timestamp(datetime.now()) - stime
                g.results.append(tc_best_rules)
            if 'Video stream:' in line and not triggered_stop:
                triggered_stop = True
                threading.Thread(target=stop_detection, args=(ai_dtime+3,)).start()
                stime = datetime.timestamp(datetime.now()) +3
            if 'person:' in line:
                result={}
                tc_rules = (requests.get(url=tc_control)).json()
                dtime = datetime.timestamp(datetime.now()) - stime
                ap = (line.split(': ')[1])[:2]
                logp = "Time: {:.2f}".format(dtime) + f" | AP:{ap}%"
                # format values type
                result['time'] = dtime
                result['ap'] = int(ap)
                if 'delay' in tc_rules: result['delay'] = tc_rules['delay'][:-2]
                if 'rate' in tc_rules: result['rate'] = tc_rules['rate'][:-4]
                if 'loss' in tc_rules: result['loss'] = tc_rules['loss'][:-1]

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

def plot_figure(should_save, should_display, results):
    # def open_results():
    #     import json
    #     with open('/home/elton/Repositories/ffmpeg-stream/data/results.json', 'r') as cfile:
    #         return json.load(cfile)
    # if not results: results = open_results()

    fig, ax = plt.subplots(figsize=(7, 4))
    color1 = 'tab:blue'
    color2 = 'tab:orange'
    color3 = 'tab:green'
    color4 = 'tab:red'
    color5 = 'tab:purple'
    
    times = []
    aps = []
    aps_time = []
    rates = []
    for result in results:
        times.append(result['time'])
        if 'ap' in result: 
            aps.append(result['ap'])
            aps_time.append(result['time'])
        r = result['rate']
        if r == 500: r = 120
        rates.append(r)
    
    line6, = ax.plot(aps_time, aps, label="Person's Average Precision (%)",
                     color=color1, marker='o', markersize=4, linewidth=0)
    line7, = ax.plot(times, [(result['delay'])[:-2] for result in results], label="UE latency (ms)",
                     color=color2, marker='o', markersize=3, linewidth=3)
    line8, = ax.plot(times, rates, label="UE bandwidth (Mbps)",
                     color=color3, marker='o', markersize=3)
    line9, = ax.plot(times, [(result['loss'])[:-1] for result in results], label="UE packet loss (%)",
                     color=color5, marker='o', markersize=3)
    # line0, = ax.plot(times, [i * 3.6 for i in Cons_anel_n5_l1], label='H2 Root',
    #                  color=color4, marker='o', markersize=4)
    
    
    # plt.xticks([0, 5, 10, 15, 20, 25, 30])
    plt.xticks([0, 5, 10, 15, 20])

    # plt.yticks([0, 40, 100, 200, 350])
    plt.yticks([0, 25, 50, 75, 100])
    ax.tick_params(axis='y', which='major', labelsize=13)
    ax.tick_params(axis='x', which='major', labelsize=13)
    ax.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.set_ylabel('', fontsize=14, fontfamily='Arial')
    ax.set_xlabel('Object Detection Duration (sec)', fontsize=13, fontfamily='Arial')
    ax.legend(loc='upper left', fontsize=11)
    # ax.set_title(f"Object Detection with network bandwidth at {results[0]['rate']}")

    if should_save:
        plt.savefig(f"{gc_folder}result_{int(datetime.timestamp(datetime.now()))}.pdf", bbox_inches='tight')
    if should_display:
        plt.show()

def update_uav_tc_rules(rules):
    logger.debug(rules)
    return (requests.post(url=tc_control, json=rules)).json()

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