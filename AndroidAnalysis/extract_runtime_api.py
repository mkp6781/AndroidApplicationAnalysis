import argparse

def extract_payload(filename):
    try:
        payloads = []
        with open(filename, 'r') as file:
            for line in file:
                if 'MobSF-API-Monitor' in line:
                    payload = line.split('MobSF-API-Monitor: ')[-1].split('}')[0] + '}'
                    payloads.append(payload)
        return payloads
    except FileNotFoundError:
        print("Error occurred while trying to open file.")
        return None

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',
                        help='File containing runtime API logs')
    args = parser.parse_args()

    if args.file:
        payload = extract_payload(args.file)
        if payload:
            print(payload)
        print(len(payload))
