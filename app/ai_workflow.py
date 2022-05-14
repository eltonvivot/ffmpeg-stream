# Simulates AI/ML workflow
from datetime import datetime
from flask import g
from matplotlib.pyplot import xlim
from config import ai_user, ai_passwd, ai_host, ai_port, ai_dtime, uav_cam, od_output, od_results, tc_control, gc_folder
import paramiko, logging, time, os, threading, requests, random
import matplotlib.pylab as plt 
import pandas as pd 
import seaborn as sns
import numpy as np
 
logger = logging.getLogger(__name__)
logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

client = None

tc_results = {}

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

# Decreases bandwidth
def auto_rules(detection_name, change_rate, change_loss, change_delay, stime, dec_time, inc_time, timeout=ai_dtime, delay=0):
    logger.debug(f"Starting auto rules \t|\t rate: {change_rate} | loss: {change_loss} timeout: {timeout} | dec: {dec_time} | inc: {inc_time}  -----------------")
    time.sleep(delay)
    # last
    lrate = 500.0
    lloss = 0.0
    ldelay = 0.6
    # min
    min_rate = 300.0
    min_loss = 0.0
    min_delay = 0.3
    # max
    max_rate = 500.0
    max_loss = 2.5
    max_delay = 20
    # decrease and increase time
    already_dec = False
    already_inc = False
    # test
    while True:
        if datetime.timestamp(datetime.now()) - stime >= timeout: break
        if not already_dec and datetime.timestamp(datetime.now()) - stime >= dec_time:
            already_dec = True
            if change_rate:
                max_rate = 1
                min_rate = 0.1
            if change_loss:
                max_loss = 80.0
                min_loss = 70.0
            if change_delay:
                max_delay = 250
                min_delay = 100
        if not already_inc and datetime.timestamp(datetime.now()) - stime >= inc_time:
            already_inc = True
            if change_rate:
                max_rate = 500
                min_rate = 300
            if change_loss:
                max_loss = 2.5
                min_loss = 0.0
            if change_delay:
                max_delay = 15
                min_delay = 0.3

        time.sleep(random.uniform(0.5, 1.0))
        # random
        rules = {}
        rules['rate'] = f"{random.uniform(lrate-30 if lrate-30 > min_rate else min_rate, lrate+30 if lrate+30 < max_rate else max_rate)}Mbps"
        rules['loss'] = f"{random.uniform(lloss-1.0 if lloss-1.0 > min_loss else min_loss, lloss+1.0 if lloss+1.0 < max_loss else max_loss)}%"
        rules['delay'] = f"{random.uniform(ldelay-4 if ldelay-4 > min_delay else min_delay, ldelay+4.0 if ldelay+4.0 < max_delay else max_delay)}ms"

        update_uav_tc_rules(detection_name, rules, stime)
        lrate = rules['rate']
        lloss = rules['loss']
        ldelay = rules['delay']


# Starts AI Object Detection
def start_detection(detection_name, change_rate, change_loss, change_delay):
    #logger.debug(f"NEW RULES {tc_new_rules}")
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
    try:
        triggered_stop = False
        stime = 0.0
        g.results[detection_name] = []
        tc_results[detection_name] = []
        # executes command
        _,stdout,stderr = client.exec_command(command, get_pty=True)
        for line in iter(stdout.readline, ""):
            if stime > 1 and datetime.timestamp(datetime.now()) - stime >= ai_dtime + 3:
                logger.info(f"Stopping Detection. Duration = {datetime.timestamp(datetime.now()) - stime}")
                break
            log_to_file(line.rstrip("\n"), od_output)
            if 'Video stream:' in line and not triggered_stop:
                triggered_stop = True
                # threading.Thread(target=stop_detection, args=(ai_dtime+3,)).start()
                stime = datetime.timestamp(datetime.now()) +3
                # add dec and inc time to g
                g.dec_time[detection_name] = random.uniform(((ai_dtime+3)/3)-5, ((ai_dtime+3)/3)+5)
                g.inc_time[detection_name] = random.uniform(((ai_dtime+3)/3)-5, ((ai_dtime+3)/3)+5) * 2
                threading.Thread(target=auto_rules, args=(detection_name, change_rate, change_loss, change_delay, stime, g.dec_time[detection_name], g.inc_time[detection_name])).start()
            if 'person:' in line:
                result={}
                tc_rules = (requests.get(url=tc_control)).json()
                dtime = datetime.timestamp(datetime.now()) - stime
                ap = (line.split(': ')[1])[:2]
                logp = "Time: {:.2f}".format(dtime) + f" | AP:{ap}%"
                # format values type
                result['time'] = dtime
                result['ap'] = int(ap)
                logger.debug(f"Current Rule: {tc_rules}")
                if 'delay' in tc_rules: result['delay'] = float(tc_rules['delay'][:-2])
                if 'rate' in tc_rules: result['rate'] = float(tc_rules['rate'][:-4])
                if 'loss' in tc_rules: result['loss'] = float(tc_rules['loss'][:-1])

                g.results[detection_name].append(result)
                log_to_file(logp, od_results)
        return g.results[detection_name]
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

