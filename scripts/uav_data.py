import argparse, requests

API_ENDPOINT = "http://10.10.21.10:5001/uav_data"

def get():
    r = requests.get(url=API_ENDPOINT)
    print(r.json())

def post(args):
    if not args.cam_status:
        print("Missing '--cam-status' parameter.")
        return
    data = {
        'cam_status': args.cam_status
    }
    r = requests.post(url=API_ENDPOINT, data=data)
    print(r.json())

def main():
    parser = argparse.ArgumentParser(description="UAV_DATA REST Functions")
    parser.add_argument('-m', '--method', help="REST API Method. Possible values: get | post", required=True)
    parser.add_argument('-ct', '--cam-status', help="UAV CAM STATUS. Possible values: on | off")

    args = parser.parse_args()
    
    if args.method.lower == 'get':
        return get()
    elif args.method.lower == 'post':
        return post()

if __name__ == '__main__':
    main()