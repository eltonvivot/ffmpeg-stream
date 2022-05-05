import argparse, requests

API_ENDPOINT = "http://10.10.21.10:5001/ai_detection"

def start(args):
    print("Starting Detection...")
    data = {}
    if args.delay: data['delay'] = args.delay
    if args.rate: data['rate'] = args.rate
    if args.loss: data['loss'] = args.loss
    if data == {}:
        print("You must inform at least one option of [rate | delay | loss].")
        return
    print(f"Data:\n{data}")
    r = requests.post(url=f"{API_ENDPOINT}/start", json=data)
    # r = requests.get(url=f"{API_ENDPOINT}/start")
    print(r.json())

def stop():
    print("Stopping Detection...")
    r = requests.get(url=f"{API_ENDPOINT}/stop")
    print(r.json())

def main():
    parser = argparse.ArgumentParser(description="AI DETECTION REST Functions")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-st', '--start', action='store_true', help="Starts Object Detection AI.")
    group.add_argument('-sp', '--stop', action='store_true', help="Stops Object Detection AI.")
    parser.add_argument('-d', '--delay', help="Set network latency. Available parameters: [h/m/s/ms/us]. Usage example: --delay 100ms")
    parser.add_argument('-r', '--rate', help="Set a limit on bandwidth. Available parameters: [G/M/K bps]. Usage example: --rate 0.25Mbps")
    parser.add_argument('-l', '--loss', help="Set packet loss. Available parameters: [%]. Usage example: --loss 0.1%")

    args = parser.parse_args()
    
    if args.start:
        return start(args)
    elif args.stop:
        return stop()

if __name__ == '__main__':
    main()