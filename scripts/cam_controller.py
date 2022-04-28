import argparse, requests

API_ENDPOINT = "http://10.10.21.10:5002/uav_cam"

def get(oper):
    print(f"Operation: {oper}")
    r = requests.get(url=f"{API_ENDPOINT}/{oper}")
    print(r.json())

def main():
    parser = argparse.ArgumentParser(description="AI DETECTION REST Functions")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-st', '--start', action='store_true', help="Starts Object Detection AI.")
    group.add_argument('-sp', '--stop', action='store_true', help="Stops Object Detection AI.")
    group.add_argument('-sts', '--status', action='store_true', help="Returns Object Detection AI Status.")

    args = parser.parse_args()
    
    if args.start:
        return get("start")
    elif args.stop:
        return get("stop")
    elif args.status:
        return get("status")

if __name__ == '__main__':
    main()