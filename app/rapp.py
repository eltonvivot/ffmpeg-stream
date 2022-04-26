# Simulates Object Detection rApp
import json, cv2
from datetime import datetime

stream_path = 'rtsp://localhost:8554/compose-rtsp'

# context vars
rapp = {}
# UAV stream res
stream_res = {
    "wid": 3840,
    "hgt": 2160
}

# Simulates App data collector
def data_collector():
    global rapp
    rapp_collection = json.loads("/app/o_data_collection.json")
    for data in rapp_collection:
        if data['time'] >= datetime.timestamp(datetime.now()): rapp = data

# Check if UAV camera is streaming
def is_stream_on(path=stream_path):
    # Opens the inbuilt camera to capture video.
    cap = cv2.VideoCapture(path)

    # Return True if stream is open or False if not
    if cap.isOpened():
        ret, _ = cap.read()
        cap.release()
        return ret

# Check UAV stream resolution
def get_stream_res(path=stream_path):
    global stream_res
    image = 'stream_frame.jpg'
    # Opens the inbuilt camera to capture video.
    cap = cv2.VideoCapture(path)
    while(cap.isOpened()):
        ret, frame = cap.read()
        # If video ends.
        if ret == False: break

        # cv2.imwrite(image, frame)
        # img = cv2.imread(image)
  
        # fetching the dimensions
        stream_res['wid'] = frame.shape[1]
        stream_res['hgt'] = frame.shape[0]
    
    cap.release()
