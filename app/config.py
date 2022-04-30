import os

# data files
cdata = str(os.getenv("CONTEXT_DATA_FILE"))
tc_rules = str(os.getenv("TC_RULES_FILE"))
app_data = str(os.getenv("APP_DATA_FILE"))
odata = str(os.getenv("O1_DATA_FILE"))
od_output = str(os.getenv("OBJECT_DETECTION_OUTPUT_FILE"))
od_results = str(os.getenv("OBJECT_DETECTION_RESULTS_FILE"))

# AI ssh config
ai_user = str(os.getenv("AI_SSH_USER"))
ai_passwd = str(os.getenv("AI_SSH_PASSWORD"))
ai_host = str(os.getenv("AI_SSH_HOST"))
ai_port = int(str(os.getenv("AI_SSH_PORT")))

# AI detection time
ai_dtime = int(str(os.getenv("AI_DETECTION_TIME")))

# UAV CAM config
uav_cam = str(os.getenv("UAV_CAM_ADDRESS"))

# UE Controller Endpoints
tc_control = str(os.getenv("TC_CONTROLLER_ENDPOINT"))

def show_config():
    print("------ APP CONFIG ------")
    print(f"CONTEXT_DATA_FILE={cdata}\nAPP_DATA_FILE={app_data}\nO1_DATA_FILE={odata}")
    print(f"AI_SSH_USER={ai_user}\nAI_SSH_PASSWORD={ai_passwd}\nAI_SSH_HOST={ai_host}\nAI_SSH_PORT={ai_port}")
    print(f"UAV_CAM_ADDRESS={uav_cam}")
