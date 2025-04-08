# Azure IoT Hub SDK for MicroPython

[![Join the chat at https://gitter.im/iotdisc/community](https://badges.gitter.im/iotdisc.svg)](https://gitter.im/iotdisc/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Licensed under the MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/iot-for-all/iotc-micropython-client/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/micropython-iotc.svg)](https://badge.fury.io/py/micropython-iotc)

### An Azure IoT Hub device client library for Micropython.
This repository contains code for the Azure IoT Hub SDK for Micropython. This enables micropython developers to easily create device solutions that semealessly connect to Azure IoT Hub.
It can run on various boards with some tweaks for low-memory devices.


## Prerequisites
+ Micropython 1.20+ (recommended).

## Import ``ioth``
With this release we have moved from upip to mip for installing dependencies.  The ioth and dependencies are in the package.json file in the root or the repo.  The ioth file will now be installed from this GitHub repository rather from PyPi making bug fixes easier for contributors.  The sample main.py has been changed so that it does an install when running if the ioth library is not present.  For a manual install you can use the following.  Be aware that your device will need to have internet access so it may need additional code to setup and connect to wifi.

```py
# If your device needs wifi before running uncomment and adapt the code below as necessary
#import network
#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#wlan.connect("SSID","password")
#while not wlan.isconnected():
#    pass
#print('network config:', wlan.ipconfig('addr4'))

try:
    import ioth
except:
    import mip
    mip.install('github:jcaldeira-iot/iot-hub-micropython-client/package.json')
    import ioth
```

The same commands apply when running through Micropython REPL.

## Samples
Check out the [sample repository](samples) for example code showing how the SDK can be used in the various scenarios:


## Connecting
Currently only connection through SAS token is supported. To generate a SAS token for a target IoT Hub device use the following command:
```py
az iot hub generate-sas-token -d <device_name> -n <hub_name> --du <token_expiry_time_in_sec>
```

### Init
```py
from ioth import IoTHClient
IOT_HUB = '<hub_name>.azure-devices.net'
DEVICE_ID = '<device_name>'
SAS_TOKEN = '<sas_token>' # something like "SharedAccessSignature sr=..."
client = IoTHClient(IOT_HUB, DEVICE_ID, SAS_TOKEN)
```

You can pass a logger instance to have your custom log implementation. (see [#Logging](#logging))

e.g.

```py
from ioth import ConsoleLogger, IoTHLogLevel, IoTHClient
logger = ConsoleLogger(IoTHLogLevel.ALL)
client = IoTHClient(IOT_HUB, DEVICE_ID, SAS_TOKEN, logger)
```

### Connect

```py
client.connect()
```
After successfull connection, IOTH context is available for further commands.

## Operations

### Send telemetry

```py
client.send_telemetry(payload)
```

e.g. Send telemetry every 3 seconds
```py
while client.is_connected():
    json_msg = {'temperature':randint(0,20),'pressure':randint(0,20),'acceleration':{'x':randint(0,20),'y':randint(0,20)}}
    print('Sending telemetry:', json_msg)
    client.send_telemetry(json_msg)
    sleep(3)
```

> **NOTE:** Payload content type and encoding are set by default to 'application/json' and 'utf-8'. Alternative values can be set using these functions:   _ioth.set_content_type(content_type)_ # .e.g 'text/plain'  |   _ioth.set_content_encoding(content_encoding)_ # .e.g 'ascii'

## Listen to events
Due to limitations of the Mqtt library for micropython, you must explictely declare your will to listen for incoming messages. This client implements a non-blocking way of receiving messages so if no messages are present, it will not wait for them and continue execution.

To make sure your client receives all messages just call _listen()_ function in your main loop. Be aware that some sleeping time (200 ms +) is needed in order to let the underlying library listen for messages and release the socket.

```py
while client.is_connected():
    client.listen() # listen for incoming messages
    client.send_telemetry(...)
    sleep(1)
```
You also need to subscribe to specific events to effectively process messages, otherwise client would just skip them (see below).

### Listen to commands
Subscribe to command events before calling _connect()_:
```py
client.on(IoTHEvents.COMMANDS, callback)
```
To provide feedbacks for the command like execution result or progress, the client can call the **ack** function available in the callback.

The function accepts 2 arguments: the command instance and a custom response message.
```py
def on_commands(command, ack):
    print(command.name)
    ack(command, 'Command received')

client.on(IoTHEvents.COMMANDS, on_commands)
```

## Logging

The default log prints to serial console operations status and errors.
This is the _API_ONLY_ logging level.
The function __set_log_level()__ can be used to change options or disable logs. It accepts a _IoTHLogLevel_ value among the following:

-  IoTHLogLevel.DISABLED (log disabled)
-  IoTHLogLevel.API_ONLY (information and errors, default)
-  IoTHLogLevel.ALL (all messages, debug and underlying errors)

The device client also accepts an optional Logger instance to redirect logs to other targets than console.
The custom class must implement three methods:

- info(message)
- debug(message)
- set_log_level(message);

## License
This samples is licensed with the MIT license. For more information, see [LICENSE](./LICENSE)
