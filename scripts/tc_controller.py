import argparse, requests

API_ENDPOINT = "http://10.10.21.10:5002/tc_rules"

def get():
    print("Method: GET")
    r = requests.get(url=API_ENDPOINT)
    print(r.json())

def post(args):
    print(f"Method: POST")
    data = {}
    if args.delay: data['delay'] = args.delay
    if args.rate: data['rate'] = args.rate
    if args.loss: data['loss'] = args.loss
    if data == {}:
        print("You must inform at least one option of [rate | delay | loss].")
        return
    print(f"Data:\n{data}")
    r = requests.post(url=API_ENDPOINT, json=data)
    print(r.json())

def delete():
    print(f"Method: DELETE")
    r = requests.delete(url=API_ENDPOINT)
    print(r.json())

def main():
    parser = argparse.ArgumentParser(description="TC CONTROLLER REST Functions")
    parser.add_argument('-m', '--method', help="REST API Method. Possible values: get | post | delete", required=True)
    parser.add_argument('-d', '--delay', help="Set network latency. Available parameters: [h/m/s/ms/us]. Usage example: --delay 100ms")
    parser.add_argument('-r', '--rate', help="Set a limit on bandwidth. Available parameters: [G/M/K bps]. Usage example: --rate 0.25Mbps")
    parser.add_argument('-l', '--loss', help="Set packet loss. Available parameters: [%]. Usage example: --loss 0.1%")


    args = parser.parse_args()
    
    if args.method.lower() == 'get':
        return get()
    elif args.method.lower() == 'post':
        return post(args)
    elif args.method.lower() == 'delete':
        return delete()

if __name__ == '__main__':
    main()