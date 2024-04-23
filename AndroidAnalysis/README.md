# RUNNING ANALYSIS

## Setting up python environment
```
pip install -r requirements.txt
```

## Static Analysis

Before proceeding with the analysis, we need to run the Mobile Security Framework (mobSf). The following command initialises the mobsf server locally and logs the output to `mobsf_log.txt`

We use the log file to extract the REST Api Key for invoking API's during the current session. 

```
./mobsfRun.sh > mobsf_log.txt
```

For interacting with the MOBSF server, we use `run_static.py` to  check if the server is up, extract the REST API key and perform static analysis of the apks saved in the input directory

```
python3 run_static.py -f <folder containing apks>

Eg:
If all apk's are stored in `./apk/`
python3 run_static.py -f ./apk/
```

The static analysis results are stored in `StaticAnalysisResults` with the hash of the program as the name.

## Dynamic Analysis

### Run genymotion VM in a shell to emulate Android environment

```
./genymotion/genymotion
```

Select the target Android device to run the analysis on and boot the virtual device. 

### Installing application on the virtual device

Download the apk file from the Internet. Drag and drop the apk file onto the emulated virtual device for installation.

### Download and Installation of Frida
Download the latest compatible version of the Frida server from https://github.com/frida/frida/releases

### Setting Up Frida Server Manually on VM using adb
https://medium.com/@SecureWithMohit/getting-started-with-frida-setting-up-on-an-emulator-47980170d2b2

### Setting up Frida Server Through Script
Extract the downloaded Frida server into `Frida` directory and rename it as `frida-server`.
Make sure android device is being emulated and run this script.
```
./init_frida_server.sh
```

### Frida Dynamic Application Instrumentation

* Connect to Frida server in emulator or usb device

* See which processes are running, their identifiers and names in the emulated device

```
frida-ps -Ua
```

* Injecting and running javascript code.

```
frida -U -l ./Frida/api_monitor.js <app_name> > runtime_api_log.txt

Example:
frida -U -l ./Frida/api_monitor.js Spotify > runtime_api_log.txt
```

* Instrument the application by going through the various flows of the application


The above Frida script generates a log file by the name `runtime_api_log.txt`. From this file, the `extract_runtime_api.py` script extracts out only the intercepted API related logs for further analysis.

```
python3 extract_runtime_api.py -f runtime_api_log.txt
```
