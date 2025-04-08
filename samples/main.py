import sys
import time
from random import randint

# If your device needs wifi before running uncomment and adapt the code below as necessary
#import network
#wlan = network.WLAN(network.STA_IF)
#wlan.active(True)
#wlan.connect("SSID","password")
#while not wlan.isconnected():
#    pass
#print(wlan.isconnected())
#print('network config:', wlan.ipconfig('addr4'))

try:
    import ioth
except:
    import mip
    mip.install('github:jcaldeira-iot/iot-hub-micropython-client/package.json')
    import ioth
    
from ioth import IoTHClient, IoTHConnectType, IoTHEvents, IoTHLogLevel

IOT_HUB = '<hub_name>.azure-devices.net'
DEVICE_ID = '<device_name>'
SAS_TOKEN = '<sas_token>' # something like "SharedAccessSignature sr=..."
conn_type = IoTHConnectType.SYMM_KEY

client = IoTHClient(IOT_HUB, DEVICE_ID, conn_type, SAS_TOKEN)
client.set_log_level(IoTHLogLevel.ALL)

def on_commands(command, ack):
    print('Command {}.'.format(command.name))
    ack(command, command.payload)

client.on(IoTHEvents.COMMANDS, on_commands)
client.connect()

startTime = time.ticks_ms()
while client.is_connected():
    client.listen()
    if time.ticks_diff(time.ticks_ms(), startTime) > 3000:
        print('Sending telemetry')
        client.send_telemetry({'temperature':randint(0,20),'pressure':randint(0,20)})
        startTime = time.ticks_ms()
    time.sleep_ms(500)
