#!/bin/bash

docker_file = "/root/ffmpeg-stream/docker-compose.yaml"
ai_ip = "10.10.21.11"
ai_port = "22"
ai_user = "root"
ai_pass = "ffmpeg"
rtsp_trans = ""
cont_name = "uav-cam"

function get_frame(){
    echo "Changing docker-compose ..."
    sed -i "s/0001/$1/g" $docker_file

    echo "Starting docker container ..."
    docker-compose -f $docker_file up -d --build $cont_name

    echo "Wainting start ..."
    sleep 5

    echo "Getting frame ..."
    sshpass -p "$ai_pass" ssh $ai_user@$ai_ip "cd /root/loss && ./get_frame.sh $1 &>/dev/null &"
    sleep 5

    echo "Stopping docker container ..."
    docker stop $cont_name
    echo "Done."
}

get_frame "0002"