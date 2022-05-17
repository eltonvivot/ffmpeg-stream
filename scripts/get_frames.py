import os, time, threading

docker_file = "/root/ffmpeg-stream/docker-compose.yaml"
ai_ip = "10.10.21.11"
ai_port = "22"
ai_user = "root"
ai_pass = "ffmpeg"
rtsp_trans = ""
cont_name = "uav-cam"

def get_frame(last_name, new_name):
    print("Changing docker-compose ...")
    os.system(f"sed -i 's/{last_name}/{new_name}/g' {docker_file}")
    time.sleep(2)

    print("Starting docker container ...")
    os.system(f"docker-compose -f {docker_file} up -d --build {cont_name}")
    
    print("Wainting 5s ...")
    time.sleep(5)

    print("Getting frame ...")
    threading.Thread(target=os.system, args=(f"sshpass -p {ai_pass} ssh {ai_user}@{ai_ip} 'cd /root/loss && ./get_frame.sh {new_name} &>/dev/null &'", )).start()
    print("Wainting 5s ...")
    time.sleep(5)

    print("Stopping docker container ...")
    os.system(f"docker stop {cont_name}")
    time.sleep(1)
    print("Done.")

if __name__ == '__main__':
    get_frame("0002", "0003")