import subprocess
import json

def extract_payload(filename):
    try:
        cmd = "grep 'MobSF-API-Monitor' " + filename + "| sed \"s/.*MobSF-API-Monitor: \\({.*}\\)'.*/\\1/\""
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        output = output.strip()
        print(type(output))
        api_logs = output.split('\n')
        api_logs = [json.loads(api) for api in api_logs]
        return api_logs
    except subprocess.CalledProcessError:
        print("Error occurred while executing the command.")
        return None

filename = input("Enter the filename: ")
payload = extract_payload(filename)
if payload:
    print("Payload extracted:")
    print(payload)