def plot_figure_old(should_save, should_display, results):
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
    line7, = ax.plot(times, [result['delay'] for result in results], label="UE latency (ms)",
                     color=color2, marker='o', markersize=3, linewidth=3)
    line8, = ax.plot(times, rates, label="UE bandwidth (Mbps)",
                     color=color3, marker='o', markersize=3)
    line9, = ax.plot(times, [result['loss'] for result in results], label="UE packet loss (%)",
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

def plot_figures(should_save, should_display, first_name, second_name):    
    sns.set_theme(style="darkgrid")
    # load results
    # logger.debug(f"RESULT 1 ---------------------\n{g.results[first_name]}\n")
    # logger.debug(f"RESULT 2 ---------------------\n{g.results[second_name]}\n")
    results1 = pd.DataFrame(g.results[first_name] + tc_results[first_name])
    results1.sort_values(by=['time'], inplace=True)
    results2 = pd.DataFrame(g.results[second_name] + tc_results[second_name])
    results2.sort_values(by=['time'], inplace=True)
    # aps count
    aps1 = pd.DataFrame({})
    aps1['time'] = results1['time'].astype(int)
    aps1['ap'] = results1['ap']
    aps1_qnt = aps1.groupby(['time'])['ap'].count()

    aps2 = pd.DataFrame({})
    aps2['time'] = results2['time'].astype(int)
    aps2['ap'] = results2['ap']
    aps2_qnt = aps2.groupby(['time'])['ap'].count()
    
    g.dec_time[first_name]+=4
    g.inc_time[first_name]+=4
    g.dec_time[second_name]+=4
    g.inc_time[second_name]+=4

    # creates graphic
    sns.set_context('paper', font_scale=1.5)
    fig, axes = plt.subplots(nrows=4, ncols=2, sharex='col', figsize=(15,12))
    # fig, axes = plt.subplots(nrows=5, ncols=2, sharex='col', figsize=(15,15))

    # AP %
    # results1.plot(kind='line', y='ap', x='time',label="Detected People", ax=axes[0,0], color='tab:blue')
    # axes[0,0].set_ylabel("Precision(%)")
    # axes[0,0].set_yticks(np.array([30, 60, 90]))
    # axes[0,0].legend(loc='lower left')

    # results2.plot(kind='line', y='ap', x='time',label='Detected People', ax=axes[0,1], color='tab:blue')
    # axes[0,1].set_ylabel("Precision(%)")
    # axes[0,1].set_yticks(np.array([30, 60, 90]))
    # axes[0,1].legend(loc='lower left')
    
    # Detection Quantity
    aps1_qnt.plot(kind='line', y='ap', x='time',label="Detected People", ax=axes[0,0], color='tab:blue')
    axes[0,0].set_ylabel("Quantity")
    axes[0,0].legend(loc='lower left')
    axes[0,0].set_yticks(np.array([0, 20, 40]))

    aps2_qnt.plot(kind='line', y='ap', x='time',label='Detected People', ax=axes[0,1], color='tab:blue')
    axes[0,1].set_ylabel("Quantity")
    axes[0,1].legend(loc='lower left')
    axes[0,1].set_yticks(np.array([0, 20, 40]))

    # RATE
    results1.plot(kind='line',x='time',y='rate', label='UE' , ax=axes[1,0], color='tab:red')
    axes[1,0].set_ylabel('Bandwidth(Mbit/s)')
    axes[1,0].legend(loc='lower left')

    results2.plot(kind='line',x='time',y='rate', label='UE' , ax=axes[1,1], color='tab:red')
    axes[1,1].set_ylabel('Bandwidth(Mbit/s)')
    axes[1,1].legend(loc='lower left')

    # LOSS
    results1.plot(kind='line',y='loss',x='time',label='UE', ax=axes[2,0], color='tab:orange')
    axes[2,0].set_ylabel('Package loss(%)')
    axes[2,0].legend(loc='lower left')

    results2.plot(kind='line',y='loss',x='time',label='UE', ax=axes[2,1], color='tab:orange')
    axes[2,1].set_ylabel('Package loss(%)')
    axes[2,1].legend(loc='lower left')

    # DELAY
    results1.plot(kind='line',y='delay',x='time',label='UE', ax=axes[3,0], color='tab:green')
    axes[3,0].set_ylabel('Latency(ms)')
    axes[3,0].legend(loc='lower left')

    results2.plot(kind='line',y='delay',x='time',label='UE', ax=axes[3,1], color='tab:green')
    axes[3,1].set_ylabel('Latency(ms)')
    axes[3,1].legend(loc='lower left')

    axes[3,0].set_xlabel('Time(sec)')
    axes[3,1].set_xlabel('Time(sec)')   

    # Adds vertical lines
    for i in range(4):
        axes[i, 0].axvline(g.inc_time[first_name],linestyle ="dotted", color='tab:gray')
        axes[i, 0].axvline(g.dec_time[first_name],linestyle ="dotted", color='tab:gray')

        axes[i, 1].axvline(g.inc_time[second_name],linestyle ="dotted", color='tab:gray')
        axes[i, 1].axvline(g.dec_time[second_name],linestyle ="dotted", color='tab:gray')

    # titles
    axes[0,0].set_title('(a) Bandwidth decrease')
    axes[0,1].set_title('(b) Package loss')

    # adds comments
    # axes[0,0].annotate('Bandwidth decreased', xy=(g.dec_time[first_name],87), xytext=(-15, -15), textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'), fontsize=11, horizontalalignment="right")
    # axes[0,0].annotate('Bandwidth increased', xy=(g.inc_time[first_name],87), xytext=(15, -15), textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'), fontsize=11)
    axes[0,0].annotate('Bandwidth decreased', xy=(g.dec_time[first_name], axes[0,0].get_yticks()[-1] -3), xytext=(-15, -15), textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'), fontsize=11, horizontalalignment="right")
    axes[0,0].annotate('Bandwidth increased', xy=(g.inc_time[first_name], axes[0,0].get_yticks()[-1] -3), xytext=(15, -15), textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'), fontsize=11)

    axes[0,1].annotate('Package loss increased', xy=(g.dec_time[second_name], axes[0,1].get_yticks()[-1] -3), xytext=(-15, -15), textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'), fontsize=11, horizontalalignment="right")
    axes[0,1].annotate('Package loss decreased', xy=(g.inc_time[second_name], axes[0,1].get_yticks()[-1] -3), xytext=(15, -15), textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'), fontsize=11)

    # plt.xlim([0, 20])
    plt.setp(axes, xlim=(0, ai_dtime))

    if should_save:
        plt.savefig(f"{gc_folder}result_{int(datetime.timestamp(datetime.now()))}.pdf", bbox_inches='tight')
    if should_display:
        plt.show()


def update_uav_tc_rules(detection_name, rules, stime):
    global tc_results
    logger.debug(f"Applying: {rules}")
    logger.debug(f"Result: {(requests.post(url=tc_control, json=rules)).json()}")
    if 'delay' in rules: rules['delay'] = float(rules['delay'][:-2])
    if 'rate' in rules: rules['rate'] = float(rules['rate'][:-4])
    if 'loss' in rules: rules['loss'] = float(rules['loss'][:-1])
    rules['time'] = datetime.timestamp(datetime.now()) - stime + 2 # delay
    rules['ap'] = None
    tc_results[detection_name].append(rules)