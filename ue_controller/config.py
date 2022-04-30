import os

# data files
tc_rules = str(os.getenv("TC_RULES_FILE"))

# network config
if_name = str(os.getenv("NETWORK_INTERFACE_NAME"))
if_ip = str(os.getenv("NETWORK_INTERFACE_IP"))

# UAV CAM config
uav_cname = str(os.getenv("UAV_CAM_CONTAINER_NAME"))
uav_cam_addr = str(os.getenv("UAV_CAM_ADDRESS"))

uav_cfile = str(os.getenv("UAV_CAM_CONTAINER_COMPOSE_FILE"))

# FFMPEG config
ffmpeg_cmd = str(os.getenv("FFMPEG_DEFAULT_COMMAND"))

# NTR ENDPOINTS
uav_data_end = str(os.getenv("UAV_DATA_ENDPOINT"))
ai_detec_end = str(os.getenv("AI_DETECTION_ENDPOINT"))