# https://github.com/MobSF/Mobile-Security-Framework-MobSF/blob/master/scripts/mass_static_analysis.py

#!/usr/bin/env python

import requests
import json
import os
import re
import subprocess
import argparse
from urllib.request import urlopen


"""
    All requests for static and dynamic analysis
    File Upload
    curl -F file=@./apk/com-duolingo_5.121.4.apk http://localhost:8000/api/v1/upload -H Authorization:e38d5d8fc8e40e07058e2941ea36be48256a0e471779b929c52f7fe742a78f70

    Scan
    curl -X POST --url http://localhost:8000/api/v1/scan --data hash=87e7f95fbb57460966c9c4fa049857a3 -H Authorization:e38d5d8fc8e40e07058e2941ea36be48256a0e471779b929c52f7fe742a78f70
"""

BASE_URL = 'http://localhost:8000/'
UPLOAD_URL = 'api/v1/upload'
SCAN_URL = 'api/v1/scan'
DOWNLOAD_URL = ' /api/v1/download_pdf'
RECENT_SCANS = 'api/v1/scans'

def run_static_analysis(directory, api_key):
    hashes = []
    for file in os.listdir(directory):
        filepath = directory + file
        _, ext = os.path.splitext(filepath)
        if os.path.isfile(filepath) and ext == '.apk':
            # Upload File and Get hash
            headers = {
                'Authorization': api_key,
            }
            files = {
                'file': (file, open(filepath, 'rb'), 'application/octet-stream')
            }
            response = requests.post(BASE_URL+UPLOAD_URL, headers=headers, files=files)
            response_json = json.loads(response.text)
            if (response.status_code == 200) and ('hash' in response_json):
                print("Upload of file completed successfully!")
                h = response_json['hash']
                with open('./apk/hashes.txt', 'a') as f:
                    l = f'{file} - {h}\n'
                    f.write(l)
                hashes.append(h)
            else:
                print("Error occured while uploading. Please try again.")

    for h in hashes:
        # Static Scan of File
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'hash': h,
        }
        scan = BASE_URL+SCAN_URL
        response = requests.post(scan, headers=headers, data=data)
        response_json = json.loads(response.text)
        if response.status_code == 200:
            print(f"Static Analysis of {h} complete!")
            with open('StaticAnalysisResults/'+h, 'w') as f:
                json.dump(response_json, f, ensure_ascii=False, indent=4)

            download = BASE_URL + DOWNLOAD_URL
            headers['Content-Type'] = 'application/pdf'
            response = requests.post(download, headers=headers, data=data)
            print(f"File Download Complete!")
        else:
            print("Static Analysis of {h} failed!")

def is_mobsf_running():
    try:
        urlopen(BASE_URL, timeout=5)
        return True
    except:
        print("Error opening url!")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder',
                        help='Folder that contains mobile applications apks')
    args = parser.parse_args()
    api_key = None

    if is_mobsf_running() and args.folder:
        # Define the command to extract the REST API Key using awk
        command = "awk '/REST API Key/{print $NF}' mobsf_log.txt"

        try:
            # Execute the command using subprocess and capture the output
            output = subprocess.check_output(command, shell=True, text=True)

            # Extracts the REST API Key (In bold format)
            api_key = output.split('\n')[0]

            # Unbold the REST API Key and print it
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            api_key = ansi_escape.sub('', api_key)
            print(f"Extracted REST API Key: {api_key}")
        except subprocess.CalledProcessError:
            print("Error: Not able to extract REST API key.")
            exit(1)

        run_static_analysis(args.folder, api_key=api_key)
