# ffmpeg-stream
Simple application that simulates a uav-drone camera under network traffic restrictions. 
This application uses a docker image along with a ue_controller application as server; and bash scripts to extract media as client.

## Install Server
Installation guide of Server Application

### Dependecies
- Ubuntu 18.04 OS
- Python3
- Docker and docker-compose
- Ssh pass:
```
sudo apt install sshpass
```

### UE controller
Python application to set up traffic control of network.

- Install requirements:
```
pip3 install -r ue_controller/requirements.txt
```
- Configure ue_controller/ue_controller.service `Service` variables
- Copy ue_controller/ue_controller.service to systemd:
```
cp ue_controller/ue_controller.service /etc/systemd/system/
```
- Enables and start service:
```
systemctl enable ue_controller
systemctl start ue_controller
```

## Install Client
Client host that will get media from server stream.

### Dependecies
- Ubuntu 18.04 OS
- Ffmpeg:
```
sudo apt install ffmpeg
```

### Copy 'client-frames' folder to client host
If you do want to use server scripts to stream media you have to copy the `client-frames` folder to `~/` of your user.
Example:
```
scp -r client-frames/ client-user@client-ip:/root/
```

---
## Usage

### UE Controller
UE controller is a REST application to set up network traffic control. To simplify ue_controller usage we have a script file with all avaiable options and usage examples of it.
- Check ue_controller usage:
```
python3 scripts/tc_controller.py --help
```
- Apply rules
```
python3 scripts/tc_controller.py -m post --delay 10ms --loss 5.0% --rate 10.0Mbps
```
- Get applied rules:
```
python3 scripts/tc_controller.py -m get
```
- Delete rules:
```
python3 scripts/tc_controller.py -m delete
```

### UAV-Camera stream
To simulate uav camera stream we use a `uav-cam` container. It is defined in the `docker-compose.yaml` file.
* Stream single media:
To stream a single media you need to configure the media location in `docker-compose.yaml` file. 
In order to do that, change the `-i` parameter of `uav-cam` container `command`.
* Stream multiple sequential frames:
To stream multiple sequential frames we can use the `scripts/get_frames.py` script file. The frames must follow the `000%d` format, eg. 0001.mp4, 0002.mp4, 0003.mp4.
In order to rename and convert frames to jpg we can use `video-frames/rename_sequential.sh` and `video-frames/convert_mp4.sh` script files.

- Rename frames to `000%d` format:
Copy your frames to `video-frames/` folder and run `rename_sequential.sh` script file:
```
cd video-frames/ && ./rename_sequential.sh
```
List files and check if everything worked as expected:
```
cd video-frames/ && ls
```

- Convert frames to `mp4`:
```
cd video-frames/ && ./convert_mp4.sh
```
OBS.: If your frames is not jpg change `convert_mp4.sh` script file with the correct format.

- Configure script variables:
```
docker_file => docker file path
ai_ip => client ssh address
ai_port => client ssh address
ai_user => client ssh user
ai_pass => client ssh pass
```

- Execute `scripts/get_frames.py` file:
```
python3 scripts/get_frames.py
```
