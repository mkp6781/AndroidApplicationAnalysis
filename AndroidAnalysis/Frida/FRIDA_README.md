# Frida Dynamic Application Instrumentation

* Connect to Frida server in emulator or usb device

* See which processes are running, their identifiers and names in the emulated device

```
frida-ps -Ua
```

* Injecting and running javascript code.

```
frida -U -l ./Frida/api_monitor.js <app_name>

Example:
frida -U -l ./Frida/api_monitor.js Spotify
```

* Instrument the application by going through the various flows of the application