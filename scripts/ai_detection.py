import argparse, requests

API_ENDPOINT = "http://10.10.21.10:5001/ai_detection"

def start():
    print("Starting Detection...")
    r = requests.get(url=f"{API_ENDPOINT}/start")
    print(r.json())

def stop():
    print("Stopping Detection...")
    r = requests.get(url=f"{API_ENDPOINT}/stop")
    print(r.json())

def main():
    parser = argparse.ArgumentParser(description="UAV_DATA REST Functions")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-st', '--start', help="Starts Object Detection AI.")
    group.add_argument('-sp', '--stop', help="Stops Object Detection AI.")

    args = parser.parse_args()
    
    if args.start:
        return start()
    elif args.stop:
        return stop()

if __name__ == '__main__':
    main()