import esp
esp.osdebug(None)

import network

ssid = "New Home"
password = "1223334444"

station = network.WLAN(network.STA_IF)

if station.isconnected() == True:
    print("Already connected")

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print("Connection successful")
print(station.ifconfig())
