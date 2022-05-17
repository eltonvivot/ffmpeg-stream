import os, time, threading
from os import listdir
from os.path import isfile, join

docker_file = "/root/ffmpeg-stream/docker-compose.yaml"
ai_ip = "10.10.21.11"
ai_port = "22"
ai_user = "root"
ai_pass = "ffmpeg"
rtsp_trans = ""
cont_name = "uav-cam"

def get_frame(last_name, new_name):
    print(f"\n------- GETTING FRAME {new_name} -------")
    print("Changing docker-compose ...")
    os.system(f"sed -i 's/{last_name}/{new_name}/g' {docker_file}")
    time.sleep(2)

    print("Starting docker container ...")
    os.system(f"docker-compose -f {docker_file} up -d --build {cont_name}")
    
    print("Wainting 5s ...")
    time.sleep(7)

    print("Getting frame ...")
    threading.Thread(target=os.system, args=(f"sshpass -p {ai_pass} ssh {ai_user}@{ai_ip} 'cd /root/loss && ./get_frame.sh {new_name} &>/dev/null &'", )).start()
    print("Wainting 5s ...")
    time.sleep(7)

    print("Stopping docker container ...")
    os.system(f"docker stop {cont_name}")
    time.sleep(2)
    print("Done.")

if __name__ == '__main__':

    mypath = "/root/ffmpeg-stream/video-test/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.mp4' in f]
    onlyfiles.sort()
    last = '0001'
    for f in onlyfiles:
        get_frame(last, f[:-4])
        last = f[:-4]
    
    os.system(f"sed -i 's/{last}/0001/g' {docker_file}")
