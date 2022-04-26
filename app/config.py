import os

root_dir = '/app/'

# data files
cdata = root_dir + str(os.getenv("CONTEXT_DATA_FILE"))
app_data = root_dir + str(os.getenv("APP_DATA_FILE"))
odata = root_dir + str(os.getenv("O1_DATA_FILE"))

# AI ssh config
ai_user = str(os.getenv("AI_SSH_USER"))
ai_passwd = str(os.getenv("AI_SSH_PASSWORD"))
ai_host = str(os.getenv("AI_SSH_HOST"))
ai_port = int(str(os.getenv("AI_SSH_PORT")))

# UAV CAM config
uav_cam = str(os.getenv("UAV_CAM_ADDRESS"))

def show_config():
    print("------ APP CONFIG ------")
    print(f"CONTEXT_DATA_FILE={cdata}\nAPP_DATA_FILE={app_data}\nO1_DATA_FILE={odata}")
    print(f"AI_SSH_USER={ai_user}\nAI_SSH_PASSWORD={ai_passwd}\nAI_SSH_HOST={ai_host}\nAI_SSH_PORT={ai_port}")
    print(f"UAV_CAM_ADDRESS={uav_cam}")
